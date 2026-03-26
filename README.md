# Patrimonium — Dashboard Institucional

Plataforma de inteligencia patrimonial que consolida contas XP em uma interface analítica com 8+ módulos, dados macro em tempo real e geração de relatórios em PDF.

---

## Quick Start

```bash
npm install
npm run dev              # http://localhost:5173
```

Client B (instância independente):

```bash
cd client-b && npm install && npm run dev    # http://localhost:5174
```

---

## Atualização de Dados

### Macro — automático

```bash
npm run update-macro
```

Atualiza `src/data/macro.json` com dados de quatro fontes:

| Dado | Fonte | Série / Endpoint |
|------|-------|------------------|
| Selic | BCB SGS | 432 |
| CDI mensal / anualizado | BCB SGS | 4389 / 4393 |
| IPCA mensal / acumulado 12M | BCB SGS | 433 |
| Câmbio USD/BRL | AwesomeAPI | `last/USD-BRL` |
| Ibovespa, S&P 500, DXY, VIX, Ouro, Petróleo, Bitcoin, US 10Y | Yahoo Finance | `v8/finance/chart` |
| Projeções Focus (IPCA, Selic, PIB, Câmbio) | BCB Olinda | Expectativas |

> Rode antes de cada reunião para ter dados frescos.

### Carteira — manual

Edite `src/data/cliente.json` com os dados do relatório XP Performance mensal:

1. **`referencia`** — data do relatório (ex: `"27/02/2026"`)
2. **`empresas[]`** — por conta: `patrimonio`, `rentMes`, `ganhoMes`, `pctCDI`, `rentAno`, `volatilidade`, `mesesPositivos`, `mesesAcimaCDI`
   - Adicione o novo mês em `mensal[]` e `evolucaoPatrimonial[]`
3. **`fundos[]`** — saldos por fundo: `multiArm`, `multiExp`, `magLog`, `rentMes`, `pctCDI`
4. **`benchmarks`** — copie da página 2 do XP Performance

#### Exemplo: adicionando um novo mês

```json
// empresas[0].mensal
{ "mes": "Fev/26", "rent": 1.23, "pctCDI": 105.50 }

// empresas[0].evolucaoPatrimonial
{ "mes": "Fev/26", "pat": 11050000.00, "mov": 0 }
```

---

## Geração de PDF

```bash
npm run pdf                  # relatório completo (8 tabs → A4)
npm run pdf:watermark        # com marca d'água CONFIDENCIAL
```

Puppeteer (Chrome headless) renderiza cada aba em página A4 com numeração e quebras automáticas.

---

## Tabs do Dashboard

| # | Tab | O que mostra |
|---|-----|-------------|
| 1 | Overview | Patrimônio total, ganhos, %CDI consolidado |
| 2 | Asset Allocation | Composição por classe e fundo (pie/bar) |
| 3 | Portfolio Strategy | Estratégia e posicionamento da carteira |
| 4 | Benchmark | Comparativo com CDI, Ibovespa, IPCA+, multimercado |
| 5 | Tax Alpha | Alpha fiscal e eficiência tributária |
| 6 | Hedge | Proteções cambiais e posições defensivas |
| 7 | Portfolio Efficiency | Risco/retorno, Sharpe, drawdown |
| 8 | Macro View | Selic, câmbio, curvas, projeções Focus |
| 9 | Financial Planning | Planejamento financeiro *(Client B)* |

---

## Multi-Client

Cada instância opera com dados de carteira independentes e deploy separado:

| Instância | Diretório | Status |
|-----------|-----------|--------|
| Client A | `src/` | Ativo — 8 tabs |
| Client B | `client-b/` | Ativo — 9 tabs (+Financial Planning) |
| Client C | `client-c/` | Scaffold — pronto para onboarding |

Dados macro são compartilhados via `fetch-macro.mjs` na raiz. Cada client roda `npm run update-macro` para sincronizar.

---

## Scripts

| Script | Descrição |
|--------|-----------|
| `fetch-macro.mjs` | Pipeline de dados macro (BCB + Yahoo + AwesomeAPI) |
| `scripts/generate-pdf.mjs` | Exporta dashboard em PDF via Puppeteer |
| `scripts/generate-guide.py` | Guia de apresentação para reuniões (ReportLab) |
| `scripts/generate-roadmap.py` | Roadmap de desenvolvimento em PDF |
| `scripts/generate-summary-report.py` | Relatório consolidado de mentoria e diagnóstico |
| `scripts/gen-audit-doc.cjs` | Gerador de documento de auditoria (DOCX) |

---

## Estrutura do Projeto

```
Dash Institucional/
├── src/                            # Dashboard principal (Client A)
│   ├── AppCliente.jsx             # Interface — 8 tabs analíticas
│   ├── data/
│   │   ├── cliente.json           # Dados da carteira (manual)
│   │   └── macro.json             # Dados macro (auto)
│   ├── main.jsx
│   └── index.css
│
├── client-b/                       # Client B (9 tabs)
│   ├── src/
│   │   ├── AppCliente.jsx         # +tab Financial Planning
│   │   └── data/                  # Dados independentes
│   ├── package.json
│   └── vite.config.js
│
├── client-c/                       # Client C (scaffold)
│   └── src/data/
│
├── scripts/                        # Geradores de documentos e relatórios
├── fetch-macro.mjs                 # Pipeline BCB + Yahoo + AwesomeAPI
├── SYSTEM_PLAYBOOK.md              # Arquitetura e operações
├── SECURITY_AUDIT.md               # Inventário de sensibilidade de dados
├── package.json
└── README.md
```

---

## Tech Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React 18 + Recharts |
| Bundler | Vite 6 |
| PDF | Puppeteer (Chrome headless) |
| Docs Python | ReportLab |
| Deploy | Vercel (static) |
| APIs | BCB SGS, BCB Olinda, Yahoo Finance, AwesomeAPI |

---

## Deploy

```bash
npm run build            # gera dist/
npx serve dist           # serve localmente
```

Ou deploy no Vercel/Netlify arrastando a pasta `dist/`.
