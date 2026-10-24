# Diretiva — Dados, Taxonomia e Base RAG

**Pilar do edital:** 3 (Base RAG & Mineração).
**Quando ler:** antes de escrever qualquer código que leia a pasta `data/`.

## 1. Objetivo

Garantir que a base local em `data/` seja lida sempre do mesmo jeito, validada ao carregar e usada como **fonte única de verdade** para três perguntas: o que cada curso ensina, quais competências existem no vocabulário do projeto e quais vagas de demonstração servem de plano B.

## 2. Arquivos da pasta `data/`

| Arquivo | Papel | Linhas |
|---|---|---|
| `competencias_cursos.csv` | O que cada módulo de cada curso ensina (base RAG) | 60 |
| `taxonomia_competencias.csv` | Vocabulário controlado de competências, com sinônimos | 61 |
| `vagas_demo.csv` | Vagas **fictícias** de demonstração (plano B do scraping e massa de testes) | 30 |
| `cursos_areas.csv` | Áreas de foco de cada curso (filtra as vagas antes de calcular cobertura) | 8 |
| `perfil_egressos.csv` | Opcional, sintético e anônimo: `egresso_id, curso, ano, area_atuacao, empregado` | — |
| `README.md` | Dicionário de dados, origem de cada arquivo e data da última conferência | — |

Os quatro primeiros já existem. **Não os reescreva nem "melhore" o conteúdo.** Se algo parecer errado, avise o usuário.

## 3. Esquemas

### 3.1 `competencias_cursos.csv`

| Coluna | Tipo | Valores / regra |
|---|---|---|
| `curso` | texto | 4 cursos: Técnico em Desenvolvimento de Sistemas; Qualificação em IA Generativa; Qualificação em Análise de Dados; Qualificação em Infraestrutura e Nuvem |
| `modulo` | texto | 33 módulos no total |
| `competencia` | texto | **Sempre um nome de `competencia_padrao` da taxonomia** (47 competências distintas) |
| `carga_horaria` | inteiro | Horas **do módulo**. Repete em todas as linhas do mesmo módulo. Para somar horas de um curso, conte cada módulo uma vez |
| `nivel` | texto | `basico` ou `intermediario` (sem acento) |
| `area` | texto | `desenvolvimento`, `dados`, `ia`, `infraestrutura`, `seguranca`, `design`, `gestao` |
| `ferramenta_ensinada` | texto | Ferramenta associada, só informativa |

### 3.2 `taxonomia_competencias.csv`

| Coluna | Descrição |
|---|---|
| `competencia_padrao` | Nome oficial (61): as 47 que os cursos ensinam mais 14 que o mercado pede e a base **não** ensina (React, TypeScript, Kubernetes, AWS, Azure, Spring Boot, .NET, PHP, Microsserviços, Big Data, Deep Learning, Frameworks Python, Infraestrutura como Código, Inglês Técnico) |
| `sinonimos` | Termos alternativos separados por `\|`, em minúsculas |
| `area` | As áreas acima mais `geral` (usada só por Inglês Técnico) |

As 14 competências não ensinadas são **necessárias**: sem elas o sistema nunca conseguiria apontar uma lacuna.

### 3.3 `vagas_demo.csv`

Colunas: `vaga_id, titulo, empresa, cidade, data, salario_min, salario_max, fonte_url, requisitos_texto, competencias_esperadas, senioridade, coletado_em`.

- `requisitos_texto` é a **entrada do Agente Extrator** nos testes.
- `competencias_esperadas` (separadas por `|`) é o **gabarito**: serve para medir o Extrator e para alimentar o Matcher no modo demo. Nunca exiba essa coluna ao usuário final.
- `V029` e `V030` não têm salário (campos vazios). Trate como `null`, nunca como zero.
- Empresas são "Empresa Demo NN" e `fonte_url` usa o domínio reservado `exemplo.invalid`. **Todo dado vindo deste arquivo deve ser marcado como demonstração** (`modo_demo = true` no Firestore e a frase "Dados de demonstração" na interface).

### 3.4 `cursos_areas.csv`

Mapeia cada curso às áreas de foco (`curso, area_foco`; um curso pode ter várias linhas). O Matcher só considera as vagas cuja área principal esteja nas áreas de foco do curso. Sem esse filtro, um curso de infraestrutura seria medido contra vagas de programação e a cobertura ficaria artificialmente baixa.

## 4. Área principal de uma vaga

Calcule em Python, de forma determinística:

1. Para cada competência da vaga, pegue a `area` na taxonomia.
2. Ignore a área `geral`.
3. A área com mais competências vence.
4. Empate: use esta ordem fixa de prioridade: `desenvolvimento`, `dados`, `ia`, `infraestrutura`, `seguranca`, `design`, `gestao`.
5. Se a vaga só tiver competências `geral`, a área é `geral`.

Resultado esperado para as 30 vagas de demonstração: `desenvolvimento` 17, `dados` 6, `infraestrutura` 6, `ia` 1.

## 5. Regras de leitura

- Use `pandas.read_csv(caminho, dtype=str, keep_default_na=False, encoding="utf-8")` e converta os tipos depois. Assim, valores como "NA" ou campos vazios não viram `NaN` sem aviso.
- Use `pathlib` para caminhos (o projeto roda em Windows).
- **Normalização para comparar nomes:** minúsculas, sem acento, espaços únicos. Guarde o nome de exibição original e compare só pela forma normalizada.
- Um campo `|` separa listas dentro de uma célula. Remova itens vazios e repetidos mantendo a ordem.

## 6. Correspondência de sinônimos (usada pelo extrator de plano B e nos testes)

Ao procurar termos da taxonomia em um texto:

1. Normalize texto e termos (minúsculas, sem acento).
2. Teste os termos **do mais longo para o mais curto**. Depois de achar um, remova o trecho do texto para que termos menores não casem de novo dentro dele.
3. Exija limites de palavra: o termo não pode ter letra ou número imediatamente antes ou depois (`(?<![a-z0-9])termo(?![a-z0-9])`).
4. Consequências esperadas: "java" **não** casa dentro de "javascript"; "react native" conta como **Desenvolvimento Mobile** e **não** como React; "sql" não casa dentro de "nosql"; "node.js" não vira "node" mais "js".

## 7. Critérios de aceite

- [ ] `competencias_cursos.csv` tem 60 linhas, 33 módulos, 47 competências distintas e a carga horária é igual em todas as linhas de um mesmo módulo.
- [ ] Toda competência de `competencias_cursos.csv` existe na taxonomia, e a taxonomia não tem nomes repetidos.
- [ ] Toda competência da coluna `competencias_esperadas` existe na taxonomia.
- [ ] Rodando a correspondência de sinônimos (seção 6) sobre `requisitos_texto`, o resultado é **igual** a `competencias_esperadas` nas 30 vagas.
- [ ] Contagens globais de demanda: SQL 13, Docker 11, APIs REST 10, Kubernetes 4.
- [ ] Área principal das vagas bate com a seção 4.
- [ ] Testes automatizados cobrem tudo acima e rodam **sem rede e sem chaves**.
