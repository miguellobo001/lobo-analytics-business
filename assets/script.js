/**
 * Interações comuns a todas as páginas.
 * Menu de navegação e cópia da mensagem de contato.
 */
(() => {
  'use strict';

  const toggle = document.querySelector('[data-menu-toggle]');
  const panel = document.querySelector('.menu-panel');

  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    toggle?.setAttribute('aria-expanded', String(open));
    panel?.setAttribute('aria-hidden', String(!open));
  }

  toggle?.addEventListener('click', () => {
    setMenu(!document.body.classList.contains('menu-open'));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setMenu(false);
  });

  panel?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setMenu(false));
  });

  // O formulário não envia dados: apenas prepara uma mensagem para copiar.
  const copyButton = document.querySelector('[data-copy-message]');

  copyButton?.addEventListener('click', async () => {
    const message = document.querySelector('#projectMessage')?.value ||
      'Olá! Gostaria de conversar sobre um projeto com a Lobo Analytics & Business.';

    try {
      await navigator.clipboard.writeText(message);
      copyButton.textContent = 'Mensagem copiada ✓';
    } catch {
      const field = document.querySelector('#projectMessage');
      field?.select();
      copyButton.textContent = 'Selecione e copie a mensagem';
    }
  });
})();
