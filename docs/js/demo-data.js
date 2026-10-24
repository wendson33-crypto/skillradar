// docs/js/demo-data.js
// Dados embutidos determinísticos do SkillRadar para demonstração offline e fallback imediato

export const DEMO_PAYLOAD = {
  "contexto": {
    "atual": {
      "total_vagas": 30,
      "ultima_coleta": "2026-10-24T11:24:14.986794-03:00",
      "modo_demo": true,
      "fonte": "vagas_demo.csv",
      "graficos": {
        "salario_por_area": {
          "desenvolvimento": [
            4250.0,
            7250.0,
            1700.0,
            5500.0,
            5000.0,
            3600.0,
            7000.0,
            5500.0,
            7750.0,
            3300.0,
            3850.0,
            10500.0,
            3300.0,
            5500.0,
            6000.0,
            5000.0
          ],
          "dados": [
            4750.0,
            2550.0,
            8750.0,
            6500.0,
            1800.0,
            6500.0
          ],
          "infraestrutura": [
            2800.0,
            9500.0,
            7750.0,
            13000.0,
            2650.0
          ],
          "ia": [
            6250.0
          ]
        }
      },
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    }
  },
  "vagas_ativas": {
    "f5ad2d83bdcf": {
      "vaga_id": "f5ad2d83bdcf",
      "titulo": "Desenvolvedor Full Stack Júnior",
      "empresa": "Empresa Demo 01",
      "cidade": "Ourinhos",
      "data": "2026-10-20",
      "salario_min": 3500,
      "salario_max": 5000,
      "fonte_url": "https://exemplo.invalid/vagas/V001",
      "competencias": [
        "React",
        "Node.js",
        "TypeScript",
        "APIs REST",
        "SQL",
        "Git",
        "Docker"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "db5ae4cfd926": {
      "vaga_id": "db5ae4cfd926",
      "titulo": "Desenvolvedor Back-end Java Pleno",
      "empresa": "Empresa Demo 02",
      "cidade": "Marília",
      "data": "2026-10-19",
      "salario_min": 6000,
      "salario_max": 8500,
      "fonte_url": "https://exemplo.invalid/vagas/V002",
      "competencias": [
        "Java",
        "Spring Boot",
        "Microsserviços",
        "Docker",
        "Kubernetes",
        "Testes Automatizados",
        "SQL",
        "CI/CD",
        "Inglês Técnico"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "0520536a35fd": {
      "vaga_id": "0520536a35fd",
      "titulo": "Estagiário de Desenvolvimento",
      "empresa": "Empresa Demo 03",
      "cidade": "Ourinhos",
      "data": "2026-10-21",
      "salario_min": 1500,
      "salario_max": 1900,
      "fonte_url": "https://exemplo.invalid/vagas/V003",
      "competencias": [
        "Lógica de Programação",
        "HTML",
        "CSS",
        "JavaScript",
        "Git"
      ],
      "senioridade": "estagio",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "1e7413adf31e": {
      "vaga_id": "1e7413adf31e",
      "titulo": "Analista de Dados Júnior",
      "empresa": "Empresa Demo 04",
      "cidade": "Bauru",
      "data": "2026-10-18",
      "salario_min": 4000,
      "salario_max": 5500,
      "fonte_url": "https://exemplo.invalid/vagas/V004",
      "competencias": [
        "Python",
        "Pandas",
        "SQL",
        "Visualização de Dados",
        "Power BI",
        "Estatística",
        "Excel",
        "Storytelling com Dados"
      ],
      "senioridade": "junior",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "c72745c3a022": {
      "vaga_id": "c72745c3a022",
      "titulo": "Técnico em Redes e Suporte",
      "empresa": "Empresa Demo 05",
      "cidade": "Ourinhos",
      "data": "2026-10-15",
      "salario_min": 2400,
      "salario_max": 3200,
      "fonte_url": "https://exemplo.invalid/vagas/V005",
      "competencias": [
        "Redes de Computadores",
        "TCP/IP",
        "Linux",
        "Monitoramento e Logs"
      ],
      "senioridade": "junior",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "460f3076bbf5": {
      "vaga_id": "460f3076bbf5",
      "titulo": "Engenheiro DevOps Pleno",
      "empresa": "Empresa Demo 06",
      "cidade": "Londrina",
      "data": "2026-10-17",
      "salario_min": 8000,
      "salario_max": 11000,
      "fonte_url": "https://exemplo.invalid/vagas/V006",
      "competencias": [
        "CI/CD",
        "Docker",
        "Kubernetes",
        "Cloud Computing",
        "AWS",
        "Infraestrutura como Código",
        "Linux",
        "Shell Script",
        "Inglês Técnico"
      ],
      "senioridade": "pleno",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "de30099de681": {
      "vaga_id": "de30099de681",
      "titulo": "Desenvolvedor Front-end React",
      "empresa": "Empresa Demo 07",
      "cidade": "Assis",
      "data": "2026-10-16",
      "salario_min": 4500,
      "salario_max": 6500,
      "fonte_url": "https://exemplo.invalid/vagas/V007",
      "competencias": [
        "React",
        "TypeScript",
        "HTML",
        "CSS",
        "APIs REST",
        "UX/UI Design",
        "Testes Automatizados"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "1ec773cb1784": {
      "vaga_id": "1ec773cb1784",
      "titulo": "Desenvolvedor Mobile Flutter",
      "empresa": "Empresa Demo 08",
      "cidade": "Marília",
      "data": "2026-10-14",
      "salario_min": 4000,
      "salario_max": 6000,
      "fonte_url": "https://exemplo.invalid/vagas/V008",
      "competencias": [
        "Desenvolvimento Mobile",
        "APIs REST",
        "Firebase",
        "Git",
        "Metodologias Ágeis"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "af4b325d25e5": {
      "vaga_id": "af4b325d25e5",
      "titulo": "Analista de Suporte Técnico N1",
      "empresa": "Empresa Demo 09",
      "cidade": "Ourinhos",
      "data": "2026-10-13",
      "salario_min": 2200,
      "salario_max": 2900,
      "fonte_url": "https://exemplo.invalid/vagas/V009",
      "competencias": [
        "Redes de Computadores",
        "Excel"
      ],
      "senioridade": "junior",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "9af0e92d2dfb": {
      "vaga_id": "9af0e92d2dfb",
      "titulo": "Cientista de Dados Pleno",
      "empresa": "Empresa Demo 10",
      "cidade": "Bauru",
      "data": "2026-10-12",
      "salario_min": 7500,
      "salario_max": 10000,
      "fonte_url": "https://exemplo.invalid/vagas/V010",
      "competencias": [
        "Machine Learning",
        "Python",
        "Deep Learning",
        "SQL",
        "Estatística",
        "Docker",
        "Inglês Técnico"
      ],
      "senioridade": "pleno",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "93c80aab126c": {
      "vaga_id": "93c80aab126c",
      "titulo": "Desenvolvedor PHP Júnior",
      "empresa": "Empresa Demo 11",
      "cidade": "Santa Cruz do Rio Pardo",
      "data": "2026-10-11",
      "salario_min": 3000,
      "salario_max": 4200,
      "fonte_url": "https://exemplo.invalid/vagas/V011",
      "competencias": [
        "PHP",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "Programação Orientada a Objetos"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "ecec54200217": {
      "vaga_id": "ecec54200217",
      "titulo": "Desenvolvedor .NET Pleno",
      "empresa": "Empresa Demo 12",
      "cidade": "Londrina",
      "data": "2026-10-10",
      "salario_min": 6000,
      "salario_max": 8000,
      "fonte_url": "https://exemplo.invalid/vagas/V012",
      "competencias": [
        ".NET",
        "SQL",
        "APIs REST",
        "Azure",
        "Testes Automatizados",
        "Docker",
        "Microsserviços"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "e36720e5463b": {
      "vaga_id": "e36720e5463b",
      "titulo": "Engenheiro de Prompt e IA Generativa",
      "empresa": "Empresa Demo 13",
      "cidade": "Ourinhos",
      "data": "2026-10-21",
      "salario_min": 5000,
      "salario_max": 7500,
      "fonte_url": "https://exemplo.invalid/vagas/V013",
      "competencias": [
        "IA Generativa",
        "Engenharia de Prompt",
        "RAG",
        "Agentes de IA",
        "Python",
        "APIs REST",
        "Docker"
      ],
      "senioridade": "pleno",
      "area": "ia",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "9f897b3c534b": {
      "vaga_id": "9f897b3c534b",
      "titulo": "Analista de BI Pleno",
      "empresa": "Empresa Demo 14",
      "cidade": "Marília",
      "data": "2026-10-09",
      "salario_min": 5500,
      "salario_max": 7500,
      "fonte_url": "https://exemplo.invalid/vagas/V014",
      "competencias": [
        "Visualização de Dados",
        "Power BI",
        "Modelagem de Dados",
        "SQL",
        "ETL",
        "Excel"
      ],
      "senioridade": "pleno",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "4c19afaee5c5": {
      "vaga_id": "4c19afaee5c5",
      "titulo": "Desenvolvedor Python Back-end",
      "empresa": "Empresa Demo 15",
      "cidade": "Assis",
      "data": "2026-10-08",
      "salario_min": 4500,
      "salario_max": 6500,
      "fonte_url": "https://exemplo.invalid/vagas/V015",
      "competencias": [
        "Python",
        "Frameworks Python",
        "APIs REST",
        "SQL",
        "Banco de Dados NoSQL",
        "Docker",
        "Git",
        "Testes Automatizados"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "40096708f2aa": {
      "vaga_id": "40096708f2aa",
      "titulo": "Estagiário de Dados",
      "empresa": "Empresa Demo 16",
      "cidade": "Ourinhos",
      "data": "2026-10-07",
      "salario_min": 1600,
      "salario_max": 2000,
      "fonte_url": "https://exemplo.invalid/vagas/V016",
      "competencias": [
        "Excel",
        "SQL",
        "Python",
        "Power BI"
      ],
      "senioridade": "estagio",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "afffaadaea73": {
      "vaga_id": "afffaadaea73",
      "titulo": "Analista de Segurança da Informação",
      "empresa": "Empresa Demo 17",
      "cidade": "Londrina",
      "data": "2026-10-06",
      "salario_min": 6500,
      "salario_max": 9000,
      "fonte_url": "https://exemplo.invalid/vagas/V017",
      "competencias": [
        "Segurança da Informação",
        "LGPD",
        "Redes de Computadores",
        "Linux",
        "Monitoramento e Logs"
      ],
      "senioridade": "pleno",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "8b50de7cd575": {
      "vaga_id": "8b50de7cd575",
      "titulo": "Desenvolvedor Full Stack Pleno",
      "empresa": "Empresa Demo 18",
      "cidade": "Bauru",
      "data": "2026-10-05",
      "salario_min": 6500,
      "salario_max": 9000,
      "fonte_url": "https://exemplo.invalid/vagas/V018",
      "competencias": [
        "React",
        "Node.js",
        "TypeScript",
        "APIs REST",
        "SQL",
        "Docker",
        "AWS",
        "CI/CD",
        "Testes Automatizados"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "3b3b35045508": {
      "vaga_id": "3b3b35045508",
      "titulo": "Técnico em Desenvolvimento de Sistemas",
      "empresa": "Empresa Demo 19",
      "cidade": "Ourinhos",
      "data": "2026-10-04",
      "salario_min": 2800,
      "salario_max": 3800,
      "fonte_url": "https://exemplo.invalid/vagas/V019",
      "competencias": [
        "Java",
        ".NET",
        "SQL",
        "UML",
        "Levantamento de Requisitos"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "1febca72e00c": {
      "vaga_id": "1febca72e00c",
      "titulo": "Arquiteto de Soluções em Nuvem",
      "empresa": "Empresa Demo 20",
      "cidade": "Londrina",
      "data": "2026-10-03",
      "salario_min": 11000,
      "salario_max": 15000,
      "fonte_url": "https://exemplo.invalid/vagas/V020",
      "competencias": [
        "Cloud Computing",
        "AWS",
        "Azure",
        "Kubernetes",
        "Microsserviços",
        "Segurança da Informação",
        "Infraestrutura como Código",
        "Inglês Técnico"
      ],
      "senioridade": "senior",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "af5ed3e7c7c9": {
      "vaga_id": "af5ed3e7c7c9",
      "titulo": "Designer UX/UI Júnior",
      "empresa": "Empresa Demo 21",
      "cidade": "Marília",
      "data": "2026-10-02",
      "salario_min": 3200,
      "salario_max": 4500,
      "fonte_url": "https://exemplo.invalid/vagas/V021",
      "competencias": [
        "UX/UI Design",
        "Design System",
        "HTML",
        "CSS"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "6785c461f755": {
      "vaga_id": "6785c461f755",
      "titulo": "Analista de Sistemas Sênior",
      "empresa": "Empresa Demo 22",
      "cidade": "Bauru",
      "data": "2026-09-30",
      "salario_min": 9000,
      "salario_max": 12000,
      "fonte_url": "https://exemplo.invalid/vagas/V022",
      "competencias": [
        "Java",
        "Spring Boot",
        "Microsserviços",
        "Docker",
        "Kubernetes",
        "Metodologias Ágeis",
        "Levantamento de Requisitos",
        "Inglês Técnico"
      ],
      "senioridade": "senior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "ebd21d3c58dd": {
      "vaga_id": "ebd21d3c58dd",
      "titulo": "Desenvolvedor Web Júnior",
      "empresa": "Empresa Demo 23",
      "cidade": "Cambará",
      "data": "2026-09-29",
      "salario_min": 2800,
      "salario_max": 3800,
      "fonte_url": "https://exemplo.invalid/vagas/V023",
      "competencias": [
        "HTML",
        "CSS",
        "JavaScript",
        "PHP",
        "Git"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "9759dc65e403": {
      "vaga_id": "9759dc65e403",
      "titulo": "Engenheiro de Dados Júnior",
      "empresa": "Empresa Demo 24",
      "cidade": "Londrina",
      "data": "2026-09-28",
      "salario_min": 5500,
      "salario_max": 7500,
      "fonte_url": "https://exemplo.invalid/vagas/V024",
      "competencias": [
        "ETL",
        "Python",
        "SQL",
        "Big Data",
        "Cloud Computing",
        "AWS",
        "Docker"
      ],
      "senioridade": "junior",
      "area": "dados",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "4d079db01eb1": {
      "vaga_id": "4d079db01eb1",
      "titulo": "Analista de Automação com IA",
      "empresa": "Empresa Demo 25",
      "cidade": "Ourinhos",
      "data": "2026-09-26",
      "salario_min": 4500,
      "salario_max": 6500,
      "fonte_url": "https://exemplo.invalid/vagas/V025",
      "competencias": [
        "IA Generativa",
        "Web Scraping",
        "Python",
        "APIs REST",
        "Firebase"
      ],
      "senioridade": "junior",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "bea815e49dec": {
      "vaga_id": "bea815e49dec",
      "titulo": "Auxiliar de Infraestrutura de TI",
      "empresa": "Empresa Demo 26",
      "cidade": "Jacarezinho",
      "data": "2026-09-25",
      "salario_min": 2300,
      "salario_max": 3000,
      "fonte_url": "https://exemplo.invalid/vagas/V026",
      "competencias": [
        "Linux",
        "Shell Script",
        "Redes de Computadores",
        "TCP/IP",
        "Monitoramento e Logs"
      ],
      "senioridade": "junior",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "5428de4c9b7c": {
      "vaga_id": "5428de4c9b7c",
      "titulo": "Desenvolvedor React Native",
      "empresa": "Empresa Demo 27",
      "cidade": "Assis",
      "data": "2026-09-23",
      "salario_min": 5000,
      "salario_max": 7000,
      "fonte_url": "https://exemplo.invalid/vagas/V027",
      "competencias": [
        "Desenvolvimento Mobile",
        "TypeScript",
        "APIs REST",
        "Testes Automatizados",
        "Git",
        "Metodologias Ágeis"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "c7c79bf27f33": {
      "vaga_id": "c7c79bf27f33",
      "titulo": "Analista de Qualidade (QA)",
      "empresa": "Empresa Demo 28",
      "cidade": "Marília",
      "data": "2026-09-22",
      "salario_min": 4000,
      "salario_max": 6000,
      "fonte_url": "https://exemplo.invalid/vagas/V028",
      "competencias": [
        "Testes Automatizados",
        "SQL",
        "Metodologias Ágeis",
        "Inglês Técnico"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "73f61bc83289": {
      "vaga_id": "73f61bc83289",
      "titulo": "Técnico de Suporte e Redes Júnior",
      "empresa": "Empresa Demo 29",
      "cidade": "Santa Cruz do Rio Pardo",
      "data": "2026-09-18",
      "salario_min": null,
      "salario_max": null,
      "fonte_url": "https://exemplo.invalid/vagas/V029",
      "competencias": [
        "Redes de Computadores",
        "Linux",
        "TCP/IP",
        "Monitoramento e Logs"
      ],
      "senioridade": "junior",
      "area": "infraestrutura",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    },
    "593b4dd5b6a7": {
      "vaga_id": "593b4dd5b6a7",
      "titulo": "Desenvolvedor Back-end Node.js",
      "empresa": "Empresa Demo 30",
      "cidade": "Ourinhos",
      "data": "2026-09-16",
      "salario_min": null,
      "salario_max": null,
      "fonte_url": "https://exemplo.invalid/vagas/V030",
      "competencias": [
        "Node.js",
        "APIs REST",
        "Banco de Dados NoSQL",
        "Docker",
        "Git",
        "Firebase"
      ],
      "senioridade": "pleno",
      "area": "desenvolvimento",
      "modo_demo": true,
      "coletado_em": "2026-10-23"
    }
  },
  "lacunas_cursos": {
    "qualificacao-em-analise-de-dados": {
      "curso": "Qualificação em Análise de Dados",
      "areas_foco": [
        "dados",
        "ia"
      ],
      "amostra_n": 7,
      "total_coletadas": 30,
      "cobertura_pct": 47.8,
      "cobertura_ponderada_pct": 65.9,
      "lacunas": [
        {
          "competencia": "Docker",
          "area": "infraestrutura",
          "frequencia": 3,
          "pct_vagas": 42.9
        },
        {
          "competencia": "Agentes de IA",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "APIs REST",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "AWS",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Big Data",
          "area": "dados",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Cloud Computing",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Deep Learning",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Engenharia de Prompt",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "IA Generativa",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Inglês Técnico",
          "area": "geral",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "RAG",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 14.3
        },
        {
          "competencia": "Redes de Computadores",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 14.3
        }
      ],
      "kpis": {
        "salario_mediano": 6250,
        "salario_n": 7
      },
      "graficos": {
        "radar": {
          "eixos": [
            "Python",
            "SQL",
            "Excel",
            "Docker",
            "Agentes de IA",
            "APIs REST"
          ],
          "mercado": [
            71.4,
            71.4,
            57.1,
            42.9,
            14.3,
            14.3
          ],
          "curso": [
            71.4,
            71.4,
            57.1,
            0.0,
            0.0,
            0.0
          ]
        },
        "top_tecnologias": {
          "competencias": [
            "Python",
            "SQL",
            "Excel",
            "Docker",
            "Power BI",
            "Estatística",
            "ETL",
            "Visualização de Dados",
            "Agentes de IA",
            "APIs REST"
          ],
          "pct": [
            71.4,
            71.4,
            57.1,
            42.9,
            42.9,
            28.6,
            28.6,
            28.6,
            14.3,
            14.3
          ],
          "cobertas": [
            true,
            true,
            true,
            false,
            true,
            true,
            true,
            true,
            false,
            false
          ]
        },
        "vagas_semana": {
          "semanas": [
            "2026-W40",
            "2026-W41",
            "2026-W42",
            "2026-W43"
          ],
          "total": [
            1,
            2,
            3,
            1
          ]
        },
        "matriz": {
          "competencias": [
            "Python",
            "SQL",
            "Excel",
            "Docker",
            "Power BI",
            "Estatística",
            "ETL",
            "Visualização de Dados",
            "Agentes de IA",
            "APIs REST",
            "AWS",
            "Big Data",
            "Cloud Computing",
            "Deep Learning",
            "Engenharia de Prompt"
          ],
          "linhas": [
            {
              "modulo": "Fundamentos de Dados e Estatística",
              "valores": [
                0,
                0,
                1,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "SQL para Análise",
              "valores": [
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Python para Dados",
              "valores": [
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Visualização e Dashboards",
              "valores": [
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Engenharia de Dados Básica",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Machine Learning Introdutório",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Storytelling com Dados",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            }
          ]
        }
      },
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "qualificacao-em-ia-generativa": {
      "curso": "Qualificação em IA Generativa",
      "areas_foco": [
        "ia",
        "desenvolvimento",
        "dados"
      ],
      "amostra_n": 24,
      "total_coletadas": 30,
      "cobertura_pct": 31.4,
      "cobertura_ponderada_pct": 29.7,
      "lacunas": [
        {
          "competencia": "SQL",
          "area": "dados",
          "frequencia": 13,
          "pct_vagas": 54.2
        },
        {
          "competencia": "APIs REST",
          "area": "desenvolvimento",
          "frequencia": 10,
          "pct_vagas": 41.7
        },
        {
          "competencia": "Docker",
          "area": "infraestrutura",
          "frequencia": 10,
          "pct_vagas": 41.7
        },
        {
          "competencia": "Testes Automatizados",
          "area": "desenvolvimento",
          "frequencia": 7,
          "pct_vagas": 29.2
        },
        {
          "competencia": "Excel",
          "area": "dados",
          "frequencia": 4,
          "pct_vagas": 16.7
        },
        {
          "competencia": "Inglês Técnico",
          "area": "geral",
          "frequencia": 4,
          "pct_vagas": 16.7
        },
        {
          "competencia": "Metodologias Ágeis",
          "area": "gestao",
          "frequencia": 4,
          "pct_vagas": 16.7
        },
        {
          "competencia": "TypeScript",
          "area": "desenvolvimento",
          "frequencia": 4,
          "pct_vagas": 16.7
        },
        {
          "competencia": "Java",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": "JavaScript",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": "Microsserviços",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": "Node.js",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": "Power BI",
          "area": "dados",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": "React",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 12.5
        },
        {
          "competencia": ".NET",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "AWS",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Desenvolvimento Mobile",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Estatística",
          "area": "dados",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "ETL",
          "area": "dados",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Kubernetes",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Levantamento de Requisitos",
          "area": "gestao",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "PHP",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Spring Boot",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 8.3
        },
        {
          "competencia": "Azure",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Big Data",
          "area": "dados",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Cloud Computing",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Deep Learning",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Frameworks Python",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Lógica de Programação",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Machine Learning",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Modelagem de Dados",
          "area": "dados",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Programação Orientada a Objetos",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Redes de Computadores",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "Storytelling com Dados",
          "area": "dados",
          "frequencia": 1,
          "pct_vagas": 4.2
        },
        {
          "competencia": "UML",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 4.2
        }
      ],
      "kpis": {
        "salario_mediano": 5500,
        "salario_n": 23
      },
      "graficos": {
        "radar": {
          "eixos": [
            "Git",
            "Python",
            "CSS",
            "SQL",
            "APIs REST",
            "Docker"
          ],
          "mercado": [
            33.3,
            29.2,
            20.8,
            54.2,
            41.7,
            41.7
          ],
          "curso": [
            33.3,
            29.2,
            20.8,
            0.0,
            0.0,
            0.0
          ]
        },
        "top_tecnologias": {
          "competencias": [
            "SQL",
            "APIs REST",
            "Docker",
            "Git",
            "Python",
            "Testes Automatizados",
            "CSS",
            "HTML",
            "Excel",
            "Inglês Técnico"
          ],
          "pct": [
            54.2,
            41.7,
            41.7,
            33.3,
            29.2,
            29.2,
            20.8,
            20.8,
            16.7,
            16.7
          ],
          "cobertas": [
            false,
            false,
            false,
            true,
            true,
            false,
            true,
            true,
            false,
            false
          ]
        },
        "vagas_semana": {
          "semanas": [
            "2026-W38",
            "2026-W39",
            "2026-W40",
            "2026-W41",
            "2026-W42",
            "2026-W43"
          ],
          "total": [
            1,
            3,
            5,
            6,
            5,
            4
          ]
        },
        "matriz": {
          "competencias": [
            "SQL",
            "APIs REST",
            "Docker",
            "Git",
            "Python",
            "Testes Automatizados",
            "CSS",
            "HTML",
            "Excel",
            "Inglês Técnico",
            "Metodologias Ágeis",
            "TypeScript",
            "Firebase",
            "Java",
            "JavaScript"
          ],
          "linhas": [
            {
              "modulo": "Fundamentos de IA Generativa",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Engenharia e Diretivas de Projeto",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "UI/UX e Design System",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Mineração de Dados e RAG",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Web Scraping",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Multi-agentes e Gemini API",
              "valores": [
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Banco Realtime NoSQL",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0
              ]
            },
            {
              "modulo": "Governança e Segurança de Credenciais",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "CI/CD e Deploy em Nuvem",
              "valores": [
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Analytics e Visualizações",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            }
          ]
        }
      },
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "qualificacao-em-infraestrutura-e-nuvem": {
      "curso": "Qualificação em Infraestrutura e Nuvem",
      "areas_foco": [
        "infraestrutura",
        "seguranca"
      ],
      "amostra_n": 6,
      "total_coletadas": 30,
      "cobertura_pct": 43.8,
      "cobertura_ponderada_pct": 62.9,
      "lacunas": [
        {
          "competencia": "AWS",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 33.3
        },
        {
          "competencia": "Infraestrutura como Código",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 33.3
        },
        {
          "competencia": "Inglês Técnico",
          "area": "geral",
          "frequencia": 2,
          "pct_vagas": 33.3
        },
        {
          "competencia": "Kubernetes",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 33.3
        },
        {
          "competencia": "Azure",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 16.7
        },
        {
          "competencia": "CI/CD",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 16.7
        },
        {
          "competencia": "Docker",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 16.7
        },
        {
          "competencia": "LGPD",
          "area": "seguranca",
          "frequencia": 1,
          "pct_vagas": 16.7
        },
        {
          "competencia": "Microsserviços",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 16.7
        }
      ],
      "kpis": {
        "salario_mediano": 7750,
        "salario_n": 5
      },
      "graficos": {
        "radar": {
          "eixos": [
            "Linux",
            "Monitoramento e Logs",
            "Redes de Computadores",
            "AWS",
            "Infraestrutura como Código",
            "Inglês Técnico"
          ],
          "mercado": [
            83.3,
            66.7,
            66.7,
            33.3,
            33.3,
            33.3
          ],
          "curso": [
            83.3,
            66.7,
            66.7,
            0.0,
            0.0,
            0.0
          ]
        },
        "top_tecnologias": {
          "competencias": [
            "Linux",
            "Monitoramento e Logs",
            "Redes de Computadores",
            "TCP/IP",
            "AWS",
            "Cloud Computing",
            "Infraestrutura como Código",
            "Inglês Técnico",
            "Kubernetes",
            "Segurança da Informação"
          ],
          "pct": [
            83.3,
            66.7,
            66.7,
            50.0,
            33.3,
            33.3,
            33.3,
            33.3,
            33.3,
            33.3
          ],
          "cobertas": [
            true,
            true,
            true,
            true,
            false,
            true,
            false,
            false,
            false,
            true
          ]
        },
        "vagas_semana": {
          "semanas": [
            "2026-W38",
            "2026-W39",
            "2026-W40",
            "2026-W41",
            "2026-W42"
          ],
          "total": [
            1,
            1,
            1,
            1,
            2
          ]
        },
        "matriz": {
          "competencias": [
            "Linux",
            "Monitoramento e Logs",
            "Redes de Computadores",
            "TCP/IP",
            "AWS",
            "Cloud Computing",
            "Infraestrutura como Código",
            "Inglês Técnico",
            "Kubernetes",
            "Segurança da Informação",
            "Shell Script",
            "Azure",
            "CI/CD",
            "Docker",
            "LGPD"
          ],
          "linhas": [
            {
              "modulo": "Redes de Computadores",
              "valores": [
                0,
                0,
                1,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Administração de Linux",
              "valores": [
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Fundamentos de Nuvem",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Segurança de Redes",
              "valores": [
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0
              ]
            }
          ]
        }
      },
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "tecnico-em-desenvolvimento-de-sistemas": {
      "curso": "Técnico em Desenvolvimento de Sistemas",
      "areas_foco": [
        "desenvolvimento"
      ],
      "amostra_n": 17,
      "total_coletadas": 30,
      "cobertura_pct": 48.6,
      "cobertura_ponderada_pct": 66.4,
      "lacunas": [
        {
          "competencia": "TypeScript",
          "area": "desenvolvimento",
          "frequencia": 4,
          "pct_vagas": 23.5
        },
        {
          "competencia": "Firebase",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 17.6
        },
        {
          "competencia": "Inglês Técnico",
          "area": "geral",
          "frequencia": 3,
          "pct_vagas": 17.6
        },
        {
          "competencia": "Microsserviços",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 17.6
        },
        {
          "competencia": "React",
          "area": "desenvolvimento",
          "frequencia": 3,
          "pct_vagas": 17.6
        },
        {
          "competencia": ".NET",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "Banco de Dados NoSQL",
          "area": "dados",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "CI/CD",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "Kubernetes",
          "area": "infraestrutura",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "PHP",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "Python",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "Spring Boot",
          "area": "desenvolvimento",
          "frequencia": 2,
          "pct_vagas": 11.8
        },
        {
          "competencia": "AWS",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 5.9
        },
        {
          "competencia": "Azure",
          "area": "infraestrutura",
          "frequencia": 1,
          "pct_vagas": 5.9
        },
        {
          "competencia": "Design System",
          "area": "design",
          "frequencia": 1,
          "pct_vagas": 5.9
        },
        {
          "competencia": "Frameworks Python",
          "area": "desenvolvimento",
          "frequencia": 1,
          "pct_vagas": 5.9
        },
        {
          "competencia": "IA Generativa",
          "area": "ia",
          "frequencia": 1,
          "pct_vagas": 5.9
        },
        {
          "competencia": "Web Scraping",
          "area": "dados",
          "frequencia": 1,
          "pct_vagas": 5.9
        }
      ],
      "kpis": {
        "salario_mediano": 5250,
        "salario_n": 16
      },
      "graficos": {
        "radar": {
          "eixos": [
            "APIs REST",
            "Git",
            "SQL",
            "TypeScript",
            "Firebase",
            "Inglês Técnico"
          ],
          "mercado": [
            52.9,
            47.1,
            47.1,
            23.5,
            17.6,
            17.6
          ],
          "curso": [
            52.9,
            47.1,
            47.1,
            0.0,
            0.0,
            0.0
          ]
        },
        "top_tecnologias": {
          "competencias": [
            "APIs REST",
            "Git",
            "SQL",
            "Docker",
            "Testes Automatizados",
            "CSS",
            "HTML",
            "Metodologias Ágeis",
            "TypeScript",
            "Firebase"
          ],
          "pct": [
            52.9,
            47.1,
            47.1,
            41.2,
            41.2,
            29.4,
            29.4,
            23.5,
            23.5,
            17.6
          ],
          "cobertas": [
            true,
            true,
            true,
            true,
            true,
            true,
            true,
            true,
            false,
            false
          ]
        },
        "vagas_semana": {
          "semanas": [
            "2026-W38",
            "2026-W39",
            "2026-W40",
            "2026-W41",
            "2026-W42",
            "2026-W43"
          ],
          "total": [
            1,
            3,
            4,
            4,
            2,
            3
          ]
        },
        "matriz": {
          "competencias": [
            "APIs REST",
            "Git",
            "SQL",
            "Docker",
            "Testes Automatizados",
            "CSS",
            "HTML",
            "Metodologias Ágeis",
            "TypeScript",
            "Firebase",
            "Inglês Técnico",
            "Java",
            "JavaScript",
            "Microsserviços",
            "Node.js"
          ],
          "linhas": [
            {
              "modulo": "Lógica de Programação",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Programação Orientada a Objetos",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Banco de Dados Relacional",
              "valores": [
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Desenvolvimento Web Front-end",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0
              ]
            },
            {
              "modulo": "Desenvolvimento Web Back-end",
              "valores": [
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1
              ]
            },
            {
              "modulo": "Versionamento e Metodologias Ágeis",
              "valores": [
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Engenharia de Software",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Desenvolvimento Mobile",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Segurança no Desenvolvimento",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Contêineres e Implantação",
              "valores": [
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Testes de Software",
              "valores": [
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            },
            {
              "modulo": "Design de Interfaces",
              "valores": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            }
          ]
        }
      },
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    }
  },
  "trilhas_sugeridas": {
    "qualificacao-em-analise-de-dados": {
      "curso": "Qualificação em Análise de Dados",
      "modulos": [
        {
          "curso": "Técnico em Desenvolvimento de Sistemas",
          "modulo": "Contêineres e Implantação",
          "motivo": "Módulo com 40h práticas cobrindo as lacunas: Docker.",
          "carga_horaria": 40,
          "competencias_cobertas": [
            "Docker"
          ],
          "peso": 3
        },
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "Fundamentos de IA Generativa",
          "motivo": "Módulo com 16h práticas cobrindo as lacunas: Engenharia de Prompt, IA Generativa.",
          "carga_horaria": 16,
          "competencias_cobertas": [
            "Engenharia de Prompt",
            "IA Generativa"
          ],
          "peso": 2
        },
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "Mineração de Dados e RAG",
          "motivo": "Módulo com 16h práticas cobrindo as lacunas: RAG.",
          "carga_horaria": 16,
          "competencias_cobertas": [
            "RAG"
          ],
          "peso": 1
        }
      ],
      "sem_modulo": [
        "AWS",
        "Big Data",
        "Deep Learning",
        "Inglês Técnico"
      ],
      "aderencia_antes_pct": 66.3,
      "aderencia_depois_pct": 78.6,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "qualificacao-em-ia-generativa": {
      "curso": "Qualificação em IA Generativa",
      "modulos": [
        {
          "curso": "Qualificação em Análise de Dados",
          "modulo": "SQL para Análise",
          "motivo": "Módulo com 60h práticas cobrindo as lacunas: Modelagem de Dados, SQL.",
          "carga_horaria": 60,
          "competencias_cobertas": [
            "Modelagem de Dados",
            "SQL"
          ],
          "peso": 14
        },
        {
          "curso": "Técnico em Desenvolvimento de Sistemas",
          "modulo": "Desenvolvimento Web Back-end",
          "motivo": "Módulo com 100h práticas cobrindo as lacunas: APIs REST, Node.js.",
          "carga_horaria": 100,
          "competencias_cobertas": [
            "APIs REST",
            "Node.js"
          ],
          "peso": 13
        },
        {
          "curso": "Técnico em Desenvolvimento de Sistemas",
          "modulo": "Contêineres e Implantação",
          "motivo": "Módulo com 40h práticas cobrindo as lacunas: Docker.",
          "carga_horaria": 40,
          "competencias_cobertas": [
            "Docker"
          ],
          "peso": 10
        }
      ],
      "sem_modulo": [
        ".NET",
        "AWS",
        "Azure",
        "Big Data",
        "Deep Learning",
        "Frameworks Python",
        "Inglês Técnico",
        "Kubernetes",
        "Microsserviços",
        "PHP",
        "React",
        "Spring Boot",
        "TypeScript"
      ],
      "aderencia_antes_pct": 31.1,
      "aderencia_depois_pct": 54.1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "qualificacao-em-infraestrutura-e-nuvem": {
      "curso": "Qualificação em Infraestrutura e Nuvem",
      "modulos": [
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "CI/CD e Deploy em Nuvem",
          "motivo": "Módulo com 12h práticas cobrindo as lacunas: CI/CD.",
          "carga_horaria": 12,
          "competencias_cobertas": [
            "CI/CD"
          ],
          "peso": 1
        },
        {
          "curso": "Técnico em Desenvolvimento de Sistemas",
          "modulo": "Contêineres e Implantação",
          "motivo": "Módulo com 40h práticas cobrindo as lacunas: Docker.",
          "carga_horaria": 40,
          "competencias_cobertas": [
            "Docker"
          ],
          "peso": 1
        },
        {
          "curso": "Técnico em Desenvolvimento de Sistemas",
          "modulo": "Segurança no Desenvolvimento",
          "motivo": "Módulo com 40h práticas cobrindo as lacunas: LGPD.",
          "carga_horaria": 40,
          "competencias_cobertas": [
            "LGPD"
          ],
          "peso": 1
        }
      ],
      "sem_modulo": [
        "AWS",
        "Azure",
        "Infraestrutura como Código",
        "Inglês Técnico",
        "Kubernetes",
        "Microsserviços"
      ],
      "aderencia_antes_pct": 73.0,
      "aderencia_depois_pct": 80.1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "tecnico-em-desenvolvimento-de-sistemas": {
      "curso": "Técnico em Desenvolvimento de Sistemas",
      "modulos": [
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "Banco Realtime NoSQL",
          "motivo": "Módulo com 12h práticas cobrindo as lacunas: Banco de Dados NoSQL, Firebase.",
          "carga_horaria": 12,
          "competencias_cobertas": [
            "Banco de Dados NoSQL",
            "Firebase"
          ],
          "peso": 5
        },
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "CI/CD e Deploy em Nuvem",
          "motivo": "Módulo com 12h práticas cobrindo as lacunas: CI/CD.",
          "carga_horaria": 12,
          "competencias_cobertas": [
            "CI/CD"
          ],
          "peso": 2
        },
        {
          "curso": "Qualificação em IA Generativa",
          "modulo": "Multi-agentes e Gemini API",
          "motivo": "Módulo com 16h práticas cobrindo as lacunas: Python.",
          "carga_horaria": 16,
          "competencias_cobertas": [
            "Python"
          ],
          "peso": 2
        }
      ],
      "sem_modulo": [
        ".NET",
        "AWS",
        "Azure",
        "Frameworks Python",
        "Inglês Técnico",
        "Kubernetes",
        "Microsserviços",
        "PHP",
        "React",
        "Spring Boot",
        "TypeScript"
      ],
      "aderencia_antes_pct": 68.1,
      "aderencia_depois_pct": 76.4,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    }
  },
  "insights": {
    "coordenacao-qualificacao-em-analise-de-dados-1": {
      "id": "coordenacao-qualificacao-em-analise-de-dados-1",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-analise-de-dados",
      "titulo": "Oportunidade de Atualização",
      "texto": "Docker é a maior lacuna da área, presente em 3 de 7 vagas, e é ensinada em Contêineres e Implantação.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-analise-de-dados-2": {
      "id": "coordenacao-qualificacao-em-analise-de-dados-2",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-analise-de-dados",
      "titulo": "Impacto da Trilha Recomendada",
      "texto": "Os 3 módulos da trilha elevam a aderência média de 66.3% para 78.6%.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-analise-de-dados-3": {
      "id": "coordenacao-qualificacao-em-analise-de-dados-3",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-analise-de-dados",
      "titulo": "Amostra de Mercado Regional",
      "texto": "Métricas calculadas a partir de 7 vagas do setor tecnológico de Ourinhos e região.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-ia-generativa-1": {
      "id": "coordenacao-qualificacao-em-ia-generativa-1",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-ia-generativa",
      "titulo": "Oportunidade de Atualização",
      "texto": "SQL é a maior lacuna da área, presente em 13 de 24 vagas, e é ensinada em SQL para Análise.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-ia-generativa-2": {
      "id": "coordenacao-qualificacao-em-ia-generativa-2",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-ia-generativa",
      "titulo": "Impacto da Trilha Recomendada",
      "texto": "Os 3 módulos da trilha elevam a aderência média de 31.1% para 54.1%.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-ia-generativa-3": {
      "id": "coordenacao-qualificacao-em-ia-generativa-3",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-ia-generativa",
      "titulo": "Amostra de Mercado Regional",
      "texto": "Métricas calculadas a partir de 24 vagas do setor tecnológico de Ourinhos e região.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-infraestrutura-e-nuvem-1": {
      "id": "coordenacao-qualificacao-em-infraestrutura-e-nuvem-1",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-infraestrutura-e-nuvem",
      "titulo": "Demanda Externa Não Coberta",
      "texto": "AWS aparece em 2 de 6 vagas e não é ensinada em nenhum módulo da base.",
      "severidade": "aviso",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-infraestrutura-e-nuvem-2": {
      "id": "coordenacao-qualificacao-em-infraestrutura-e-nuvem-2",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-infraestrutura-e-nuvem",
      "titulo": "Impacto da Trilha Recomendada",
      "texto": "Os 3 módulos da trilha elevam a aderência média de 73.0% para 80.1%.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-qualificacao-em-infraestrutura-e-nuvem-3": {
      "id": "coordenacao-qualificacao-em-infraestrutura-e-nuvem-3",
      "escopo": "coordenacao",
      "curso": "qualificacao-em-infraestrutura-e-nuvem",
      "titulo": "Amostra de Mercado Regional",
      "texto": "Métricas calculadas a partir de 6 vagas do setor tecnológico de Ourinhos e região.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-tecnico-em-desenvolvimento-de-sistemas-1": {
      "id": "coordenacao-tecnico-em-desenvolvimento-de-sistemas-1",
      "escopo": "coordenacao",
      "curso": "tecnico-em-desenvolvimento-de-sistemas",
      "titulo": "Demanda Externa Não Coberta",
      "texto": "TypeScript aparece em 4 de 17 vagas e não é ensinada em nenhum módulo da base.",
      "severidade": "aviso",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-tecnico-em-desenvolvimento-de-sistemas-2": {
      "id": "coordenacao-tecnico-em-desenvolvimento-de-sistemas-2",
      "escopo": "coordenacao",
      "curso": "tecnico-em-desenvolvimento-de-sistemas",
      "titulo": "Impacto da Trilha Recomendada",
      "texto": "Os 3 módulos da trilha elevam a aderência média de 68.1% para 76.4%.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "coordenacao-tecnico-em-desenvolvimento-de-sistemas-3": {
      "id": "coordenacao-tecnico-em-desenvolvimento-de-sistemas-3",
      "escopo": "coordenacao",
      "curso": "tecnico-em-desenvolvimento-de-sistemas",
      "titulo": "Amostra de Mercado Regional",
      "texto": "Métricas calculadas a partir de 17 vagas do setor tecnológico de Ourinhos e região.",
      "severidade": "info",
      "origem": "template",
      "criado_em": "2026-10-24T11:24:14.986794-03:00"
    }
  },
  "competencias_demandadas": {
    "react": {
      "competencia": "React",
      "area": "desenvolvimento",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "nodejs": {
      "competencia": "Node.js",
      "area": "desenvolvimento",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "typescript": {
      "competencia": "TypeScript",
      "area": "desenvolvimento",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "apis-rest": {
      "competencia": "APIs REST",
      "area": "desenvolvimento",
      "frequencia": 10,
      "pct_vagas": 33.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "sql": {
      "competencia": "SQL",
      "area": "dados",
      "frequencia": 13,
      "pct_vagas": 43.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "git": {
      "competencia": "Git",
      "area": "desenvolvimento",
      "frequencia": 8,
      "pct_vagas": 26.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "docker": {
      "competencia": "Docker",
      "area": "infraestrutura",
      "frequencia": 11,
      "pct_vagas": 36.7,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "java": {
      "competencia": "Java",
      "area": "desenvolvimento",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "spring-boot": {
      "competencia": "Spring Boot",
      "area": "desenvolvimento",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "microsservicos": {
      "competencia": "Microsserviços",
      "area": "desenvolvimento",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "kubernetes": {
      "competencia": "Kubernetes",
      "area": "infraestrutura",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "testes-automatizados": {
      "competencia": "Testes Automatizados",
      "area": "desenvolvimento",
      "frequencia": 7,
      "pct_vagas": 23.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "cicd": {
      "competencia": "CI/CD",
      "area": "infraestrutura",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "ingles-tecnico": {
      "competencia": "Inglês Técnico",
      "area": "geral",
      "frequencia": 6,
      "pct_vagas": 20.0,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "logica-de-programacao": {
      "competencia": "Lógica de Programação",
      "area": "desenvolvimento",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "html": {
      "competencia": "HTML",
      "area": "desenvolvimento",
      "frequencia": 5,
      "pct_vagas": 16.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "css": {
      "competencia": "CSS",
      "area": "desenvolvimento",
      "frequencia": 5,
      "pct_vagas": 16.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "javascript": {
      "competencia": "JavaScript",
      "area": "desenvolvimento",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "python": {
      "competencia": "Python",
      "area": "desenvolvimento",
      "frequencia": 7,
      "pct_vagas": 23.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "pandas": {
      "competencia": "Pandas",
      "area": "dados",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "visualizacao-de-dados": {
      "competencia": "Visualização de Dados",
      "area": "dados",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "power-bi": {
      "competencia": "Power BI",
      "area": "dados",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "estatistica": {
      "competencia": "Estatística",
      "area": "dados",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "excel": {
      "competencia": "Excel",
      "area": "dados",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "storytelling-com-dados": {
      "competencia": "Storytelling com Dados",
      "area": "dados",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "redes-de-computadores": {
      "competencia": "Redes de Computadores",
      "area": "infraestrutura",
      "frequencia": 5,
      "pct_vagas": 16.7,
      "variacao_semana": -2,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "tcpip": {
      "competencia": "TCP/IP",
      "area": "infraestrutura",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "linux": {
      "competencia": "Linux",
      "area": "infraestrutura",
      "frequencia": 5,
      "pct_vagas": 16.7,
      "variacao_semana": -2,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "monitoramento-e-logs": {
      "competencia": "Monitoramento e Logs",
      "area": "infraestrutura",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "cloud-computing": {
      "competencia": "Cloud Computing",
      "area": "infraestrutura",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "aws": {
      "competencia": "AWS",
      "area": "infraestrutura",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "infraestrutura-como-codigo": {
      "competencia": "Infraestrutura como Código",
      "area": "infraestrutura",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "shell-script": {
      "competencia": "Shell Script",
      "area": "infraestrutura",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "uxui-design": {
      "competencia": "UX/UI Design",
      "area": "design",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "desenvolvimento-mobile": {
      "competencia": "Desenvolvimento Mobile",
      "area": "desenvolvimento",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "firebase": {
      "competencia": "Firebase",
      "area": "desenvolvimento",
      "frequencia": 3,
      "pct_vagas": 10.0,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "metodologias-ageis": {
      "competencia": "Metodologias Ágeis",
      "area": "gestao",
      "frequencia": 4,
      "pct_vagas": 13.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "machine-learning": {
      "competencia": "Machine Learning",
      "area": "ia",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "deep-learning": {
      "competencia": "Deep Learning",
      "area": "ia",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "php": {
      "competencia": "PHP",
      "area": "desenvolvimento",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "programacao-orientada-a-objetos": {
      "competencia": "Programação Orientada a Objetos",
      "area": "desenvolvimento",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": -1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "net": {
      "competencia": ".NET",
      "area": "desenvolvimento",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "azure": {
      "competencia": "Azure",
      "area": "infraestrutura",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "ia-generativa": {
      "competencia": "IA Generativa",
      "area": "ia",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "engenharia-de-prompt": {
      "competencia": "Engenharia de Prompt",
      "area": "ia",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "rag": {
      "competencia": "RAG",
      "area": "ia",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "agentes-de-ia": {
      "competencia": "Agentes de IA",
      "area": "ia",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 1,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "modelagem-de-dados": {
      "competencia": "Modelagem de Dados",
      "area": "dados",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "etl": {
      "competencia": "ETL",
      "area": "dados",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "frameworks-python": {
      "competencia": "Frameworks Python",
      "area": "desenvolvimento",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "banco-de-dados-nosql": {
      "competencia": "Banco de Dados NoSQL",
      "area": "dados",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "seguranca-da-informacao": {
      "competencia": "Segurança da Informação",
      "area": "seguranca",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "lgpd": {
      "competencia": "LGPD",
      "area": "seguranca",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "uml": {
      "competencia": "UML",
      "area": "desenvolvimento",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "levantamento-de-requisitos": {
      "competencia": "Levantamento de Requisitos",
      "area": "gestao",
      "frequencia": 2,
      "pct_vagas": 6.7,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "design-system": {
      "competencia": "Design System",
      "area": "design",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "big-data": {
      "competencia": "Big Data",
      "area": "dados",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    },
    "web-scraping": {
      "competencia": "Web Scraping",
      "area": "dados",
      "frequencia": 1,
      "pct_vagas": 3.3,
      "variacao_semana": 0,
      "atualizado_em": "2026-10-24T11:24:14.986794-03:00"
    }
  }
};
