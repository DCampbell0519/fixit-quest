module.exports = {
  content: [
    '../templates/**/*.html',
    '../../fixit_tracker/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["cupcake"],
  },
}
