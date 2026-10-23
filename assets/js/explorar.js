/* Filtra contenido existente: no genera ni añade hechos profesionales. */
(function(){
 'use strict';
 const root=document.querySelector('.explorar-filtros');if(!root)return;
 root.hidden=false;
 const jobs=[...document.querySelectorAll('details.puesto')];
 const groups={
  documental:['p-1','p-2','p-3','p-4','p-5','p-6','p-7'],
  datos:['p-0','p-1','p-5','p-6'],
  comercial:['p-1','p-2','p-5'],
  tecnica:['p-2','p-9','p-10'],
  operativa:['p-3','p-4','p-8','p-10']
 };
 const search=document.querySelector('#buscar-puesto'),status=document.querySelector('#resultado-puestos');
 const buttons=[...document.querySelectorAll('[data-area]')];let area='todas';
 const normalize=t=>t.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 function render(){
  const q=normalize(search.value.trim());let visible=0;
  jobs.forEach(p=>{const match=(area==='todas'||groups[area].includes(p.id))&&normalize(p.textContent).includes(q);p.hidden=!match;if(match){visible++;p.classList.add('visto');}});
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.area===area)));
  status.textContent=visible?`${visible} de ${jobs.length} puestos · Consulta sus funciones desplegables.`:'No hay coincidencias. Prueba otra palabra o restablece la vista.';
 }
 buttons.forEach(b=>b.addEventListener('click',()=>{area=b.dataset.area;render()}));
 search.addEventListener('input',render);
 document.querySelectorAll('[data-ruta]').forEach(a=>a.addEventListener('click',()=>{area=a.dataset.ruta;search.value='';render()}));
 document.querySelector('#limpiar-puestos').addEventListener('click',()=>{area='todas';search.value='';render();search.focus()});
 // Una selección en la cronología siempre debe revelar el puesto, incluso si estaba filtrado.
 document.querySelectorAll('.fila-t').forEach(a=>a.addEventListener('click',()=>{area='todas';search.value='';render()},true));
 let prior=[];
 window.addEventListener('beforeprint',()=>{prior=jobs.map(p=>p.hidden);jobs.forEach(p=>p.hidden=false)});
 window.addEventListener('afterprint',()=>jobs.forEach((p,i)=>p.hidden=prior[i]));
 render();
})();
