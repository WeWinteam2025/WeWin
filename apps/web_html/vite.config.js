import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  server: {
    port: 5173,
    strictPort: true
  },
  resolve: {
    alias: {
      '@design': path.resolve(__dirname, '../../packages/design')
    }
  },
  build: {
    rollupOptions: {
      input: {
        index: path.resolve(__dirname, 'index.html'),
        login: path.resolve(__dirname, 'auth/login.html'),
        register: path.resolve(__dirname, 'auth/register.html'),
        dash_index: path.resolve(__dirname, 'dash/index.html'),
        dash_catalogo: path.resolve(__dirname, 'dash/catalogo.html'),
        dash_energia: path.resolve(__dirname, 'dash/energia.html'),
        dash_instaladores: path.resolve(__dirname, 'dash/instaladores.html'),
        dash_inversion: path.resolve(__dirname, 'dash/inversion.html'),
        dash_ppa: path.resolve(__dirname, 'dash/ppa.html'),
        dash_profile: path.resolve(__dirname, 'dash/profile.html'),
        dash_proyecto: path.resolve(__dirname, 'dash/proyecto.html'),
        dash_proyectos: path.resolve(__dirname, 'dash/proyectos.html'),
        dash_stakeholders: path.resolve(__dirname, 'dash/stakeholders.html'),
        dash_techos: path.resolve(__dirname, 'dash/techos.html')
      }
    }
  }
})


