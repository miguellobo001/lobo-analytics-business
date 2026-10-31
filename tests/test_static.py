"""Offline static checks. Run from the distribution root: python tests/test_static.py
Does not prove deployed version, visual fidelity with original assets or WCAG AA.
"""
from pathlib import Path
from urllib.parse import urlsplit,parse_qs,unquote
from bs4 import BeautifulSoup
import hashlib, json, re, xml.etree.ElementTree as ET
import tinycss2
R=Path(__file__).resolve().parents[1]
html_files=[R/'index.html',R/'experiencia-e-resultados.html',*sorted((R/'servicos').glob('*.html'))]
ok=[]
def check(test,msg):
 assert test,msg
 ok.append(msg)
check(len(html_files)==6,'six expected HTML pages')
check(set(p.name for p in html_files if p.parent.name=='servicos')=={'diagnostico.html','analise-de-dados.html','automacao-e-ia.html','ciencia-de-dados.html'},'four service URLs retained')
for path in html_files:
 s=BeautifulSoup(path.read_text(), 'html.parser')
 check(s.html.get('lang')=='pt-BR',f'{path.name}: pt-BR lang')
 check(len(s.select('h1'))==1,f'{path.name}: one H1')
 check(len(s.select('main#conteudo'))==1,f'{path.name}: main landmark')
 check(len(s.select('.skip-link[href="#conteudo"]'))==1,f'{path.name}: skip link')
 check(len(s.select('head > title'))==1 and bool(s.title.get_text(strip=True)),f'{path.name}: title')
 check(len(s.select('meta[name="description"]'))==1,f'{path.name}: description')
 check(len(s.select('link[rel="canonical"]'))==1,f'{path.name}: canonical')
 check(len(s.select('meta[property="og:image"]'))==1,f'{path.name}: OG image declared (asset availability not tested)')
 check(len(s.select('nav[data-mobile-nav]'))==1,f'{path.name}: legacy menu markup preserved')
 check(len(s.select('script[src$="main.js"]'))==1,f'{path.name}: original JS reference preserved')
 check(len(s.select('a[href^="https://wa.me/"]'))>0,f'{path.name}: WhatsApp contact exists')
 for a in s.select('a[href]'):
  u=a['href']
  if urlsplit(u).scheme or u.startswith('#'):continue
  resolved=(path.parent/urlsplit(u).path).resolve()
  if resolved.suffix.lower() in ('.html','.xml','.txt'):
   check(resolved.exists(),f'{path.name}: local link target exists: {u}')
  if '#' in u and u.split('#')[1] and resolved.exists() and resolved.suffix=='.html':
   dest=BeautifulSoup(resolved.read_text(),'html.parser')
   check(dest.find(id=u.split('#')[1]) is not None, f'{path.name}: fragment target {u} exists')
 if path.parent.name=='servicos':
  check(len(s.select('h3'))>=4,f'{path.name}: explanatory headings present')
  check('Quando este serviço faz sentido?' in s.get_text(' ',strip=True),f'{path.name}: fit guidance')
  check(len(s.select('.project-phases li'))==5,f'{path.name}: project phases')
  check(len(s.select('.demo-reasoning-item'))==4,f'{path.name}: question data observation decision')
  check(len(s.select('figure.visual figcaption'))==1,f'{path.name}: illustrative disclosure')
  check(s.select_one('.crumb [aria-current="page"]') is not None,f'{path.name}: descriptive breadcrumb')
  links=[urlsplit(x['href']) for x in s.select('section.subhero a[href^="https://wa.me/"],section.detail-cta a[href^="https://wa.me/"]')]
  check(len(links)==2 and links[0].query==links[1].query,f'{path.name}: contextual CTA')
check(len({BeautifulSoup(p.read_text(),'html.parser').title.text for p in html_files})==6,'unique title tags')
check('Estratégia que orienta.' in (R/'index.html').read_text() and 'Tecnologia que transforma.' in (R/'index.html').read_text(),'official slogan')
from zipfile import ZipFile
previous=Path('/mnt/data/lobo-analytics-business-v6.zip')
if previous.exists():
 def method(t):return re.search(r'<section class="method-classic".*?</section>',t,re.S).group(0)
 with ZipFile(previous) as z:previous_home=z.read('index.html').decode('utf8')
 check(method(previous_home)==method((R/'index.html').read_text()),'Method Lobo block byte for byte unchanged from V6')
experience=BeautifulSoup((R/'experiencia-e-resultados.html').read_text(),'html.parser')
check(len(experience.select('article.case-study'))==3,'three career cases')
check(all(len(case.select('.case-brief'))==5 for case in experience.select('article.case-study')),'context, investigation, business reading, result, ownership')
check('não são contratos da lobo' in experience.get_text(' ',strip=True).lower(),'results clearly not customers')
check('projeto coletivo' in experience.get_text(' ',strip=True),'collective role stated')
check('anteriores à criação' in experience.get_text(' ',strip=True),'prior employment disclaimer')
bi=BeautifulSoup((R/'servicos/analise-de-dados.html').read_text(),'html.parser')
rows={x.th.text.strip():[c.text.strip() for c in x.select('td')] for x in bi.select('.bi-decision-table tbody tr')}
check(rows['Margem de contribuição']==['30','34'],'BI contribution margin Jan, Apr')
check(rows['Margem sobre receita líquida']==['33,3%','28,8%'],'BI percentages consistent')
assert abs(30/(100-10)*100-33.3)<.05 and abs(34/(140-22)*100-28.8)<.05
check(True,'BI sample financial arithmetic')
sci=BeautifulSoup((R/'servicos/ciencia-de-dados.html').read_text(),'html.parser')
rows=[[td.get_text(strip=True) for td in tr.select('td')] for tr in sci.select('.retention-table tbody tr')]
check(rows==[['40','12','30%'],['160','16','10%']],'science sample rates and sample sizes')
check('não demonstra causalidade' in sci.get_text(' ',strip=True),'correlation caveat')
css=(R/'assets/institucional.css').read_text();parse=tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True)
check(not [x for x in parse if x.type=='error'],'supplemental CSS parses')
urls=[x.text for x in ET.parse(R/'sitemap.xml').iter() if x.tag.endswith('loc')]
check(len(urls)==len(set(urls))==6,'sitemap six unique pages')
check('miguellobo001.github.io/lobo-analytics-business/' in (R/'robots.txt').read_text(),'robots references sitemap')
for original in ['assets/style.css','assets/main.js','assets/logo-clara.png','assets/simbolo-claro.png','assets/favicon.png']:
 check(not (R/original).exists(),f'original asset deliberately not included: {original}')
print('PASS',len(ok),'offline static assertions across',len(html_files),'pages')
