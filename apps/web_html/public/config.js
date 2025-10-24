// Computa la URL base del API según el host actual
// En localhost usa 8001, en producción usa el subdominio api.
(function(){
  var isLocal = /localhost|127\.0\.0\.1/.test(location.hostname);
  var api = isLocal ? 'http://localhost:8001' : 'https://api.wewin.space';
  window.API_BASE = window.API_BASE || api;
  
  // Log para debugging
  console.log('API_BASE configurado:', window.API_BASE, 'desde host:', location.hostname);
  
  // Expose at root for static hosting
  try {
    if (!document.getElementById('wewin-config')) {
      var s = document.createElement('script');
      s.id = 'wewin-config';
      s.type = 'application/json';
      s.text = JSON.stringify({ API_BASE: window.API_BASE });
      document.head.appendChild(s);
    }
  } catch (e) {}

  // Inyectar burbuja WeHelp en todas las páginas
  try {
    document.addEventListener('DOMContentLoaded', function(){
      if (document.getElementById('wehelp-bubble')) return;
      // Evitar duplicar en la propia página del bot
      var path = (location.pathname||'').toLowerCase();
      var isBotPage = path.indexOf('/dash/wehelp.html') >= 0;
      // contenedor modal
      var modal = document.createElement('div');
      modal.id = 'wehelp-modal';
      modal.style.position = 'fixed';
      modal.style.inset = '0';
      modal.style.background = 'rgba(0,0,0,0.5)';
      modal.style.display = 'none';
      modal.style.zIndex = '9998';
      modal.innerHTML = ''+
        '<div style="display:flex;align-items:center;justify-content:center;min-height:100vh;padding:16px">'+
        '  <div style="background:#fff;border-radius:12px;max-width:720px;width:100%;max-height:80vh;overflow:hidden;box-shadow:0 20px 30px rgba(0,0,0,0.25)">'+
        '    <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-bottom:1px solid #e5e7eb">'+
        '      <strong>WeHelp • Asistente Solar</strong>'+
        '      <button id="wehelp-close" style="background:transparent;border:0;font-size:20px;cursor:pointer">✕</button>'+
        '    </div>'+
        '    <div id="wehelp-host" style="padding:12px"></div>'+
        '  </div>'+
        '</div>';
      document.body.appendChild(modal);
      var closeBtn = modal.querySelector('#wehelp-close');
      if (closeBtn) closeBtn.addEventListener('click', function(){ modal.style.display = 'none'; });

      // burbuja
      if (!isBotPage){
        var a = document.createElement('button');
        a.type = 'button';
        a.id = 'wehelp-bubble';
        a.title = 'Habla con WeHelp';
        a.setAttribute('aria-label', 'Habla con WeHelp');
        a.style.position = 'fixed';
        a.style.right = '16px';
        a.style.bottom = '16px';
        a.style.width = '56px';
        a.style.height = '56px';
        a.style.borderRadius = '50%';
        a.style.background = '#22c55e';
        a.style.color = '#fff';
        a.style.display = 'flex';
        a.style.alignItems = 'center';
        a.style.justifyContent = 'center';
        a.style.boxShadow = '0 10px 15px rgba(0,0,0,0.15)';
        a.style.fontSize = '24px';
        a.style.textDecoration = 'none';
        a.style.zIndex = '9999';
        a.innerHTML = '🤖';
        a.addEventListener('click', function(){
          modal.style.display = 'block';
          // cargar script si no está
          function ensureScript(cb){
            if (window.initWeHelp) return cb();
            var s = document.createElement('script'); s.src = '/wehelp.js?v=1735248000'; s.onload = cb; document.body.appendChild(s);
          }
          ensureScript(function(){
            var host = document.getElementById('wehelp-host');
            if (host){ host.innerHTML = ''; try { window.initWeHelp(host); } catch(e) { host.innerHTML = '<div class=\'p-3 text-sm\'>No se pudo cargar WeHelp.</div>'; } }
          });
        });
        document.body.appendChild(a);
      }
    });
  } catch(e) {}
})();


