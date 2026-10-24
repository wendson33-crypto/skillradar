# Diretiva — Web Scraping de Vagas (Dados Vivos)

**Pilar do edital:** 4 (Web Scraping).
**Quando ler:** antes de escrever ou alterar qualquer coisa em `Execution/scrapers/`.

## 1. Objetivo

Coletar, de forma automatizada e **dentro das regras dos sites**, vagas abertas na região de Ourinhos e entorno. Cada vaga vira um registro padronizado que alimenta o restante do pipeline. Se não houver fonte que permita coleta, o projeto roda com `data/vagas_demo.csv` e **diz isso na interface**.

## 2. Regras inegociáveis

1. **Antes de qualquer requisição a um site**, leia o `robots.txt` (`urllib.robotparser`) e leia os termos de uso. Se a coleta for proibida, **não use esse site**.
2. Use `User-Agent` identificado, por exemplo `SkillRadarBot/1.0 (projeto educacional SENAI Ourinhos)`.
3. Intervalo mínimo de **2 segundos** entre requisições ao mesmo site; timeout de 15 segundos; até 3 tentativas com espera crescente.
4. **Proibido:** contornar login, CAPTCHA ou bloqueios; usar proxies ou troca de IP para driblar bloqueio; simular vários usuários.
5. Se o site responder 403 ou 429 de forma repetida, **pare** e use o fallback. Não insista.
6. Nunca invente vagas "reais". O que vier de `vagas_demo.csv` é sempre marcado como demonstração.
7. Guarde só o necessário: título, empresa, cidade, data, requisitos, faixa salarial, link da fonte. **Remova e-mails e telefones** que apareçam no texto da vaga antes de salvar.

## 3. Escolha da fonte

O usuário (não o agente) decide qual portal usar. O agente deve:

1. Perguntar ao usuário qual(is) portal(is) público(s) de vagas ele quer usar.
2. Verificar `robots.txt` e termos do portal escolhido e **mostrar o resultado** ao usuário.
3. Registrar em `data/README.md`: nome da fonte, URL base, data da conferência do `robots.txt` e se a coleta é permitida.
4. Se nenhuma fonte permitir coleta, ativar o modo demo e informar o usuário.

## 4. Estrutura do código

```
Execution/scrapers/
├── base.py            # classe BaseScraper: robots, user-agent, intervalo, retry, timeout
└── fonte_vagas_1.py   # uma subclasse por fonte; só contém seletores e o parse
```

`BaseScraper` expõe:

- `pode_coletar(url) -> bool` (consulta o `robots.txt`, com cache);
- `baixar(url) -> str` (aplica intervalo, timeout e retry; levanta erro claro se bloqueado);
- `extrair(html) -> list[dict]` (abstrato; cada fonte implementa);
- `coletar() -> list[dict]` (orquestra os passos acima).

**Isole os seletores de HTML em um único lugar por fonte**, para que uma mudança no site exija alterar só um arquivo.

## 5. Registro bruto de vaga

```json
{
  "titulo": "string",
  "empresa": "string",
  "cidade": "string",
  "data": "AAAA-MM-DD",
  "salario_min": 3500,
  "salario_max": 5000,
  "fonte_url": "https://...",
  "requisitos_texto": "string sem HTML",
  "coletado_em": "2026-10-24T08:15:00-03:00"
}
```

Normalizações:

- `data` em formato ISO. Se o site só mostrar "há 3 dias", calcule a data a partir do dia da coleta.
- Salário mensal em reais, inteiros. "A combinar" ou ausente vira `null` (nunca `0`).
- Texto: sem HTML, espaços normalizados, sem e-mail nem telefone (substitua por vazio).
- Fuso horário: `America/Sao_Paulo` (no Windows, inclua `tzdata` no `requirements.txt`).

## 6. Deduplicação

`vaga_id = sha1(normalizar(titulo) + "|" + normalizar(empresa) + "|" + normalizar(cidade)).hexdigest()[:12]`

A mesma vaga em coletas diferentes mantém o mesmo ID, então regravar **atualiza** em vez de duplicar.

## 7. Saída intermediária e fallback

- Grave o resultado bruto em `.temp/vagas_brutas_AAAAMMDD_HHMM.json` (a pasta `.temp/` está no `.gitignore`).
- Falha na coleta (rede, bloqueio, HTML mudou): **mantenha o último lote válido no Firestore**, registre o erro no log e não apague nada.
- Sem nenhuma fonte disponível: use `data/vagas_demo.csv` e marque `modo_demo = true`.

## 8. Testes (sem rede)

- Salve 1 ou 2 páginas reais como fixtures em `tests/fixtures/` e teste `extrair()` contra elas.
- Teste que `pode_coletar()` respeita um `robots.txt` que proíbe o caminho (use um texto de `robots.txt` em memória, sem acessar a rede).
- Teste a normalização de salário, data e remoção de e-mail e telefone.
- Teste que a deduplicação gera o mesmo `vaga_id` para a mesma vaga com caixa e espaços diferentes.

## 9. Critérios de aceite

- [ ] Nenhuma requisição é feita a um site cujo `robots.txt` proíba o caminho.
- [ ] O registro bruto segue exatamente o esquema da seção 5; salário ausente é `null`.
- [ ] Rodar duas vezes seguidas não duplica vagas.
- [ ] Sem rede, o pipeline continua funcionando com `vagas_demo.csv` e a interface mostra "Dados de demonstração".
- [ ] Nenhum e-mail ou telefone aparece em `requisitos_texto`.
