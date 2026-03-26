# Patrimonium — Dashboard Institucional

## Setup Inicial

```bash
npm install
npm run dev          # abre em http://localhost:5173
```

---

## Como Atualizar

### Dados Macro (AUTOMÁTICO)

Roda um script que puxa dados atualizados direto das APIs do Banco Central, Focus, Yahoo Finance e AwesomeAPI:

```bash
npm run update-macro
```

Isso atualiza o arquivo `src/data/macro.json` com:
- **Selic** (BCB SGS série 432)
- **CDI** mensal e anualizado (BCB SGS séries 4389 e 4393)
- **IPCA** mensal e acumulado 12M (BCB SGS série 433)
- **Câmbio** dólar/real em tempo real (AwesomeAPI)
- **Ibovespa**, **Ouro**, **S&P 500**, **Bitcoin**, **DXY**, **VIX**, **Petróleo**, **US 10Y** (Yahoo Finance)
- **Focus**: IPCA, Selic, PIB, Câmbio projetados (BCB Olinda API)

> **Dica:** Rode antes de cada reunião de board para ter dados frescos.

### Dados da Carteira (MANUAL)

Edite `src/data/carteira.json` quando receber o relatório mensal.

O que atualizar:

1. **`referencia`** — data de referência do relatório (ex: `"28/02/2026"`)

2. **`empresas[]`** — para cada empresa, copie do XP Performance:
   - `patrimonio`, `rentMes`, `ganhoMes`, `pctCDI`
   - `rentAno`, `pctCDIAno`
   - `volatilidade`, `mesesPositivos`, `mesesAcimaCDI`
   - Adicione o novo mês em `mensal[]` e `evolucaoPatrimonial[]`

3. **`fundos[]`** — atualize os saldos por empresa:
   - `multiArm`, `multiExp`, `magLog`
   - `rentMes`, `pctCDI`

4. **`benchmarks`** — copie da página 2 do XP Performance

### Exemplo: Adicionando Fevereiro/2026

```json
// Em empresas[0].mensal, adicione:
{ "mes": "Fev/26", "rent": 1.23, "pctCDI": 105.50 }

// Em empresas[0].evolucaoPatrimonial, adicione:
{ "mes": "Fev/26", "pat": 11050000.00, "mov": 0 }
```

---

## Estrutura do Projeto

```
dashboard-grupo/
├── src/
│   ├── data/
│   │   ├── carteira.json    ← VOCÊ EDITA (dados XP)
│   │   └── macro.json       ← AUTOMÁTICO (npm run update-macro)
│   ├── App.jsx              ← Dashboard principal
│   ├── main.jsx
│   └── index.css
├── scripts/
│   └── fetch-macro.mjs      ← Script de atualização macro
├── package.json
└── README.md
```

## Fontes de Dados das APIs

| Dado | API | URL Base |
|------|-----|----------|
| Selic, CDI, IPCA | BCB SGS | `api.bcb.gov.br/dados/serie/bcdata.sgs.{id}` |
| Focus (projeções) | BCB Olinda | `olinda.bcb.gov.br/olinda/servico/Expectativas` |
| Dólar real-time | AwesomeAPI | `economia.awesomeapi.com.br/last/USD-BRL` |
| Bolsas, Ouro, etc | Yahoo Finance | `query2.finance.yahoo.com/v8/finance/chart/{sym}` |

## Deploy (opcional)

```bash
npm run build        # gera pasta dist/
npx serve dist       # serve localmente
```

Ou faça deploy no Vercel/Netlify arrastando a pasta `dist/`.
