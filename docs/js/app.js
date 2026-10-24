// docs/js/app.js
// Orquestrador principal da interface do SkillRadar: reatividade, data-binding, filtros e conformidade de segurança

import "./theme.js";
import { mostrarVisao } from "./views.js";
import {
  atualizarGrafico,
  renderAderencia,
  EXEMPLO,
} from "./charts.js";
import {
  inicializarFirebase,
  trocarCurso,
  salvarInteresseAluno,
} from "./firebase.js";

// Estado local da aplicação
let vagasOriginais = [];
let cursoDadosAtivo = null;
let trilhaDadosAtiva = null;
let contextoAtivo = null;

const formatarMoeda = (val) =>
  val != null
    ? Number(val).toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 })
    : "—";

const formatarPct = (val) =>
  val != null
    ? `${Number(val).toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`
    : "—";

/** Atualiza os 4 KPIs no topo do painel compartilhado */
function atualizarKPIs(lacunas) {
  if (!lacunas) return;

  // 1. Vagas Ativas
  const elVagas = document.querySelector('[data-bind="kpi.vagasAtivas"]');
  const elVagasTrend = document.querySelector('[data-bind="kpi.vagasAtivas.trend"]');
  if (elVagas) elVagas.textContent = lacunas.amostra_n ?? "—";
  if (elVagasTrend) {
    const areasFoco = (lacunas.areas_foco || []).join(", ") || "geral";
    elVagasTrend.textContent = `de ${lacunas.total_coletadas || 30} coletadas · área: ${areasFoco}`;
  }

  // 2. Cobertura do Currículo
  const elCob = document.querySelector('[data-bind="kpi.cobertura"]');
  const elCobTrend = document.querySelector('[data-bind="kpi.cobertura.trend"]');
  const cobPct = lacunas.cobertura_pct;
  if (elCob) elCob.textContent = formatarPct(cobPct);
  if (elCobTrend) {
    elCobTrend.className = "kpi-card__trend " + (cobPct >= 70 ? "positive" : cobPct >= 40 ? "neutral" : "negative");
    elCobTrend.textContent = "das competências pedidas o curso já ensina";
  }

  // 3. Principais Lacunas
  const elLac = document.querySelector('[data-bind="kpi.lacunas"]');
  const elLacTrend = document.querySelector('[data-bind="kpi.lacunas.trend"]');
  const listaLacunas = lacunas.lacunas || [];
  if (elLac) {
    const top2 = listaLacunas.slice(0, 2).map((l) => l.competencia).join(", ");
    elLac.textContent = top2 || "Nenhuma";
  }
  if (elLacTrend) {
    if (listaLacunas.length >= 2) {
      elLacTrend.textContent = `pedidas em ${listaLacunas[0].contagem} e ${listaLacunas[1].contagem} de ${lacunas.amostra_n || 17} vagas`;
    } else if (listaLacunas.length === 1) {
      elLacTrend.textContent = `pedida em ${listaLacunas[0].contagem} de ${lacunas.amostra_n || 17} vagas`;
    } else {
      elLacTrend.textContent = "sem lacunas críticas detectadas";
    }
  }

  // 4. Salário Mediano
  const elSal = document.querySelector('[data-bind="kpi.salario"]');
  const elSalTrend = document.querySelector('[data-bind="kpi.salario.trend"]');
  const salarioMed = lacunas.kpis?.salario_mediano;
  const salarioN = lacunas.kpis?.salario_n || 0;
  if (elSal) elSal.textContent = formatarMoeda(salarioMed);
  if (elSalTrend) {
    elSalTrend.textContent = `ponto médio das faixas · ${salarioN} vagas com faixa`;
  }
}

/**
 * Renderiza a seção de Insights da IA via DOM seguro (sem innerHTML para dados de IA).
 * Conformidade com Diretivas de Segurança e Prevenção de XSS.
 */
function atualizarInsights(insights) {
  const container = document.getElementById("iaInsights");
  if (!container) return;

  container.replaceChildren();

  if (!insights || insights.length === 0) {
    const card = document.createElement("article");
    card.className = "insight-card";

    const header = document.createElement("div");
    header.className = "insight-card__header";
    header.innerHTML = '<span class="insight-card__icon" aria-hidden="true">💡</span><span class="badge-ai">IA SkillRadar</span>';

    const title = document.createElement("h2");
    title.className = "insight-card__title";
    title.textContent = "Varredura e alinhamento concluídos";

    const body = document.createElement("p");
    body.className = "insight-card__body";
    body.textContent = "Nenhum insight crítico pendente de revisão para esta área no momento.";

    card.append(header, title, body);
    container.appendChild(card);
    return;
  }

  insights.slice(0, 3).forEach((ins) => {
    const card = document.createElement("article");
    card.className = "insight-card";

    const header = document.createElement("div");
    header.className = "insight-card__header";
    header.innerHTML = '<span class="insight-card__icon" aria-hidden="true">💡</span><span class="badge-ai">Gerado por IA</span>';

    const title = document.createElement("h2");
    title.className = "insight-card__title";
    title.textContent = ins.titulo || "Insight Curricular";

    const body = document.createElement("p");
    body.className = "insight-card__body";
    body.textContent = ins.texto || "";

    card.append(header, title, body);
    container.appendChild(card);
  });
}

/** Renderiza a tabela de Lacunas Curriculares para Coordenação usando DOM seguro */
function atualizarTabelaLacunas(lacunas) {
  const tbody = document.querySelector("#tabelaLacunas tbody");
  if (!tbody) return;

  tbody.replaceChildren();

  const lista = lacunas.lacunas || [];
  if (lista.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.style.textAlign = "center";
    td.style.padding = "16px";
    td.textContent = "Nenhuma lacuna detectada para o curso selecionado.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  lista.forEach((item) => {
    const tr = document.createElement("tr");

    const tdComp = document.createElement("td");
    const strong = document.createElement("strong");
    strong.textContent = item.competencia;
    tdComp.appendChild(strong);

    const tdArea = document.createElement("td");
    tdArea.textContent = item.area || "desenvolvimento";

    const tdCount = document.createElement("td");
    tdCount.className = "num";
    tdCount.textContent = String(item.contagem);

    const tdPct = document.createElement("td");
    tdPct.className = "num";
    tdPct.textContent = formatarPct(item.pct_vagas);

    tr.append(tdComp, tdArea, tdCount, tdPct);
    tbody.appendChild(tr);
  });
}

/** Renderiza a timeline da trilha recomendada para o Aluno usando DOM seguro */
function atualizarTrilha(trilha) {
  const listaEl = document.getElementById("trilhaAprendizado");
  const resumoEl = document.getElementById("trilhaResumo");
  if (!listaEl) return;

  listaEl.replaceChildren();

  const modulos = trilha?.modulos || [];
  if (modulos.length === 0) {
    const li = document.createElement("li");
    li.className = "state-empty";
    li.textContent = "Currículo já atende plenamente à demanda mapeada das vagas.";
    listaEl.appendChild(li);
    if (resumoEl) resumoEl.textContent = "";
    return;
  }

  modulos.forEach((mod, idx) => {
    const li = document.createElement("li");
    li.className = "timeline-step";

    const marker = document.createElement("div");
    marker.className = "timeline-step__marker";
    marker.setAttribute("aria-hidden", "true");
    marker.textContent = String(idx + 1);

    const content = document.createElement("div");
    content.className = "timeline-step__content";

    const title = document.createElement("h3");
    title.className = "timeline-step__title";
    title.textContent = mod.modulo;

    const desc = document.createElement("p");
    desc.className = "timeline-step__desc";
    const compTexto = Array.isArray(mod.competencias_cobertas)
      ? mod.competencias_cobertas.join(", ")
      : mod.competencias_cobertas;
    desc.textContent = `Carga horária: ${mod.carga_horaria}h • Cobre: ${compTexto} (${mod.curso}).`;

    const badge = document.createElement("span");
    const prioridadeAlta = mod.peso >= 3;
    badge.className = "badge-status " + (prioridadeAlta ? "badge-status--priority" : "badge-status--medium");
    badge.textContent = prioridadeAlta ? "Alta prioridade" : "Média prioridade";

    content.append(title, desc, badge);
    li.append(marker, content);
    listaEl.appendChild(li);
  });

  if (resumoEl && trilha.aderencia_antes_pct != null && trilha.aderencia_depois_pct != null) {
    resumoEl.textContent = `Aderência média estimada: ${formatarPct(trilha.aderencia_antes_pct)} → ${formatarPct(trilha.aderencia_depois_pct)} ao concluir os ${modulos.length} módulos (cálculo feito no backend).`;
  }
}

/** Calcula aderência de uma vaga em relação ao curso atual */
function calcularAderenciaVaga(vaga, lacunas) {
  const comps = vaga.competencias || [];
  if (comps.length === 0) return { pct: 100, cobertas: [], lacunas: [] };

  const lacunasSet = new Set((lacunas?.lacunas || []).map((l) => l.competencia.toLowerCase()));
  const cobertas = [];
  const gapped = [];

  for (const c of comps) {
    if (lacunasSet.has(c.toLowerCase())) {
      gapped.push(c);
    } else {
      cobertas.push(c);
    }
  }

  const pctCalc = Math.round((cobertas.length / comps.length) * 1000) / 10;
  return { pct: pctCalc, cobertas, lacunas: gapped };
}

/**
 * Renderiza a lista de vagas filtrada para o Aluno usando DOM seguro (sem innerHTML para texto de vagas).
 * Atende às diretrizes de segurança contra XSS e LGPD.
 */
function renderizarVagas() {
  const container = document.getElementById("listaVagas");
  const emptyEl = document.getElementById("estadoVazioVagas");
  if (!container) return;

  const termoBusca = (document.getElementById("inputBuscaVaga")?.value || "").toLowerCase().trim();
  const filtroArea = document.getElementById("filtroArea")?.value || "todas";
  const filtroSalario = document.getElementById("filtroSalario")?.value || "todas";

  // Filtra vagas
  const filtradas = vagasOriginais.filter((v) => {
    if (termoBusca) {
      const matchTitulo = (v.titulo || "").toLowerCase().includes(termoBusca);
      const matchEmpresa = (v.empresa || "").toLowerCase().includes(termoBusca);
      const matchSkills = (v.competencias || []).some((c) => c.toLowerCase().includes(termoBusca));
      if (!matchTitulo && !matchEmpresa && !matchSkills) return false;
    }

    if (filtroArea !== "todas") {
      const areaVaga = (v.area_principal || "").toLowerCase();
      if (areaVaga !== filtroArea.toLowerCase()) return false;
    }

    if (filtroSalario !== "todas") {
      const salMin = v.salario_min || 0;
      const salMax = v.salario_max || salMin;
      const pontoMedio = salMax > 0 ? (salMin + salMax) / 2 : salMin;

      if (filtroSalario === "ate-3000" && (pontoMedio > 3000 || pontoMedio === 0)) return false;
      if (filtroSalario === "3000-6000" && (pontoMedio < 3000 || pontoMedio > 6000)) return false;
      if (filtroSalario === "acima-6000" && pontoMedio < 6000) return false;
    }

    return true;
  });

  const comAderencia = filtradas.map((v) => {
    const res = calcularAderenciaVaga(v, cursoDadosAtivo);
    return { ...v, aderenciaCalc: res.pct, tagsCobertas: res.cobertas, tagsLacunas: res.lacunas };
  });

  comAderencia.sort((a, b) => b.aderenciaCalc - a.aderenciaCalc);

  // Atualiza gráfico Top 5
  const top5 = comAderencia.slice(0, 5);
  if (top5.length > 0) {
    renderAderencia({
      vagas: top5.map((v) => `${v.vaga_id || v.id || "V"} · ${v.titulo}`),
      pct: top5.map((v) => v.aderenciaCalc),
    });
  }

  container.replaceChildren();

  if (comAderencia.length === 0) {
    if (emptyEl) emptyEl.hidden = false;
    return;
  }

  if (emptyEl) emptyEl.hidden = true;

  comAderencia.forEach((vaga) => {
    const score = vaga.aderenciaCalc;
    const scoreClass = score >= 80 ? "match-score--high" : score >= 50 ? "match-score--mid" : "match-score--low";

    const faixaTexto = vaga.salario_min && vaga.salario_max
      ? `${formatarMoeda(vaga.salario_min)} – ${formatarMoeda(vaga.salario_max)}`
      : vaga.salario_min
      ? `A partir de ${formatarMoeda(vaga.salario_min)}`
      : "Salário a combinar";

    const article = document.createElement("article");
    article.className = "vaga-card";
    article.dataset.vagaId = vaga.vaga_id || vaga.id || "";

    const mainDiv = document.createElement("div");
    mainDiv.className = "vaga-card__main";

    const role = document.createElement("h3");
    role.className = "vaga-card__role";
    role.textContent = vaga.titulo;

    const meta = document.createElement("p");
    meta.className = "vaga-card__meta";
    meta.textContent = `${vaga.empresa} • ${vaga.cidade || "Ourinhos"} • ${faixaTexto}`;

    const tagsDiv = document.createElement("div");
    tagsDiv.className = "vaga-card__tags";

    vaga.tagsCobertas.forEach((c) => {
      const chip = document.createElement("span");
      chip.className = "chip-skill chip-skill--ok";
      const icon = document.createElement("span");
      icon.className = "chip-skill__icon";
      icon.setAttribute("aria-hidden", "true");
      icon.textContent = "✓ ";
      chip.append(icon, document.createTextNode(`${c} (Dominada)`));
      tagsDiv.appendChild(chip);
    });

    vaga.tagsLacunas.forEach((c) => {
      const chip = document.createElement("span");
      chip.className = "chip-skill chip-skill--gap";
      const icon = document.createElement("span");
      icon.className = "chip-skill__icon";
      icon.setAttribute("aria-hidden", "true");
      icon.textContent = "! ";
      chip.append(icon, document.createTextNode(`${c} (Lacuna)`));
      tagsDiv.appendChild(chip);
    });

    mainDiv.append(role, meta, tagsDiv);

    const sideDiv = document.createElement("div");
    sideDiv.className = "vaga-card__side";

    const scoreBadge = document.createElement("span");
    scoreBadge.className = `match-score ${scoreClass}`;
    scoreBadge.setAttribute("aria-label", `${score} por cento de aderência`);
    scoreBadge.textContent = `${Math.round(score)}% Match`;

    const btnLink = document.createElement("a");
    btnLink.className = "btn-action";
    btnLink.href = vaga.fonte_url || vaga.url_vaga || "#";
    btnLink.target = "_blank";
    btnLink.rel = "noopener noreferrer";
    btnLink.textContent = "Acessar vaga";

    sideDiv.append(scoreBadge, btnLink);
    article.append(mainDiv, sideDiv);
    container.appendChild(article);
  });
}

/** Atualiza a barra de status de amostra e modo demo */
function atualizarBarraAmostra(contexto, lacunas) {
  const el = document.getElementById("amostraInfo");
  if (!el) return;

  const dataColeta = contexto?.ultima_coleta
    ? new Date(contexto.ultima_coleta).toLocaleDateString("pt-BR")
    : "23/10/2026";
  const amostra = lacunas?.amostra_n || 17;
  const total = contexto?.total_vagas || 30;
  const ehDemo = contexto?.modo_demo !== false;

  el.textContent = `Última coleta: ${dataColeta} · Amostra: ${amostra} vagas na área do curso (${total} coletadas) · ${ehDemo ? "Dados de demonstração" : "Dados em tempo real"}`;
}

/** Inicialização da aplicação após o carregamento da página */
window.addEventListener("DOMContentLoaded", () => {
  mostrarVisao("aluno");

  // Handlers dos filtros de vagas
  document.getElementById("inputBuscaVaga")?.addEventListener("input", renderizarVagas);
  document.getElementById("filtroArea")?.addEventListener("change", renderizarVagas);
  document.getElementById("filtroSalario")?.addEventListener("change", renderizarVagas);

  // Handler de troca de curso
  document.getElementById("selectCurso")?.addEventListener("change", (e) => {
    trocarCurso(e.target.value);
  });

  // Handler do formulário de Perfil do Aluno (interesses_alunos)
  document.getElementById("formPerfil")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const statusEl = document.getElementById("perfilStatus");
    const nivel = document.getElementById("perfilNivel")?.value || "basico";
    const curso = document.getElementById("selectCurso")?.value || "tecnico-em-desenvolvimento-de-sistemas";
    const areas = Array.from(document.querySelectorAll('input[name="areas"]:checked')).map((cb) => cb.value);

    if (statusEl) {
      statusEl.textContent = "Salvando perfil...";
      statusEl.style.color = "var(--text-muted)";
    }

    const resultado = await salvarInteresseAluno({
      curso_interesse: curso,
      nivel,
      areas,
    });

    if (statusEl) {
      if (resultado.sucesso) {
        statusEl.textContent = resultado.remoto
          ? "✓ Perfil salvo e sincronizado com o Firestore!"
          : "✓ Perfil registrado localmente com sucesso!";
        statusEl.style.color = "var(--ok)";
      } else {
        statusEl.textContent = "Erro ao salvar perfil. Tente novamente.";
        statusEl.style.color = "var(--danger)";
      }
      setTimeout(() => {
        statusEl.textContent = "";
      }, 4000);
    }
  });

  // Inicializa comunicação Firebase ou dados locais
  inicializarFirebase({
    onStatus: (status) => {
      const liveIndicator = document.getElementById("liveIndicator");
      if (liveIndicator) {
        const dot = document.createElement("span");
        dot.className = "badge-live__dot";
        dot.style.backgroundColor = status.conectado ? "var(--ok)" : "var(--warn)";
        liveIndicator.replaceChildren(dot, document.createTextNode(" " + status.texto));
      }
    },
    onContexto: (ctx) => {
      contextoAtivo = ctx;
      if (ctx.graficos?.salario_por_area) {
        atualizarGrafico("salario", ctx.graficos.salario_por_area);
      }
      atualizarBarraAmostra(ctx, cursoDadosAtivo);
    },
    onLacunas: (lac) => {
      cursoDadosAtivo = lac;
      atualizarKPIs(lac);
      atualizarTabelaLacunas(lac);
      if (lac.graficos) {
        if (lac.graficos.radar) atualizarGrafico("radar", lac.graficos.radar);
        if (lac.graficos.top_tecnologias) atualizarGrafico("topTec", lac.graficos.top_tecnologias);
        if (lac.graficos.matriz) atualizarGrafico("matriz", lac.graficos.matriz);
        if (lac.graficos.vagas_semana) atualizarGrafico("semana", lac.graficos.vagas_semana);
      }
      atualizarBarraAmostra(contextoAtivo, lac);
      renderizarVagas();
    },
    onTrilhas: (tri) => {
      trilhaDadosAtiva = tri;
      atualizarTrilha(tri);
    },
    onVagas: (vagas) => {
      vagasOriginais = vagas;
      renderizarVagas();
    },
    onInsights: (ins) => {
      atualizarInsights(ins);
    },
  });
});
