// docs/js/views.js
// Alternância entre as visões Aluno e Coordenação, sincronização WAI-ARIA e redimensionamento Plotly

const VISOES = {
  aluno:       { aba: "tabAluno",       painel: "viewAluno",       nav: "navAluno" },
  coordenacao: { aba: "tabCoordenacao", painel: "viewCoordenacao", nav: "navCoordenacao" },
};

const ROTULOS_BOTTOM = {
  aluno:       ["Painel", "Vagas", "Trilha", "Perfil"],
  coordenacao: ["Painel", "Gráficos", "Lacunas", "Matriz"],
};

export function mostrarVisao(nome) {
  for (const [id, v] of Object.entries(VISOES)) {
    const ativa = id === nome;
    const aba = document.getElementById(v.aba);
    if (aba) {
      aba.classList.toggle("active", ativa);
      aba.setAttribute("aria-selected", String(ativa));
      aba.tabIndex = ativa ? 0 : -1;
    }
    const painel = document.getElementById(v.painel);
    if (painel) painel.hidden = !ativa;
    const nav = document.getElementById(v.nav);
    if (nav) nav.hidden = !ativa;
  }

  // Navegação inferior (mobile): sincroniza rótulos e âncoras de destino
  document.querySelectorAll("#bottomNav .bottom-nav__item").forEach((botao, i) => {
    botao.dataset.alvo = botao.dataset[nome === "aluno" ? "alvoAluno" : "alvoCoordenacao"];
    const label = botao.querySelector(".bottom-nav__label");
    if (label && ROTULOS_BOTTOM[nome] && ROTULOS_BOTTOM[nome][i]) {
      label.textContent = ROTULOS_BOTTOM[nome][i];
    }
  });

  // Gráficos recém-exibidos necessitam de recalculo de viewport no Plotly
  requestAnimationFrame(() => {
    const painelId = VISOES[nome]?.painel;
    if (painelId) {
      document
        .querySelectorAll(`#${painelId} .chart-container`)
        .forEach((el) => {
          if (window.Plotly && el.data) {
            window.Plotly.Plots.resize(el);
          }
        });
    }
  });
}

// Suporte a navegação por setas do teclado (WAI-ARIA tablist)
document.getElementById("togglePerfil")?.addEventListener("keydown", (e) => {
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const tabAluno = document.getElementById("tabAluno");
  const proxima = tabAluno?.getAttribute("aria-selected") === "true" ? "coordenacao" : "aluno";
  mostrarVisao(proxima);
  document.getElementById(VISOES[proxima].aba)?.focus();
});

document.getElementById("tabAluno")?.addEventListener("click", () => mostrarVisao("aluno"));
document.getElementById("tabCoordenacao")?.addEventListener("click", () => mostrarVisao("coordenacao"));

document.getElementById("bottomNav")?.addEventListener("click", (e) => {
  const alvo = e.target.closest(".bottom-nav__item")?.dataset.alvo;
  if (alvo) {
    document.getElementById(alvo)?.scrollIntoView({ behavior: "smooth" });
  }
});

document.getElementById("btnRelatorio")?.addEventListener("click", () => window.print());
