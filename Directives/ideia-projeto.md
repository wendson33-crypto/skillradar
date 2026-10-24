# SkillRadar — Ideia do Projeto

## 1. Resumo
**SkillRadar** é uma aplicação web que compara as competências ensinadas nos cursos de uma escola técnica com as competências exigidas nas vagas abertas na região, mostra as lacunas e sugere trilhas de qualificação para cada aluno.

**Setor:** educação profissional e empregabilidade.
**Modalidade do edital:** Opção A (tema próprio) — base RAG em `data/competencias_cursos.csv`.

## 2. Problema real
- Os currículos demoram a refletir o que o mercado local pede (ferramentas, tecnologias, certificações).
- Coordenações descobrem as lacunas tarde, por feedback informal de empresas e egressos.
- O aluno não sabe qual módulo ou curso complementar aumenta mais suas chances de contratação.

## 3. Proposta de valor
1. **Para a coordenação:** painel de lacunas entre curso e mercado, atualizado com vagas reais.
2. **Para o aluno:** vagas compatíveis, competências que faltam e trilha personalizada com módulos existentes.
3. **Para a escola:** evidência objetiva para revisar conteúdo e priorizar novos módulos.

## 4. Público-alvo
- Coordenadores e docentes de escolas técnicas.
- Alunos e egressos de cursos técnicos e de qualificação.
- Equipes de empregabilidade e relacionamento com empresas.

## 5. Escopo do MVP (hackathon)
**Dentro:**
- Duas visões: Aluno e Coordenação.
- Pipeline Python: scraping de vagas → extração de competências → matching → Firestore.
- Dashboard com gráficos Plotly.js e cartões de IA Insights.
- Dark/Light Mode e layout responsivo.
- Deploy via GitHub MCP Server no GitHub Pages.

**Fora (futuro):**
- Login institucional e dados reais de alunos.
- Candidatura direta às vagas.
- Integração com sistemas acadêmicos.

## 6. Métricas de sucesso
- Cobertura do currículo medida em % de competências demandadas já ensinadas.
- Pelo menos 3 lacunas relevantes identificadas na demonstração.
- Nova vaga raspada aparece no painel sem recarregar a página (`onSnapshot`).
- 0 credenciais no repositório público e 0 dados pessoais reais.

## 7. Dados
- **Base local (RAG):** `data/competencias_cursos.csv` com módulos e competências dos cursos (pode partir de planos de curso reais da área de TI e ser complementada com dados sintéticos). Opcional: `data/perfil_egressos.csv` (sintético e anonimizado).
- **Dados vivos:** vagas abertas na região, com cargo, requisitos, faixa salarial e tecnologias citadas.
- **Taxonomia de competências:** lista controlada (`data/taxonomia_competencias.csv`, com sinônimos) para padronizar "JS", "JavaScript" e "Java Script" como a mesma coisa.

## 8. Privacidade e ética (LGPD)
- Nenhum dado pessoal real no MVP: alunos e egressos são anônimos/sintéticos.
- O campo de interesses do aluno guarda só preferências (área, nível), sem nome, e-mail ou documento.
- Vagas são tratadas como informação pública e agregada; guardar apenas os campos necessários e o link da fonte.
- A IA recomenda trilhas de estudo, não decide contratação nem ranqueia pessoas.

## 9. Riscos e mitigação
| Risco | Mitigação |
|---|---|
| Portais bloqueiam scraping ou proíbem em seus termos | Respeitar `robots.txt` e termos de uso; priorizar fontes públicas e abertas; manter um conjunto de vagas de demonstração como plano B |
| HTML da fonte muda | Seletores isolados por fonte, com testes e fallback para o último lote válido |
| IA inventa competências | Gemini só pode escolher itens da taxonomia (saída em JSON validado); o que não bater vai para "não mapeado" |
| Poucas vagas na região | Ampliar o raio de busca e exibir o tamanho da amostra nos gráficos |
| Cota do Gemini | Processar cada vaga uma vez, com cache por hash do texto |
| Chave exposta | `.env` + `.gitignore` + front-end sem segredos |

## 10. Conformidade com os 9 pilares do edital
| # | Pilar | Como a SkillRadar atende |
|---|---|---|
| 1 | Engenharia & Diretivas | `ideia-projeto.md`, `ideia-design.md`, `projeto.md` |
| 2 | UI/UX & Design System | Tokens CSS, Dark/Light, duas visões responsivas |
| 3 | Base RAG | `data/competencias_cursos.csv` lido com pandas |
| 4 | Web Scraping | Vagas abertas da região em fontes públicas |
| 5 | Multi-Agentes & Gemini | Coletor e Matcher (Python) + Orientador (Gemini) |
| 6 | Firestore Realtime | `onSnapshot` em vagas, lacunas e trilhas |
| 7 | Governança & Segurança | `.env`, `.gitignore`, `.env.example`, regras do Firestore |
| 8 | CI/CD | GitHub MCP Server + `mcp_config.json` → GitHub Pages |
| 9 | Analytics | Plotly.js + cartões de IA Insights |
