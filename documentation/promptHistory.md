# Histórico de Prompts — SkillRadar

Este documento registra de forma contínua e integral todos os prompts enviados pelo usuário durante o desenvolvimento do projeto SkillRadar, em conformidade com as diretrizes de governança e rastreabilidade da arquitetura de 3 camadas.

---

## Sessão 1: Inicialização e Etapa 0 (Ambiente e Governança)
**Data:** 2026-10-24  
**Agente:** Antigravity Expert — SENAI Ourinhos Edition  

### Prompt 1
```text
/agente-orquestrador /grill-me /goal Você é o agente de desenvolvimento do projeto SkillRadar, deste workspace.

ANTES DE QUALQUER AÇÃO, leia nesta ordem:
1. projeto.md (documento mestre: regras de ouro, arquitetura, plano em etapas)
2. Directives/seguranca/seguranca.md
3. Directives/dados/dados.md
Leia as demais diretivas (scraping, agentes, firestore, desing/design.md, deploy) só quando chegar na etapa que as usa, conforme o plano do projeto.md.
4. Importe o projeto do google stitch
COMO TRABALHAR
- Siga o plano de execução do projeto.md, UMA ETAPA POR VEZ, começando pela Etapa 0.
- Ao fim de cada etapa: rode os testes, confira os critérios de aceite da diretiva correspondente, mostre um resumo curto do que foi feito e do que passou ou falhou, e ESPERE minha confirmação antes de seguir para a próxima.
- Código determinístico (cálculos, leitura de dados, validações) vai em Execution/, com testes em tests/. Nenhum número pode ser calculado pelo Gemini.
- Os arquivos em data/ já existem. Não os altere. Se achar algum erro neles, me avise.
- Os arquivos em Directives/ e os ideia-*.md são a especificação. Não os altere sem me perguntar. Se encontrar contradição ou lacuna, pare e pergunte.
- Interface, textos e comentários em português do Brasil.
- Durante o desenvolvimento, use sempre o modo demo (--modo demo --sem-gemini). O projeto precisa funcionar sem internet e sem chaves.

SEGURANÇA (INEGOCIÁVEL)
- Não peça, não leia, não imprima e não grave chaves, tokens ou JSON de conta de serviço. Nunca escreva valores secretos em arquivos versionados, logs ou mensagens.
- Crie .gitignore e .env.example (sem valores) ANTES do primeiro commit. Quem preenche o .env sou eu, no meu editor.
- Só verifique se as variáveis do .env existem (sim ou não); nunca mostre o conteúdo.
- Use google-genai (não use google-generativeai). O nome do modelo vem de GEMINI_MODEL no .env, nunca escrito no código.

NÃO FAÇA SEM MINHA AUTORIZAÇÃO
- Acessar sites de vagas (primeiro me pergunte qual portal usar e mostre o resultado da checagem do robots.txt).
- Gravar no Firestore (até eu confirmar que o .env e a conta de serviço estão prontos).
- Criar repositório, enviar arquivos ou ativar Pages (isso é a etapa 9, via servidor MCP do GitHub configurado no mcp_config.json).

PONTOS EM ABERTO (veja a seção 9 do projeto.md): se algum deles bloquear o trabalho, pare e me pergunte; não invente um caminho.

PRIMEIRA TAREFA
Execute apenas a Etapa 0 (ambiente: .gitignore, .env.example, requirements.txt, estrutura de pastas Execution/, tests/, docs/, ambiente virtual no Windows/PowerShell). Em seguida, escreva o README.md inicial e me mostre o resumo. Não avance para a Etapa 1 sem meu "pode seguir".

Antes de rodar

Se o Antigravity oferecer um modo de revisão ou planejamento, deixe ligado. Assim você vê o plano antes de ele criar arquivos.
Na etapa 6 (Firestore), tenha pronto o projeto Firebase, o JSON da conta de serviço fora da pasta do projeto e o .env preenchido. Os passos estão no firestore.md.
Na etapa 9 (deploy), tenha o token do GitHub no mcp_config.json, e só depois de resolver com o instrutor os pontos da seção 9 do projeto.md.

Se o agente começar a pular etapas ou pedir chaves, responda: “Releia o projeto.md, seções 2 e 6, e volte para a etapa atual.”
```

### Prompt 2
```text
pode seguir
```

### Prompt 3
```text
pode seguir
```

### Prompt 4
```text
defina o portal público e na sequência pode seguir para Etapa 4
```

### Prompt 5
```text
Pode seguir
```

### Prompt 6
```text
já tenho o .env pode seguir
```

### Prompt 7
```text
Pode seguir
```

### Prompt 8
```text
Pode seguir
```

### Prompt 9
```text
Antes de seguir revise o arquivo .env pois adiconei GEMINI_API_KEI caso seja necessário em algum ponto que ficou faltando
```

### Prompt 10
```text
Ajuste o ponto de atenção 2 e pode seguir para etapa 8
```

### Prompt 11
```text
Antes verifique novamente o arquivo .env e já pode seguir para a Etapa 9
```










