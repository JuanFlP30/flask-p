import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    outDir: 'static/dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: './static/css/input.css'
      },
      output: {
        assetFileNames: 'css/[name].[ext]'
      }
    }
  }
})
