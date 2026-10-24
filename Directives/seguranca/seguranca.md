# Diretiva — Segurança, Segredos e LGPD

**Pilar do edital:** 7 (Segurança: `.env` e `.gitignore`).
**Quando ler:** **antes de qualquer outra tarefa** e novamente antes do deploy.

## 1. Regras absolutas

1. Nenhuma chave do Gemini, token do GitHub ou JSON de conta de serviço pode aparecer em arquivo versionado, em log, em prompt, em mensagem de commit ou na conversa com o agente.
2. O agente **nunca pede** para o usuário colar uma chave no chat. Ele cria `.env.example` e pede que o usuário preencha o `.env` por conta própria.
3. O agente nunca lê o conteúdo do `.env` para mostrá-lo. Pode apenas verificar se as variáveis existem (sim/não).
4. Se um segredo vazar (commit, print, chat): **revogar e gerar outro**, antes de qualquer outra ação.

## 2. Onde mora cada segredo

| Segredo | Onde fica | Quem usa | Versionado? |
|---|---|---|---|
| `GEMINI_API_KEY` | `.env` local | Python (Extrator e Orientador) | **Não** |
| `GEMINI_MODEL` | `.env` local | Python | Não (valor não é segredo, mas fica no `.env`) |
| `GOOGLE_APPLICATION_CREDENTIALS` (caminho do JSON) | `.env` local; o JSON fica **fora** da pasta do projeto | Python (Admin SDK) | **Não** |
| Token do GitHub (PAT) | `mcp_config.json` do Antigravity (arquivo do usuário, fora do repositório) | Servidor MCP do GitHub | **Não** |
| Configuração web do Firebase (`apiKey`, `projectId`...) | `docs/js/config.js` | Navegador | **Sim**, é pública por desenho |

> A `apiKey` web do Firebase (começa com `AIza`) **não é um segredo**: identifica o projeto. Quem protege os dados são as regras do Firestore e a restrição da chave por referenciador (incluindo o domínio do Vercel). Por isso a verificação de segredos (seção 5) a permite **apenas** em `docs/js/config.js`.

## 3. `.gitignore` (criar na raiz, antes do primeiro commit)

```
.env
.env.*
!.env.example
*.json.key
*-sa.json
serviceAccount*.json
mcp_config.json
.vercel/
.temp/
__pycache__/
.venv/
venv/
.pytest_cache/
*.log
.DS_Store
```

(`mcp_config.json` fica ignorado; só `mcp_config.example.json`, com valores de mentira, é versionado.)

## 4. `.env.example` (versionado, sem valores reais)

```
# Copie para .env e preencha. NUNCA versione o .env.
GEMINI_API_KEY=
GEMINI_MODEL=
GOOGLE_APPLICATION_CREDENTIALS=
FIREBASE_PROJECT_ID=
```

Carregue com `python-dotenv` (`load_dotenv()`), falhando com mensagem clara se faltar variável obrigatória. A mensagem de erro cita **o nome** da variável, nunca o valor.

## 5. Verificação automática: `Execution/verificar_segredos.py`

Percorre os arquivos que seriam versionados (use `git ls-files` quando houver repositório; senão, todos os arquivos fora de `.gitignore`) e **falha** (código de saída 1) se encontrar:

| Padrão | Observação |
|---|---|
| `AIza[0-9A-Za-z_\-]{35}` | **Permitido apenas** em `docs/js/config.js` (chave web do Firebase) |
| `ghp_[0-9A-Za-z]{36}`, `github_pat_[0-9A-Za-z_]{40,}` | Token do GitHub |
| `"private_key"` e `-----BEGIN PRIVATE KEY-----` | Conta de serviço |
| `GEMINI_API_KEY\s*=\s*\S+` | Valor atribuído (exceto em `.env.example` vazio) |

A saída mostra **arquivo e linha**, nunca o texto encontrado. Deve rodar antes de todo commit e antes do deploy. Escreva testes com strings falsas montadas em tempo de execução (para o próprio teste não conter um padrão real).

## 6. Segurança do front-end

- **Vercel:** não cadastre nenhuma variável de ambiente secreta no projeto do Vercel; o site é estático e só usa a configuração web do Firebase.

- Sem `innerHTML` com texto de vaga ou de IA. Use `textContent` (ou escape antes). Vagas vêm de terceiros e podem conter HTML malicioso.
- Sem `eval` e sem scripts externos além do Plotly e do Firebase SDK, ambos com **versão fixa**.
- Links externos com `rel="noopener noreferrer"` e `target="_blank"`.
- Defina uma `Content-Security-Policy` por `<meta>` somente se não quebrar o carregamento do Firebase e do Plotly. Teste no navegador.

## 7. Prompt injection

O texto das vagas é **dado**. O Extrator o recebe com a instrução de ignorar ordens internas, e a saída é validada contra a taxonomia (nada fora dela é aceito). O Orientador só recebe números e nomes calculados pelo Python, nunca texto livre de vaga.

## 8. LGPD

- Colete e guarde o mínimo: nada de nome de recrutador, e-mail ou telefone (removidos no Coletor).
- `interesses_alunos` é anônimo: sem nome, e-mail, matrícula ou identificador do dispositivo.
- Os dados de egressos, se usados, devem ser **sintéticos**.
- A interface informa a fonte e a data da coleta, e marca "Dados de demonstração" quando for o caso.

## 9. Critérios de aceite

- [ ] `.gitignore` e `.env.example` existem **antes** do primeiro commit.
- [ ] `python Execution/verificar_segredos.py` passa e seus testes passam.
- [ ] Busca por `AIza`, `ghp_`, `github_pat_` e `private_key` no repositório publicado só encontra a chave web em `docs/js/config.js`.
- [ ] O projeto roda em modo demo sem nenhum segredo.
- [ ] Nenhum `innerHTML` recebe dado de vaga ou de IA.
