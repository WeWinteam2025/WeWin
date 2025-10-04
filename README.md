## Reto 2 Monorepo

Estructura básica para un monorepo con:
- apps/api_django (API Django 5 + DRF + JWT + CORS + Supabase Postgres)
- apps/web_html (Vite vanilla + TailwindCSS + HTMX)
- apps/mobile_flutter (placeholder)
- packages/design (tokens de diseño compartidos + tema Tailwind)
- packages/docs (documentación de arquitectura)

### Requisitos previos
- Python 3.11+
- Node.js 18+
- npm 9+ (o pnpm/yarn si prefieres)

### Variables de entorno
Crea el archivo `apps/api_django/.env` con (ver `env.sample`):

```
DATABASE_URL=postgresql://postgres.<project_ref>:<password>@aws-1-us-east-2.pooler.supabase.com:6543/postgres
SECRET_KEY=REEMPLAZAR_POR_UNA_CLAVE_SEGURA
ALLOWED_HOSTS=*
CORS_ALLOW_ALL_ORIGINS=true
```

Notas:
- Usamos el pooler IPv4 de Supabase (puerto 6543) para evitar problemas IPv6.
- Si tu proyecto está en otra región, Supabase mostrará el host del pooler adecuado.

### Instalar y correr (API Django)
```
cd apps/api_django
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

Probar salud:
```
GET http://localhost:8001/healthz
```

### Instalar y correr (Web HTML)
```
cd apps/web_html
npm install
npm run dev
```

El sitio estará disponible en `http://localhost:5173` (por defecto Vite) e incluye:
- Landing mínima con navbar "We Win" y CTA
- Dash shell en `/dash/`
- Páginas `/auth/login.html` y `/auth/register.html`

### Diseño compartido
- Tokens en `packages/design/design_tokens.css`
- Tokens de Tailwind exportados en `packages/design/tailwind.tokens.cjs`
- Consume tokens desde `apps/web_html/tailwind.config.js`

### Documentación
Ver `packages/docs/arquitectura.md` para un diagrama de módulos y flujos.

### Notas
- La paleta y radios/sombras vienen de `design_tokens.css`. Puedes editar valores en un solo lugar y se reflejarán en la web.
- Para producción, configura variables de entorno seguras y dominios en `ALLOWED_HOSTS`.

## Despliegue en Render + DNS en GoDaddy

### 1) Preparar repo
- Asegúrate de tener este repo en GitHub o GitLab.
- El blueprint `deploy/render.yaml` define 2 servicios:
  - `wewin-api` (Django, gunicorn)
  - `wewin-web` (sitio estático Vite)

### 2) Crear servicios en Render
1. Ve a `https://render.com` y conecta tu repositorio.
2. New → Blueprint → selecciona el repo (Render detecta `deploy/render.yaml`).
3. Crea el blueprint.
4. Variables del servicio `wewin-api`:
   - `SECRET_KEY`: cadena segura.
   - `DEBUG`: `false`.
   - `ALLOWED_HOSTS`: `wewin.space,www.wewin.space,api.wewin.space`.
   - `DATABASE_URL`: tu URI de Supabase (con SSL).
   - `CORS_ALLOW_ALL_ORIGINS`: `true` (o define orígenes específicos).
5. Despliega. Render dará URLs públicas (p.ej. `wewin-api.onrender.com`, `wewin-web.onrender.com`).

### 3) DNS en GoDaddy (dominio wewin.space)
En el panel DNS de GoDaddy agrega:

- Web (www):
  - Tipo: `CNAME`
  - Nombre/Host: `www`
  - Apunta a: host de Render del sitio estático (p.ej. `wewin-web.onrender.com`)

- Raíz (wewin.space):
  - Usa redirección/forwarding a `https://www.wewin.space` (301) o un proxy.

- API (api.wewin.space):
  - Tipo: `CNAME`
  - Nombre/Host: `api`
  - Apunta a: host de Render del API (p.ej. `wewin-api.onrender.com`)

Después, en Render → cada servicio → Custom Domains:
- Web: agregar `www.wewin.space`
- API: agregar `api.wewin.space`
Render generará SSL automáticamente tras la verificación DNS.

### 4) Configuración frontend/backend
- Frontend usa `public/config.js` para detectar el API:
  - Local: `http://localhost:8001`
  - Producción: `https://api.wewin.space`
- Backend corre con `gunicorn` y healthcheck `/healthz`.

### 5) Build local (opcional)
Frontend:
```
cd apps/web_html
npm install
npx vite build
```
Backend:
```
cd apps/api_django
pip install -r requirements.txt
python manage.py migrate
```

### 6) Problemas comunes
- 404 web: verifica `publishPath: apps/web_html/dist` y build exitoso.
- CORS/401: tokens vencidos o `ALLOWED_HOSTS`/CORS mal configurados.
- DB: revisa `DATABASE_URL` y permisos de red en tu proveedor.


