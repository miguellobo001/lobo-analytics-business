"""Verificações estáticas da estrutura do site (sem instalar dependências Python).

Execute a partir da raiz do projeto:
    python tests/validar_estatico.py

O script não edita arquivos nem publica conteúdo.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.resources: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.internal_anchors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])

        attribute = "src" if tag in {"img", "script", "source"} else "href"
        if tag in {"a", "link", "img", "script", "source"}:
            reference = attributes.get(attribute)
            if reference:
                self.resources.append((tag, reference))
                if tag == "a" and reference.startswith("#"):
                    self.internal_anchors.append(reference[1:])


def main() -> int:
    pages = sorted(ROOT.rglob("*.html"))
    scripts = sorted((ROOT / "assets").glob("*.js"))
    problems: list[str] = []
    checked = 0

    if len(pages) != 9:
        problems.append(f"Esperadas 9 páginas HTML; encontradas {len(pages)}.")

    for html in pages:
        parser = ResourceParser()
        parser.feed(html.read_text(encoding="utf-8"))
        for fragment in parser.internal_anchors:
            if fragment and fragment not in parser.ids:
                problems.append(f"Âncora inexistente: {html.relative_to(ROOT)}#{fragment}")

        for tag, reference in parser.resources:
            url = urlparse(reference)
            if url.scheme or url.netloc or reference.startswith(("//", "mailto:", "tel:", "data:")):
                continue
            if not url.path:
                continue
            target = (html.parent / unquote(url.path)).resolve()
            # URLs relativas apontando para uma pasta são válidas quando contêm index.html.
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                problems.append(f"Recurso inexistente: {html.relative_to(ROOT)} -> {reference}")
            else:
                checked += 1

    node = shutil.which("node")
    if node:
        for js in scripts:
            result = subprocess.run([node, "--check", str(js)], capture_output=True, text=True)
            if result.returncode:
                problems.append(f"JavaScript inválido em {js.relative_to(ROOT)}: {result.stderr.strip()}")
    else:
        print("Node.js não encontrado: verificação de sintaxe JavaScript omitida.")

    print(f"Páginas HTML: {len(pages)}")
    print(f"Referências locais verificadas: {checked}")
    print(f"Arquivos JavaScript: {len(scripts)}" + (" (sintaxe validada)" if node else ""))

    if problems:
        for problem in problems:
            print(f"ERRO: {problem}", file=sys.stderr)
        return 1

    print("Resultado: nenhuma referência quebrada ou erro de sintaxe identificado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
