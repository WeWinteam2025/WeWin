// Theme tokens referencing CSS variables defined in design_tokens.css
/** @type {import('tailwindcss').Config['theme']} */
const tokens = {
  colors: {
    brand: {
      primary: 'var(--brand-primary)',
      secondary: 'var(--brand-secondary)',
      accent: 'var(--brand-accent)',
      bg: 'var(--brand-bg)',
      surface: 'var(--brand-surface)'
    },
    text: {
      primary: 'var(--text-primary)',
      secondary: 'var(--text-secondary)'
    },
    success: 'var(--success)',
    warning: 'var(--warning)',
    error: 'var(--error)'
  },
  borderRadius: {
    DEFAULT: 'var(--radius)'
  },
  boxShadow: {
    DEFAULT: 'var(--shadow)'
  },
  fontFamily: {
    sans: [
      'Inter',
      'system-ui',
      'Segoe UI',
      'Roboto',
      'Helvetica Neue',
      'Arial',
      'Noto Sans',
      'Apple Color Emoji',
      'Segoe UI Emoji'
    ]
  }
};

module.exports = tokens;



