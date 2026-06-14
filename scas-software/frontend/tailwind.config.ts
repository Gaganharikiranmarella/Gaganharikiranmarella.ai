import type { Config } from "tailwindcss";

export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}"
  ],

  theme: {
    extend: {

      colors: {

        background: "#0B0F14",

        card: "#121A22",

        border: "#243244",

        critical: "#EF4444",

        warning: "#F59E0B",

        success: "#10B981",

        info: "#38BDF8"
      }
    }
  },

  plugins: []
} satisfies Config;