# Master V5 — relatório de implementação e validação

31/10/2026. Trabalho local em `feat/lobo-master-v5`, baseado em `62d61cdec5802bcabc8070ec84a0625433d76593`. Sem publicação.

## Auditoria da base

A árvore estava limpa em `main`. `origin` aponta para `https://github.com/miguellobo001/lobo-analytics-business.git`; `git ls-remote` confirmou o mesmo commit em `main` remota. O HTML obtido de `https://miguellobo001.github.io/lobo-analytics-business/` era byte a byte idêntico à Home local antes da edição. A API pública `/repos/miguellobo001/lobo-analytics-business/pages` retornou 404: a configuração de origem do Pages não pôde ser confirmada. Igualdade da Home não comprova a origem completa do deploy.

Foram lidos os seis HTML, os dois CSS e o JavaScript. A versão anterior foi renderizada com os assets reais no Chrome, em 390 e 1440 px, antes das mudanças. Os problemas principais eram o Hero dependente do símbolo e a repetição de processo, contexto e ressalvas nos serviços e nos estudos. Os testes antigos afirmavam que os assets originais estavam ausentes; foram atualizados para refletir o checkout completo.

## Direção de arte e edição

Arquitetura abstrata, luz lateral, azul-noturno e cobre como imagem editorial; serifada EB Garamond e sans DM Sans preservadas. Logotipos e imagens oficiais não foram alterados. A geometria exata do Método Lobo e sua ligação com as três etapas permanecem. Nenhum cliente, pessoa, depoimento ou resultado novo foi criado.

A Home mantém apenas Hero, soluções, método, instituição/resultados, contato e rodapé. As descrições dos serviços continuam visíveis no celular. A liderança aparece pelo nome, campo de atuação e LinkedIn; não foi encontrado retrato real no acervo, e não foi gerado substituto.

Comparação editorial das duas hierarquias de Hero: “Negócio primeiro. Ferramentas depois.” comunica diretamente o critério de atuação e ocupa menos espaço; o slogan oficial funciona como assinatura institucional. A alternativa com slogan como H1 foi renderizada na mesma composição e registrada em `evidencias/master-v5/hero-alternativa-slogan-1440.png`. A escolha é uma avaliação de direção de arte, não um teste de conversão com usuários.

### Redução de conteúdo

Contagem de palavras no texto de `main`, via BeautifulSoup `get_text(' ', strip=True).split()`, comparada ao checkout inicial. Inclui rótulos das visualizações e suas alternativas acessíveis; não inclui header e footer.

| Página | Antes | Depois* | Redução aproximada |
| --- | ---: | ---: | ---: |
| Home | 424 | 275 | 35% |
| Experiências | 468 | 231 | 51% |
| Diagnóstico | 447 | 287 | 36% |
| BI | 407 | 232 | 43% |
| Automação e IA | 382 | 216 | 43% |
| Ciência de dados | 390 | 214 | 45% |

*Pequenas variações na contagem resultam de espaços entre elementos após a formatação do HTML. O arquivo `editorial.json` registra a contagem final com o mesmo critério.

### Demonstrações

- Diagnóstico: matriz impacto/esforço em SVG; alternativa mobile com os mesmos quadrantes e iniciativas.
- BI: receita, descontos, custos e contribuição; 30/90 = 33,3%, 34/118 = 28,8%. Não equivale a lucro líquido. A queda da taxa não atribui causalidade.
- Automação: antes/depois de reembolsos, captura e integração, regras e revisão humana de exceções.
- Ciência de dados: 40 clientes/12 cancelamentos = 30%; 160/16 = 10%; 200 clientes e 28 cancelamentos. Associação observacional sem promessa preditiva.

## Imagem e procedência

`assets/hero-arquitetura.webp`: 1024 × 1280, 86.302 bytes. Gerada com a ferramenta integrada Imagegen, sem fotografia externa, pessoas, marca redesenhada ou representação de instalações reais. `assets/hero-social.jpg`: derivação de 1200 × 630 para Open Graph. O PNG original permanece no diretório de imagens geradas do Codex. A conversão local apenas ajusta dimensões e codificação.

Prompt final da geração:

> Use case: stylized-concept. Asset type: original editorial website hero for Lobo Analytics & Business, no text. Create a sophisticated architectural still life, portrait 4:5 composition: monumental minimalist dark midnight blue (#102631) planar walls and broad ascending platforms, a single matte brushed copper (#B99569) vertical plane catching soft natural side light. Warm ivory light through a tall opening. Strong spatial depth, tactile fine plaster and metal, restrained cinematic shadows, quiet premium B2B editorial art direction. Abstract architecture symbolizing direction, structure and progress. Cropped close, no horizon, no decorative objects. Not an actual company office. No people, no logos, no triangles resembling a logo, no lettering, no charts, no holograms. Entire image filled with rich architectural composition, balanced light and shadow.

A imagem do Hero tem dimensões explícitas, `fetchpriority="high"` e permanece visível em mobile. Não foram acrescentadas outras fotografias abaixo da primeira tela. Logo e símbolo são os ativos originais.

Referências: consultado o conteúdo público da [Manyone](https://manyone.com/) para organização de serviços e trabalhos. As tentativas de acesso a Boi Design e Prophet pela ferramenta web falharam; não se afirma auditoria visual desses sites. Nenhuma imagem de referência foi incorporada.

## Validação executada

- `python tests/test_static.py`: 302 verificações aprovadas sobre seis páginas, links/fragmentos locais, recursos existentes, segurança de links externos, metadados, canonical, sitemap, dimensões de imagem, integridade da geometria, entregáveis e aritmética dos exemplos.
- `python tests/test_browser.py`: Chrome headless real, HTTP local e arquivos reais. Seis páginas × 360, 390, 768, 1024 e 1440 px. Verifica overflow, imagens, H1, menu e Escape, ciclo de foco no menu, ligação por foco/Enter com o símbolo e skip link; também compara as larguras das escalas nas barras.
- Capturas completas de todas as páginas em 390 e 1440 px, com alternativa do Hero. Revisão visual levou a ajustes de quebras do Hero, margens do rodapé e rótulo de tabela mobile.
- CSS complementar consolidado, removendo as camadas históricas redundantes. HTML formatado para revisão. Nenhuma biblioteca adicionada ao site; dependências Python são apenas para testes.
- `git diff --check`: executado para verificar espaços e conflitos textuais.

As evidências novas estão em `evidencias/master-v5/`. As capturas antigas de CSS simulado permanecem identificadas como históricas e não representam esta versão.

## Limites e pendências

Não foram executados Lighthouse, testes com leitores de tela ou medições de Core Web Vitals em produção. Não se declara conformidade WCAG integral nem pontuação de desempenho. As fontes continuam usando o Google Fonts já existente. Links de WhatsApp/LinkedIn/e-mail foram preservados; testes não enviam mensagens nem validam a titularidade das contas.

Antes de publicar, revisar o conteúdo e confirmar as autorizações de divulgação dos três resultados, preservando a natureza coletiva do estudo de descontos. Confirmar também branch/pasta ou workflow efetivo do GitHub Pages. O retrato real e profissional de Miguel Lobo é o único ativo fotográfico opcional pendente. Não há aprovação presumida de publicação.
