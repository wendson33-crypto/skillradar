# SkillRadar — Design e UI/UX

## 1. Conceito visual
Visual de **painel de inteligência de carreira**: sóbrio e legível para a coordenação, motivador para o aluno. Dark mode como padrão no painel; light mode para relatórios impressos e uso em sala. A cor de destaque remete a "radar".

## 2. Design tokens (CSS)
Definir em `:root` e sobrescrever em `[data-theme="dark"]` / `[data-theme="light"]`. O tema inicial segue `prefers-color-scheme`, com preferência salva em `localStorage` (com `try/catch`).

| Token | Dark | Light |
|---|---|---|
| `--bg` | `#0B1020` | `#F5F7FC` |
| `--surface` | `#141B30` | `#FFFFFF` |
| `--surface-2` | `#1D2742` | `#ECF0F9` |
| `--text` | `#E8ECF8` | `#18213A` |
| `--text-muted` | `#93A0C0` | `#5A6682` |
| `--accent` (radar) | `#4F8CFF` | `#2F6BE0` |
| `--accent-2` (mercado) | `#FF8A3D` | `#D9600F` |
| `--ok` | `#3DD68C` | `#1E9E5A` |
| `--warn` | `#F5B83D` | `#B07800` |
| `--danger` | `#FF5C6C` | `#C62839` |
| `--border` | `#2A3558` | `#D5DBEA` |

Convenção de cor nos gráficos: **azul = o que o curso ensina**, **laranja = o que o mercado pede**. Raio de borda 12px. Contraste mínimo AA.

## 3. Tipografia
- Títulos e KPIs: **Space Grotesk** (ou Inter) 600–700.
- Texto: Inter 400/500.
- Números com `font-variant-numeric: tabular-nums`.
- Escala: 12 / 14 / 16 / 20 / 28 / 40 px.

## 4. Layout
- Grade de 12 colunas no desktop, 4 no tablet, 1 no celular; gutter lateral de 16px.
- Topo: logo, **alternador Aluno / Coordenação** (abas), seletor de curso, alternador de tema e indicador "ao vivo".
- Navegação lateral no desktop; barra inferior no celular.

## 5. Componentes
- **KPI Card:** vagas ativas, cobertura do currículo (%), principais lacunas, salário mediano.
- **Vaga Card:** cargo, empresa, cidade, faixa salarial, selos de competências (verde = o aluno/curso cobre, laranja = lacuna), link para a fonte.
- **Chip de competência:** estados "dominada", "parcial" e "lacuna".
- **Card de IA Insight:** ícone, título curto, 1–2 frases, selo "Gerado por IA".
- **Trilha:** linha do tempo com módulos, carga horária e justificativa.
- **Gráficos Plotly:** fundo transparente, cores lidas dos tokens e reaplicadas ao trocar o tema.
- Estados vazios, skeleton de carregamento e mensagem de erro em todos os blocos.

## 6. Fluxos
**Aluno:** Perfil → Vagas compatíveis → Lacunas → Trilha.
1. **Perfil:** escolhe curso, nível e áreas de interesse (sem dados pessoais).
2. **Vagas compatíveis:** lista ordenada por aderência, com filtro por área e faixa salarial.
3. **Lacunas:** quais competências faltam para as vagas escolhidas.
4. **Trilha:** módulos sugeridos com ordem e carga horária.

**Coordenação:** Painel de lacunas → Detalhe por curso → Relatório.
1. **Painel:** cobertura por curso, top tecnologias demandadas e evolução de vagas.
2. **Detalhe por curso:** matriz módulo × competência demandada.
3. **Relatório:** versão imprimível (light mode) com lacunas e recomendações de revisão.

## 7. Gráficos (Plotly.js)
| Gráfico | Tipo | Visão |
|---|---|---|
| Curso × mercado | Radar (scatterpolar) | ambas |
| Top tecnologias demandadas | Barras horizontais | coordenação |
| Faixa salarial por área | Box plot | ambas |
| Vagas por semana | Linha | coordenação |
| Módulo × competência | Heatmap | coordenação |
| Aderência do aluno às vagas | Barras | aluno |

## 8. Cartões de IA Insights (exemplos)
- "As vagas pedem Docker, que aparece em apenas 1 módulo."
- "Trilha recomendada: 3 módulos para chegar a 80% de aderência."
- "Competência em alta nesta semana: integração com APIs."

## 9. Acessibilidade e responsividade
- Navegação por teclado, foco visível, `aria-label` e tabela alternativa para os gráficos.
- Não depender só de cor: chips com ícone e texto ("lacuna", "dominada").
- Sem rolagem horizontal; testar em 360px, 768px e 1280px.
- Respeitar `prefers-reduced-motion`.
