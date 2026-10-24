// docs/js/theme-init.js
// Inicialização síncrona do tema para prevenir FOUC (Flash of Unstyled Content)
(function initTheme() {
  try {
    const savedTheme = localStorage.getItem("skillradar-theme");
    if (savedTheme) {
      document.documentElement.setAttribute("data-theme", savedTheme);
    } else {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      document.documentElement.setAttribute("data-theme", prefersDark ? "dark" : "light");
    }
  } catch (e) {
    document.documentElement.setAttribute("data-theme", "dark");
  }
})();
