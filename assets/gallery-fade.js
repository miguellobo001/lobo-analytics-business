/**
 * Galeria da home — máscara progressiva na borda inferior.
 * A seção seguinte cobre a galeria pelo próprio fluxo do layout.
 * Valores aprovados: base 66/95 px, movimento adicional 40/65 px (mobile/desktop).
 */
(() => {
  'use strict';
  const gallery = document.querySelector('.ribbon');
  const section = document.querySelector('.studio');
  if (!gallery || !section) return;
  const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
  let scheduled = false;
  const clamp = (v) => Math.max(0, Math.min(1, v));
  const update = () => {
    scheduled = false;
    if (motionPreference.matches) {
      gallery.style.removeProperty('--gallery-cover');
      return;
    }
    const mobile = innerWidth <= 730;
    // A máscara acompanha o deslocamento da seção nos dois sentidos.
    const base = mobile ? 66 : 95;
    const extra = mobile ? 40 : 65;
    const top = section.getBoundingClientRect().top;
    const progress = clamp((innerHeight * .88 - top) / (innerHeight * .48));
    const eased = progress * progress * (3 - 2 * progress);
    gallery.style.setProperty('--gallery-cover', (base + extra * eased).toFixed(1) + 'px');
  };
  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  };
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  motionPreference.addEventListener?.('change', schedule);
  schedule();
})();
