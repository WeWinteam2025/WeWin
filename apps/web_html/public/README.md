# Imágenes locales de proyectos (frontend)

Coloca aquí imágenes WebP para proyectos con el patrón de nombre:

- `img/solar/{slug}.webp`

Ejemplos de `slug` utilizados:
- `bogota-norte`
- `medellin-sur`
- `comunidad-energetica`
- `zona-industrial`
- `residencial-12`

Conversión automática desde JPG/PNG
- Coloca tus imágenes fuente en `apps/web_html/public/img_src/` con nombres tipo `bogota-norte.jpg`, `medellin-sur.png`, etc.
- Ejecuta desde la raíz del repo:

```bash
cd "Reto 2/apps/web_html"
npm i --no-audit --no-fund
npm run img:convert
```

Notas:
- Formato recomendado: WebP, ancho 1600px aprox.
- El frontend intentará cargar `/img/solar/{slug}.webp` primero; si no existe, usa un fallback de paneles solares.
- Puedes reemplazar las imágenes sin reiniciar el backend; usa cache-busting con `?v=TIMESTAMP` o recarga dura (Ctrl+Shift+R).
