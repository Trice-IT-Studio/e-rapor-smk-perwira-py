/** @type {import('tailwindcss').Config} */

import withMT from "@material-tailwind/html/utils/withMT";

module.exports = withMT({
  content: ["./src/templates/**/*.html", "./src/static/src/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [],
});
