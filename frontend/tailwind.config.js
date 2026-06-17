/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        satisfactory: {
          orange:      "#e8902d",
          "orange-lt": "#f5a84e",
          dark:        "#0f1117",
          surface:     "#1a1f2e",
          elevated:    "#242938",
          border:      "#2d3748",
        },
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "monospace"],
      },
    },
  },
  plugins: [],
};
