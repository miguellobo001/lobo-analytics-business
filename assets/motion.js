/* Movimento editorial: rolagem, revelação bidirecional e profundidade, sem bibliotecas externas.
 * Desktop: roda do mouse suavizada sem interceptar trackpads nem elementos com scroll próprio.
 * Todos: entrada discreta reversível de conteúdo. Desktop: profundidade delicada nas imagens.
 * Preferência de movimento reduzido respeitada integralmente.
 */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches) return;

  // Revelação ligada à posição do scroll, sem disparos one-shot.
  // Ao descer: progride 0 -> 1; ao subir: reverte 1 -> 0 no mesmo trajeto.
  // Apenas o ponto de entrada próximo à base da tela participa do fade;
  // o texto fica totalmente visível enquanto atravessa a área de leitura.
  const selectors = [
    '.studio__statement', '.studio__body', '.metric-strip',
    '.services__intro', '.service-card', '.process__intro', '.process__item',
    '.featured__head', '.gallery__card', '.footer__meta', '.footer__title',
    '.footer__reach', '.page-hero__title', '.page-hero__aside',
    '.dark-block .statement', '.dark-block .body', '.dark-block .number-list__item',
    '.light-block .statement', '.light-block .feature-row', '.special-card',
    '.approach-band', '.value-item', '.service-link', '.project-mosaic__tile'
  ];
  // querySelectorAll já elimina duplicatas entre seletores agrupados.
  const revealNodes = document.querySelectorAll(selectors.join(','));
  let revealsQueued = false;
  const updateReveals = () => {
    revealsQueued = false;
    const h = innerHeight;
    const start = h * .91;
    const distance = Math.max(105, Math.min(200, h * .22));
    for (const el of revealNodes) {
      const r = el.getBoundingClientRect();
      const p = Math.max(0, Math.min(1, (start - r.top) / distance));
      el.style.setProperty('--reveal-progress', p.toFixed(3));
    }
  };
  const requestReveals = () => {
    if (!revealsQueued) { revealsQueued = true; requestAnimationFrame(updateReveals); }
  };
  revealNodes.forEach(el => el.classList.add('motion-reveal'));
  requestReveals();
  window.addEventListener('scroll', requestReveals, { passive: true });
  window.addEventListener('resize', requestReveals, { passive: true });
  document.addEventListener('focusin', e => {
    const target = e.target.closest?.('.motion-reveal');
    if (target) target.style.setProperty('--reveal-progress', '1');
  });
  reduced.addEventListener?.('change', () => {
    if (reduced.matches) revealNodes.forEach(el => el.style.removeProperty('--reveal-progress'));
    else requestReveals();
  });

  const desktop = window.matchMedia('(min-width: 731px) and (hover: hover) and (pointer: fine)');
  const visuals = [...document.querySelectorAll('.hero__art img, .page-image img')];
  let motionRequested = false;
  const updateImages = () => {
    motionRequested = false;
    if (!desktop.matches || reduced.matches) return;
    const h = window.innerHeight;
    for (const img of visuals) {
      const r = img.parentElement.getBoundingClientRect();
      if (r.bottom < -30 || r.top > h + 30) continue;
      const center = (r.top + r.bottom) / 2;
      const distance = Math.max(-12, Math.min(12, (center - h/2) * -.025));
      img.style.setProperty('--motion-depth-y', `${distance.toFixed(2)}px`);
    }
  };
  const requestImages = () => {
    if (motionRequested) return;
    motionRequested = true;
    requestAnimationFrame(updateImages);
  };
  if (desktop.matches) {
    visuals.forEach(el => el.classList.add('motion-depth'));
    requestImages();
  }
  window.addEventListener('scroll', requestImages, { passive: true });
  window.addEventListener('resize', requestImages, { passive: true });
  desktop.addEventListener?.('change', e => {
    visuals.forEach(el => el.classList.toggle('motion-depth', e.matches));
    if (!e.matches) visuals.forEach(el => el.style.removeProperty('--motion-depth-y'));
    requestImages();
  });

  // Damping leve exclusivamente para a roda tradicional do mouse em desktops.
  // Trackpads, touch, teclado, seleção de texto e áreas roláveis mantêm a rolagem nativa.
  if (!desktop.matches) return;
  let current = window.scrollY;
  let target = current;
  let frame = 0;
  const root = document.documentElement;
  const maxScroll = () => Math.max(0, root.scrollHeight - window.innerHeight);
  const stop = () => {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    root.classList.remove('motion-wheel-active');
    current = target = window.scrollY;
  };
  const tick = () => {
    const diff = target - current;
    if (Math.abs(diff) < .65) {
      window.scrollTo({ top: target, behavior: 'instant' });
      stop();
      return;
    }
    current += diff * .19;
    window.scrollTo({ top: current, behavior: 'instant' });
    frame = requestAnimationFrame(tick);
  };
  const nestedScrollable = (node, dy) => {
    for (let el = node; el instanceof Element && el !== document.body; el = el.parentElement) {
      const style = getComputedStyle(el);
      if (!/(auto|scroll)/.test(style.overflowY)) continue;
      if (el.scrollHeight <= el.clientHeight + 2) continue;
      if (dy > 0 && el.scrollTop < el.scrollHeight - el.clientHeight - 1) return true;
      if (dy < 0 && el.scrollTop > 1) return true;
    }
    return false;
  };
  document.addEventListener('wheel', e => {
    if (!desktop.matches || reduced.matches || document.body.classList.contains('menu-open') ||
        e.ctrlKey || e.metaKey || e.shiftKey || e.defaultPrevented || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    // Pixel deltas of small size typically indicate a trackpad. Leave those untouched.
    if (e.deltaMode === 0 && (Math.abs(e.deltaY) < 65 || !Number.isInteger(e.deltaY))) {
      if (frame) stop();
      return;
    }
    if (e.deltaMode > 1 || nestedScrollable(e.target, e.deltaY)) return;
    const delta = e.deltaMode === 1 ? e.deltaY * 19 : e.deltaY;
    const next = Math.max(0, Math.min(maxScroll(), (frame ? target : window.scrollY) + Math.max(-165, Math.min(165, delta))));
    if (Math.abs(next - window.scrollY) < .5) return;
    e.preventDefault();
    target = next;
    if (!frame) {
      current = window.scrollY;
      root.classList.add('motion-wheel-active');
      frame = requestAnimationFrame(tick);
    }
  }, { passive: false });
  document.addEventListener('pointerdown', stop, { passive: true });
  document.addEventListener('touchstart', stop, { passive: true });
  document.addEventListener('keydown', e => {
    if (['ArrowUp','ArrowDown','PageUp','PageDown','Home','End',' '].includes(e.key)) stop();
  });
  document.addEventListener('click', e => {
    if (e.target.closest?.('a[href*="#"]')) stop();
  });
  window.addEventListener('resize', stop, { passive: true });
  reduced.addEventListener?.('change', () => {
    stop();
    if (reduced.matches) {
      document.querySelectorAll('.motion-reveal').forEach(el => el.classList.add('is-visible'));
      visuals.forEach(el => el.classList.remove('motion-depth'));
    }
  });
})();
