/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "#F5F6F3",
        ink: {
          DEFAULT: "#12172B",
          soft: "#3B4160",
        },
        indigo: {
          50: "#EEF0F7",
          100: "#D9DDEE",
          300: "#8D97C4",
          500: "#4C5A94",
          600: "#374775",
          700: "#2B3A67",
          900: "#171F3B",
        },
        signal: {
          50: "#E7F6EF",
          200: "#A9DEC4",
          500: "#1F9D6F",
          600: "#187F59",
        },
        amber: {
          50: "#FCF0E3",
          200: "#F2C793",
          500: "#E08A3C",
          600: "#BE6E27",
        },
        slate: {
          50: "#F4F4F5",
          200: "#DFDFE3",
          400: "#8A8D98",
          600: "#5B5E6B",
        },
      },
      fontFamily: {
        display: ["Clash Display", "sans-serif"],
        body: ["Satoshi", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
      },
      boxShadow: {
        card: "0 1px 2px rgba(18,23,43,0.04), 0 8px 24px -12px rgba(18,23,43,0.12)",
      },
    },
  },
  plugins: [],
}

