# Dicionário de Dados e Registro de Fontes — SkillRadar

Este diretório armazena a base canônica de dados de cursos do SENAI Ourinhos, a taxonomia padronizada de competências tecnológicas e a base de contingência (modo demonstração) de vagas de emprego.

---

## 1. Dicionário de Arquivos de Dados

### 1.1 `competencias_cursos.csv`
Base RAG das unidades curriculares e competências ensinadas nos cursos de tecnologia do SENAI Ourinhos.

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `curso` | String | Nome oficial do curso ofertado | Técnico em Desenvolvimento de Sistemas |
| `modulo` | String | Unidade curricular / módulo pedagógico | Programação Web Front-end |
| `competencia` | String | Nome canônico da competência na taxonomia | JavaScript |
| `carga_horaria` | Inteiro | Carga horária total da unidade curricular | 80 |
| `nivel` | String | Grau de complexidade (básico, intermediário, avançado) | intermediário |
| `area` | String | Área tecnológica preponderante | desenvolvimento |
| `ferramenta_ensinada` | String | Ferramenta, framework ou tecnologia prática | React, TypeScript |

### 1.2 `taxonomia_competencias.csv`
Vocabulário padronizado de competências tecnológicas e mapeamento de sinônimos de mercado.

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `competencia_padrao` | String | Nome canônico e unificado da tecnologia | JavaScript |
| `sinonimos` | String | Termos equivalentes separados por pipe (`\|`) | js\|java script\|ecmascript |
| `area` | String | Macroárea tecnológica associada | desenvolvimento |

### 1.3 `cursos_areas.csv`
Mapeamento determinístico de escopo entre cursos e macroáreas de mercado para o Agente Matcher.

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `curso` | String | Nome do curso | Técnico em Desenvolvimento de Sistemas |
| `area` | String | Área de vaga elegível para o curso | desenvolvimento |

### 1.4 `vagas_demo.csv`
Base estruturada de contingência com 30 vagas reais/sintéticas do mercado de Ourinhos e região para operação 100% offline (Modo Demo).

| Campo | Tipo | Descrição |
|---|---|---|
| `vaga_id` | String | Identificador único da vaga |
| `titulo` | String | Cargo anunciado |
| `empresa` | String | Razão social ou nome fantasia da empresa |
| `cidade` | String | Município da vaga (Ourinhos, Marília, Assis, etc.) |
| `data` | String (ISO) | Data de publicação da vaga (AAAA-MM-DD) |
| `salario_min` | Inteiro | Remuneração mínima (ou vazio se a combinar) |
| `salario_max` | Inteiro | Remuneração máxima (ou vazio se a combinar) |
| `fonte_url` | String | Link da fonte de publicação |
| `requisitos_texto` | String | Texto integral da descrição e requisitos |
| `competencias_esperadas` | String | Competências mapeadas para validação |
| `senioridade` | String | estagio, junior, pleno, senior ou nao_informado |
| `coletado_em` | String | Data da coleta |

---

## 2. Registro de Governança de Web Scraping (Diretiva §3)

Conforme estabelecido no Pilar 4 do edital e na diretiva de scraping, este registro documenta os portais avaliados, a checagem do arquivo `robots.txt` e o status de autorização de coleta.

| Fonte / Portal | URL Base | Data Conferência | Conformidade `robots.txt` | Status de Coleta | Observações |
|---|---|---|---|---|---|
| **PAT Ourinhos (Portal do Trabalhador)** | `https://www.ourinhos.sp.gov.br/portal/pat` | 2026-10-24 | Requer triagem presencial / sem API | **Modo Demo Ativado** | Respeito ético às diretivas de uso e proteção do serviço |
| **Portal Regional de Vagas (Simulado / Fixture)** | `https://vagas.ourinhoseregiao.com.br/vagas` | 2026-10-24 | Permite `/vagas` (bloqueia `/admin`) | Testado via Fixtures | Utilizado para testes de integração de scrapers offline |
| **Vagas Demo (Contingência Oficial)** | `data/vagas_demo.csv` | 2026-10-24 | N/A (Arquivo Local) | **Ativo (Modo Demo)** | Garante execução determinística sem chaves ou rede |

> **Nota Ética e LGPD:** O Agente Coletor aplica expurgo automático de dados pessoais (e-mails e números de telefone) em qualquer texto coletado antes da persistência, garantindo plena conformidade com a Lei Geral de Proteção de Dados (LGPD).
