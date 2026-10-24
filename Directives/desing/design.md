# SkillRadar — Especificação Completa de Design e UI/UX

## 1. Visão Geral e Conceito Visual

O **SkillRadar** é um painel de inteligência de carreira e alinhamento curricular projetado para conectar o universo acadêmico às demandas do mercado de trabalho. O design atua sob duas perspectivas complementares:

* **Visão da Coordenação:** Analítica, precisa e sóbria. Focada em identificar lacunas curriculares, tomada de decisão e relatórios institucionais.
* **Visão do Aluno:** Motivadora, intuitiva e orientada à ação. Focada em clareza de trajetória, fechamento de lacunas e evolução profissional contínua.

### Filosofia Visual
* **Tema Base:** Dark Mode por padrão no painel operacional diário para redução de fadiga visual e destaque dos dados em tela; Light Mode automático ou alternável para relatórios impressos, exportações e projeções em sala de aula.
* **Linguagem de Cores:** Foco analítico. A cor de acento primária (`--accent`) representa o conceito de "Radar/Varredura/Academia" (Azul elétrico), enquanto a cor secundária (`--accent-2`) simboliza o "Mercado Externo" (Laranja dinâmico).
* **Formas e Estrutura:** Cantos consistentes com raio de curvatura de `12px`, superfícies com elevação sutil baseada em contraste tonal e bordas delimitadoras discretas, sem excesso de gradientes decorativos.

---

## 2. Design Tokens e Sistema de Cores (CSS)

Os tokens são definidos na pseudo-classe `:root` e redefinidos dinamicamente sob os seletores `[data-theme="dark"]` e `[data-theme="light"]`.

### 2.1 Paleta Hexadecimal

| Token | Dark (Padrão) | Light (Relatórios/Doc) | Semântica e Uso |
|---|---|---|---|
| `--bg` | `#0B1020` | `#F5F7FC` | Fundo principal da aplicação |
| `--surface` | `#141B30` | `#FFFFFF` | Fundo de cartões, painéis e modais |
| `--surface-2` | `#1D2742` | `#ECF0F9` | Superfície secundária, inputs e hover cards |
| `--surface-hover` | `#253154` | `#DFE5F2` | Estados de hover em listas e botões sutis |
| `--text` | `#E8ECF8` | `#18213A` | Texto primário, títulos e dados de destaque |
| `--text-muted` | `#93A0C0` | `#5A6682` | Legendas, metadados, labels secundárias |
| `--accent` | `#4F8CFF` | `#2F6BE0` | Radar / Cobertura do Curso / Foco acadêmico |
| `--accent-2` | `#FF8A3D` | `#D9600F` | Mercado / Vagas / Foco profissional |
| `--ok` | `#3DD68C` | `#1E9E5A` | Status positivo, competência dominada, alta compatibilidade |
| `--warn` | `#F5B83D` | `#B07800` | Atenção, cobertura parcial, competência intermediária |
| `--danger` | `#FF5C6C` | `#C62839` | Lacunas críticas, risco curricular, baixa aderência |
| `--border` | `#2A3558` | `#D5DBEA` | Linhas divisórias, contornos de cartões e inputs |
| `--focus-ring` | `#4F8CFF` | `#2F6BE0` | Anel de foco para acessibilidade (teclado) |

### 2.2 Implementação CSS dos Tokens

```css
:root {
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-pill: 9999px;
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.25);
}

/* Dark Mode (Padrão) */
[data-theme="dark"],
:root:not([data-theme="light"]) {
  --bg: #0B1020;
  --surface: #141B30;
  --surface-2: #1D2742;
  --surface-hover: #253154;
  --text: #E8ECF8;
  --text-muted: #93A0C0;
  --accent: #4F8CFF;
  --accent-2: #FF8A3D;
  --ok: #3DD68C;
  --warn: #F5B83D;
  --danger: #FF5C6C;
  --border: #2A3558;
  --focus-ring: #4F8CFF;
}

/* Light Mode */
[data-theme="light"] {
  --bg: #F5F7FC;
  --surface: #FFFFFF;
  --surface-2: #ECF0F9;
  --surface-hover: #DFE5F2;
  --text: #18213A;
  --text-muted: #5A6682;
  --accent: #2F6BE0;
  --accent-2: #D9600F;
  --ok: #1E9E5A;
  --warn: #B07800;
  --danger: #C62839;
  --border: #D5DBEA;
  --focus-ring: #2F6BE0;
}
```

### 2.3 Script de Inicialização de Tema (Prevenção de FOUC)

```javascript
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
```

---

## 3. Tipografia e Hierarquia Visual

- **Família Primária (Títulos, Métricas e KPIs):** `'Space Grotesk'`, sans-serif (pesos 600 e 700).
- **Família Secundária (Corpo, Tabelas, Formulários e Navegação):** `'Inter'`, sans-serif (pesos 400 e 500).
- **Alinhamento Numérico:** Todos os valores numéricos em tabelas e KPIs utilizam obrigatoriamente `font-variant-numeric: tabular-nums` para estabilidade visual e alinhamento vertical.

### Escala Tipográfica Modular

| Nível / Uso | Tamanho | Peso | Line-Height | Aplicação |
|---|---|---|---|---|
| **Display / KPI** | `40px` (`2.5rem`) | 700 | 1.1 | Grande métrica em destaque no painel principal |
| **H1** | `28px` (`1.75rem`) | 700 | 1.2 | Título de visualização principal e nomes de tela |
| **H2** | `20px` (`1.25rem`) | 600 | 1.3 | Cabeçalhos de seção e títulos de cards |
| **H3 / Subtitle** | `16px` (`1.0rem`) | 600 | 1.4 | Títulos de itens, vagas e nomes de módulos |
| **Body (Base)** | `14px` (`0.875rem`) | 400 / 500 | 1.5 | Texto descritivo, parágrafos e itens de menu |
| **Caption / Badge** | `12px` (`0.75rem`) | 500 | 1.4 | Selos, status, metadados e tags de competência |

---

## 4. Arquitetura de Layout e Grid Responsivo

O SkillRadar implementa um sistema de grid responsivo com margem lateral uniforme de 16px (gutter lateral) adaptando-se a três breakpoints fundamentais:

- **Desktop (≥ 1024px):** Grid de 12 colunas com barra de navegação lateral fixa (`aside#sidebarNav`).
- **Tablet (768px a 1023px):** Grid de 4 colunas; barra lateral recolhível em gaveta (off-canvas).
- **Mobile (360px a 767px):** Grid de 1 coluna sem scroll horizontal; navegação principal transposta para barra de rodapé fixa (`nav#bottomNav`).

```
+-----------------------------------------------------------------------------------------+
|                                    header#topBar                                        |
| [Logo SkillRadar]  [Abas: #togglePerfil]  [#selectCurso]  [#liveIndicator]  [#toggleTheme] |
+-----------------------+-----------------------------------------------------------------+
|                       |  main#appMain                                                   |
| aside#sidebarNav      |  +------------------------------------------------------------+ |
|                       |  | section#kpiContainer (Grid 4 colunas)                       | |
| - Painel de Lacunas   |  +------------------------------------------------------------+ |
| - Vagas de Mercado    |  | section#iaInsights (cards de IA com status dinâmico)        | |
| - Matriz & Currículo  |  +------------------------------------------------------------+ |
| - Trilha de Estudo    |  | div#viewAluno ou div#viewCoordenacao (conteúdo por visão)   | |
|                       |  +------------------------------------------------------------+ |
+-----------------------+-----------------------------------------------------------------+
| (Mobile: nav#bottomNav com 4 ícones essenciais)                                         |
+-----------------------------------------------------------------------------------------+
```

---

## 5. Estrutura HTML5 Semântica

> **Dados de exemplo.** Todos os números, nomes de vagas e módulos abaixo vêm dos CSVs da pasta `data/` e representam o curso **Técnico em Desenvolvimento de Sistemas** (áreas de foco: `desenvolvimento`; 17 das 30 vagas de demonstração). Servem para o protótipo. No app final **nenhum valor é fixo no HTML**: cada elemento com `data-bind` ou dentro de uma lista dinâmica é preenchido pelo Firestore (veja a seção 10).

O esqueleto abaixo tem **duas visões reais** (`#viewAluno` e `#viewCoordenacao`), ligadas às abas por `aria-controls`. Os KPIs, os insights e a barra de status são compartilhados.

```html
<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SkillRadar — Inteligência de Carreira & Currículo</title>
  <!-- Script síncrono e curto: aplica o tema antes da primeira pintura (seção 2.3) -->
  <script src="js/theme-init.js"></script>
  <link rel="stylesheet" href="style.css">
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js" defer></script>
  <!-- Módulos ES são adiados por padrão e executam depois do Plotly, na ordem do documento -->
  <script type="module" src="js/app.js"></script>
</head>
<body class="app-body">
  <a href="#appMain" class="skip-link">Ir para o conteúdo principal</a>

  <!-- Topo da aplicação -->
  <header id="topBar" class="topbar">
    <div class="topbar__brand">
      <span class="topbar__icon" aria-hidden="true">🎯</span>
      <h1 class="topbar__title">SkillRadar</h1>
      <span id="liveIndicator" class="badge-live" role="status" aria-live="polite">
        <span class="badge-live__dot" aria-hidden="true"></span> Atualizado ao vivo
      </span>
    </div>

    <!-- Alternador Aluno / Coordenação -->
    <nav class="topbar__nav" aria-label="Seleção de visão">
      <div id="togglePerfil" class="role-switch" role="tablist" aria-label="Visão do painel">
        <button id="tabAluno" class="role-switch__btn active" type="button" role="tab"
                aria-selected="true" aria-controls="viewAluno" tabindex="0">Aluno</button>
        <button id="tabCoordenacao" class="role-switch__btn" type="button" role="tab"
                aria-selected="false" aria-controls="viewCoordenacao" tabindex="-1">Coordenação</button>
      </div>
    </nav>

    <div class="topbar__actions">
      <!-- O valor de cada opção é o ID do documento em lacunas_cursos (slug do nome do curso) -->
      <label for="selectCurso" class="sr-only">Selecione o curso</label>
      <select id="selectCurso" class="dropdown-input">
        <option value="tecnico-em-desenvolvimento-de-sistemas" selected>Técnico em Desenvolvimento de Sistemas</option>
        <option value="qualificacao-em-ia-generativa">Qualificação em IA Generativa</option>
        <option value="qualificacao-em-analise-de-dados">Qualificação em Análise de Dados</option>
        <option value="qualificacao-em-infraestrutura-e-nuvem">Qualificação em Infraestrutura e Nuvem</option>
      </select>

      <button id="toggleTheme" class="btn-icon" type="button" aria-label="Alternar tema claro/escuro">
        <span class="theme-icon" aria-hidden="true">🌗</span>
      </button>
    </div>
  </header>

  <div class="app-shell">
    <!-- Navegação lateral (desktop/tablet): um menu por visão -->
    <aside id="sidebarNav" class="sidebar">
      <nav id="navAluno" class="sidebar__menu" aria-label="Navegação do aluno">
        <a href="#kpiContainer" class="sidebar__link active">Visão geral</a>
        <a href="#perfilSection" class="sidebar__link">Meu perfil</a>
        <a href="#vagasSection" class="sidebar__link">Vagas compatíveis</a>
        <a href="#trilhaSection" class="sidebar__link">Trilha recomendada</a>
      </nav>
      <nav id="navCoordenacao" class="sidebar__menu" aria-label="Navegação da coordenação" hidden>
        <a href="#kpiContainer" class="sidebar__link active">Visão geral</a>
        <a href="#visualizacaoGraficos" class="sidebar__link">Gráficos analíticos</a>
        <a href="#lacunasSection" class="sidebar__link">Lacunas do curso</a>
        <a href="#matrizSection" class="sidebar__link">Matriz de competências</a>
      </nav>
    </aside>

    <main id="appMain" class="main-content">

      <!-- ===== Compartilhado: KPIs ===== -->
      <section id="kpiContainer" class="kpi-grid" aria-label="Indicadores chave">
        <article class="kpi-card" id="kpiVagas">
          <span class="kpi-card__label">Vagas Ativas Monitoradas</span>
          <strong class="kpi-card__value" data-bind="kpi.vagasAtivas">17</strong>
          <span class="kpi-card__trend neutral" data-bind="kpi.vagasAtivas.trend">de 30 coletadas · área: desenvolvimento</span>
        </article>

        <article class="kpi-card" id="kpiCobertura">
          <span class="kpi-card__label">Cobertura do Currículo</span>
          <strong class="kpi-card__value" data-bind="kpi.cobertura">48,6%</strong>
          <span class="kpi-card__trend neutral" data-bind="kpi.cobertura.trend">das competências pedidas o curso já ensina</span>
        </article>

        <article class="kpi-card" id="kpiLacunas">
          <span class="kpi-card__label">Principais Lacunas</span>
          <strong class="kpi-card__value kpi-card__value--text" data-bind="kpi.lacunas">TypeScript, Firebase</strong>
          <span class="kpi-card__trend negative" data-bind="kpi.lacunas.trend">pedidas em 4 e 3 de 17 vagas</span>
        </article>

        <article class="kpi-card" id="kpiSalario">
          <span class="kpi-card__label">Salário Mediano</span>
          <strong class="kpi-card__value" data-bind="kpi.salario">R$ 5.250</strong>
          <span class="kpi-card__trend neutral" data-bind="kpi.salario.trend">ponto médio das faixas · 16 vagas com faixa</span>
        </article>
      </section>

      <!-- ===== Compartilhado: IA Insights ===== -->
      <section id="iaInsights" class="insights-section" aria-label="Insights da inteligência artificial" aria-live="polite">
        <article class="insight-card">
          <div class="insight-card__header">
            <span class="insight-card__icon" aria-hidden="true">💡</span>
            <span class="badge-ai">Gerado por IA</span>
          </div>
          <h2 class="insight-card__title">TypeScript é a maior lacuna da área</h2>
          <p class="insight-card__body">
            TypeScript aparece em 4 de 17 vagas de desenvolvimento e não é ensinado em nenhum módulo da base.
            Os 3 módulos da trilha sugerida elevam a aderência média de 68,1% para 76,4%.
          </p>
        </article>
      </section>

      <!-- ================= VISÃO DO ALUNO ================= -->
      <div id="viewAluno" class="view" role="tabpanel" aria-labelledby="tabAluno">

        <!-- Perfil anônimo: grava só curso, nível e áreas (coleção interesses_alunos) -->
        <section id="perfilSection" class="section-container" aria-labelledby="tituloPerfil">
          <header class="section-container__header">
            <h2 id="tituloPerfil" class="section-container__title">Meu perfil (anônimo)</h2>
          </header>
          <form id="formPerfil" class="profile-form" novalidate>
            <div class="form-field">
              <label for="perfilNivel">Nível atual</label>
              <select id="perfilNivel" class="dropdown-input">
                <option value="basico">Básico</option>
                <option value="intermediario">Intermediário</option>
                <option value="avancado">Avançado</option>
              </select>
            </div>
            <fieldset class="form-field fieldset-chips">
              <legend>Áreas de interesse</legend>
              <label class="chip-option"><input type="checkbox" name="areas" value="desenvolvimento" checked> Desenvolvimento</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="dados"> Dados</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="infraestrutura"> Infraestrutura</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="ia"> IA</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="design"> Design</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="seguranca"> Segurança</label>
              <label class="chip-option"><input type="checkbox" name="areas" value="gestao"> Gestão</label>
            </fieldset>
            <p class="form-hint">O curso vem do seletor no topo. Nenhum dado pessoal é coletado: só curso, nível e áreas.</p>
            <button type="submit" class="btn-primary">Atualizar recomendações</button>
            <p id="perfilStatus" class="form-status" role="status"></p>
          </form>
        </section>

        <!-- Vagas compatíveis, ordenadas por aderência -->
        <section id="vagasSection" class="section-container" aria-labelledby="tituloVagas">
          <header class="section-container__header">
            <h2 id="tituloVagas" class="section-container__title">Vagas Compatíveis</h2>
            <div id="filtroVagas" class="filters-bar">
              <input type="search" id="inputBuscaVaga" class="filter-input"
                     placeholder="Buscar tecnologia ou cargo..." aria-label="Filtrar vagas por texto">
              <select id="filtroArea" class="filter-select" aria-label="Filtrar por área">
                <option value="todas">Todas as áreas</option>
                <option value="desenvolvimento">Desenvolvimento</option>
                <option value="dados">Dados</option>
                <option value="infraestrutura">Infraestrutura</option>
                <option value="ia">IA</option>
                <option value="design">Design</option>
                <option value="seguranca">Segurança</option>
                <option value="gestao">Gestão</option>
              </select>
              <select id="filtroSalario" class="filter-select" aria-label="Filtrar por faixa salarial">
                <option value="todas">Qualquer faixa</option>
                <option value="ate-3000">Até R$ 3.000</option>
                <option value="3000-6000">R$ 3.000 a R$ 6.000</option>
                <option value="acima-6000">Acima de R$ 6.000</option>
              </select>
            </div>
          </header>

          <div id="listaVagas" class="cards-list">
            <!-- Card de vaga (exemplo real: V001, aderência 71,4% para o curso TDS) -->
            <article class="vaga-card" data-vaga-id="V001">
              <div class="vaga-card__main">
                <h3 class="vaga-card__role">Desenvolvedor Full Stack Júnior</h3>
                <p class="vaga-card__meta">Empresa Demo 01 • Ourinhos • R$ 3.500 – R$ 5.000</p>
                <div class="vaga-card__tags">
                  <span class="chip-skill chip-skill--ok"><span class="chip-skill__icon" aria-hidden="true">✓</span> Node.js (Dominada)</span>
                  <span class="chip-skill chip-skill--ok"><span class="chip-skill__icon" aria-hidden="true">✓</span> APIs REST (Dominada)</span>
                  <span class="chip-skill chip-skill--ok"><span class="chip-skill__icon" aria-hidden="true">✓</span> SQL (Dominada)</span>
                  <span class="chip-skill chip-skill--ok"><span class="chip-skill__icon" aria-hidden="true">✓</span> Git (Dominada)</span>
                  <span class="chip-skill chip-skill--ok"><span class="chip-skill__icon" aria-hidden="true">✓</span> Docker (Dominada)</span>
                  <span class="chip-skill chip-skill--gap"><span class="chip-skill__icon" aria-hidden="true">!</span> React (Lacuna)</span>
                  <span class="chip-skill chip-skill--gap"><span class="chip-skill__icon" aria-hidden="true">!</span> TypeScript (Lacuna)</span>
                </div>
              </div>
              <div class="vaga-card__side">
                <span class="match-score match-score--mid" aria-label="71 por cento de aderência">71% Match</span>
                <a href="#" class="btn-action" target="_blank" rel="noopener noreferrer">Acessar vaga</a>
              </div>
            </article>
          </div>
          <div id="estadoVazioVagas" class="state-empty" hidden>
            Nenhuma vaga encontrada com esses filtros. Tente ampliar a busca.
          </div>
        </section>

        <!-- Aderência do aluno às vagas (top 5) -->
        <section id="aderenciaSection" class="chart-card chart-card--wide" aria-labelledby="tituloAderencia">
          <header class="chart-card__header">
            <h2 id="tituloAderencia" class="chart-card__title">Aderência às vagas mais compatíveis</h2>
          </header>
          <div id="aderenciaChart" class="chart-container" role="region"
               aria-label="Gráfico de barras com a aderência do curso às cinco vagas mais compatíveis"></div>
          <details class="sr-data-table">
            <summary>Ver dados da aderência em formato de tabela</summary>
            <table>
              <thead><tr><th>Vaga</th><th>Aderência</th></tr></thead>
              <tbody id="tbodyAderencia">
                <tr><td>V003 · Estagiário de Desenvolvimento</td><td>100,0%</td></tr>
                <tr><td>V011 · Desenvolvedor PHP Júnior</td><td>85,7%</td></tr>
                <tr><td>V027 · Desenvolvedor React Native</td><td>83,3%</td></tr>
                <tr><td>V008 · Desenvolvedor Mobile Flutter</td><td>80,0%</td></tr>
                <tr><td>V019 · Técnico em Desenvolvimento de Sistemas</td><td>80,0%</td></tr>
              </tbody>
            </table>
          </details>
        </section>

        <!-- Trilha de aprendizado: só módulos que existem em data/competencias_cursos.csv -->
        <section id="trilhaSection" class="section-container" aria-labelledby="tituloTrilha">
          <h2 id="tituloTrilha" class="section-container__title">Trilha Recomendada para Suprir Lacunas</h2>
          <ol id="trilhaAprendizado" class="timeline">
            <li class="timeline-step">
              <div class="timeline-step__marker" aria-hidden="true">1</div>
              <div class="timeline-step__content">
                <h3 class="timeline-step__title">Banco Realtime NoSQL</h3>
                <p class="timeline-step__desc">Carga horária: 12h • Cobre Firebase (3 vagas) e Banco de Dados NoSQL (2 vagas).</p>
                <span class="badge-status badge-status--priority">Alta prioridade</span>
              </div>
            </li>
            <li class="timeline-step">
              <div class="timeline-step__marker" aria-hidden="true">2</div>
              <div class="timeline-step__content">
                <h3 class="timeline-step__title">CI/CD e Deploy em Nuvem</h3>
                <p class="timeline-step__desc">Carga horária: 12h • Cobre CI/CD (2 vagas).</p>
                <span class="badge-status badge-status--medium">Média prioridade</span>
              </div>
            </li>
            <li class="timeline-step">
              <div class="timeline-step__marker" aria-hidden="true">3</div>
              <div class="timeline-step__content">
                <h3 class="timeline-step__title">Multi-agentes e Gemini API</h3>
                <p class="timeline-step__desc">Carga horária: 16h • Cobre Python (2 vagas).</p>
                <span class="badge-status badge-status--medium">Média prioridade</span>
              </div>
            </li>
          </ol>
          <p id="trilhaResumo" class="form-hint">Aderência média estimada: 68,1% → 76,4% ao concluir os 3 módulos (cálculo feito no backend).</p>
        </section>
      </div>

      <!-- ================= VISÃO DA COORDENAÇÃO ================= -->
      <div id="viewCoordenacao" class="view" role="tabpanel" aria-labelledby="tabCoordenacao" hidden>

        <section id="visualizacaoGraficos" class="charts-grid" aria-label="Visualizações gráficas">
          <article class="chart-card">
            <header class="chart-card__header">
              <h2 class="chart-card__title">Radar de Alinhamento: Curso vs. Mercado</h2>
            </header>
            <div id="radarChart" class="chart-container" role="region"
                 aria-label="Gráfico de radar comparando o que o curso ensina e o que o mercado pede"></div>
            <details class="sr-data-table">
              <summary>Ver dados do radar em formato de tabela</summary>
              <table>
                <thead><tr><th>Competência</th><th>Ensinado no curso</th><th>% das vagas que pedem</th></tr></thead>
                <tbody id="tbodyRadar">
                  <tr><td>APIs REST</td><td>52,9%</td><td>52,9%</td></tr>
                  <tr><td>Git</td><td>47,1%</td><td>47,1%</td></tr>
                  <tr><td>SQL</td><td>47,1%</td><td>47,1%</td></tr>
                  <tr><td>TypeScript</td><td>0%</td><td>23,5%</td></tr>
                  <tr><td>Firebase</td><td>0%</td><td>17,6%</td></tr>
                  <tr><td>Inglês Técnico</td><td>0%</td><td>17,6%</td></tr>
                </tbody>
              </table>
            </details>
          </article>

          <article class="chart-card">
            <header class="chart-card__header">
              <h2 class="chart-card__title">Tecnologias Mais Demandadas</h2>
            </header>
            <div id="topTecnologiasChart" class="chart-container" role="region"
                 aria-label="Gráfico de barras horizontais com as tecnologias mais pedidas nas vagas"></div>
            <details class="sr-data-table">
              <summary>Ver dados das tecnologias em formato de tabela</summary>
              <table>
                <thead><tr><th>Competência</th><th>% das vagas</th><th>Situação</th></tr></thead>
                <tbody id="tbodyTopTecnologias"></tbody>
              </table>
            </details>
          </article>

          <article class="chart-card">
            <header class="chart-card__header">
              <h2 class="chart-card__title">Faixa Salarial por Área</h2>
            </header>
            <div id="salarioChart" class="chart-container" role="region"
                 aria-label="Gráfico de caixas com a distribuição salarial por área"></div>
            <details class="sr-data-table">
              <summary>Ver dados salariais em formato de tabela</summary>
              <table>
                <thead><tr><th>Área</th><th>Vagas com faixa</th><th>Mediana (R$)</th></tr></thead>
                <tbody id="tbodySalario"></tbody>
              </table>
            </details>
          </article>

          <article class="chart-card">
            <header class="chart-card__header">
              <h2 class="chart-card__title">Evolução de Vagas por Semana</h2>
            </header>
            <div id="vagasSemanaChart" class="chart-container" role="region"
                 aria-label="Gráfico de linha com o número de vagas coletadas por semana"></div>
            <details class="sr-data-table">
              <summary>Ver dados semanais em formato de tabela</summary>
              <table>
                <thead><tr><th>Semana</th><th>Vagas</th></tr></thead>
                <tbody id="tbodyVagasSemana"></tbody>
              </table>
            </details>
          </article>
        </section>

        <section id="lacunasSection" class="section-container" aria-labelledby="tituloLacunas">
          <header class="section-container__header">
            <h2 id="tituloLacunas" class="section-container__title">Lacunas do Curso</h2>
            <button id="btnRelatorio" class="btn-primary" type="button">Gerar relatório (imprimir)</button>
          </header>
          <div class="table-wrap">
            <table id="tabelaLacunas" class="table-lacunas">
              <caption class="sr-only">Competências pedidas nas vagas e não ensinadas no curso</caption>
              <thead>
                <tr><th scope="col">Competência</th><th scope="col">Área</th><th scope="col" class="num">Vagas</th><th scope="col" class="num">% das vagas</th></tr>
              </thead>
              <tbody>
                <tr><td>TypeScript</td><td>desenvolvimento</td><td class="num">4</td><td class="num">23,5%</td></tr>
                <tr><td>Firebase</td><td>desenvolvimento</td><td class="num">3</td><td class="num">17,6%</td></tr>
                <tr><td>Inglês Técnico</td><td>geral</td><td class="num">3</td><td class="num">17,6%</td></tr>
                <tr><td>Microsserviços</td><td>desenvolvimento</td><td class="num">3</td><td class="num">17,6%</td></tr>
                <tr><td>React</td><td>desenvolvimento</td><td class="num">3</td><td class="num">17,6%</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section id="matrizSection" class="chart-card chart-card--wide" aria-labelledby="tituloMatriz">
          <header class="chart-card__header">
            <h2 id="tituloMatriz" class="chart-card__title">Matriz de Competências por Módulo</h2>
          </header>
          <div id="matrizCompetencias" class="chart-container chart-container--tall" role="region"
               aria-label="Mapa de calor que mostra quais módulos ensinam cada competência demandada"></div>
        </section>
      </div>

      <!-- ===== Compartilhado: transparência sobre a amostra ===== -->
      <p id="amostraInfo" class="status-bar" role="status">
        Última coleta: 23/10/2026 · Amostra: 17 vagas na área do curso (30 coletadas) · Dados de demonstração
      </p>
    </main>
  </div>

  <!-- Navegação inferior (mobile). Os destinos mudam conforme a visão ativa (veja a tabela abaixo) -->
  <nav id="bottomNav" class="bottom-nav" aria-label="Navegação móvel">
    <button class="bottom-nav__item active" type="button" data-alvo-aluno="kpiContainer" data-alvo-coordenacao="kpiContainer">
      <span class="bottom-nav__icon" aria-hidden="true">📊</span><span class="bottom-nav__label">Painel</span>
    </button>
    <button class="bottom-nav__item" type="button" data-alvo-aluno="vagasSection" data-alvo-coordenacao="visualizacaoGraficos">
      <span class="bottom-nav__icon" aria-hidden="true">💼</span><span class="bottom-nav__label">Vagas</span>
    </button>
    <button class="bottom-nav__item" type="button" data-alvo-aluno="trilhaSection" data-alvo-coordenacao="lacunasSection">
      <span class="bottom-nav__icon" aria-hidden="true">🗺️</span><span class="bottom-nav__label">Trilha</span>
    </button>
    <button class="bottom-nav__item" type="button" data-alvo-aluno="perfilSection" data-alvo-coordenacao="matrizSection">
      <span class="bottom-nav__icon" aria-hidden="true">👤</span><span class="bottom-nav__label">Perfil</span>
    </button>
  </nav>
</body>
</html>
```

**Destinos da navegação inferior (mobile):**

| Botão | Visão Aluno | Visão Coordenação |
|---|---|---|
| 1º (📊) | `#kpiContainer` | `#kpiContainer` |
| 2º (💼) | `#vagasSection` | `#visualizacaoGraficos` |
| 3º (🗺️) | `#trilhaSection` | `#lacunasSection` |
| 4º (👤) | `#perfilSection` | `#matrizSection` |

Na visão da coordenação os rótulos visíveis dos botões 2, 3 e 4 passam a **Gráficos**, **Lacunas** e **Matriz** (troca feita por JavaScript junto com os destinos).

---

## 6. Estilo CSS3 Modular e Moderno

```css
/* Resets e Configuração de Caixa */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body.app-body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.5;
  transition: background-color var(--transition-normal), color var(--transition-normal);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Tipografia Estrutural */
h1, h2, h3, .kpi-card__value, .match-score {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.kpi-card__value, .match-score, table td {
  font-variant-numeric: tabular-nums;
}

/* Topbar */
.topbar {
  height: 64px;
  background-color: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.topbar__brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.topbar__title {
  font-size: 20px;
  color: var(--text);
}

.badge-live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--ok);
  background-color: rgba(61, 214, 140, 0.1);
  padding: 2px 8px;
  border-radius: var(--radius-pill);
}

.badge-live__dot {
  width: 8px;
  height: 8px;
  background-color: var(--ok);
  border-radius: 50%;
  animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

/* Alternador de Perfil */
.role-switch {
  display: flex;
  background-color: var(--surface-2);
  border-radius: var(--radius-pill);
  padding: 3px;
  border: 1px solid var(--border);
}

.role-switch__btn {
  background: transparent;
  border: none;
  padding: 6px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.role-switch__btn.active {
  background-color: var(--accent);
  color: #FFFFFF;
}

/* Shell & Navegação */
.app-shell {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 240px;
  background-color: var(--surface);
  border-right: 1px solid var(--border);
  padding: 24px 16px;
  display: none;
}

.sidebar__menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar__link {
  color: var(--text-muted);
  text-decoration: none;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.sidebar__link:hover, .sidebar__link.active {
  background-color: var(--surface-hover);
  color: var(--text);
}

.sidebar__link.active {
  border-left: 3px solid var(--accent);
}

.main-content {
  flex: 1;
  padding: 24px 16px 80px 16px;
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Grade de KPIs */
.kpi-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.kpi-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-sm);
}

.kpi-card__label {
  font-size: 14px;
  color: var(--text-muted);
}

.kpi-card__value {
  font-size: 32px;
  color: var(--text);
}

.kpi-card__trend {
  font-size: 12px;
  font-weight: 500;
}

.kpi-card__trend.positive { color: var(--ok); }
.kpi-card__trend.negative { color: var(--danger); }
.kpi-card__trend.neutral { color: var(--warn); }

/* Card de IA Insights */
.insight-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.insight-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.badge-ai {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  background-color: rgba(79, 140, 255, 0.15);
  color: var(--accent);
  padding: 3px 8px;
  border-radius: var(--radius-pill);
}

.insight-card__title {
  font-size: 16px;
  margin-bottom: 6px;
}

.insight-card__body {
  font-size: 14px;
  color: var(--text-muted);
}

/* Cartões de Gráfico */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.chart-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 380px;
}

/* Chips de Competência */
.chip-skill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  border: 1px solid transparent;
}

.chip-skill--ok {
  background-color: rgba(61, 214, 140, 0.12);
  color: var(--ok);
  border-color: rgba(61, 214, 140, 0.3);
}

.chip-skill--gap {
  background-color: rgba(255, 138, 61, 0.12);
  color: var(--accent-2);
  border-color: rgba(255, 138, 61, 0.3);
}

/* Card de Vagas */
.cards-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 14px;
}

.vaga-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: transform var(--transition-fast), border-color var(--transition-fast);
}

.vaga-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.vaga-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.match-score {
  font-size: 18px;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  display: inline-block;
}

.match-score--high {
  background-color: rgba(61, 214, 140, 0.15);
  color: var(--ok);
}

/* Trilha em Timeline */
.timeline {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 16px;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 12px;
  bottom: 12px;
  left: 17px;
  width: 2px;
  background-color: var(--border);
}

.timeline-step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  position: relative;
}

.timeline-step__marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--surface-2);
  border: 2px solid var(--accent);
  color: var(--text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
  z-index: 1;
}

/* Barra de Navegação Inferior (Mobile) */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: var(--surface);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 50;
}

.bottom-nav__item {
  background: none;
  border: none;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 11px;
  gap: 2px;
  cursor: pointer;
}

.bottom-nav__item.active {
  color: var(--accent);
}

/* Skeletons de Carregamento e Estados Vazios */
.skeleton {
  background: linear-gradient(90deg, var(--surface) 25%, var(--surface-2) 50%, var(--surface) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: var(--radius-sm);
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.state-empty {
  text-align: center;
  padding: 48px 24px;
  color: var(--text-muted);
  border: 1px dashed var(--border);
  border-radius: var(--radius-md);
}

/* Breakpoint Tablet (768px a 1023px) */
@media (min-width: 768px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .vaga-card {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

/* Breakpoint Desktop (≥ 1024px) */
@media (min-width: 1024px) {
  .sidebar {
    display: block;
  }

  .bottom-nav {
    display: none;
  }

  .main-content {
    padding-bottom: 24px;
  }

  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .charts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Suporte à Impressão (Geração de Relatórios da Coordenação) */
@media print {
  body.app-body {
    background-color: #FFFFFF !important;
    color: #18213A !important;
  }

  .topbar, .sidebar, .bottom-nav, .btn-action, #filtroVagas {
    display: none !important;
  }

  .chart-card, .kpi-card, .vaga-card {
    border: 1px solid #D5DBEA !important;
    box-shadow: none !important;
    break-inside: avoid;
  }
}
```

### 6.1 Complemento de Estilos (classes usadas no HTML da seção 5)

Este bloco **soma** ao CSS acima. Ele define as classes que o HTML usa e que o CSS base não cobria, e adiciona os componentes novos (formulário de perfil, tabela de lacunas, barra de status, estado de erro). Cores translúcidas usam `color-mix` sobre os tokens, assim funcionam nos dois temas.

```css
/* ---------- Utilitários e acessibilidade ---------- */
[hidden] { display: none !important; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.skip-link {
  position: absolute;
  left: 8px;
  top: -48px;
  z-index: 100;
  padding: 8px 14px;
  background-color: var(--accent);
  color: #FFFFFF;
  border-radius: var(--radius-sm);
}

.skip-link:focus { top: 8px; }

/* ---------- Topo ---------- */
.topbar { gap: 12px; }

.topbar__nav {
  display: flex;
  flex: 1;
  justify-content: center;
}

.topbar__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.topbar__icon { font-size: 20px; }
.theme-icon { font-size: 18px; line-height: 1; }

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background-color: var(--surface-2);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.btn-icon:hover { background-color: var(--surface-hover); }

/* ---------- Campos de formulário ---------- */
.dropdown-input,
.filter-select,
.filter-input,
.profile-form select {
  background-color: var(--surface-2);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 8px 12px;
  font: inherit;
  font-size: 14px;
  min-height: 38px;
  max-width: 100%;
}

.filters-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-input { min-width: 220px; }

.profile-form {
  display: grid;
  gap: 16px;
  margin-top: 14px;
  max-width: 640px;
}

.form-field { display: grid; gap: 6px; border: 0; padding: 0; }
.form-field label, .form-field legend { font-size: 14px; font-weight: 500; }

.fieldset-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.fieldset-chips legend { width: 100%; margin-bottom: 4px; }

.chip-option {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background-color: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  font-size: 13px;
  cursor: pointer;
}

.chip-option:has(input:checked) {
  border-color: var(--accent);
  background-color: color-mix(in srgb, var(--accent) 15%, transparent);
}

.form-hint { font-size: 12px; color: var(--text-muted); }
.form-status { font-size: 13px; min-height: 1.2em; color: var(--ok); }

.btn-primary,
.btn-action {
  display: inline-block;
  padding: 9px 16px;
  font: inherit;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: filter var(--transition-fast), background-color var(--transition-fast);
}

.btn-primary {
  background-color: var(--accent);
  color: #FFFFFF;
  border: 1px solid var(--accent);
}

.btn-primary:hover { filter: brightness(1.1); }

.btn-action {
  background-color: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
}

.btn-action:hover { background-color: color-mix(in srgb, var(--accent) 12%, transparent); }

/* ---------- Seções e cartões ---------- */
.view { display: flex; flex-direction: column; gap: 28px; }

.section-container {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
}

.section-container__header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.section-container__title { font-size: 20px; }

.insights-section { display: grid; gap: 12px; }
.insight-card__icon { font-size: 18px; }

.chart-card__header { margin-bottom: 12px; }
.chart-card__title { font-size: 16px; }
.chart-card--wide { grid-column: 1 / -1; }
.chart-container--tall { height: 460px; }

.kpi-card__value--text { font-size: 22px; line-height: 1.3; overflow-wrap: anywhere; }

.status-bar { font-size: 12px; color: var(--text-muted); text-align: center; }

.state-error {
  padding: 24px;
  color: var(--danger);
  border: 1px solid var(--danger);
  border-radius: var(--radius-md);
  text-align: center;
}

/* ---------- Tabela alternativa dos gráficos e tabela de lacunas ---------- */
.sr-data-table { margin-top: 12px; font-size: 13px; color: var(--text-muted); }
.sr-data-table summary { cursor: pointer; }
.sr-data-table table,
.table-lacunas { width: 100%; border-collapse: collapse; margin-top: 8px; }

.sr-data-table th, .sr-data-table td,
.table-lacunas th, .table-lacunas td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  font-variant-numeric: tabular-nums;
}

.table-lacunas th { font-size: 12px; color: var(--text-muted); font-weight: 500; }
.table-lacunas .num { text-align: right; }
.table-wrap { overflow-x: auto; margin-top: 12px; max-width: 100%; }

/* ---------- Vagas ---------- */
.vaga-card__main { min-width: 0; }
.vaga-card__role { font-size: 16px; }
.vaga-card__meta { font-size: 13px; color: var(--text-muted); margin-top: 2px; }
.vaga-card__side { display: flex; flex-direction: column; align-items: flex-start; gap: 10px; }

.chip-skill__icon { font-weight: 700; }

.chip-skill--partial {
  background-color: color-mix(in srgb, var(--warn) 14%, transparent);
  color: var(--warn);
  border-color: color-mix(in srgb, var(--warn) 35%, transparent);
}

/* Aderência: alta >= 80, média 50-79, baixa < 50 */
.match-score--mid {
  background-color: color-mix(in srgb, var(--warn) 16%, transparent);
  color: var(--warn);
}

.match-score--low {
  background-color: color-mix(in srgb, var(--danger) 16%, transparent);
  color: var(--danger);
}

/* ---------- Trilha ---------- */
.timeline-step__content { display: grid; gap: 4px; min-width: 0; }
.timeline-step__title { font-size: 16px; }
.timeline-step__desc { font-size: 14px; color: var(--text-muted); }

.badge-status {
  justify-self: start;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
}

.badge-status--priority {
  background-color: color-mix(in srgb, var(--danger) 15%, transparent);
  color: var(--danger);
}

.badge-status--medium {
  background-color: color-mix(in srgb, var(--warn) 15%, transparent);
  color: var(--warn);
}

/* ---------- Navegação inferior ---------- */
.bottom-nav__icon { font-size: 18px; line-height: 1; }
.bottom-nav__label { font-size: 11px; }

/* ---------- Ajustes de breakpoint ---------- */
@media (max-width: 767px) {
  .topbar { height: auto; min-height: 64px; flex-wrap: wrap; padding: 8px 16px; }
  .topbar__nav { order: 3; flex-basis: 100%; }
  .badge-live { display: none; }
  .chart-container { height: 320px; }
  .filter-input { min-width: 0; width: 100%; }
}

@media (min-width: 768px) {
  .vaga-card__side { align-items: flex-end; }
}

@media (min-width: 1024px) {
  .chart-card--wide { grid-column: 1 / -1; }
}

@media print {
  .view[hidden] { display: none !important; }
  #formPerfil, #perfilSection, #btnRelatorio, #sidebarNav { display: none !important; }
}
```

---

## 7. JavaScript da Interface e Integração com Plotly.js

Os módulos abaixo ficam em `docs/js/`. O Firebase só entra na seção 10 (contrato de dados); aqui as funções recebem **objetos simples**, para funcionar tanto com os dados de exemplo (protótipo) quanto com o que vier do `onSnapshot`.

### 7.1 Tema claro/escuro (`theme.js`)

O script `theme-init.js` (seção 2.3) define o tema antes da primeira pintura. O módulo abaixo faz a **troca** e avisa os gráficos por evento. Sem o evento `themeChanged`, os gráficos continuariam com as cores do tema anterior.

```javascript
const CHAVE_TEMA = "skillradar-theme";

export function aplicarTema(tema) {
  document.documentElement.setAttribute("data-theme", tema);
  try {
    localStorage.setItem(CHAVE_TEMA, tema);
  } catch (e) {
    /* modo privado ou armazenamento bloqueado: segue sem persistir */
  }
  window.dispatchEvent(new CustomEvent("themeChanged", { detail: { tema } }));
}

export function alternarTema() {
  const atual = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  aplicarTema(atual === "dark" ? "light" : "dark");
}

document.getElementById("toggleTheme")?.addEventListener("click", alternarTema);
```

### 7.2 Troca de visão Aluno / Coordenação (`views.js`)

O Plotly mede `0px` em contêineres escondidos. Por isso, ao mostrar a visão, é preciso mandar os gráficos recalcularem o tamanho.

```javascript
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
    aba.classList.toggle("active", ativa);
    aba.setAttribute("aria-selected", String(ativa));
    aba.tabIndex = ativa ? 0 : -1;
    document.getElementById(v.painel).hidden = !ativa;
    document.getElementById(v.nav).hidden = !ativa;
  }

  // Navegação inferior: troca rótulos e destinos conforme a visão
  document.querySelectorAll("#bottomNav .bottom-nav__item").forEach((botao, i) => {
    botao.dataset.alvo = botao.dataset[nome === "aluno" ? "alvoAluno" : "alvoCoordenacao"];
    botao.querySelector(".bottom-nav__label").textContent = ROTULOS_BOTTOM[nome][i];
  });

  // Gráficos que acabaram de ficar visíveis precisam se redimensionar
  requestAnimationFrame(() => {
    document
      .querySelectorAll(`#${VISOES[nome].painel} .chart-container`)
      .forEach((el) => window.Plotly?.Plots.resize(el));
  });
}

// Setas do teclado entre as abas (padrão WAI-ARIA para tablist)
document.getElementById("togglePerfil")?.addEventListener("keydown", (e) => {
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const proxima = document.getElementById("tabAluno").getAttribute("aria-selected") === "true" ? "coordenacao" : "aluno";
  mostrarVisao(proxima);
  document.getElementById(VISOES[proxima].aba).focus();
});

document.getElementById("tabAluno")?.addEventListener("click", () => mostrarVisao("aluno"));
document.getElementById("tabCoordenacao")?.addEventListener("click", () => mostrarVisao("coordenacao"));

document.getElementById("bottomNav")?.addEventListener("click", (e) => {
  const alvo = e.target.closest(".bottom-nav__item")?.dataset.alvo;
  if (alvo) document.getElementById(alvo)?.scrollIntoView({ behavior: "smooth" });
});

/** Estado inicial: a visão do aluno é a primeira exibida */
mostrarVisao("aluno");

document.getElementById("btnRelatorio")?.addEventListener("click", () => window.print());
```

### 7.3 Utilitários do Plotly (`charts.js`)

```javascript
const CONFIG_PLOTLY = { responsive: true, displayModeBar: false };

/** Lê os tokens CSS do tema ativo */
export function getPlotlyThemeTokens() {
  const css = getComputedStyle(document.documentElement);
  const ler = (nome) => css.getPropertyValue(nome).trim();
  return {
    text: ler("--text"),
    textMuted: ler("--text-muted"),
    border: ler("--border"),
    surface2: ler("--surface-2"),
    curso: ler("--accent"),     // azul: o que o curso ensina
    mercado: ler("--accent-2"), // laranja: o que o mercado pede
    ok: ler("--ok"),
    warn: ler("--warn"),
    danger: ler("--danger"),
  };
}

/** '#4F8CFF' + 0.25 -> 'rgba(79,140,255,0.25)' (para preenchimentos que acompanham o tema) */
function comAlpha(hex, alpha) {
  const h = hex.replace("#", "");
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
  return `rgba(${r},${g},${b},${alpha})`;
}

const pct = (n) => `${n.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

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
```

### 7.4 Gráficos

Cada função recebe um objeto de dados com o formato indicado no comentário. Use `Plotly.react`, que atualiza o gráfico existente sem recriá-lo (ideal para `onSnapshot`).

```javascript
/**
 * Radar Curso x Mercado.
 * Eixos = as 3 competências mais pedidas que o curso ensina + as 3 maiores lacunas.
 * mercado[i] = % das vagas que pedem a competência; curso[i] = o mesmo valor se o curso ensina, senão 0.
 * dados = { eixos: ["APIs REST", ...], mercado: [52.9, ...], curso: [52.9, ..., 0] }
 */
export function renderRadar(dados) {
  const t = getPlotlyThemeTokens();
  const teto = Math.ceil((Math.max(...dados.mercado) + 5) / 10) * 10;
  const fechar = (arr) => [...arr, arr[0]];
  const eixos = fechar(dados.eixos);
  Plotly.react("radarChart", [
    {
      type: "scatterpolar", name: "Ensinado no curso", theta: eixos, r: fechar(dados.curso),
      fill: "toself", line: { color: t.curso, width: 2 }, fillcolor: comAlpha(t.curso, 0.25),
      hovertemplate: "%{theta}: %{r:.1f}%<extra>Curso</extra>",
    },
    {
      type: "scatterpolar", name: "Pedido pelo mercado", theta: eixos, r: fechar(dados.mercado),
      fill: "toself", line: { color: t.mercado, width: 2 }, fillcolor: comAlpha(t.mercado, 0.25),
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
}

/**
 * Barras horizontais: competências mais demandadas (azul = o curso ensina, laranja = lacuna).
 * dados = { competencias: ["SQL", ...], pct: [47.1, ...], cobertas: [true, ...] }
 */
export function renderTopTecnologias(dados) {
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
}

/**
 * Box plot da faixa salarial por área (ponto médio da faixa de cada vaga).
 * dados = { desenvolvimento: [4250, 5500, ...], dados: [...], infraestrutura: [...] }
 */
export function renderSalarioPorArea(dados) {
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
}

/**
 * Linha: vagas coletadas por semana.
 * dados = { semanas: ["2026-W38", ...], total: [1, 3, 4, 4, 2, 3] }
 */
export function renderVagasPorSemana(dados) {
  const t = getPlotlyThemeTokens();
  Plotly.react("vagasSemanaChart", [{
    type: "scatter", mode: "lines+markers", x: dados.semanas, y: dados.total,
    line: { color: t.mercado, width: 3, shape: "spline" }, marker: { size: 8, color: t.mercado },
    hovertemplate: "%{x}: %{y} vagas<extra></extra>",
  }], layoutBase(t, {
    yaxis: { gridcolor: t.border, color: t.textMuted, rangemode: "tozero", dtick: 1 },
  }), CONFIG_PLOTLY);
}

/**
 * Heatmap módulo x competência demandada (✓ = o módulo ensina a competência).
 * Colunas ordenadas da competência mais pedida para a menos pedida.
 * dados = { competencias: ["SQL", ...], linhas: [ { modulo: "Banco de Dados Relacional", valores: [1, 0, ...] }, ... ] }
 * (O Firestore não aceita arrays dentro de arrays; por isso `linhas`, e não uma matriz `z`.)
 */
export function renderMatriz(dados) {
  const t = getPlotlyThemeTokens();
  const modulos = dados.linhas.map((l) => l.modulo);
  const z = dados.linhas.map((l) => l.valores);
  Plotly.react("matrizCompetencias", [{
    type: "heatmap", x: dados.competencias, y: modulos, z,
    colorscale: [[0, t.surface2], [1, t.curso]], showscale: false, xgap: 2, ygap: 2,
    text: z.map((linha) => linha.map((v) => (v ? "✓" : ""))), texttemplate: "%{text}",
    hovertemplate: "%{y} → %{x}: %{text}<extra></extra>",
  }], layoutBase(t, {
    margin: { t: 16, r: 16, b: 110, l: 220 },
    xaxis: { tickangle: -40, color: t.text, side: "bottom" },
    yaxis: { autorange: "reversed", color: t.text },
  }), CONFIG_PLOTLY);
}

/**
 * Barras de aderência do aluno às vagas (cores por faixa: alta, média, baixa).
 * dados = { vagas: ["V003 · Estagiário de Desenvolvimento", ...], pct: [100, 85.7, ...] }
 */
export function renderAderencia(dados) {
  const t = getPlotlyThemeTokens();
  Plotly.react("aderenciaChart", [{
    type: "bar", orientation: "h", y: dados.vagas, x: dados.pct,
    marker: { color: dados.pct.map((v) => corAderencia(t, v)) },
    text: dados.pct.map(pct), textposition: "outside", cliponaxis: false,
    hovertemplate: "%{y}: %{x:.1f}% de aderência<extra></extra>",
  }], layoutBase(t, {
    margin: { t: 16, r: 56, b: 40, l: 260 },
    xaxis: { range: [0, 110], gridcolor: t.border, color: t.textMuted, ticksuffix: "%" },
    yaxis: { autorange: "reversed", color: t.text },
  }), CONFIG_PLOTLY);
}
```

### 7.5 Orquestração dos gráficos e dados de exemplo

O objeto `estado` guarda os últimos dados recebidos. Quando o tema muda, os gráficos são redesenhados com as novas cores, sem nova consulta ao banco.

```javascript
const estado = { radar: null, topTec: null, salario: null, semana: null, matriz: null, aderencia: null };

const RENDERIZADORES = {
  radar: renderRadar, topTec: renderTopTecnologias, salario: renderSalarioPorArea,
  semana: renderVagasPorSemana, matriz: renderMatriz, aderencia: renderAderencia,
};

/** Chame com um pedaço do estado sempre que o Firestore enviar dados novos */
export function atualizarGrafico(nome, dados) {
  estado[nome] = dados;
  RENDERIZADORES[nome](dados);
}

window.addEventListener("themeChanged", () => {
  for (const [nome, dados] of Object.entries(estado)) {
    if (dados) RENDERIZADORES[nome](dados);
  }
});

/** Dados de exemplo (curso TDS, 17 vagas na área de desenvolvimento) para o protótipo */
export const EXEMPLO = {
  radar: {
    eixos: ["APIs REST", "Git", "SQL", "TypeScript", "Firebase", "Inglês Técnico"],
    mercado: [52.9, 47.1, 47.1, 23.5, 17.6, 17.6],
    curso: [52.9, 47.1, 47.1, 0, 0, 0],
  },
  topTec: {
    // Regra: as 10 competências mais pedidas (empate resolvido pelo nome)
    competencias: ["APIs REST", "Git", "SQL", "Docker", "Testes Automatizados", "CSS", "HTML", "Metodologias Ágeis", "TypeScript", "Firebase"],
    pct: [52.9, 47.1, 47.1, 41.2, 41.2, 29.4, 29.4, 23.5, 23.5, 17.6],
    cobertas: [true, true, true, true, true, true, true, true, false, false],
  },
  semana: { semanas: ["2026-W38", "2026-W39", "2026-W40", "2026-W41", "2026-W42", "2026-W43"], total: [1, 3, 4, 4, 2, 3] },
  aderencia: {
    vagas: [
      "V003 · Estagiário de Desenvolvimento",
      "V011 · Desenvolvedor PHP Júnior",
      "V027 · Desenvolvedor React Native",
      "V008 · Desenvolvedor Mobile Flutter",
      "V019 · Técnico em Desenvolvimento de Sistemas",
    ],
    pct: [100, 85.7, 83.3, 80, 80],
  },
};
```

---

## 8. Mapeamento de Gráficos por Perfil de Usuário

| Gráfico | Contêiner (ID) | Tipo Plotly | Visão Aluno | Visão Coordenação | Fonte dos dados (seção 10) | Finalidade |
|---|---|---|---|---|---|---|
| **Curso × Mercado** | `#radarChart` | `scatterpolar` | Não* | Sim | `lacunas_cursos/{curso}.graficos.radar` | Mostrar onde a grade e a demanda divergem (3 mais pedidas ensinadas + 3 maiores lacunas) |
| **Tecnologias Mais Demandadas** | `#topTecnologiasChart` | `bar` (horizontal) | Não | Sim | `lacunas_cursos/{curso}.graficos.top_tecnologias` | Top 10 mais pedidas e o que é lacuna |
| **Faixa Salarial por Área** | `#salarioChart` | `box` | Não | Sim | `contexto/atual.graficos.salario_por_area` | Dispersão e mediana por área |
| **Evolução de Vagas por Semana** | `#vagasSemanaChart` | `scatter` (linha) | Não | Sim | `lacunas_cursos/{curso}.graficos.vagas_semana` | Tendência de contratação |
| **Matriz Módulo × Competência** | `#matrizCompetencias` | `heatmap` | Não | Sim | `lacunas_cursos/{curso}.graficos.matriz` (`competencias` + `linhas`) | Ver se os módulos cobrem as competências pedidas |
| **Aderência às Vagas** | `#aderenciaChart` | `bar` (horizontal) | Sim | Não | `vagas_ativas` + competências do curso | Listar as vagas mais compatíveis |

\* O aluno vê a mesma informação de forma resumida nos chips das vagas e na trilha. Se a turma quiser o radar também para o aluno, basta reutilizar o mesmo `#radarChart` em `#viewAluno`.

---

## 9. Diretrizes de Acessibilidade (WCAG 2.1 AA) e Responsividade

1. **Navegação por Teclado e Anel de Foco:**
   - Todos os elementos acionáveis (`<button>`, `<a>`, `<select>`, `<input>`) contam com anel de foco bem delineado:
   ```css
   :focus-visible {
     outline: 2px solid var(--focus-ring);
     outline-offset: 2px;
   }
   ```
2. **Dupla Codificação de Informação:**
   - Nenhum status depende exclusivamente de cor. Os chips de competências unem cor com ícones textuais explicativos: `✓` para Dominada e `!` para Lacuna.
3. **Equivalentes Textuais para Gráficos:**
   - Todo contêiner de gráfico possui `role="region"`, `aria-label` e uma tabela HTML alternativa oculta ou expansível via `<details>`, permitindo que leitores de tela interpretem os dados ponto a ponto.
4. **Respeito ao `prefers-reduced-motion`:**
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```
5. **Prevenção de Rolagem Horizontal:**
   - Regra estrita de `max-width: 100%`, com contêineres e tabelas responsivas que garantem fluidez em dispositivos de `360px` a `1440px`.

6. **Abas com papel de tablist:**
   - As abas `#tabAluno` e `#tabCoordenacao` usam `role="tab"`, `aria-selected` e `aria-controls`, e cada painel (`#viewAluno`, `#viewCoordenacao`) usa `role="tabpanel"` com `aria-labelledby`. A aba ativa tem `tabindex="0"`, a outra `-1`, e as setas do teclado alternam entre elas.
7. **Mensagens dinâmicas:**
   - `#iaInsights` e `#liveIndicator` usam `aria-live="polite"`; `#perfilStatus` e `#amostraInfo` usam `role="status"`. Mensagens de erro usam `.state-error` com texto claro, nunca só cor.
8. **Formatação em português do Brasil:**
   - Números e moeda com `toLocaleString("pt-BR")` (vírgula decimal, `R$ 5.250`). Datas no formato `dd/mm/aaaa`.

---

## 10. Contrato de Dados da Interface (UI ↔ Firestore)

Esta seção liga cada elemento da tela à coleção do Firestore que o alimenta. Os nomes de coleções e campos são os definidos em `Directives/firestore/firestore.md`. **Nenhum valor numérico é escrito à mão no HTML final.**

### 10.1 Origem dos dados por elemento

| Elemento na tela | Coleção / documento | Campos usados | Regra de exibição |
|---|---|---|---|
| `[data-bind="kpi.vagasAtivas"]` e trend | `lacunas_cursos/{curso}` | `amostra_n`, `total_coletadas`, `areas_foco` | "N vagas" na área do curso; trend: "de `total_coletadas` coletadas · área: ..." |
| `[data-bind="kpi.cobertura"]` | `lacunas_cursos/{curso}` | `cobertura_pct` | `null` vira "—". Cor do trend: ≥ 70 positivo, 40–69 neutro, < 40 negativo |
| `[data-bind="kpi.lacunas"]` | `lacunas_cursos/{curso}` | `lacunas[0..1]` | Duas maiores lacunas; trend com a frequência de cada uma |
| `[data-bind="kpi.salario"]` | `lacunas_cursos/{curso}` | `kpis.salario_mediano`, `kpis.salario_n` | Valor já calculado em Python; `null` vira "—"; trend: "base: N vagas com faixa" |
| `#iaInsights` | `insights` | `titulo`, `texto`, `severidade`, `escopo` | Os 3 mais recentes do escopo da visão ativa |
| `#listaVagas` | `vagas_ativas` | todos | Ordenada por aderência ao curso; aderência calculada no front com as competências do curso |
| `#trilhaAprendizado` | `trilhas_sugeridas/{curso}` | `modulos[]` (`curso`, `modulo`, `carga_horaria`, `competencias_cobertas`, `peso`, `motivo`), `aderencia_antes_pct`, `aderencia_depois_pct` | Só módulos que existem na base. Prioridade: maior `peso` = alta |
| `#radarChart`, `#topTecnologiasChart`, `#matrizCompetencias`, `#vagasSemanaChart` | `lacunas_cursos/{curso}` | `graficos.radar`, `graficos.top_tecnologias`, `graficos.matriz`, `graficos.vagas_semana` | Passar cada bloco direto para `atualizarGrafico` (seção 7.5) |
| `#salarioChart` | `contexto/atual` | `graficos.salario_por_area` | `{ area: [pontos médios] }`, todas as vagas com faixa |
| `#tabelaLacunas` | `lacunas_cursos/{curso}` | `lacunas[]` | Ordenada por frequência decrescente |
| `#amostraInfo` | `contexto/atual` e `lacunas_cursos/{curso}` | `ultima_coleta`, `total_vagas`, `modo_demo`, `amostra_n` | Sempre visível. Se `modo_demo` for verdadeiro, escreve "Dados de demonstração" |
| `#liveIndicator` | estado da conexão do `onSnapshot` | — | "Atualizado ao vivo" com ponto verde; se o listener falhar: "Sem conexão" em tom de aviso |

### 10.2 Interações

- **`#selectCurso`:** o valor da opção é o ID do documento em `lacunas_cursos` e `trilhas_sugeridas` (slug do nome do curso). Ao trocar, os listeners são reiniciados para o novo curso.
- **`#formPerfil`:** ao enviar, grava **um documento anônimo** em `interesses_alunos` com `curso_interesse`, `nivel`, `areas[]` e `criado_em`. Nenhum outro campo é aceito pelas regras do Firestore. Mostra a confirmação em `#perfilStatus`.
- **`#filtroVagas`:** filtra no navegador a lista já carregada (texto, `area`, faixa salarial). Se nada sobrar, mostra `#estadoVazioVagas`.
- **Estados de carregamento e erro:** cada bloco começa com `.skeleton`, troca pelo conteúdo no primeiro snapshot e, se a leitura falhar, mostra `.state-error` com opção de tentar de novo.

### 10.3 Checklist de conformidade do protótipo

- [ ] As duas visões existem e alternam por aba, por teclado e no mobile.
- [ ] Todos os IDs citados no prompt original estão no HTML: `#togglePerfil`, `#filtroVagas`, `#matrizCompetencias`, `#radarChart`, `#trilhaAprendizado`, `#iaInsights`.
- [ ] Toda classe usada no HTML tem regra no CSS (seção 6 + 6.1).
- [ ] O tema alterna sem recarregar e os gráficos mudam de cor junto.
- [ ] Os cursos do seletor são os quatro cursos da base de dados.
- [ ] A frase "Dados de demonstração" aparece enquanto o app usar as vagas sintéticas.
