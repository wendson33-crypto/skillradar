# SkillRadar — Projeto Técnico

## 1. Visão da arquitetura

```
┌──────────────────────── BACKEND (Python, roda local ou agendado) ────────────────────────┐
│                                                                                          │
│  scrapers/ ──► vagas brutas ──► Agente Coletor (limpeza, deduplicação)                   │
│                                        │                                                 │
│                                        ▼                                                 │
│                          Agente Extrator (Gemini): texto da vaga → competências          │
│                                        │        (somente itens da taxonomia)             │
│                                        ▼                                                 │
│  data/competencias_cursos.csv ──► Agente Matcher (pandas, determinístico)                │
│  data/taxonomia_competencias.csv         │  cobertura, lacunas, aderência                │
│                                        ▼                                                 │
│                          Agente Orientador (Gemini): insights e trilhas                  │
│                                        │                                                 │
│                                        ▼                                                 │
│                       Firebase Admin SDK (credencial no .env)                            │
└────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                         ▼
                              Cloud Firestore (NoSQL)
                                         │  onSnapshot
                                         ▼
┌──────────────────── FRONT-END ESTÁTICO (GitHub Pages, HTTPS) ────────────────────────────┐
│  HTML/CSS/JS + Firebase Web SDK + Plotly.js + Dark/Light + visões Aluno/Coordenação      │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

**Decisão-chave:** o GitHub Pages só serve arquivos estáticos. A chave do Gemini e a credencial de administrador do Firebase ficam só no backend; o front-end lê o Firestore e, no máximo, grava interesses anônimos do aluno sob regras restritas.

## 2. Estrutura de pastas

```
skillradar/
├── ideia-projeto.md
├── ideia-design.md
├── projeto.md
├── mcp_config.json            # GitHub MCP Server (token por variável de ambiente)
├── .env                       # NUNCA versionado
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── competencias_cursos.csv
│   ├── taxonomia_competencias.csv
│   ├── perfil_egressos.csv    # opcional, sintético
│   ├── vagas_demo.csv         # plano B se o scraping falhar
│   └── README.md              # dicionário de dados
├── backend/
│   ├── config.py
│   ├── scrapers/
│   │   ├── base.py            # robots.txt, user-agent, retry, timeout
│   │   └── fonte_vagas_1.py   # um módulo por fonte
│   ├── agentes/
│   │   ├── coletor.py
│   │   ├── extrator.py        # Gemini
│   │   ├── matcher.py
│   │   └── orientador.py      # Gemini
│   ├── firestore_client.py
│   └── orquestrador.py
├── docs/                      # front-end publicado no GitHub Pages
│   ├── index.html
│   ├── css/ (tokens.css, app.css)
│   └── js/ (firebase-init.js, realtime.js, charts.js, theme.js, views.js)
├── firestore.rules
└── tests/
```

## 3. `.gitignore` (mínimo obrigatório)

```
.env
.env.*
!.env.example
serviceAccount*.json
*.json.key
__pycache__/
.venv/
.DS_Store
```

## 4. `.env.example`

```
GEMINI_API_KEY=
GEMINI_MODEL=
GITHUB_TOKEN=
FIREBASE_PROJECT_ID=
GOOGLE_APPLICATION_CREDENTIALS=./caminho/local/service-account.json
REGIAO_BUSCA=
RAIO_KM=
```

> A configuração pública do Firebase Web (apiKey, projectId etc.) não é segredo de acesso; a proteção vem das regras do Firestore. A credencial de administrador deve ficar fora do repositório.

## 5. Base RAG e taxonomia

**`data/competencias_cursos.csv`**

| Coluna | Descrição |
|---|---|
| `curso` | nome do curso |
| `modulo` | módulo/unidade curricular |
| `competencia` | competência (já no vocabulário da taxonomia) |
| `carga_horaria` | horas do módulo |
| `nivel` | básico / intermediário / avançado |
| `area` | área (ex.: desenvolvimento, dados, infraestrutura) |
| `ferramenta_ensinada` | ferramenta/tecnologia associada |

**`data/taxonomia_competencias.csv`:** `competencia_padrao, sinonimos (separados por |), area`. Exemplo de linha: `JavaScript, js|java script|ecmascript, desenvolvimento`.

**`data/perfil_egressos.csv` (opcional, sintético):** `egresso_id, curso, ano, area_atuacao, empregado`.

**Uso como RAG:** o Orientador recebe do Python um resumo enxuto (lacunas calculadas, módulos candidatos do CSV com carga horária) e monta a trilha **apenas com módulos que existem no CSV**. Não se envia o arquivo inteiro.

## 6. Web scraping (dados vivos)

| Item | Detalhe |
|---|---|
| Fontes | portais públicos de emprego e de vagas da região; confirmar quais permitem coleta |
| Campos | título, empresa, cidade, data, requisitos (texto), faixa salarial (quando houver), URL |
| Frequência | 1–4 vezes ao dia, com intervalo entre requisições |
| Conformidade | ler `robots.txt`, respeitar termos de uso, `User-Agent` identificado, sem contornar bloqueios ou login |
| Fallback | último lote válido no Firestore e `vagas_demo.csv` |
| Deduplicação | hash de (título + empresa + cidade) |

Se uma fonte não permitir coleta, trocar de fonte. Não use CAPTCHA bypass ou proxies para driblar bloqueios.

## 7. Multi-agentes

| Agente | Tipo | Entrada | Saída |
|---|---|---|---|
| **Coletor** | Python | páginas das fontes | vagas limpas e deduplicadas |
| **Extrator** | Gemini | texto da vaga + taxonomia | JSON com competências padronizadas e itens "não mapeados" |
| **Matcher** | Python (pandas) | competências das vagas × CSV dos cursos | cobertura %, lacunas ordenadas por frequência, aderência por vaga |
| **Orientador** | Gemini | lacunas calculadas + módulos candidatos | JSON com insights e trilha |

**Regra de ouro:** contagens, percentuais e cobertura saem do Python. O Gemini extrai e redige, sempre com saída validada.

**Contrato do Extrator:**
```json
{
  "vaga_id": "",
  "competencias": ["JavaScript", "Docker"],
  "nao_mapeadas": ["termo livre"],
  "senioridade": "estagio|junior|pleno|senior|nao_informado"
}
```

**Contrato do Orientador:**
```json
{
  "insights": [{"titulo": "", "texto": "", "severidade": "info|aviso|critico"}],
  "trilha": [{"modulo": "", "curso": "", "carga_horaria": 0, "motivo": ""}],
  "aderencia_estimada_pos_trilha": 0
}
```
O orquestrador valida os dois contratos (schema). Se a resposta for inválida, tenta uma vez de novo; se falhar, grava só os resultados determinísticos do Matcher. O campo `aderencia_estimada_pos_trilha` deve ser recalculado pelo Python, não confiado ao modelo.

## 8. Firestore — esquema

```
vagas_ativas/{vagaId}
  titulo, empresa, cidade, data, salario_min, salario_max, fonte_url,
  competencias[], senioridade, coletado_em

competencias_demandadas/{competencia}      # agregado
  frequencia, variacao_semana, area, coberta_pelo_curso (bool)

lacunas_cursos/{cursoId}
  cobertura_pct, lacunas[{competencia, frequencia}], atualizado_em

insights/{insightId}
  criado_em, titulo, texto, severidade, escopo ("coordenacao"|"geral")

trilhas_sugeridas/{trilhaId}
  perfil_anonimo{curso, nivel, areas[]}, modulos[], criado_em

interesses_alunos/{docId}                  # anônimo, sem dados pessoais
  curso_interesse, areas[], nivel, criado_em

contexto/atual
  total_vagas, ultima_coleta, amostra_n
```

**Listeners `onSnapshot`:** `vagas_ativas` (ordenadas por data, com limite), `lacunas_cursos`, `competencias_demandadas`, `insights` e `trilhas_sugeridas` (do próprio perfil). O painel da coordenação e a visão do aluno atualizam sozinhos quando o backend grava novos dados.

## 9. Regras do Firestore (`firestore.rules`)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if true;
      allow write: if false;
    }
    match /interesses_alunos/{docId} {
      allow create: if request.resource.data.keys().hasOnly(['curso_interesse','areas','nivel','criado_em'])
                    && request.resource.data.curso_interesse is string
                    && request.resource.data.curso_interesse.size() < 80
                    && request.resource.data.areas is list
                    && request.resource.data.areas.size() <= 10;
    }
  }
}
```
O Admin SDK do backend ignora essas regras. Como `interesses_alunos` é lido publicamente, ele **não pode** conter dados pessoais. Para um produto real, trocar por Firebase Authentication e leitura restrita ao próprio usuário.

## 10. Analytics e IA Insights
Gráficos e cartões conforme `ideia-design.md`. Agregações (cobertura, top competências, vagas por semana) são calculadas no backend e persistidas; o front só desenha. Exibir sempre o tamanho da amostra (`amostra_n`) e a data da última coleta para evitar conclusões em cima de poucos dados.

## 11. CI/CD com GitHub MCP Server

- `mcp_config.json` configura o servidor MCP do GitHub, lendo o token por variável de ambiente (nunca em texto).
- Passos executados via MCP: criar repositório público → enviar os arquivos (sem `.env`) → habilitar o GitHub Pages pela pasta `docs/` → conferir o link HTTPS.
- **Entregáveis do edital:** (1) link do repositório público e (2) link do app no GitHub Pages.
- Antes do primeiro push: rodar `git status` e uma busca por padrões de chave (`AIza`, `ghp_`, `-----BEGIN`) para garantir que nada vaza.

## 12. Plano de entrega

| Etapa | Entrega |
|---|---|
| 1 | Governança (3 `.md`), `.gitignore`, `.env.example`, projeto Firebase criado |
| 2 | `competencias_cursos.csv` + `taxonomia_competencias.csv` + `vagas_demo.csv` |
| 3 | Scraper de uma fonte (com `robots.txt`, fallback e testes) |
| 4 | Agente Matcher e métricas de cobertura (com testes) |
| 5 | Agentes Extrator e Orientador (Gemini) + validação de JSON + gravação no Firestore |
| 6 | Front-end: tokens, tema, abas Aluno/Coordenação, listeners `onSnapshot` |
| 7 | Gráficos Plotly e cartões de IA Insights |
| 8 | Revisão de segurança/LGPD + deploy via MCP + teste do link público |

## 13. Checklist final do edital

- [ ] Três arquivos de governança na raiz
- [ ] UI responsiva com Dark/Light e duas visões
- [ ] CSV em `data/` lido como RAG
- [ ] Scraping de vagas funcionando (e conforme `robots.txt`)
- [ ] Python determinístico + Gemini integrados
- [ ] Firestore com `onSnapshot` visível na interface
- [ ] `.env` fora do Git e nenhuma chave no código
- [ ] Repositório e Pages criados via MCP (`mcp_config.json`)
- [ ] Dashboard Plotly.js + cartões de IA Insights
- [ ] Links do repositório e do app prontos para envio
