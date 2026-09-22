/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "#F7F3EC",
        surface: "#FBF9F5",
        ink: {
          DEFAULT: "#1A1815",
          soft: "#57534A",
          faint: "#746E5E",
        },
        // "indigo" now carries the ink/gold primary-action scale — kept under
        // the old name so every existing bg-indigo-*/text-indigo-*/etc class
        // repaints automatically. 700 = solid ink (button fills). 500 = the
        // accessible gold (focus rings, borders). Link/accent TEXT usages
        // were redirected to text-gold directly (see README).
        indigo: {
          50: "#F3EADA",
          100: "#E4D9C4",
          200: "#DCCFAE",
          300: "#B79A63",
          400: "#9C7A3C",
          500: "#8A6A34",
          600: "#2E2B26",
          700: "#1A1815",
          900: "#100E0C",
        },
        // "signal" = eligible/approved — deep forest instead of emerald.
        signal: {
          50: "#E8EDE9",
          200: "#A9C4B2",
          500: "#2F4739",
          600: "#243830",
        },
        // "amber" = attention/deadline — a deeper ochre, kept distinct from
        // both gold (brand accent) and red (rejected/failed).
        amber: {
          50: "#F5EDDC",
          200: "#E3CFA0",
          300: "#D6B87C",
          400: "#BE9752",
          500: "#A6752F",
          600: "#8A6023",
          700: "#6E4C1C",
        },
        // Admin's rejected/failed red, remapped to a muted rust so nothing
        // in the app is a stock saturated color.
        red: {
          50: "#F3E7E1",
          100: "#E8D2C7",
          200: "#D9B8AC",
          300: "#C79885",
          500: "#8C4A3A",
          600: "#733C2F",
          700: "#5C3025",
        },
        gold: {
          DEFAULT: "#8A6A34",
          soft: "#B79A63",
          faint: "#DCCFAE",
        },
        slate: {
          50: "#F1ECE1",
          100: "#EFE8DA",
          200: "#DCD3C0",
          300: "#C4B8A0",
          400: "#746E5E",
          500: "#57534A",
          600: "#453F33",
          700: "#332E24",
        },
      },
      fontFamily: {
        display: ["Newsreader", "Georgia", "serif"],
        body: ["General Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      borderRadius: {
        xl: "8px",
        "2xl": "10px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(26,24,21,0.03)",
        soft: "0 12px 32px -16px rgba(26,24,21,0.14)",
      },
    },
  },
  plugins: [],
}

