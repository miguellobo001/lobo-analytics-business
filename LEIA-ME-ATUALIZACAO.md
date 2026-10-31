# Evolução visual e comercial — Master V5

Implementada no projeto existente, na branch local `feat/lobo-master-v5`. Sem commit, push, merge ou publicação automática.

A Home agora combina a mensagem **“Negócio primeiro. Ferramentas depois.”** com uma imagem editorial original. O slogan oficial continua como assinatura. Marca, quatro serviços, geometria e interação do Método Lobo, contatos e URLs foram preservados.

As quatro páginas de serviços apresentam situação de uso, três entregáveis, demonstração específica com dados fictícios e CTA contextual. A página de experiências tem três estudos em Problema / Abordagem / Resultado, com atribuição profissional anterior e natureza coletiva explícitas.

- [Relatório de validação e direção de arte](RELATORIO-DE-VALIDACAO.md)
- [Captura desktop](evidencias/master-v5/index-1440.png)
- [Captura mobile](evidencias/master-v5/index-390.png)
- [Resultados dos testes reais](evidencias/master-v5/resultados.json)

Para visualizar, execute `python3 -m http.server 8000` na raiz e abra `http://localhost:8000`. Encerre o servidor com Ctrl+C.

Para validar, instale `tests/requirements.txt` em um ambiente Python isolado e execute `python tests/test_static.py` e `python tests/test_browser.py`. O teste visual usa Chrome instalado. Para Chromium do Playwright, instale-o e use `BROWSER_CHANNEL=chromium`.

Os arquivos em `patches/`, o aplicador em `scripts/` e as evidências com CSS simulado são históricos da edição anterior. Não execute o aplicador antigo para instalar esta versão: os arquivos desta branch já constituem a evolução integrada.

Pendências para publicação: revisão final do conteúdo, confirmação das autorizações de divulgação dos resultados e da configuração efetiva de GitHub Pages. Não foi encontrado retrato profissional autorizado de Miguel; sua inclusão futura é opcional e não há placeholder público.
