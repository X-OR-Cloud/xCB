/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#121212',
          black: '#0a0a0a',
          blue: '#007AFF',
          purple: '#AF52DE',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Inter', 'Public Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
