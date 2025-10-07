(function(){
  function renderAuth(slot){
    if (!slot) return;
    const token = localStorage.getItem('access');
    if (!token){
      slot.innerHTML = '<a href="/auth/login.html" class="hover:opacity-80">Ingresar</a>';
      return;
    }
    var API = window.API_BASE || 'http://localhost:8001';
    fetch(API + '/api/profiles/?current=1', { headers: { Authorization: 'Bearer ' + token }})
      .then(r => r.ok ? r.json() : [])
      .then(data => {
        var profile = Array.isArray(data) ? data[0] : (data && data.value ? data.value[0] : null);
        var avatar = (profile && profile.avatar_url) ? profile.avatar_url : 'https://www.gravatar.com/avatar/?d=identicon';
        slot.innerHTML = '<a href="/dash/profile.html" title="Perfil"><img src="'+avatar+'" style="width:32px;height:32px;border-radius:50%;vertical-align:middle"/></a>'+
          '<button id="logout-btn" style="margin-left:8px" class="btn-primary">Salir</button>';
        var btn = document.getElementById('logout-btn');
        if (btn) btn.addEventListener('click', function(){
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          window.location.href = '/auth/login.html';
        });
      }).catch(function(){
        slot.innerHTML = '<a href="/dash/profile.html" title="Perfil"><div style="width:32px;height:32px;border-radius:50%;background:#9CA3AF;display:inline-block;vertical-align:middle"></div></a>'+
          '<button id="logout-btn" style="margin-left:8px" class="btn-primary">Salir</button>';
        var btn = document.getElementById('logout-btn');
        if (btn) btn.addEventListener('click', function(){
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          window.location.href = '/auth/login.html';
        });
      });
  }

  function init(){
    var slot = document.getElementById('auth-slot');
    if (slot) renderAuth(slot);
  }

  document.addEventListener('DOMContentLoaded', init);
  document.body && document.body.addEventListener('htmx:afterSwap', function(){
    init();
  });
})();



