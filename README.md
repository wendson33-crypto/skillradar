# 🎯 SkillRadar — Inteligência de Carreira e Alinhamento Curricular
### *Career Intelligence & Curriculum Alignment Platform*

---

[![Google Antigravity](https://img.shields.io/badge/Developed%20with-Google%20Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-8E75C2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![Plotly.js](https://img.shields.io/badge/Analytics-Plotly.js-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/javascript/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **SENAI Ourinhos — Hackathon de Inovação & IA Generativa**  
> Projeto concebido e construído sob a **Arquitetura de 3 Camadas** e acelerado pelo **Google Antigravity**.

---

## 🇧🇷 Português do Brasil

### 📌 1. Visão Geral
O **SkillRadar** é uma plataforma analítica que conecta o universo acadêmico à demanda do mercado de trabalho regional (foco em Ourinhos e região). A ferramenta compara de forma determinística as competências ensinadas nos cursos técnicos do SENAI com os requisitos reais extraídos de vagas de emprego, revelando lacunas curriculares e orientando alunos com trilhas de aprendizagem personalizadas.

#### 👥 Duas Visões Especializadas
* **🎓 Visão do Aluno:** Painel motivador e centrado no estudante. Apresenta cálculo de aderência individual às vagas abertas, lacunas de competências identificadas e sugestão de trilha de módulos formativos prioritários baseados no plano de curso.
* **📊 Visão da Coordenação:** Painel analítico de apoio à gestão escolar. Oferece taxa de cobertura global do currículo, identificação de tecnologias emergentes em alta e matriz de módulos para fundamentar revisões de planos de curso.

---

### 🏗️ 2. Arquitetura em 3 Camadas

O desenvolvimento adota o framework determinístico do **Google Antigravity**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Camada de Diretivas (/Directives)                        │
│    SOPs, regras de governança, segurança e especificações   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Camada de Orquestração (Antigravity Orchestrator Agent)  │
│    Inteligência probabilística: Gemini 2.5 (google-genai)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Camada de Execução (/Execution)                          │
│    Lógica de negócio determinística: pandas, scrapers, math │
└─────────────────────────────────────────────────────────────┘
```

* **Regra de Ouro:** Métricas, percentuais e cálculos são **100% determinísticos** calculados em Python. O modelo Gemini é utilizado estritamente para extração semântica de competências e redação de insights pedagógicos sob contratos de JSON estritos.

---

### 🤖 3. Agentes de IA e Skills Antigravity

| Agente / Componente | Papel & Tecnologia | Entrada | Saída |
|---|---|---|---|
| **Agente Coletor** | Scraper Python (BeautifulSoup / Fixtures) | Portais públicos (respeito a `robots.txt`) | Vagas estruturadas e deduplicadas |
| **Agente Extrator** | IA Generativa (`google-genai` / Gemini 2.5) | Texto livre de requisitos da vaga | JSON com competências mapeadas na taxonomia |
| **Agente Matcher** | Motor determinístico (Python / pandas) | Base RAG local de cursos × competências da vaga | Percentual de cobertura, lacunas e aderência |
| **Agente Orientador** | IA Pedagógica (Gemini 2.5 + RAG) | Lacunas calculadas + módulos candidatos do CSV | Recomendações de trilhas e insights em JSON |
| **Verificador de Segurança** | Script determinístico (`Execution/verificar_segredos.py`) | Arquivos do workspace | Garantia de 0 chaves versionadas |

---

### 🚀 4. Instalação e Execução (Windows PowerShell)

#### Pré-requisitos
* Python 3.11+ instalado
* Git configurado

#### Passo a Passo

```powershell
# 1. Clonar ou navegar até a pasta do projeto
cd projeto-skillradar

# 2. Criar e ativar o ambiente virtual (opcional)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
copy .env.example .env
# Edite o .env no seu editor de preferência preenchendo as chaves necessárias

# 5. Executar verificação de segurança
python Execution/verificar_segredos.py

# 6. Executar os testes automatizados
pytest tests/

# 7. Rodar o orquestrador em Modo Demonstração (sem internet e sem chaves)
python Execution/orquestrador.py --modo demo --sem-gemini --dry-run
```

---

## 🇺🇸 English (Overview)

### 📌 1. Project Overview
**SkillRadar** is a real-time career intelligence and curriculum alignment dashboard designed to bridge the gap between technical education curricula and dynamic regional job market demands. Developed for SENAI Ourinhos, the application matches technical course competencies against job posting requirements to compute coverage ratios, surface skill gaps, and suggest learning roadmaps.

### 🌟 Key Highlights
* **Google Antigravity Integration:** Orchestrated using multi-agent directives, strict safety rules, and automated secret scanning.
* **Dual Experience:** Tailored views for **Students** (job matching, personal gap breakdown, guided study paths) and **Academic Leadership** (curriculum health, industry skill trends, interactive Plotly matrices).
* **Deterministic Core:** Python/Pandas handles all statistical and scoring math; Google Gemini is restricted to semantic entity extraction and instructional feedback under validated JSON schemas.
* **Realtime & Offline-Ready:** Works with Google Cloud Firestore (`onSnapshot`) and features a complete offline fallback demo mode (`--modo demo --sem-gemini`).

---

### 🛡️ 5. Governança, LGPD e Segurança
* **Zero Secrets in Repository:** Chaves de API, credenciais de serviço e tokens pessoais **nunca** são versionados ou impressos em logs.
* **LGPD Compliance:** Dados de vagas são públicos e anonimizados; formulário do estudante não coleta nomes, e-mails, documentos ou dados sensíveis.
* **Base RAG Local:** Fonte da verdade curricular em `data/competencias_cursos.csv` e `data/taxonomia_competencias.csv`.

---

*Desenvolvido no ecossistema SENAI com Google Antigravity.*
