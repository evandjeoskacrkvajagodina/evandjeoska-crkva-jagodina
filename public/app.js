const button=document.querySelector('.menu');button.addEventListener('click',()=>{const on=button.getAttribute('aria-expanded')==='true';button.setAttribute('aria-expanded',String(!on));document.querySelector('nav').classList.toggle('open',!on)});
const search=document.querySelector('#search');if(search){fetch('/data.json').then(r=>r.json()).then(data=>{const controls=[...document.querySelectorAll('select[data-field]')];function filter(){let count=0;document.querySelectorAll('.result').forEach(card=>{const slug=card.getAttribute('href').split('/')[2],d=data.find(x=>x.slug===slug);const normalized=s=>String(s||'').toLocaleLowerCase('sr').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'dj');const match=normalized(card.dataset.search).includes(normalized(search.value))&&controls.every(c=>!c.value||d[c.dataset.field]===c.value);card.hidden=!match;if(match)count++});document.querySelector('#no-results').hidden=count!==0;}controls.forEach(c=>c.addEventListener('change',filter));search.addEventListener('input',filter)}).catch(()=>{search.placeholder='Pretraga trenutno nije dostupna';search.disabled=true})}

// Galerija: koristi sve dostupne fotografije po redosledu u HTML-u.
(()=>{const frame=document.querySelector('.church-photos');if(!frame)return;
const imgs=[...frame.querySelectorAll('.church-photo')]; const placeholder=frame.querySelector('.photo-placeholder');const controls=frame.querySelector('.photo-controls');
let current=0, timer;const available=()=>imgs.filter(i=>i.dataset.ready==='1');
function render(){const ready=available();imgs.forEach(i=>i.hidden=true);if(!ready.length){placeholder.hidden=false;controls.hidden=true;return}current%=ready.length;placeholder.hidden=true;ready[current].hidden=false;controls.hidden=ready.length<2;}
imgs.forEach(img=>{img.addEventListener('load',()=>{img.dataset.ready='1';render()});img.addEventListener('error',()=>{img.dataset.ready='0';render()});if(img.complete){img.dataset.ready=img.naturalWidth>0?'1':'0';}});
function step(n){const ready=available();if(ready.length<2)return;current=(current+n+ready.length)%ready.length;render()}
frame.querySelector('.photo-prev').addEventListener('click',()=>step(-1));frame.querySelector('.photo-next').addEventListener('click',()=>step(1));render();timer=setInterval(()=>step(1),4500);
})();
