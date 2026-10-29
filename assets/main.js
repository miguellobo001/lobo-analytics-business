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
