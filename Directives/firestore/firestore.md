# Diretiva — Firebase Firestore (tempo real)

**Pilar do edital:** 6 (Firebase Firestore em tempo real).
**Quando ler:** antes de gravar no banco (`Execution/firestore_cliente.py`) e antes de escrever o front-end (`docs/js/firebase.js`).

## 1. Visão

- **Escrita:** só o Python, com o **Firebase Admin SDK** e uma conta de serviço (arquivo JSON local, nunca versionado). O Admin SDK ignora as regras de segurança.
- **Leitura:** o site estático (hospedado no Vercel) lê com o **Firebase Web SDK** usando `onSnapshot`, então a tela se atualiza sozinha quando o Python grava.
- O navegador **não** grava em nenhuma coleção, exceto `interesses_alunos` (anônimo e restrito pelas regras).

## 2. Preparação (feita pelo usuário no console do Firebase)

O agente **não** cria projeto nem chaves. Ele pede ao usuário que:

1. Crie um projeto no Firebase e um banco **Cloud Firestore** (modo de produção, região sugerida `southamerica-east1`).
2. Registre um **app Web** e copie o objeto de configuração (`apiKey`, `authDomain`, `projectId`, `appId`...).
3. Em *Configurações do projeto → Contas de serviço*, gere uma chave privada e salve o JSON **fora do repositório** (ex.: `C:\segredos\skillradar-sa.json`). O caminho vai em `GOOGLE_APPLICATION_CREDENTIALS` no `.env`.
4. Publique as regras da seção 6.
5. Restrinja a `apiKey` web por referenciador HTTP (o domínio do Vercel, ex.: `https://SEU-PROJETO.vercel.app/*`, e também `http://localhost:*` para testes locais) no Google Cloud Console (veja `Directives/seguranca/seguranca.md`).

## 3. Coleções e documentos

Todos os IDs são determinísticos (slug sem acento, minúsculas, hífens; sem `/`). Regravar atualiza.

### 3.1 `contexto/atual`

```json
{
  "total_vagas": 30,
  "ultima_coleta": "2026-10-24T08:15:00-03:00",
  "modo_demo": true,
  "fonte": "vagas_demo.csv",
  "graficos": { "salario_por_area": { "desenvolvimento": [4250, 5250], "dados": [4800] } },
  "atualizado_em": "<serverTimestamp>"
}
```

### 3.2 `vagas_ativas/{vaga_id}`

`vaga_id, titulo, empresa, cidade, data, salario_min, salario_max, fonte_url, competencias[], senioridade, area, modo_demo, coletado_em`. Salário ausente = `null`.

### 3.3 `lacunas_cursos/{cursoSlug}`

IDs: `tecnico-em-desenvolvimento-de-sistemas`, `qualificacao-em-ia-generativa`, `qualificacao-em-analise-de-dados`, `qualificacao-em-infraestrutura-e-nuvem`.

```json
{
  "curso": "Técnico em Desenvolvimento de Sistemas",
  "areas_foco": ["desenvolvimento"],
  "amostra_n": 17,
  "total_coletadas": 30,
  "competencias_demandadas": 35,
  "competencias_cobertas": 17,
  "cobertura_pct": 48.6,
  "cobertura_ponderada_pct": 66.4,
  "lacunas": [ { "competencia": "TypeScript", "area": "desenvolvimento", "frequencia": 4, "pct_vagas": 23.5 } ],
  "kpis": { "salario_mediano": 5250, "salario_n": 16 },
  "graficos": {
    "radar": { "eixos": [], "mercado": [], "curso": [] },
    "top_tecnologias": { "competencias": [], "pct": [], "cobertas": [] },
    "vagas_semana": { "semanas": [], "total": [] },
    "matriz": { "competencias": [], "linhas": [ { "modulo": "string", "valores": [1, 0] } ] }
  },
  "atualizado_em": "<serverTimestamp>"
}
```

Os números do exemplo são os do curso Técnico em Desenvolvimento de Sistemas com as vagas de demonstração (veja a tabela de referência em `Directives/agentes/agentes.md` §8).

### 3.4 `trilhas_sugeridas/{cursoSlug}`

```json
{
  "curso": "string",
  "modulos": [ { "curso": "string", "modulo": "string", "carga_horaria": 12, "competencias_cobertas": ["Firebase"], "peso": 3, "motivo": "string" } ],
  "sem_modulo": ["TypeScript"],
  "aderencia_antes_pct": 68.1,
  "aderencia_depois_pct": 76.4,
  "atualizado_em": "<serverTimestamp>"
}
```

### 3.5 `insights/{id}`

`escopo` (`aluno`, `coordenacao` ou `geral`), `curso` (slug ou `null`), `titulo`, `texto`, `severidade` (`info`, `aviso`, `critico`), `origem` (`gemini` ou `template`), `criado_em`. ID = `{escopo}-{cursoSlug|geral}-{n}`, assim cada rodada **substitui** os anteriores em vez de acumular.

### 3.6 `competencias_demandadas/{competenciaSlug}` (global, para tendência)

`competencia, area, frequencia, pct_vagas, variacao_semana, atualizado_em`.

### 3.7 `interesses_alunos/{autoId}` (única escrita pública)

`curso_interesse` (slug), `nivel` (`iniciante`, `intermediario`, `avancado`), `areas[]`, `criado_em` (`serverTimestamp`). Nenhum dado pessoal.

## 4. Restrições do Firestore que o código deve respeitar

- **Sem arrays dentro de arrays.** Por isso `matriz.linhas` é lista de mapas.
- Documento com no máximo 1 MiB (os documentos acima ficam muito abaixo).
- `null` é aceito; `NaN` e `Infinity` não. Converta antes de gravar.
- Lote (`batch`) com no máximo 500 operações; divida lotes maiores.
- Datas como string ISO em `data` e `coletado_em`; `atualizado_em` e `criado_em` com `SERVER_TIMESTAMP`.

## 5. Código de referência

### 5.1 Python (gravação)

```python
import os
import firebase_admin
from firebase_admin import credentials, firestore

def obter_db():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        firebase_admin.initialize_app(cred)
    return firestore.client()

def gravar_lote(db, operacoes):
    """operacoes: lista de (caminho 'colecao/id', dict). Divide em lotes de até 500."""
    for i in range(0, len(operacoes), 500):
        lote = db.batch()
        for caminho, dados in operacoes[i:i + 500]:
            lote.set(db.document(caminho), dados)
        lote.commit()
```

### 5.2 Front-end (leitura em tempo real)

`docs/js/firebase.js` importa o SDK modular por URL de CDN com **versão fixa** (confira a versão atual e fixe-a em uma constante `VERSAO`):

```javascript
const VERSAO = "COLOQUE_A_VERSAO_ATUAL_AQUI";
const base = `https://www.gstatic.com/firebasejs/${VERSAO}`;
const { initializeApp } = await import(`${base}/firebase-app.js`);
const { getFirestore, doc, collection, query, where, orderBy, limit, onSnapshot, addDoc, serverTimestamp } =
  await import(`${base}/firebase-firestore.js`);

const app = initializeApp(window.SKILLRADAR_CONFIG);   // vem de docs/js/config.js
const db = getFirestore(app);

export function ouvirCurso(slug, aoReceber, aoFalhar) {
  return onSnapshot(doc(db, "lacunas_cursos", slug),
    (snap) => aoReceber(snap.exists() ? snap.data() : null),
    aoFalhar);
}
```

- Cada `onSnapshot` retorna uma função de cancelamento. Ao trocar o curso em `#selectCurso`, **chame-a** antes de abrir os novos listeners.
- Primeiro snapshot: troca o `.skeleton` pelo conteúdo. Erro: `.state-error` e `#liveIndicator` em "Sem conexão".
- Para a aba do navegador: conectar `onSnapshot` de `contexto/atual`, `lacunas_cursos/{slug}`, `trilhas_sugeridas/{slug}`, `vagas_ativas` (limite 100) e `insights` (filtrados por `escopo` e `curso`, os 3 mais recentes).
- `docs/js/config.js` define `window.SKILLRADAR_CONFIG` com a configuração **web** do Firebase. Esse arquivo **é público** e isso é esperado (veja segurança). Ele não pode conter chave do Gemini, token do GitHub nem JSON de conta de serviço.

## 6. Regras de segurança (`firestore.rules`, na raiz)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{colecao}/{doc=**} {
      allow read: if colecao in ['contexto', 'vagas_ativas', 'lacunas_cursos',
                                 'trilhas_sugeridas', 'insights', 'competencias_demandadas'];
      allow write: if false;
    }
    match /interesses_alunos/{id} {
      allow read: if false;
      allow create: if request.resource.data.keys().hasOnly(['curso_interesse', 'nivel', 'areas', 'criado_em'])
        && request.resource.data.criado_em == request.time
        && request.resource.data.nivel in ['iniciante', 'intermediario', 'avancado']
        && request.resource.data.curso_interesse is string
        && request.resource.data.curso_interesse.size() <= 80
        && request.resource.data.areas is list
        && request.resource.data.areas.size() <= 7
        && request.resource.data.areas.hasOnly(['desenvolvimento', 'dados', 'ia', 'infraestrutura', 'seguranca', 'design', 'gestao']);
      allow update, delete: if false;
    }
  }
}
```

O usuário cola essas regras no console do Firebase (aba *Regras*). Confira a sintaxe no simulador de regras antes de publicar.

## 7. Testes

- **Sem rede:** use a função `montar_documentos(...)` (pura, sem Firebase) e teste que: não há array dentro de array; não há `NaN`; os IDs são slugs válidos; os campos de `lacunas_cursos` seguem a seção 3.3.
- `--dry-run` do orquestrador grava esses mesmos documentos em `.temp/`.

## 8. Critérios de aceite

- [ ] Com `.env` e conta de serviço válidos, `python Execution/orquestrador.py --modo demo --sem-gemini` grava os documentos das seções 3.1 a 3.6.
- [ ] Rodar duas vezes não duplica nada.
- [ ] O site, sem recarregar, mostra a mudança quando um documento é alterado no console do Firebase.
- [ ] Uma tentativa de escrita em qualquer coleção pelo navegador é negada (exceto `interesses_alunos` válido).
- [ ] Nenhum arquivo versionado contém o JSON da conta de serviço.
