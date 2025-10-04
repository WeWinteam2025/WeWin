const tokens = require('../../packages/design/tailwind.tokens.cjs')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './dash/**/*.html',
    './auth/**/*.html',
    './partials/**/*.html',
    './src/**/*.{js,ts}'
  ],
  theme: {
    extend: {
      colors: tokens.colors,
      boxShadow: tokens.boxShadow,
      borderRadius: tokens.borderRadius,
      fontFamily: tokens.fontFamily
    }
  }
}




