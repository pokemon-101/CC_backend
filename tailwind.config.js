/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#1DB954',
          600: '#16a34a',
        },
        secondary: {
          900: '#191414',
        },
      },
    },
  },
  plugins: [],
}