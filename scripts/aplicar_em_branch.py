#!/usr/bin/env python3
"""Apply Lobo V4 overlay ONLY to an exact V6 baseline on a clean non-production git branch.
Never commits, pushes, publishes, or changes GitHub Pages settings.
Usage: python scripts/aplicar_em_branch.py /path/to/cloned/repo
"""
from pathlib import Path
import hashlib, json, subprocess, sys, shutil
HERE=Path(__file__).resolve().parents[1]
BASELINE=json.loads((HERE/'scripts/baseline_v6.json').read_text())
FILES=tuple(BASELINE)
def git(path,*cmd):
 result=subprocess.run(['git','-C',str(path),*cmd],capture_output=True,text=True)
 if result.returncode: raise RuntimeError(f"git {' '.join(cmd)}: {result.stderr.strip()}")
 return result.stdout.strip()

def main():
 if len(sys.argv)!=2: raise RuntimeError('Informe o caminho do repositório clonado.')
 target=Path(sys.argv[1]).resolve()
 if not (target/'.git').exists(): raise RuntimeError('Repositório Git local não encontrado. Nenhum arquivo alterado.')
 if git(target,'rev-parse','--show-toplevel')!=str(target): raise RuntimeError('Informe a raiz exata do clone.')
 branch=git(target,'branch','--show-current')
 if not branch or branch in ('main','master','gh-pages','production'):
  raise RuntimeError('Recusa: use uma branch de desenvolvimento não produtiva.')
 if git(target,'status','--porcelain'):
  raise RuntimeError('Recusa: o working tree não está limpo.')
 different=[]
 for name,sha in BASELINE.items():
  f=target/name
  if not f.exists():different.append(name+' (ausente)');continue
  if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:different.append(name+' (hash difere do V6)')
 if different:
  raise RuntimeError('Recusa: a base não é exatamente a V6. Faça merge manual; não sobrescreva arquivos novos:\n  '+'\n  '.join(different))
 for name in FILES:
  src=HERE/name;dst=target/name
  dst.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(src,dst)
 print('Aplicados',len(FILES),'arquivos na branch',branch)
 print('Nenhum commit, push ou deploy foi executado. Revise git diff e rode os testes antes de publicar.')
if __name__=='__main__':
 try:main()
 except Exception as exc:print('ERRO:',exc,file=sys.stderr);sys.exit(2)
