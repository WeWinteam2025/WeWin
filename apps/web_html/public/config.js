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
      var link = '/dash/wehelp.html?v=1735248000';
      if (isBotPage) return;
      var a = document.createElement('a');
      a.id = 'wehelp-bubble';
      a.href = link;
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
      document.body.appendChild(a);
    });
  } catch(e) {}
})();


