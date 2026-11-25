# Lobo Analytics & Business — guia técnico

Site institucional **estático**, sem build, frameworks ou dependências remotas.

## Estrutura

- `index.html`: página inicial.
- `servicos/`, `especialidades/`, `metodo/`, `sobre/`, `contato/`: páginas internas.
- `assets/style.css`: estilos do layout, cores e pontos de quebra.
- `assets/motion.css`: estilos dos movimentos e acessibilidade.
- `assets/script.js`: menu e cópia da mensagem de contato.
- `assets/motion.js`: revelação bidirecional, profundidade e rolagem suave.
- `assets/gallery-fade.js`: cobertura do carrossel, apenas na página inicial.
- `assets/hero-rotator.js`: alternância do título, apenas na página inicial.
- `assets/images/`: imagens WebP utilizadas nas páginas.

## Parâmetros atuais preservados

- Sobreposição do carrossel no JavaScript: `base = mobile ? 66 : 95`;
  `extra = mobile ? 40 : 65`.
- Máscara da borda da galeria: faixa de 2 px.
- Título dinâmico: `decidir.`, `priorizar.`, `avançar.` a cada 3,6 s.
- Movimento reduzido respeitado via `prefers-reduced-motion`.

## Publicação

O site pode ser servido como arquivos estáticos. A pasta `.git` foi excluída
**somente do ZIP de entrega**, pois são metadados locais de controle de versão,
não necessários à execução. O repositório publicado não foi alterado.

## Validação

O arquivo `tests/validar_estatico.py` confere links de arquivos locais,
uso de recursos e sintaxe dos JavaScript (se Node.js estiver disponível).
A aparência, os estados de hover e os gestos reais de rolagem devem ser
conferidos em um navegador antes de publicar a nova cópia.

## Estrutura limpa

O CSS foi formatado, a cascata preservada e declarações necessariamente
sobrescritas por regras equivalentes foram removidas. O HTML foi indentado
sem alterar seus textos ou atributos; os arquivos JavaScript foram organizados
sem introduzir bibliotecas ou infraestrutura de compilação.

