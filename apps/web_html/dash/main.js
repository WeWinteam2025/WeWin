(function(){
  var API = window.API;
  if (!API){ API = (location.hostname.indexOf('wewin.space')>=0?'https://api.wewin.space':'http://localhost:8001'); window.API = API; }

  function safeJson(r){ return r.json().catch(function(){ return []; }); }
  function avg(arr, field){ var xs = arr.map(function(x){ return Number(x[field]||0); }).filter(function(n){ return !isNaN(n) && isFinite(n); }); if (!xs.length) return 0; return xs.reduce(function(a,b){return a+b;},0)/xs.length; }

  async function loadData(){
    try{
      var offR = await fetch(API + '/api/offers/public');
      var demR = await fetch(API + '/api/demands/public');
      var ceR = await fetch(API + '/api/ce');
      var offers = await safeJson(offR); if (!Array.isArray(offers) && offers && offers.results) offers = offers.results; if (!Array.isArray(offers)) offers = [];
      var demands = await safeJson(demR); if (!Array.isArray(demands) && demands && demands.results) demands = demands.results; if (!Array.isArray(demands)) demands = [];
      var ce = await safeJson(ceR); if (!Array.isArray(ce) && ce && ce.results) ce = ce.results; if (!Array.isArray(ce)) ce = [];

      var elCe = document.getElementById('kpi-ce'); if (elCe) elCe.textContent = String(ce.length);
      var aO = avg(offers,'precio_ref'); var aD = avg(demands,'precio_obj');
      var elO = document.getElementById('kpi-oferta'); if (elO) elO.textContent = aO ? aO.toFixed(4) : '—';
      var elD = document.getElementById('kpi-demanda'); if (elD) elD.textContent = aD ? aD.toFixed(4) : '—';

      var fmt = function(n){ return new Intl.NumberFormat('en-US',{maximumFractionDigits:4}).format(n); };
      var offersHtml = offers.slice(0,6).map(function(o){ return '<div class="border-b last:border-0 py-2 text-sm flex items-center justify-between"><span>'+fmt(o.precio_ref||0)+' US$/kWh</span><span class="text-[color:var(--text-secondary)]">'+fmt(o.capacidad_kw||0)+' kW</span></div>'; }).join('') || '<div class="text-[color:var(--text-secondary)]">Sin ofertas.</div>';
      var lo = document.getElementById('list-offers'); if (lo) lo.innerHTML = offersHtml;
      var demandsHtml = demands.slice(0,6).map(function(d){ return '<div class="border-b last:border-0 py-2 text-sm flex items-center justify-between"><span>'+fmt(d.precio_obj||0)+' US$/kWh</span><span class="text-[color:var(--text-secondary)]">'+(d.estado||'')+'</span></div>'; }).join('') || '<div class="text-[color:var(--text-secondary)]">Sin demandas.</div>';
      var ld = document.getElementById('list-demands'); if (ld) ld.innerHTML = demandsHtml;
      var ceHtml = ce.slice(0,6).map(function(c){ return '<div class="border-b last:border-0 py-2 text-sm flex items-center justify-between"><span>'+(c.nombre||'Comunidad')+'</span><span class="text-[color:var(--text-secondary)]">'+(c.miembros||0)+' miembros</span></div>'; }).join('') || '<div class="text-[color:var(--text-secondary)]">Sin comunidades.</div>';
      var lc = document.getElementById('list-ce'); if (lc) lc.innerHTML = ceHtml;
    }catch(e){ console.warn(e); }
  }

  document.addEventListener('DOMContentLoaded', loadData);
})();


