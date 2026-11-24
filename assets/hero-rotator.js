/* Lobo v4.3 — troca discreta do verbo do título da home, sem dependências. */
(() => {
  'use strict';
  const word = document.querySelector('[data-hero-word]');
  if (!word) return;
  const terms = ['decidir.', 'priorizar.', 'avançar.'];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let timeout = null;
  let pending = null;
  const showNext = () => {
    if (document.hidden || reduce.matches) return;
    word.classList.add('is-leaving');
    pending = setTimeout(() => {
      index = (index + 1) % terms.length;
      word.textContent = terms[index];
      word.classList.remove('is-leaving');
      word.classList.add('is-entering');
      requestAnimationFrame(() => requestAnimationFrame(() => word.classList.remove('is-entering')));
      pending = null;
    }, 460);
  };
  const start = () => {
    clearInterval(timeout);
    if (!document.hidden && !reduce.matches) timeout = setInterval(showNext, 3600);
  };
  const reset = () => {
    clearInterval(timeout);
    clearTimeout(pending);
    pending = null;
    index = 0;
    word.textContent = terms[0];
    word.classList.remove('is-leaving', 'is-entering');
    start();
  };
  document.addEventListener('visibilitychange', reset);
  reduce.addEventListener?.('change', reset);
  start();
})();
