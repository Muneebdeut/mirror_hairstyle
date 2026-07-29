/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f4f3ff',
          100: '#ebe9fe',
          200: '#d9d5fe',
          300: '#beb4fe',
          400: '#9d88fd',
          500: '#7c54fc',
          600: '#6931f6',
          700: '#5920e1',
          800: '#4a1abf',
          900: '#3d179d',
          950: '#240d6d',
        },
        gold: {
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
        }
      },
      backgroundImage: {
        'hero-gradient': 'radial-gradient(ellipse at top, rgba(124, 84, 252, 0.15), transparent 70%)',
      }
    },
  },
  plugins: [],
}
