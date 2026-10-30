"""Browser layout simulation using Chromium page.set_content, not the deployed website.
The real assets/style.css, assets/main.js and official identity images are not available.
This test injects a clearly labeled *mock* CSS base and the actual updated supplemental CSS.
It measures overflow and renders content in 30 page/viewport combinations only.
Usage: python tests/test_browser_simulado.py
"""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1]
OUT=R/'evidencias'/'simulado-css-nao-e-producao'
OUT.mkdir(parents=True,exist_ok=True)
mock=(R/'tests/fixtures/style-base-SIMULADO.css').read_text()
real_supplement=(R/'assets/institucional.css').read_text()
widths=[360,390,768,1024,1440]
pages=['index.html','experiencia-e-resultados.html','servicos/diagnostico.html','servicos/analise-de-dados.html','servicos/automacao-e-ia.html','servicos/ciencia-de-dados.html']
records=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for filename in pages:
  soup=BeautifulSoup((R/filename).read_text(),'html.parser')
  for tag in soup.select('link[rel="stylesheet"],script[src]'):tag.decompose()
  # Explicit visual marker; screenshots are NOT those of production.
  mark=soup.new_tag('div',attrs={'class':'simulation-mark'})
  mark.string='Prévia de componentes com CSS-base simulado — não é o site publicado'
  soup.body.insert(0,mark)
  style=soup.new_tag('style')
  style.string=mock+'\n'+real_supplement+'\n.simulation-mark{position:relative;z-index:40;background:#f2eee7;color:#102631;padding:7px;text-align:center;font:600 11px Arial;letter-spacing:.02em}.brand img,.site-foot img,.hero-symbol img{visibility:hidden} .brand:after{content:"LOBO — marca não carregada";font:11px Arial;color:#f2eee7;display:block}\n'
  soup.head.append(style)
  doc=str(soup)
  for width in widths:
   page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
   page.set_content(doc,wait_until='load')
   data=page.evaluate('''() => ({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,h1:document.querySelectorAll('h1').length,demo:document.querySelectorAll('.demo-reasoning-item').length})''')
   rec={'page':filename,'viewport':width,'scrollWidth':data['scroll'],'clientWidth':data['client'],'overflow':data['scroll']>data['client']+1,'h1':data['h1'],'demo':data['demo']}
   records.append(rec)
   if (filename,width) in [('index.html',390),('index.html',1440),('experiencia-e-resultados.html',390),('experiencia-e-resultados.html',1440),('servicos/analise-de-dados.html',390),('servicos/ciencia-de-dados.html',390)]:
    page.screenshot(path=str(OUT/f"{filename.split('/')[-1].replace('.html','')}-{width}.png"),full_page=True)
   page.close()
 browser.close()
(OUT/'resultados.json').write_text(json.dumps({'caveat':'CSS base simulated, main.js absent; screenshots do not represent actual website or test real navigation','browser':'Chromium','tests':records},ensure_ascii=False,indent=2))
fail=[r for r in records if r['overflow'] or r['h1']!=1]
print('SIMULATED BROWSER',len(records),'tests:',len(fail),'overflow/H1 failures')
for rec in fail:print('FAIL',rec)
if fail:raise SystemExit(1)
