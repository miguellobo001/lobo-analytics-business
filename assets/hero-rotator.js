/**
 * Título da home — alternância entre três palavras a cada 3,6 segundos.
 * Interrompe a animação quando a página não está visível ou quando o
 * visitante prefere movimento reduzido.
 */
(() => {
  'use strict';
  const word = document.querySelector('[data-hero-word]');
  if (!word) return;
  const terms = ['decidir.', 'priorizar.', 'avançar.'];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let intervalId = null;
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
    clearInterval(intervalId);
    if (!document.hidden && !reduce.matches) intervalId = setInterval(showNext, 3600);
  };
  const reset = () => {
    clearInterval(intervalId);
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
