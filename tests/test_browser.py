"""Renderiza os arquivos reais em HTTP local com Chrome/Chromium via Playwright.
Executar: python tests/test_browser.py. BROWSER_CHANNEL=chromium usa browser instalado pelo Playwright.
Não testa a publicação nem atribui notas Lighthouse.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
import json, os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
OUT=R/'evidencias'/'master-v5';OUT.mkdir(parents=True,exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(R)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
pages=['index.html','experiencia-e-resultados.html','servicos/diagnostico.html','servicos/analise-de-dados.html','servicos/automacao-e-ia.html','servicos/ciencia-de-dados.html']
records=[];errors=[]
try:
 with sync_playwright() as p:
  channel=os.environ.get('BROWSER_CHANNEL','chrome')
  browser=p.chromium.launch(**({'channel':channel} if channel!='chromium' else {}),headless=True)
  for filename in pages:
   for width in [360,390,768,1024,1440]:
    page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.url.startswith(base) and r.status>=400 else None)
    response=page.goto(base+filename,wait_until='networkidle');assert response.status==200
    page.evaluate('document.fonts.ready')
    data=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth+1, brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src), h1:document.querySelectorAll('h1').length, hero:document.querySelector('.hero-art img')?getComputedStyle(document.querySelector('.hero-right')).display:null})''')
    assert not data['overflow'],(filename,width,'overflow')
    assert not data['brokenImages'],data
    assert data['h1']==1
    if filename=='index.html':assert data['hero']!='none'
    toggle=page.locator('[data-menu-toggle]');nav=page.locator('[data-mobile-nav]')
    if toggle.is_visible():
     toggle.click();assert nav.is_visible();assert toggle.get_attribute('aria-expanded')=='true'
     page.keyboard.press('Escape');assert not nav.is_visible();assert toggle.evaluate('(el)=>el===document.activeElement')
     toggle.click();toggle.focus();page.keyboard.press('Shift+Tab');assert nav.locator('a').last.evaluate('(el)=>el===document.activeElement');page.keyboard.press('Tab');assert toggle.evaluate('(el)=>el===document.activeElement');page.keyboard.press('Escape')
     toggle.click();nav.locator('a').first.evaluate('(el)=>el.href="#conteudo"');nav.locator('a').first.click();assert not nav.is_visible()
    if filename in ['servicos/analise-de-dados.html','servicos/ciencia-de-dados.html']:
     tracks=page.locator('.bi-bar-track,.retention-track').evaluate_all('(els)=>els.map(el=>el.getBoundingClientRect().width)')
     assert len(tracks)==2 and abs(tracks[0]-tracks[1])<1,(filename,width,tracks)
    if filename=='index.html':
     steps=page.locator('.classic-step');steps.nth(1).focus();assert page.locator('#methodMark').get_attribute('data-active')=='2'
     page.keyboard.press('Enter');assert page.locator('#methodMark').get_attribute('data-active')=='2'
     page.locator('.skip-link').focus();page.keyboard.press('Enter');assert page.url.endswith('#conteudo')
    page.add_style_tag(content='html{scroll-behavior:auto!important}');page.evaluate('document.activeElement.blur();window.scrollTo(0,0)');page.wait_for_timeout(100)
    if width in [390,1440]:page.screenshot(path=str(OUT/f'{Path(filename).stem}-{width}.png'),full_page=True)
    records.append({'page':filename,'viewport':width,**data})
    page.close()
  # Compare as duas hierarquias sob a mesma composição.
  page=browser.new_page(viewport={'width':1440,'height':900});page.goto(base)
  page.locator('h1').evaluate('(el)=>el.innerHTML="Estratégia que orienta.<br><em>Tecnologia que transforma.</em>"')
  page.screenshot(path=str(OUT/'hero-alternativa-slogan-1440.png'))
  page.close();browser.close()
finally:server.shutdown();server.server_close()
(OUT/'resultados.json').write_text(json.dumps({'browser':channel,'source':'HTTP local, HTML/CSS/JS e imagens reais','checks':records,'errors':errors},ensure_ascii=False,indent=2))
assert not errors,errors
print(f'PASS: {len(records)} combinações reais de página/largura; menu, teclado, imagens e Método Lobo.')
