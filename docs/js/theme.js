// docs/js/theme.js
// Gerenciamento dinâmico de tema claro/escuro com emissão de evento para gráficos Plotly

const CHAVE_TEMA = "skillradar-theme";

export function aplicarTema(tema) {
  document.documentElement.setAttribute("data-theme", tema);
  try {
    localStorage.setItem(CHAVE_TEMA, tema);
  } catch (e) {
    // Modo anônimo ou storage bloqueado
  }
  window.dispatchEvent(new CustomEvent("themeChanged", { detail: { tema } }));
}

export function alternarTema() {
  const atual = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  aplicarTema(atual === "dark" ? "light" : "dark");
}

document.getElementById("toggleTheme")?.addEventListener("click", alternarTema);
