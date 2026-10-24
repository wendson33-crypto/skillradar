# projeto.md — SkillRadar (documento mestre)

> **Leia este arquivo primeiro.** Ele diz o que construir, em que ordem e como saber que cada etapa está pronta. Os detalhes de cada área estão nas diretivas listadas na seção 5. As ideias originais estão em `ideia-projeto.md` e `ideia-design.md` e **não devem ser alteradas**.

## 1. Propósito

SkillRadar compara as **competências ensinadas** nos cursos de uma escola técnica (SENAI Ourinhos) com as **competências exigidas** nas vagas de emprego da região. O sistema mostra as lacunas, sugere trilhas de estudo e atualiza a tela em tempo real. Duas visões: **Aluno** (vagas compatíveis, trilha, perfil) e **Coordenação** (cobertura do currículo, lacunas, tendências).

## 2. Regras de ouro

1. **Números sempre em Python.** O Gemini só extrai competências de texto e escreve explicações, sempre com saída JSON validada.
2. **Nada inventado.** Trilhas só com módulos de `data/competencias_cursos.csv`; competências só da taxonomia; vaga de demonstração sempre rotulada.
3. **Segredo nunca em código, log ou prompt.** Veja `Directives/seguranca/seguranca.md`.
4. **Funciona sem internet e sem chaves** no modo demo (`--modo demo --sem-gemini`). Isso permite desenvolver e testar em etapas.
5. **Cada etapa só termina com os critérios de aceite cumpridos** e os testes passando.
6. Na dúvida sobre algo listado na seção 9, **pergunte ao usuário** em vez de decidir sozinho.

## 3. Arquitetura

```
 Portais de vagas (robots.txt respeitado)          data/vagas_demo.csv (plano B)
              │                                              │
              └──────────────► Coletor (Python) ◄────────────┘
                                     │
                              Extrator (Gemini ou sinônimos)
                                     │
 data/competencias_cursos.csv ─┐     ▼
 data/taxonomia_competencias.csv ├─► Matcher (pandas, determinístico)
 data/cursos_areas.csv ────────┘     │
                                     ▼
                              Orientador (Gemini ou templates)
                                     │ validação
                                     ▼
                    Firestore (gravação: Firebase Admin SDK)
                                     │ onSnapshot
                                     ▼
          Site estático em docs/ (hospedado no Vercel): HTML/CSS/JS + Plotly.js
```

## 4. Estrutura de pastas

```
projeto-skillradar/
├── projeto.md  ideia-projeto.md  ideia-design.md  README.md
├── Directives/
│   ├── desing/design.md          # interface, CSS, JS, gráficos, contrato de dados
│   ├── dados/dados.md
│   ├── scraping/scraping.md
│   ├── agentes/agentes.md
│   ├── firestore/firestore.md
│   ├── seguranca/seguranca.md
│   └── deploy/deploy.md
├── Execution/                    # scripts Python determinísticos (criar)
│   ├── scrapers/  agentes/  orquestrador.py  firestore_cliente.py  verificar_segredos.py
├── data/                         # CSVs (já existem) + README.md
├── docs/                         # site publicado (criar a partir do design.md)
├── tests/
├── .temp/                        # intermediários (ignorada pelo Git)
├── .gitignore  .env.example  requirements.txt  firestore.rules  mcp_config.example.json  vercel.json
```

> A pasta `Execution/` segue o padrão "diretivas dizem o quê, scripts fazem o quê". Se o instrutor preferir outro nome, renomeie e atualize as diretivas.

## 5. Mapa: pilares do edital × diretivas

| # | Pilar do edital | Diretiva | Onde se verifica |
|---|---|---|---|
| 1 | Governança Antigravity (`ideia-projeto.md`, `ideia-design.md`, `projeto.md`) | este arquivo | os três existem na raiz |
| 2 | UI responsiva com Dark/Light | `Directives/desing/design.md` | tema alterna sem recarregar; layout em celular |
| 3 | Base RAG local em CSV | `Directives/dados/dados.md` | CSVs em `data/` lidos e validados |
| 4 | Web scraping ao vivo | `Directives/scraping/scraping.md` | coleta respeitando `robots.txt`, com plano B |
| 5 | Multi-agentes Python + Gemini | `Directives/agentes/agentes.md` | orquestrador, validações, plano B sem IA |
| 6 | Firestore com `onSnapshot` | `Directives/firestore/firestore.md` | tela muda sem recarregar |
| 7 | Segurança `.env` / `.gitignore` | `Directives/seguranca/seguranca.md` | `verificar_segredos.py` passa |
| 8 | Repositório via MCP + hospedagem no Vercel | `Directives/deploy/deploy.md` | link HTTPS público abre |
| 9 | Dashboard Plotly.js + Insights de IA | `design.md` §7–8, `agentes.md` §6 | 6 gráficos e `#iaInsights` |

## 6. Plano de execução por etapas

Faça **uma etapa por vez**, mostre o resultado ao usuário e só avance com os critérios cumpridos.

| Etapa | Entrega | Diretivas | Aceite |
|---|---|---|---|
| 0 | Ambiente: `.gitignore`, `.env.example`, `requirements.txt`, venv | seguranca | arquivos criados antes do 1º commit |
| 1 | Camada de dados: leitura, normalização, área da vaga, extrator por sinônimos | dados | testes de `dados.md` §7 passam |
| 2 | Matcher, trilha-base, aderência, estruturas de gráfico | agentes §5 | números da tabela de `agentes.md` §8 reproduzidos |
| 3 | Coletor e scraper com plano B | scraping | testes com fixtures; modo demo funciona |
| 4 | Extrator e Orientador com Gemini + validações + templates | agentes §3, §6 | testes com respostas simuladas; fluxo real se houver chave |
| 5 | Orquestrador e `--dry-run` | agentes §7 | JSONs em `.temp/` com os números esperados |
| 6 | Gravação no Firestore e regras | firestore | documentos criados; reexecução não duplica |
| 7 | Front-end em `docs/` | design + firestore §5.2 | checklist de `design.md` §10.3; indicador "ao vivo" |
| 8 | Verificação de segredos e revisão geral | seguranca | `verificar_segredos.py` e todos os testes passam |
| 9 | Deploy e entrega | deploy | links do repositório e do Vercel funcionando |

Instalação (Windows, PowerShell), para o `README.md`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env     # preencha o .env pelo editor
python Execution\orquestrador.py --modo demo --sem-gemini --dry-run
```

`requirements.txt`: `pandas`, `firebase-admin`, `google-genai`, `requests`, `beautifulsoup4`, `lxml`, `python-dotenv`, `pydantic`, `tzdata`, `pytest`.

## 7. Convenções

- Idioma da interface, textos e comentários: **português do Brasil**. Nomes de arquivo sem acento.
- Python 3.11+, `pathlib`, UTF-8, type hints, funções pequenas e puras para o que for cálculo.
- Decimais com 1 casa; `null` quando não há base de cálculo, nunca `0`.
- Fuso `America/Sao_Paulo`.
- Mensagens de commit curtas e descritivas, sem segredos.
- O agente atualiza `README.md` com: o que é, como rodar, link do repositório e do site no Vercel.

## 8. Checklist final do edital

- [ ] `ideia-projeto.md`, `ideia-design.md` e `projeto.md` na raiz.
- [ ] Interface responsiva com modo escuro e claro.
- [ ] Base RAG local em CSV na pasta `data/`.
- [ ] Coleta de vagas ao vivo (ou plano B rotulado como demonstração).
- [ ] Agentes em Python determinístico + Gemini com saída validada.
- [ ] Firestore com atualização em tempo real (`onSnapshot`).
- [ ] Nenhuma chave do Gemini nem token do GitHub no repositório público.
- [ ] Repositório criado e arquivos enviados **pelo servidor MCP** com `mcp_config.json`.
- [ ] Dashboard com Plotly.js e **AI Insights**.
- [ ] Entregues: link do repositório público e link HTTPS público do site no Vercel (o instrutor aceitou o Vercel no lugar do GitHub Pages).

## 9. Pontos a confirmar com o instrutor

1. Nome e uso da pasta `Execution/` (e se `projeto.md` deve ficar na raiz ou dentro de `Directives/`).
2. Servidor MCP do GitHub usado pela turma e formato do `mcp_config.json` no Antigravity.
3. Se a importação do repositório no Vercel é feita pelo usuário (painel do Vercel) ou se a turma tem outro procedimento. O instrutor já aceitou o Vercel como hospedagem.
4. Qual portal de vagas usar na coleta ao vivo e se há regras da escola sobre isso.
5. Se o edital aceita as vagas de demonstração como plano B quando não houver coleta permitida.
