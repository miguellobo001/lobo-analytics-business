# Lobo Analytics & Business — evolução institucional V6

## O que este pacote é

**Overlay de atualização**, preparado a partir do pacote institucional V5 entregue anteriormente nesta conversa. Contém os HTMLs completos das páginas alteradas, o CSS complementar, sitemap, robots e os testes. **Não é uma cópia integral e autônoma do repositório.**

Neste ambiente, a tentativa de acessar o repositório/website atual via rede falhou. Portanto, **não foi possível comparar ou auditar a versão atual publicada, clonar o projeto nem inspecionar os arquivos originais** `assets/style.css`, `assets/main.js` e as imagens oficiais. Os arquivos existentes referenciados nos HTMLs devem ser preservados no repositório. Não presuma que o pacote corresponde à última versão remota caso tenham ocorrido alterações após a V5.

Nenhum arquivo foi enviado ao GitHub, nenhum conteúdo foi publicado e nenhuma informação externa foi coletada automaticamente.

## Como aplicar

1. Faça backup/commit da versão atual do repositório e confirme que ela corresponde estruturalmente ao pacote V5.
2. Compare os HTMLs atuais com este pacote, especialmente o Método Lobo, antes de substituir arquivos.
3. Copie os arquivos deste ZIP para a raiz do repositório: `index.html`, `experiencia-e-resultados.html`, `servicos/*.html`, `assets/institucional.css`, `sitemap.xml` e `robots.txt`. **Não remova outros arquivos**.
4. Preserve integralmente `assets/style.css`, `assets/main.js`, `assets/logo-clara.png`, `assets/simbolo-claro.png`, `assets/favicon.png` e demais assets oficiais existentes.
5. Revise a divulgação dos três resultados da trajetória de Miguel Lobo. Os dados ainda **não possuem autorização de divulgação confirmada neste ambiente**. Não publique os HTMLs com esses números sem revisão e autorização aplicáveis.
6. Execute `python tests/test_static.py` na raiz do projeto e teste navegação, menu, Método Lobo, imagens, responsividade e CTAs no navegador **com os assets reais**.
7. Somente após revisão e testes, faça commit/push e verifique o GitHub Pages publicado.

## Alterações importantes

- **Home:** preserva slogan oficial e Método Lobo, refina texto de negócio, hierarquia, CTA, acesso à página de experiência, seção institucional e resultados anteriores.
- **Quatro serviços:** adiciona situação de uso, entregáveis possíveis, contato contextualizado, visualizações distintas e exemplificações declaradamente fictícias.
- **Mobile:** para as demonstrações de diagnóstico, BI e ciência de dados há versões adaptadas em HTML/CSS para leitura em telas pequenas; automação usa um processo responsivo nativo.
- **Experiência e resultados:** reformula a narrativa dos três estudos sem transformar o histórico profissional em casos comerciais da Lobo; participação em projeto coletivo permanece explícita.
- **Acessibilidade:** inclui link de salto para o conteúdo, estados de foco, descrições de SVG, legendas e melhorias de contraste no CSS complementar.
- **SEO:** atualiza título e descrição existentes, inclui JSON-LD institucional factual na Home, sitemap e robots; canonical e Open Graph continuam nas páginas.
- **Mensuração:** adiciona atributos `data-page-type`, `data-page-id`, `data-event` e `data-service` para **integração futura** com analytics; nenhum script de rastreamento e nenhuma coleta foram habilitados.

## Notas específicas

- A composição central do Método Lobo (SVG original e etapas interativas) foi preservada byte a byte em relação ao pacote V5. Apenas a nota explicativa ao fim da seção foi editada.
- O arquivo `assets/institucional.css` é **complementar** ao CSS original. Não substitui a base nem redefine a identidade oficial.
- `robots.txt` dentro de um projeto GitHub Pages em subcaminho pode **não ser considerado por robôs que procuram `https://usuario.github.io/robots.txt`**. Mantenha-o preparado para migração a domínio próprio, mas não trate isso como validação de indexação.
- Open Graph usa `assets/logo-clara.png` existente. A qualidade do cartão de compartilhamento depende das dimensões e da aparência do arquivo oficial, que não pôde ser inspecionado aqui.
- Não foi criada política de privacidade fictícia. Caso analytics seja instalado, documente o uso efetivo e revise a base legal/consentimentos aplicáveis.

Consulte `RELATORIO-DE-VALIDACAO.md` para testes executados e pendências.
