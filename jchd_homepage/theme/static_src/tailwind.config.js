module.exports = {
    content: ["../templates/**/*.html", "../../templates/**/*.html", "../../**/templates/**/*.html"],
    theme: {
        extend: {
            colors: {
                primary: "#005bac",
                primarydark: "#004080",
                primarylight: "#e6f0ff",
                accent: "#00a0e9",
            },
            fontFamily: {
                sans: ['"Noto Sans JP"', "sans-serif"],
            },
            transitionProperty: {
                height: "height",
                spacing: "margin, padding",
            },
            keyframes: {
                fadeInUp: {
                    "0%": { opacity: "0", transform: "translateY(20px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
                fadeIn: {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
            },
            animation: {
                fadeInUp: "fadeInUp 0.7s ease-out forwards",
                fadeIn: "fadeIn 0.8s ease-out forwards",
            },
        },
    },
    plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography"), require("@tailwindcss/aspect-ratio")],
};
