# Diretiva — Repositório via GitHub MCP Server e hospedagem no Vercel

**Pilar do edital:** 8 (Deploy via MCP).
**Quando ler:** só depois de `seguranca.md` estar aprovado e o site local funcionando.

> **Decisão confirmada pelo instrutor:** a hospedagem do site é feita no **Vercel**, no lugar do GitHub Pages.
> **Regra mantida do edital:** o repositório público é criado e recebe os arquivos **pelo servidor MCP do GitHub**, configurado em `mcp_config.json`. O agente não usa `git push` com token no código nem pede ao usuário para subir arquivos manualmente.

## 1. Pontos que o usuário precisa confirmar com o instrutor

1. Qual servidor MCP do GitHub a turma usa (o oficial remoto do GitHub ou um servidor local via Docker/npx).
2. Onde o Antigravity da turma lê o `mcp_config.json`.
3. Se o link do repositório deve estar ligado ao Vercel (importação pelo painel) ou se a turma usa outro procedimento (por exemplo, o Vercel CLI).

O agente deve **parar e perguntar** se qualquer um desses pontos estiver indefinido, em vez de inventar um caminho.

## 2. Configuração do MCP (feita pelo usuário)

Crie o token: GitHub → *Settings → Developer settings → Personal access tokens*. Escopo mínimo para criar repositório e enviar arquivos (token clássico: `repo`; fine-grained: escrita em *Contents* e *Administration*). **Validade curta** (7 dias) e **revogue após a entrega**.

Arquivo versionado de exemplo, `mcp_config.example.json`, com valor falso:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "COLE_SEU_TOKEN_AQUI" }
    }
  }
}
```

Variante com servidor remoto (se a turma usar):

```json
{
  "mcpServers": {
    "github": {
      "serverUrl": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer COLE_SEU_TOKEN_AQUI" }
    }
  }
}
```

O formato exato depende da versão do Antigravity e do servidor. O `mcp_config.json` **real** fica na pasta de configuração do usuário (ou, se precisar ficar no projeto, está no `.gitignore`). O agente não imprime o conteúdo dele.

## 3. Estrutura publicada

```
README.md
projeto.md  ideia-projeto.md  ideia-design.md
Directives/
Execution/
data/            (somente os CSVs; sem dados pessoais)
tests/
docs/            (o site; é a pasta servida pelo Vercel)
vercel.json
.gitignore  .env.example  mcp_config.example.json  requirements.txt  firestore.rules
```

Nunca vai: `.env`, `.temp/`, `mcp_config.json`, JSON da conta de serviço, `.venv/`, `.vercel/`.

## 4. Site em `docs/` e configuração do Vercel

- `docs/index.html`, `docs/css/`, `docs/js/` (`theme.js`, `views.js`, `charts.js`, `firebase.js`, `app.js`, `config.js`).
- Site **estático, sem build**. Plotly e Firebase SDK por CDN com versão fixa. Só recursos HTTPS.
- Caminhos relativos (`css/estilo.css`) funcionam no Vercel e na abertura local.
- `vercel.json` na raiz, com o mínimo necessário:

```json
{
  "outputDirectory": "docs",
  "buildCommand": null,
  "cleanUrls": true
}
```

- No painel do Vercel, ao importar o repositório: *Framework Preset* = **Other**, *Build Command* vazio, *Output Directory* = `docs`.
- Cabeçalhos de segurança podem ser adicionados em `vercel.json` (`headers`), por exemplo `X-Content-Type-Options: nosniff` e `Referrer-Policy: strict-origin-when-cross-origin`. Se for usar `Content-Security-Policy`, teste antes: o Firebase SDK e o Plotly precisam carregar.
- **Nenhuma variável de ambiente é necessária no Vercel.** O site só usa a configuração web do Firebase (pública, em `docs/js/config.js`). **Nunca** cadastre `GEMINI_API_KEY` nem a conta de serviço no Vercel: o site estático não os usa, e o Python roda localmente.

## 5. Fluxo de execução

1. Rodar localmente: testes, `verificar_segredos.py` e abrir o site por um servidor local (`python -m http.server --directory docs`), conferindo a leitura do Firestore.
2. Mostrar ao usuário **a lista de arquivos que serão enviados** e pedir confirmação.
3. Criar o repositório **público** pelo MCP (`create_repository`) com o nome combinado (ex.: `skillradar`).
4. Enviar os arquivos da seção 3 com `push_files` (um commit só, mensagem clara) para a branch `main`.
5. **Passo do usuário:** no Vercel, *Add New → Project → Import Git Repository*, escolher o repositório e usar as configurações da seção 4. O agente orienta e espera a confirmação.
6. Abrir a URL gerada (`https://NOME-DO-PROJETO.vercel.app`) e executar a verificação da seção 6.
7. A partir daí, cada novo commit enviado pelo MCP à branch `main` gera uma nova publicação automática.

## 6. Verificações depois do deploy

- [ ] O repositório é **público** e não contém nenhum segredo (repita a busca da `seguranca.md` §9 no repositório remoto).
- [ ] A URL do Vercel abre por HTTPS e não há erros no console do navegador.
- [ ] A restrição da `apiKey` web por referenciador já inclui o domínio do Vercel (`https://*.vercel.app/*` ou o domínio exato do projeto), senão o Firestore recusa a leitura.
- [ ] Os dois temas funcionam, as duas visões (Aluno e Coordenação) alternam e os 6 gráficos aparecem.
- [ ] O indicador mostra "Atualizado ao vivo"; ao alterar um documento no console do Firebase, a tela muda sem recarregar.
- [ ] Em celular (ou emulação), o layout é usável e a barra inferior funciona.
- [ ] O token do GitHub foi **revogado** depois da entrega.

## 7. Entregáveis do edital

1. Link do repositório público no GitHub.
2. Link público HTTPS do site no Vercel.

Registre ambos no `README.md`.
