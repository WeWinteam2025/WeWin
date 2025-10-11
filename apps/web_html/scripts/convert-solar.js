#!/usr/bin/env node
// Convertir imágenes fuente (JPG/PNG) a WebP por slug
// Origen: apps/web_html/public/img_src/
// Destino: apps/web_html/public/img/solar/{slug}.webp

import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

// Ejecutar este script desde apps/web_html
const base = path.resolve('.');
const root = base;
const srcDir = path.join(base, 'public', 'img_src');
const outDir = path.join(base, 'public', 'img', 'solar');

function toSlug(name){
  return String(name)
    .toLowerCase()
    .replace(/[áàä]/g,'a')
    .replace(/[éèë]/g,'e')
    .replace(/[íìï]/g,'i')
    .replace(/[óòö]/g,'o')
    .replace(/[úùü]/g,'u')
    .replace(/ñ/g,'n')
    .replace(/[^a-z0-9]+/g,'-')
    .replace(/(^-|-$)/g,'');
}

async function main(){
  if (!fs.existsSync(srcDir)){
    console.error('No existe el directorio de origen:', srcDir);
    console.error('Crea apps/web_html/public/img_src y coloca ahí tus imágenes (bogota-norte.jpg, etc).');
    process.exit(1);
  }
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const files = fs.readdirSync(srcDir).filter(f => /\.(jpe?g|png|webp)$/i.test(f));
  if (files.length === 0){
    console.warn('No se encontraron imágenes JPG/PNG en', srcDir);
    return;
  }

  // Mapeo opcional: si detectamos nombres project1..project6, asignamos slugs conocidos
  const defaultSlugOrder = ['medellin-sur','bogota-norte','comunidad-energetica','zona-industrial','residencial-12','zona-industrial-b'];
  const isProjectN = files.every(f => /^project\d+\.(jpe?g|png|webp)$/i.test(f));

  for (let idx=0; idx<files.length; idx++){
    const file = files[idx];
    const basename = path.basename(file).replace(/\.(jpe?g|png|webp)$/i,'');
    const slug = isProjectN ? defaultSlugOrder[idx % defaultSlugOrder.length] : toSlug(basename);
    const input = path.join(srcDir, file);
    const output = path.join(outDir, slug + '.webp');
    console.log('→', path.relative(root, input), '⇒', path.relative(root, output));
    try {
      if (/\.webp$/i.test(file)){
        // Copiar/optimizar webp existente
        const buf = fs.readFileSync(input);
        await sharp(buf).rotate().resize(1600, null, { fit: 'inside', withoutEnlargement: true }).webp({ quality: 85 }).toFile(output);
      } else {
        await sharp(input).rotate().resize(1600, null, { fit: 'inside', withoutEnlargement: true }).webp({ quality: 85 }).toFile(output);
      }
    } catch (e){
      console.error('Error convirtiendo', file, e.message);
    }
  }
  console.log('Conversión finalizada.');
}

main().catch(e=>{ console.error(e); process.exit(1); });


