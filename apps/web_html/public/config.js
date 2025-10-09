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
})();


