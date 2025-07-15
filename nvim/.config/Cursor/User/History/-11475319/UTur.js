/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,templ}",
    "./static/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"],
  },
} 