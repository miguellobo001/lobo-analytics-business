# Lobo Analytics & Business — refinamento Master V4 (sobre base local V6)

**Status: pacote de desenvolvimento; NÃO publicado.** Esta atualização não é um clone completo do repositório. Foi construída a partir de `lobo-analytics-business-v6.zip`, entregue nesta conversa, e contém os arquivos alterados e documentação de validação. Seu nome V4 acompanha o prompt de refinamento; a referência técnica é o pacote local V6.

## Restrição de origem — importante

As tentativas de acesso direto a `github.com/miguellobo001/lobo-analytics-business` e `miguellobo001.github.io/lobo-analytics-business/` falharam neste ambiente, inclusive pelo mecanismo de navegação web. **Não foi possível verificar a versão publicada, as branches, o commit de produção, a origem do GitHub Pages ou a presença de atualizações feitas depois da V6.** Não foram inspecionados os originais `assets/style.css`, `assets/main.js` ou as imagens e fontes oficiais.

Este pacote é, portanto, **uma evolução condicionada à conferência da base**. Não o descompacte diretamente sobre um repositório que possa conter arquivos mais recentes. O aplicador seguro verifica hashes da V6 e impede substituição automática em branches de produção ou em worktrees alterados.

## Como integrar sem risco de sobrescrever trabalho mais novo

1. No GitHub, abra **Settings → Pages**, anote a origem da publicação (`Deploy from a branch` ou `GitHub Actions`) e confirme a branch/pasta de publicação. Se usa Actions, confira o workflow em `.github/workflows/`.
2. Em clone local atualizado, execute `git fetch --all --prune`, `git branch -avv` e examine `git log -5 --oneline --decorate` na branch fonte do deploy. Compare as versões de `index.html` e `experiencia-e-resultados.html` com o pacote local V6 antes de prosseguir.
3. Confira o HTML publicado no navegador, usando uma janela privada e um parâmetro de URL de teste (`?revisao=...`) para diferenciar cache de alteração na origem. Um parâmetro não invalida necessariamente todos os caches, por isso avalie também o commit do deploy. Não altere a configuração do Pages sem entender o processo.
4. Crie uma branch de trabalho **a partir da origem efetiva que estiver atualizada**, não necessariamente de `main`: `git switch -c feat/lobo-master-v4`.
5. Descompacte este ZIP **fora** do repositório. Se a sua branch contém exatamente os sete arquivos V6 esperados e está limpa, execute, a partir da pasta extraída: `python scripts/aplicar_em_branch.py /caminho/para/seu/clone`.
6. Se o aplicador bloquear, **não force a cópia**: o repositório não corresponde à V6 esperada. Use `patches/v6-para-master-v4.patch` somente após inspecionar cada hunk e realizar merge das melhorias à versão atualizada. Não use `git apply --check` como prova de que a base é a mesma; hashes e revisão manual continuam necessários.
7. Preserve os assets originais `assets/style.css`, `assets/main.js`, `assets/logo-clara.png`, `assets/simbolo-claro.png`, `assets/favicon.png`, fontes e demais recursos. O arquivo `assets/institucional.css` complementa, não substitui, `assets/style.css`.
8. Execute `python tests/test_static.py` na pasta extraída para checagens offline. Com o projeto completo, teste a página no navegador real, em 360, 390, 768, 1024 e 1440 px; verifique visualmente marca, Método Lobo, menu móvel, links de contato e funcionalidades do JavaScript original.
9. **Antes de merge/deploy**, confirme autorização de divulgação dos indicadores profissionais e eventuais informações confidenciais, além de revisar os textos históricos. Só publique com aprovação expressa do conteúdo e da equipe responsável.

O script NÃO faz commit, push ou deploy. `sitemap.xml` e `robots.txt` permanecem os arquivos da V6: não foram modificados no refinamento. Mantenha versões remotas mais recentes se existirem.

## Arquivos de produção alterados

- `index.html` — posicionamento da seção institucional, descrição de resultados e conversa consultiva. Hero, slogans e bloco HTML do Método Lobo preservados.
- `experiencia-e-resultados.html` — três estudos editoriais com contexto, investigação conhecida, leitura de negócio claramente diferenciada de fatos, resultado e participação; atribuição correta de projeto coletivo.
- `servicos/diagnostico.html` — situação de uso, condução do projeto e matriz com iniciativas fictícias identificadas e leitura da decisão.
- `servicos/analise-de-dados.html` — exemplo financeiro fechado e coerente, com fórmula de margem de contribuição e ressalvas.
- `servicos/automacao-e-ia.html` — processo ilustrativo de reembolso com validação de regras e revisão humana.
- `servicos/ciencia-de-dados.html` — comparação fictícia de cancelamento em dois grupos, sem confundir associação com causalidade.
- `assets/institucional.css` — layout editorial, tabelas acessíveis, demonstrações, responsividade e refinamento de títulos.

## Arquivos de apoio (não publicar como páginas de produção)

- `scripts/aplicar_em_branch.py`, `scripts/baseline_v6.json`: aplicação condicional com proteções de Git e integridade.
- `patches/v6-para-master-v4.patch`: diff para revisão, não aplicar cegamente sobre arquivos mais novos.
- `tests/test_static.py`: asserções offline de estrutura, links, SEO declarativo e fórmulas.
- `tests/test_browser_simulado.py`: renderização Chromium `set_content` com CSS-base **SIMULADO**, já que os assets originais não foram obtidos.
- `tests/fixtures/style-base-SIMULADO.css`: arquivo exclusivamente para testes, **não usar em produção**.
- `evidencias/simulado-css-nao-e-producao/`: prints e registro de 30 combinações de página/largura com CSS-base simulado. **Não são prints do site publicado nem certificam sua aparência final.**
- `RELATORIO-DE-VALIDACAO.md`: testes e pendências explícitas.

## Considerações de publicação e privacidade

- Os três resultados da liderança são informações fornecidas na conversa, não evidências documentais verificadas neste ambiente; a divulgação pública depende de autorização/confidencialidade.
- Os exemplos das páginas de serviços usam dados **fictícios e explicitamente identificados**; não são contratos comerciais da Lobo.
- Mantivemos as URLs e contatos existentes no pacote V6, mas a validade atual ainda precisa ser confirmada pelo responsável.
- Atributos `data-event`/`data-service` preparam integração futura, mas não há coleta de analytics e não foram adicionados scripts/IDs fictícios.
- Dados empresariais, política de privacidade, domínio, e-mail corporativo e certificações não foram inventados.
- **Nenhuma pontuação Lighthouse, medição real de Core Web Vitals, conformidade WCAG integral ou verificação live do GitHub Pages foi reivindicada.**
