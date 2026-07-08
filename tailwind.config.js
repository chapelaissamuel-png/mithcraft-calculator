/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'jei-bg': '#0F0F0F',
        'jei-panel': '#1A1A1A',
        'jei-border': '#2A2A2A',
        'jei-hover': '#252525',
        'jei-accent': '#C8A86C',
        'jei-accent-light': '#D4B87A',
        'jei-text': '#E0E0E0',
        'jei-text-dim': '#808080',
        'jei-search': '#161616',
        'jei-input': '#1E1E1E',
      },
      fontFamily: {
        'minecraft': ['"Minecraft"', 'monospace'],
        'sans': ['"Segoe UI"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      gridTemplateColumns: {
        'jei': 'repeat(auto-fill, minmax(64px, 1fr))',
        'craft': 'repeat(3, 48px)',
      },
      animation: {
        'fade-in': 'fadeIn 0.15s ease-out',
        'slide-up': 'slideUp 0.2s ease-out',
      },
      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp: { '0%': { opacity: '0', transform: 'translateY(8px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
