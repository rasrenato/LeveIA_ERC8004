/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        success: '#10B981',
        warning: '#F59E0B',
        critical: '#EF4444',
        dead: '#6B7280',
        primary: '#06B6D4',
      }
    },
  },
  plugins: [],
}
