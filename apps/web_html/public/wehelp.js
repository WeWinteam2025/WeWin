(function(){
  function mountUI(root){
    // crea UI si no existe
    var chatEl = root.querySelector('#chat');
    var form = root.querySelector('#ask');
    var input = root.querySelector('#q');
    if (!chatEl || !form || !input){
      root.innerHTML = ''+
        '<div class="space-y-3 max-h-[60vh] overflow-y-auto" id="chat"></div>'+
        '<form id="ask" class="mt-4 grid grid-cols-[1fr_auto] gap-2">'+
        '  <input id="q" class="input" placeholder="Escribe tu pregunta..." autocomplete="off"/>'+
        '  <button class="btn-primary">Preguntar</button>'+
        '</form>';
      chatEl = root.querySelector('#chat');
      form = root.querySelector('#ask');
      input = root.querySelector('#q');
    }
    return { chatEl: chatEl, form: form, input: input };
  }

  function addMsg(chatEl, role, text){
    var div = document.createElement('div');
    div.className = role === 'user' ? 'p-3 rounded bg-white' : 'p-3 rounded bg-green-50 border border-green-200';
    div.innerHTML = '<div class="text-xs text-slate-500 mb-1">'+(role==='user'?'Tú':'WeHelp')+'</div>' + text;
    chatEl.appendChild(div); chatEl.scrollTop = chatEl.scrollHeight;
  }

  function loadKB(){
    return fetch('/wehelp_kb.json?v=1735248000').then(function(r){ return r.json(); }).catch(function(){ return {}; });
  }

  function searchFAQ(q, faqs){
    q = (q||'').toLowerCase();
    for (var i=0;i<faqs.length;i++){
      var it = faqs[i];
      if ((it.q||'').toLowerCase().indexOf(q)>=0) return it.a;
    }
    if (q.indexOf('ppa')>=0) return 'PPA: contrato de compra de energía a precio acordado por un periodo. Permite pagar por kWh sin CAPEX inicial.';
    if (q.indexOf('cost')>=0 || q.indexOf('precio')>=0) return 'Referencias: 2.5–3.5 MM COP/kWp en techos comerciales; residencial puede ser mayor.';
    if (q.indexOf('gener')>=0 || q.indexOf('kwh')>=0) return 'Regla rápida: kWh/mes ≈ kWp × 120–160 según ciudad. Bogotá ≈120, Medellín ≈140, Caribe ≈150‑160.';
    return null;
  }

  function estimate(payload){
    var kwp = Number(payload.kwp||0);
    var price = Number(payload.precio_cop_kwh||0);
    var kb = payload.kb||{};
    var cities = kb.cities||{};
    var cityKey = (payload.ciudad||'').toLowerCase();
    var perf = (cities[cityKey] && Number(cities[cityKey].kwh_per_kwp)) || 130;
    var kwh_mes = kwp * perf;
    var capex_kwp = (kb.defaults && kb.defaults.capex_per_kwp_cop) || 3000000;
    var capex = kwp * capex_kwp;
    var ingresos = kwh_mes * price;
    var opex = capex * ((kb.defaults && kb.defaults.opex_pct)||0.02) / 12;
    var utilidad = ingresos - opex;
    return { kwh_mes: Math.round(kwh_mes), capex: Math.round(capex), ingresos: Math.round(ingresos), utilidad: Math.round(utilidad) };
  }

  function parseCalc(q){
    var m = q.match(/(\d+[\.,]?\d*)\s*kwp.*?en\s+([a-záéíóúñ]+).*?(\d+[\.,]?\d*)\s*cop\s*\/\s*kwh/i);
    if (!m) return null;
    var kwp = parseFloat(m[1].replace(',', '.'));
    var city = m[2];
    var price = parseFloat(m[3].replace(',', '.'));
    return { kwp: kwp, ciudad: city, precio_cop_kwh: price };
  }

  function init(root){
    if (!root){
      var fallback = document.createElement('div');
      var host = document.getElementById('wehelp-host') || document.body;
      host.appendChild(fallback);
      root = fallback;
    }
    var ui = mountUI(root);
    var chatEl = ui.chatEl, form = ui.form, input = ui.input;
    loadKB().then(function(kb){
      addMsg(chatEl, 'assistant', 'Hola, soy <strong>WeHelp</strong> 🤖. Puedo resolver dudas de energía solar, dimensionamiento, costos, PPA y comunidades. Ejemplo: "calcula 200 kWp en Medellín a 250 COP/kWh"');
      form.addEventListener('submit', function(e){
        e.preventDefault();
        var q = (input.value||'').trim();
        if (!q) return;
        addMsg(chatEl, 'user', q);
        input.value = '';
        var calc = parseCalc(q);
        if (calc){
          var res = estimate({ kwp: calc.kwp, ciudad: calc.ciudad, precio_cop_kwh: calc.precio_cop_kwh, kb: kb });
          addMsg(chatEl, 'assistant', 'Para '+calc.kwp+' kWp en '+calc.ciudad+':<br/>'+
            '- Generación estimada: <strong>'+res.kwh_mes.toLocaleString('es-CO')+' kWh/mes</strong><br/>'+
            '- CAPEX aprox: <strong>$'+res.capex.toLocaleString('es-CO')+' COP</strong><br/>'+
            '- Ingresos mensuales: <strong>$'+res.ingresos.toLocaleString('es-CO')+' COP</strong><br/>'+
            '- Utilidad estimada (después OPEX): <strong>$'+res.utilidad.toLocaleString('es-CO')+' COP</strong>');
          return;
        }
        var ans = searchFAQ(q, kb.faqs||[]);
        if (ans){ addMsg(chatEl, 'assistant', ans); return; }
        addMsg(chatEl, 'assistant', 'Puedo ayudarte con: costos por kWp, PPA, dimensionamiento (kWh/mes), incentivos y CE. Intenta con: "¿Cuánto cuesta por kW?" o "calcula 50 kWp en Bogotá a 300 COP/kWh".');
      });
    });
  }

  // Exportar inicializador global para modo embebido
  window.initWeHelp = window.initWeHelp || init;

  // Modo página completa: si existen ids esperados, iniciar de inmediato
  if (document.getElementById('chat') && document.getElementById('ask') && document.getElementById('q')){
    init(document.body);
  }
})();


