"""Verifica estrutura, links/ativos reais, identidade, exemplos e SEO sem rede.
Executar: python tests/test_static.py (beautifulsoup4, tinycss2, pillow).
"""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from PIL import Image
import json,hashlib,xml.etree.ElementTree as ET
import tinycss2
R=Path(__file__).resolve().parents[1]
files=[R/'index.html',R/'experiencia-e-resultados.html',*sorted((R/'servicos').glob('*.html'))]
checks=[]
def check(test,label):
 assert test,label
 checks.append(label)
docs={p:BeautifulSoup(p.read_text(),'html.parser') for p in files}
check(len(files)==6,'six pages')
for p,s in docs.items():
 check(s.html['lang']=='pt-BR',f'{p.name}: language')
 check(len(s.select('h1'))==1 and len(s.select('main#conteudo'))==1,f'{p.name}: landmarks')
 check(s.select_one('.skip-link[href="#conteudo"]'),f'{p.name}: skip link')
 check(s.title and s.select_one('meta[name="description"]'),f'{p.name}: metadata')
 canonical=s.select_one('link[rel="canonical"]')['href']
 expected='https://miguellobo001.github.io/lobo-analytics-business/'+('' if p.name=='index.html' else str(p.relative_to(R)))
 check(canonical==expected,f'{p.name}: canonical')
 check(s.select_one('meta[property="og:url"]')['content']==canonical,f'{p.name}: OG URL')
 check(s.select_one('[data-menu-toggle]')['aria-controls']==s.select_one('[data-mobile-nav]')['id'],f'{p.name}: menu control')
 for el in s.select('a[href],img[src],script[src],link[href]'):
  url=el.get('href') or el.get('src');u=urlsplit(url)
  if el.get('target')=='_blank':check('noopener' in el.get('rel',[]),f'{p.name}: external security')
  if u.scheme or u.netloc:continue
  dest=(p.parent/unquote(u.path)).resolve() if u.path else p
  check(dest.exists(),f'{p.name}: resource {url}')
  if u.fragment and dest.suffix=='.html':check(BeautifulSoup(dest.read_text(),'html.parser').find(id=unquote(u.fragment)),f'{p.name}: fragment {url}')
 for im in s.select('img'):
  check(im.has_attr('alt') and im.has_attr('width') and im.has_attr('height'),f'{p.name}: image dimensions/alt')
 check(s.select_one('a[href^="https://wa.me/"]'),f'{p.name}: contact')
 if p.parent.name=='servicos':
  check(len(s.select('.deliverable'))==3,f'{p.name}: three deliverables')
  check(s.select_one('figure.visual figcaption') and 'fictíci' in s.get_text().lower(),f'{p.name}: illustration disclosure')
  check(not s.select('.project-phases,.demo-reasoning'),f'{p.name}: repetitive process removed')
  links=s.select('section.subhero a[href^="https://wa.me/"],section.detail-cta a[href^="https://wa.me/"]')
  check(len(links)==2 and links[0]['href']==links[1]['href'],f'{p.name}: contextual contact consistency')
check(len({s.title.text for s in docs.values()})==6,'unique titles')
home=docs[R/'index.html']
check('Estratégia que orienta. Tecnologia que transforma.' in home.get_text(' ',strip=True),'official slogan')
check([x['points'] for x in home.select('#methodMark polygon')]==['666,250 0,848 666,848','703,268 704,737 1052,588','915,0 709,206 915,398'],'official method geometry')
check(len(home.select('.service-row'))==4 and len(home.select('.classic-step'))==3,'services and method retained')
exp=docs[R/'experiencia-e-resultados.html']
check(len(exp.select('.case-study'))==3 and all(len(c.select('.case-brief'))==3 for c in exp.select('.case-study')),'three short case studies')
check('anteriores à criação' in exp.get_text() and 'coletivo' in exp.get_text(),'career and collective attribution')
bi=docs[R/'servicos/analise-de-dados.html']
rows={r.th.text.strip():[t.text.strip() for t in r.select('td')] for r in bi.select('.bi-decision-table tbody tr')}
check(rows['Margem de contribuição']==['30','34'],'BI contribution')
check(rows['Margem sobre receita líquida']==['33,3%','28,8%'],'BI rates')
check(abs(30/90*100-33.3)<.05 and abs(34/118*100-28.8)<.05,'BI arithmetic')
sci=docs[R/'servicos/ciencia-de-dados.html']
check([[t.text.strip() for t in r.select('td')] for r in sci.select('.retention-table tbody tr')]==[['40','12','30%'],['160','16','10%']],'science data')
check('não demonstra causalidade' in sci.get_text(),'science limitation')
for p in (R/'assets').glob('*.css'):
 check(not [n for n in tinycss2.parse_stylesheet(p.read_text(),skip_comments=True,skip_whitespace=True) if n.type=='error'],f'{p.name}: CSS syntax')
urls=[x.text for x in ET.parse(R/'sitemap.xml').iter() if x.tag.endswith('loc')]
check(set(urls)=={s.select_one('link[rel="canonical"]')['href'] for s in docs.values()},'sitemap matches pages')
with Image.open(R/'assets/hero-arquitetura.webp') as im:check(im.size==(1024,1280),'hero dimensions')
check((R/'assets/hero-arquitetura.webp').stat().st_size<180000,'hero weight budget')
print(f'PASS: {len(checks)} verificações estáticas em {len(files)} páginas.')
