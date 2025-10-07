(function(){
  function ensureNavbar(){
    var slot = document.getElementById('navbar-slot');
    if (!slot) return;
    // Elimina cualquier elemento residual que intente cargar rutas antiguas
    try {
      document.querySelectorAll('[hx-get*="/public/partials/navbar.html"], [hx-get="/navbar.html"]').forEach(function(el){
        el.parentNode && el.parentNode.removeChild(el);
      });
    } catch(e) {}
    // If HTMX no lo cargó, hacemos un fetch manual
    if (!slot.innerHTML || slot.innerHTML.trim().length === 0){
      // Intento 1: ruta unificada
      fetch('/partials/navbar.html', { cache: 'no-store' })
        .then(function(r){ return r.text(); })
        .then(function(html){
          // Inserta el HTML del navbar
          slot.outerHTML = html;
          // Inicializa estado de sesión
          var s = document.createElement('script');
          s.src = '/navbar-init.js';
          document.body.appendChild(s);
        })
        .catch(function(){
          // Intento 2: compat rutas antiguas (fallback definitivo a raíz)
          fetch('/partials/navbar.html', { cache: 'reload' })
            .then(function(r){ return r.text(); })
            .then(function(html){
              slot.outerHTML = html;
              var s = document.createElement('script');
              s.src = '/navbar-init.js';
              document.body.appendChild(s);
            })
            .catch(function(){ /* noop */ });
        });
    }
  }
  // Revisión en DOMContentLoaded y reintentos por si el DOM cambia
  document.addEventListener('DOMContentLoaded', function(){
    var tries = 0;
    var iv = setInterval(function(){
      ensureNavbar();
      tries++;
      if (tries > 6) clearInterval(iv); // ~3s de reintentos
    }, 500);
  });
})();


