const toggle=document.querySelector('[data-menu-toggle]');
const nav=document.querySelector('[data-mobile-nav]');
if(toggle && nav){
  const close=()=>{nav.hidden=true;toggle.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open');};
  toggle.addEventListener('click',()=>{
    const open=nav.hidden;
    nav.hidden=!open;
    toggle.setAttribute('aria-expanded',String(open));
    document.body.classList.toggle('menu-open',open);
  });
  nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',close));
  window.addEventListener('keydown',event=>{if(event.key==='Escape')close();});
}

// Ligação original entre cada etapa e uma das três formas da marca.
const methodMark=document.getElementById('methodMark');
const methodSteps=document.querySelectorAll('.classic-step');
if(methodMark && methodSteps.length){
  const activate=(element)=>{
    methodMark.dataset.active=element.dataset.s;
    methodSteps.forEach(step=>step.classList.toggle('is-on',step===element));
  };
  const deactivate=()=>{
    delete methodMark.dataset.active;
    methodSteps.forEach(step=>step.classList.remove('is-on'));
  };
  methodSteps.forEach(step=>{
    step.addEventListener('mouseenter',()=>activate(step));
    step.addEventListener('focus',()=>activate(step));
    step.addEventListener('mouseleave',deactivate);
    step.addEventListener('blur',deactivate);
    step.addEventListener('click',()=>activate(step));
    step.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();activate(step);}});
  });
}
