// docs/js/charts.js
// Renderizadores Plotly.js reativos para temas claro/escuro e acessibilidade sem innerHTML

const CONFIG_PLOTLY = { responsive: true, displayModeBar: false };

/** Lê os tokens CSS do tema ativo para sincronização de cores */
export function getPlotlyThemeTokens() {
  const css = getComputedStyle(document.documentElement);
  const ler = (nome) => css.getPropertyValue(nome).trim();
  return {
    text: ler("--text") || "#E8ECF8",
    textMuted: ler("--text-muted") || "#93A0C0",
    border: ler("--border") || "#2A3558",
    surface2: ler("--surface-2") || "#1D2742",
    curso: ler("--accent") || "#4F8CFF",     // Azul: o que o curso ensina
    mercado: ler("--accent-2") || "#FF8A3D", // Laranja: o que o mercado pede
    ok: ler("--ok") || "#3DD68C",
    warn: ler("--warn") || "#F5B83D",
    danger: ler("--danger") || "#FF5C6C",
  };
}

/** Converte hex (#4F8CFF) + alpha para rgba(r,g,b,a) */
function comAlpha(hex, alpha) {
  if (!hex || !hex.startsWith("#")) return `rgba(79, 140, 255, ${alpha})`;
  const h = hex.replace("#", "");
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) || 0);
  return `rgba(${r},${g},${b},${alpha})`;
}

const pct = (n) => `${Number(n).toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

function layoutBase(t, extra = {}) {
  return {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: "Inter, sans-serif", color: t.text, size: 12 },
    margin: { t: 24, r: 24, b: 48, l: 56 },
    xaxis: { gridcolor: t.border, zerolinecolor: t.border, color: t.textMuted },
    yaxis: { gridcolor: t.border, zerolinecolor: t.border, color: t.textMuted },
    legend: { orientation: "h", x: 0.5, xanchor: "center", y: -0.2, font: { color: t.text } },
    ...extra,
  };
}

/** Cor da barra de aderência: alta >= 80, média 50-79, baixa < 50 */
const corAderencia = (t, v) => (v >= 80 ? t.ok : v >= 50 ? t.warn : t.danger);

/**
 * Radar Curso x Mercado (scatterpolar)
 * dados = { eixos: [...], mercado: [...], curso: [...] }
 */
export function renderRadar(dados) {
  if (!window.Plotly || !dados || !dados.eixos || dados.eixos.length === 0) return;
  const el = document.getElementById("radarChart");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  const maxMercado = Math.max(...dados.mercado, 10);
  const teto = Math.ceil((maxMercado + 5) / 10) * 10;
  const fechar = (arr) => [...arr, arr[0]];
  const eixos = fechar(dados.eixos);

  Plotly.react("radarChart", [
    {
      type: "scatterpolar", name: "Ensinado no curso", theta: eixos, r: fechar(dados.curso),
      fill: "toself", line: { color: t.curso, width: 2.5 }, fillcolor: comAlpha(t.curso, 0.25),
      hovertemplate: "%{theta}: %{r:.1f}%<extra>Curso</extra>",
    },
    {
      type: "scatterpolar", name: "Pedido pelo mercado", theta: eixos, r: fechar(dados.mercado),
      fill: "toself", line: { color: t.mercado, width: 2.5 }, fillcolor: comAlpha(t.mercado, 0.25),
      hovertemplate: "%{theta}: %{r:.1f}%<extra>Mercado</extra>",
    },
  ], layoutBase(t, {
    margin: { t: 30, r: 40, b: 60, l: 40 },
    polar: {
      bgcolor: "rgba(0,0,0,0)",
      radialaxis: { visible: true, range: [0, teto], gridcolor: t.border, color: t.textMuted, ticksuffix: "%" },
      angularaxis: { gridcolor: t.border, color: t.text },
    },
  }), CONFIG_PLOTLY);

  // Atualiza tabela de acessibilidade via DOM seguro
  const tbody = document.getElementById("tbodyRadar");
  if (tbody) {
    tbody.replaceChildren();
    dados.eixos.forEach((eixo, i) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      td1.textContent = eixo;
      const td2 = document.createElement("td");
      td2.textContent = pct(dados.curso[i] || 0);
      const td3 = document.createElement("td");
      td3.textContent = pct(dados.mercado[i] || 0);
      tr.append(td1, td2, td3);
      tbody.appendChild(tr);
    });
  }
}

/**
 * Barras horizontais: competências mais demandadas
 * dados = { competencias: [...], pct: [...], cobertas: [...] }
 */
export function renderTopTecnologias(dados) {
  if (!window.Plotly || !dados || !dados.competencias || dados.competencias.length === 0) return;
  const el = document.getElementById("topTecnologiasChart");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  Plotly.react("topTecnologiasChart", [{
    type: "bar", orientation: "h",
    y: dados.competencias, x: dados.pct,
    marker: { color: dados.cobertas.map((c) => (c ? t.curso : t.mercado)) },
    text: dados.pct.map(pct), textposition: "outside", cliponaxis: false,
    customdata: dados.cobertas.map((c) => (c ? "ensinada" : "lacuna")),
    hovertemplate: "%{y}: %{x:.1f}% das vagas (%{customdata})<extra></extra>",
  }], layoutBase(t, {
    margin: { t: 16, r: 56, b: 40, l: 150 },
    xaxis: { gridcolor: t.border, color: t.textMuted, ticksuffix: "%", rangemode: "tozero" },
    yaxis: { autorange: "reversed", color: t.text },
  }), CONFIG_PLOTLY);

  // Atualiza tabela de acessibilidade via DOM seguro
  const tbody = document.getElementById("tbodyTopTecnologias");
  if (tbody) {
    tbody.replaceChildren();
    dados.competencias.forEach((comp, i) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      td1.textContent = comp;
      const td2 = document.createElement("td");
      td2.textContent = pct(dados.pct[i] || 0);
      const td3 = document.createElement("td");
      td3.textContent = dados.cobertas[i] ? "Ensinada no curso" : "Lacuna curricular";
      tr.append(td1, td2, td3);
      tbody.appendChild(tr);
    });
  }
}

/**
 * Box plot da faixa salarial por área
 * dados = { area: [salarios...] }
 */
export function renderSalarioPorArea(dados) {
  if (!window.Plotly || !dados || Object.keys(dados).length === 0) return;
  const el = document.getElementById("salarioChart");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  const traces = Object.entries(dados).map(([area, valores]) => ({
    type: "box", name: area, y: valores, boxpoints: "all", jitter: 0.4, pointpos: 0,
    marker: { color: t.mercado }, line: { color: t.mercado }, fillcolor: comAlpha(t.mercado, 0.2),
    hovertemplate: "R$ %{y:,.0f}<extra>" + area + "</extra>",
  }));

  Plotly.react("salarioChart", traces, layoutBase(t, {
    showlegend: false,
    yaxis: { title: { text: "R$ (ponto médio da faixa)" }, gridcolor: t.border, color: t.textMuted, tickformat: ",.0f" },
  }), CONFIG_PLOTLY);

  // Atualiza tabela de acessibilidade via DOM seguro
  const tbody = document.getElementById("tbodySalario");
  if (tbody) {
    tbody.replaceChildren();
    Object.entries(dados).forEach(([area, valores]) => {
      const ordenados = [...valores].sort((a, b) => a - b);
      const meio = Math.floor(ordenados.length / 2);
      const mediana = ordenados.length % 2 !== 0 ? ordenados[meio] : (ordenados[meio - 1] + ordenados[meio]) / 2;

      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      td1.textContent = area;
      const td2 = document.createElement("td");
      td2.textContent = String(valores.length);
      const td3 = document.createElement("td");
      td3.textContent = `R$ ${Number(mediana).toLocaleString("pt-BR", { maximumFractionDigits: 0 })}`;

      tr.append(td1, td2, td3);
      tbody.appendChild(tr);
    });
  }
}

/**
 * Linha: evolução de vagas por semana
 * dados = { semanas: [...], total: [...] }
 */
export function renderVagasPorSemana(dados) {
  if (!window.Plotly || !dados || !dados.semanas || dados.semanas.length === 0) return;
  const el = document.getElementById("vagasSemanaChart");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  Plotly.react("vagasSemanaChart", [{
    type: "scatter", mode: "lines+markers", x: dados.semanas, y: dados.total,
    line: { color: t.mercado, width: 3, shape: "spline" }, marker: { size: 8, color: t.mercado },
    hovertemplate: "%{x}: %{y} vagas<extra></extra>",
  }], layoutBase(t, {
    yaxis: { gridcolor: t.border, color: t.textMuted, rangemode: "tozero", dtick: 1 },
  }), CONFIG_PLOTLY);

  // Atualiza tabela de acessibilidade via DOM seguro
  const tbody = document.getElementById("tbodyVagasSemana");
  if (tbody) {
    tbody.replaceChildren();
    dados.semanas.forEach((sem, i) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      td1.textContent = sem;
      const td2 = document.createElement("td");
      td2.textContent = String(dados.total[i]);
      tr.append(td1, td2);
      tbody.appendChild(tr);
    });
  }
}

/**
 * Heatmap módulo x competência demandada
 * dados = { competencias: [...], linhas: [ { modulo: "...", valores: [1, 0...] } ] }
 */
export function renderMatriz(dados) {
  if (!window.Plotly || !dados || !dados.competencias || !dados.linhas || dados.linhas.length === 0) return;
  const el = document.getElementById("matrizCompetencias");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  const modulos = dados.linhas.map((l) => l.modulo);
  const z = dados.linhas.map((l) => l.valores);

  Plotly.react("matrizCompetencias", [{
    type: "heatmap", x: dados.competencias, y: modulos, z,
    colorscale: [[0, t.surface2], [1, t.curso]], showscale: false, xgap: 3, ygap: 3,
    text: z.map((linha) => linha.map((v) => (v ? "✓" : ""))), texttemplate: "%{text}",
    hovertemplate: "%{y} → %{x}: %{text}<extra></extra>",
  }], layoutBase(t, {
    margin: { t: 16, r: 16, b: 110, l: 220 },
    xaxis: { tickangle: -40, color: t.text, side: "bottom" },
    yaxis: { autorange: "reversed", color: t.text },
  }), CONFIG_PLOTLY);
}

/**
 * Barras de aderência do aluno às vagas mais compatíveis
 * dados = { vagas: [...], pct: [...] }
 */
export function renderAderencia(dados) {
  if (!window.Plotly || !dados || !dados.vagas || dados.vagas.length === 0) return;
  const el = document.getElementById("aderenciaChart");
  if (!el) return;

  const t = getPlotlyThemeTokens();
  Plotly.react("aderenciaChart", [{
    type: "bar", orientation: "h", y: dados.vagas, x: dados.pct,
    marker: { color: dados.pct.map((v) => corAderencia(t, v)) },
    text: dados.pct.map(pct), textposition: "outside", cliponaxis: false,
    hovertemplate: "%{y}: %{x:.1f}% de aderência<extra></extra>",
  }], layoutBase(t, {
    margin: { t: 16, r: 56, b: 40, l: 260 },
    xaxis: { range: [0, 115], gridcolor: t.border, color: t.textMuted, ticksuffix: "%" },
    yaxis: { autorange: "reversed", color: t.text },
  }), CONFIG_PLOTLY);

  // Atualiza tabela de acessibilidade via DOM seguro
  const tbody = document.getElementById("tbodyAderencia");
  if (tbody) {
    tbody.replaceChildren();
    dados.vagas.forEach((vaga, i) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      td1.textContent = vaga;
      const td2 = document.createElement("td");
      td2.textContent = pct(dados.pct[i] || 0);
      tr.append(td1, td2);
      tbody.appendChild(tr);
    });
  }
}

// Orquestrador de estado e redesenho reativo ao tema
const estado = { radar: null, topTec: null, salario: null, semana: null, matriz: null, aderencia: null };

const RENDERIZADORES = {
  radar: renderRadar,
  topTec: renderTopTecnologias,
  salario: renderSalarioPorArea,
  semana: renderVagasPorSemana,
  matriz: renderMatriz,
  aderencia: renderAderencia,
};

export function atualizarGrafico(nome, dados) {
  if (!dados) return;
  estado[nome] = dados;
  if (RENDERIZADORES[nome]) {
    RENDERIZADORES[nome](dados);
  }
}

export function renderizarTodosGraficos() {
  for (const [nome, dados] of Object.entries(estado)) {
    if (dados && RENDERIZADORES[nome]) {
      RENDERIZADORES[nome](dados);
    }
  }
}

window.addEventListener("themeChanged", () => {
  renderizarTodosGraficos();
});

window.addEventListener("viewChanged", () => {
  renderizarTodosGraficos();
});


// Dados de fallback para demonstração offline (Curso TDS / 17 vagas de desenvolvimento)
export const EXEMPLO = {
  radar: {
    eixos: ["APIs REST", "Git", "SQL", "TypeScript", "Firebase", "Inglês Técnico"],
    mercado: [52.9, 47.1, 47.1, 23.5, 17.6, 17.6],
    curso: [52.9, 47.1, 47.1, 0, 0, 0],
  },
  topTec: {
    competencias: ["APIs REST", "Git", "SQL", "Docker", "Testes Automatizados", "CSS", "HTML", "Metodologias Ágeis", "TypeScript", "Firebase"],
    pct: [52.9, 47.1, 47.1, 41.2, 41.2, 29.4, 29.4, 23.5, 23.5, 17.6],
    cobertas: [true, true, true, true, true, true, true, true, false, false],
  },
  salario: {
    desenvolvimento: [4250, 7250, 1700, 5500, 5000, 3600, 7000, 5500, 7750, 3300, 3850, 10500, 3300, 5500, 6000, 5000],
    dados: [4750, 2550, 8750, 6500, 1800, 6500],
    infraestrutura: [2800, 9500, 7750, 13000, 2650],
    ia: [6250],
  },
  semana: {
    semanas: ["2026-W38", "2026-W39", "2026-W40", "2026-W41", "2026-W42", "2026-W43"],
    total: [1, 3, 4, 4, 2, 3],
  },
  aderencia: {
    vagas: [
      "V003 · Estagiário de Desenvolvimento",
      "V011 · Desenvolvedor PHP Júnior",
      "V027 · Desenvolvedor React Native",
      "V008 · Desenvolvedor Mobile Flutter",
      "V019 · Técnico em Desenvolvimento de Sistemas",
    ],
    pct: [100.0, 85.7, 83.3, 80.0, 80.0],
  },
  matriz: {
    competencias: ["APIs REST", "Git", "SQL", "Docker", "Testes Automatizados", "CSS", "HTML", "Metodologias Ágeis", "TypeScript", "Firebase"],
    linhas: [
      { modulo: "Programação Web e APIs", valores: [1, 1, 0, 0, 0, 1, 1, 0, 0, 0] },
      { modulo: "Banco de Dados Relacional", valores: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0] },
      { modulo: "DevOps e Containers", valores: [0, 1, 0, 1, 0, 0, 0, 0, 0, 0] },
      { modulo: "Desenvolvimento Mobile", valores: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0] },
    ],
  },
};
