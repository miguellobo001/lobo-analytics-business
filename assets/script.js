(function(){
const toggle=document.querySelector('[data-menu-toggle]');const panel=document.querySelector('.menu-panel');
function setMenu(open){document.body.classList.toggle('menu-open',open);toggle?.setAttribute('aria-expanded',String(open));panel?.setAttribute('aria-hidden',String(!open));}
toggle?.addEventListener('click',()=>setMenu(!document.body.classList.contains('menu-open')));
document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
panel?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));

const copyBtn=document.querySelector('[data-copy-message]');copyBtn?.addEventListener('click',async()=>{const m=document.querySelector('#projectMessage')?.value||'Olá! Gostaria de conversar sobre um projeto com a Lobo Analytics & Business.';try{await navigator.clipboard.writeText(m);copyBtn.textContent='Mensagem copiada ✓'}catch{let el=document.querySelector('#projectMessage');el?.select();copyBtn.textContent='Selecione e copie a mensagem';}});
})();