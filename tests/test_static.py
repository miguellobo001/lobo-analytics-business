"""Offline contract checks for the V6 overlay. Run: python tests/test_static.py
No claims about the missing original assets or live deployment are made.
"""
from pathlib import Path
import re, sys, json, xml.etree.ElementTree as ET
from urllib.parse import urlsplit, parse_qs, unquote
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
HTML=[R/'index.html',R/'experiencia-e-resultados.html',*sorted((R/'servicos').glob('*.html'))]
EXPECTED={"diagnostico.html","analise-de-dados.html","automacao-e-ia.html","ciencia-de-dados.html"}
OK=[]
def check(test,msg):
 assert test,msg
 OK.append(msg)
check(len(HTML)==6,'six HTML pages')
check({p.name for p in HTML if p.parent.name=='servicos'}==EXPECTED,'four unchanged service URLs')
check((R/'assets/institucional.css').exists(),'additive CSS exists')
for p in HTML:
 s=BeautifulSoup(p.read_text(), 'html.parser')
 check(len(s.select('h1'))==1, f'{p.name}: one H1')
 check(len(s.select('main#conteudo'))==1,f'{p.name}: skip-link target')
 check(len(s.select('a.skip-link[href="#conteudo"]'))==1,f'{p.name}: keyboard bypass')
 check(len(s.select('meta[name="description"]'))==1,f'{p.name}: meta description')
 check(len(s.select('link[rel="canonical"]'))==1,f'{p.name}: canonical')
 check(len(s.select('meta[property="og:title"]'))==1,f'{p.name}: OG title')
 check(len(s.select('meta[property="og:image"]'))==1,f'{p.name}: OG image reference')
 check(len(s.select('nav[data-mobile-nav]'))==1,f'{p.name}: mobile nav markup')
 check(len(s.select('script[src$="main.js"]'))==1,f'{p.name}: preserves legacy JS')
 for a in s.select('a[href]'):
  href=a['href']
  if href.startswith(('#','http:','https:','mailto:','tel:')):continue
  target=urlsplit(href).path
  resolved=(p.parent/target).resolve()
  if resolved.suffix.lower() in ('.html','.xml','.txt'):
   check(resolved.exists(),f'{p.name}: internal {target} exists')
 for svg in s.select('svg[role="img"]'):
  refids=svg.get('aria-labelledby','').split()
  check(len(refids)>0 and all(svg.select_one('#'+i) for i in refids),f'{p.name}: SVG labeled')
# CTA copied from client context, not fictional
for p in HTML:
 if p.parent.name!='servicos':continue
 s=BeautifulSoup(p.read_text(),'html.parser')
 links=[urlsplit(x['href']) for x in s.select('section.subhero a[href^="https://wa.me/"],section.detail-cta a[href^="https://wa.me/"]')]
 check(len(links)==2 and links[0].query==links[1].query,p.name+': consistent contextual CTA')
 check(len(s.select('figure.visual'))==1,p.name+': visual demonstration')
 check(len(s.select('figure.visual figcaption'))==1,p.name+': illustrative disclosure')
 check(len(s.select('p.service-usecase'))==1,p.name+': business use-case')
 check(all(x['href'].startswith('https://wa.me/') for x in s.select('section.subhero a.button')),p.name+': WhatsApp URL')
check('process-visual' in (R/'servicos/automacao-e-ia.html').read_text(),'before/after process visualization')
check('Receita' in (R/'servicos/analise-de-dados.html').read_text() and 'Descontos' in (R/'servicos/analise-de-dados.html').read_text() and 'Margem' in (R/'servicos/analise-de-dados.html').read_text(),'revenue/discounts/margin demo')
check('Impacto esperado' in (R/'servicos/diagnostico.html').read_text(),'impact-effort matrix')
check('significância estatística' in (R/'servicos/ciencia-de-dados.html').read_text(),'uncertainty disclaimer in DS demo')
home=(R/'index.html').read_text()
check('Estratégia que orienta.' in home and 'Tecnologia que transforma.' in home,'exact brand slogan')
check('O símbolo da Lobo é também o seu método.' in home,'method headline maintained')
# interactive original method markup (figure + steps only), unchanged versus prior package if mounted
old=Path('/mnt/data/lobo_work/index.html')
if old.exists():
 def method(s):
  m=re.search(r'(<figure class="classic-mark".*?</ol>)',s,flags=re.S);assert m
  return m.group(1)
 check(method(home)==method(old.read_text()),'interactive method symbol and steps untouched')
check('resultados da trajetória profissional da liderança técnica' in home.lower(),'home career-results disclaimer')
case=(R/'experiencia-e-resultados.html').read_text()
check(case.count('class="case-study"')==3,'three prior-career case studies')
check('não são projetos comerciais da consultoria' in case.lower(),'not commercial Lobo references')
check('projeto coletivo' in case.lower(),'collective achievement clearly recognized')
check(len(re.findall(r'<script(?![^>]*application/ld\+json)',home))==1,'only original external JavaScript')
sitemap=ET.parse(R/'sitemap.xml'); urls=[e.text for e in sitemap.iter() if e.tag.endswith('loc')]
check(len(urls)==6 and len(set(urls))==6,'six unique sitemap URLs')
check('miguellobo001.github.io/lobo-analytics-business/' in (R/'robots.txt').read_text(),'sitemap URL in robots')
# Important: known original assets intentionally not bundled; never misrepresent as complete autonomous site.
for resource in ['assets/style.css','assets/main.js','assets/logo-clara.png','assets/favicon.png','assets/simbolo-claro.png']:
 check(not (R/resource).exists(),f'original {resource} intentionally not overwritten')
print(f'PASS: {len(OK)} static assertions across {len(HTML)} HTML files.')
