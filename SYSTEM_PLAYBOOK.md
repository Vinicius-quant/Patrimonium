# SYSTEM PLAYBOOK — Patrimonium Capital Allocation Platform

> Documento institucional de arquitetura, engenharia e operações.
> Gerado em: 14/03/2026 | Atualizado: 15/03/2026 | Versão: 1.1
> Classificação: Interno — Patrimonium

---

## 1. VISAO GERAL DO PROJETO

### Objetivo
Dashboard institucional de inteligencia patrimonial para assessoria de investimentos. Consolida 7 contas XP (Private + Regular) de uma carteira de R$ 26.2M (42 posicoes, R$ 25.83M em ativos + R$ 374k em caixa) em uma interface unica com 8 modulos analiticos + modo relatorio PDF.

### Problema que resolve
Assessores de investimento recebem dados fragmentados: extrato XP, relatorio de cada fundo, dados macro de multiplas fontes. A consolidacao manual consome horas. Este sistema automatiza a ingestao de dados macro/ANBIMA, consolida posicoes por conta, calcula metricas de risco/retorno e gera relatorios PDF institucionais.

### Publico-alvo
- Assessores de investimento (AAI) da Patrimonium
- Clientes Private/HNW em reunioes de comite

### Funcionalidades principais
1. **Visao consolidada** — 7 contas, patrimonio, rentabilidade vs CDI
2. **Alocacao** — Por estrategia, tipo de papel e por conta
3. **Cenario Macro** — Selic, CDI, IPCA, cambio, Focus em tempo real
4. **Benchmarks** — Performance por conta com referencia CDI
5. **KPIs** — Metas editaveis vs performance real
6. **Asset Allocation** — Liquidez, vencimentos, timeline de carrego, simulacao FIP
7. **Tax Alpha** — Ativos isentos, equivalente bruto, economia tributaria
8. **Custo & Concentracao** — TER ponderado, HHI, concentracao top 5
9. **Curvas & Risco** — ETTJ, duration, DV01, stress test, cenarios historicos
10. **Relatorio PDF** — Exportacao de todas as tabs em A4 com capa institucional

### Visao estrategica
Embriao de uma plataforma proprietaria de inteligencia de portfolio. Referencia: Aladdin (BlackRock), Bloomberg PORT, sistemas institucionais de risco.

---

## 2. ARQUITETURA DO SISTEMA

### Stack
```
Frontend:   React 18.3.1 (SPA)
Build:      Vite 6.0.0 (ESM bundler)
Charts:     Recharts 2.13.0
Deploy:     Vercel (static)
Data:       JSON files (manual + auto-update scripts)
APIs:       BCB SGS, BCB Focus, ANBIMA Feed, Yahoo Finance, AwesomeAPI
```

### Estrutura de pastas
```
Dash Institucional/
├── src/
│   ├── main.jsx                 # Entry point → monta AppCliente
│   ├── index.css                # Reset CSS global
│   ├── AppCliente.jsx           # Dashboard principal (2317 linhas, 9 tabs)
│   ├── App.jsx                  # Variante Grupo Multi
│   ├── AppClienteB.jsx          # Variante Client-B (FX)
│   └── data/
│       ├── cliente.json         # Dados do cliente (35 KB, manual)
│       ├── macro.json           # Dados macro (49 KB, auto)
│       ├── anbima.json          # Curvas ANBIMA (8.9 KB, auto/mock)
│       ├── carteira.json        # Carteira Grupo Multi
│       └── client-b.json        # Portfolio Client-B
├── fetch-macro.mjs              # Script de atualizacao macro
├── fetch-anbima.mjs             # Script de atualizacao ANBIMA
├── .env                         # Credenciais ANBIMA (gitignored)
├── .env.example                 # Template de credenciais
├── package.json                 # Dependencias e scripts
├── vite.config.js               # Config do bundler
├── index.html                   # HTML raiz
└── dist/                        # Build de producao
```

### Fluxo de dados
```
                    ┌─────────────────┐
                    │   BCB SGS API   │──── Selic, CDI, IPCA
                    │   BCB Focus     │──── Expectativas mercado
                    │   AwesomeAPI    │──── Cambio real-time
                    │   Yahoo Finance │──── Ibov, S&P, Ouro, BTC
                    └────────┬────────┘
                             │ fetch-macro.mjs
                             ▼
                    ┌─────────────────┐
                    │   macro.json    │
                    └────────┬────────┘
                             │
┌─────────────┐     ┌────────┴────────┐     ┌─────────────────┐
│ ANBIMA Feed │────▶│  anbima.json    │     │  cliente.json    │
│   API       │     └────────┬────────┘     │  (manual, XP)   │
└─────────────┘              │              └────────┬────────┘
       fetch-anbima.mjs      │                       │
                             ▼                       ▼
                    ┌─────────────────────────────────┐
                    │        AppCliente.jsx            │
                    │   (React, 9 tabs, Recharts)      │
                    └─────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │   Vite Build    │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    Vercel CDN   │
                    └─────────────────┘
```

---

## 3. TECNOLOGIAS UTILIZADAS

| Tecnologia | Versao | Papel |
|---|---|---|
| **React** | 18.3.1 | Framework UI. Componentes funcionais, hooks (useState, useMemo) |
| **Recharts** | 2.13.0 | Biblioteca de graficos SVG. LineChart, BarChart, ScatterChart, ComposedChart, AreaChart |
| **Vite** | 6.0.0 | Bundler ESM. Hot Module Replacement, tree-shaking, build otimizado |
| **@vitejs/plugin-react** | 4.3.4 | JSX transform + Fast Refresh |
| **Node.js** | 18+ | Runtime para scripts de data fetch |
| **Vercel** | — | Deploy estatico, CDN global |

### Por que estas escolhas
- **React**: Ecossistema maduro, renderizacao condicional para printMode
- **Recharts**: Declarativo, SVG nativo (funciona no print), ResponsiveContainer
- **Vite**: 10x mais rapido que CRA/Webpack, ESM nativo
- **Zero backend**: Dados pre-processados em JSON. Elimina custos de servidor, latencia, complexidade

---

## 4. DEPENDENCIAS

### Producao
```json
{
  "react": "^18.3.1",        // UI framework
  "react-dom": "^18.3.1",    // React DOM renderer
  "recharts": "^2.13.0"      // Charting library (SVG)
}
```

### Desenvolvimento
```json
{
  "vite": "^6.0.0",                    // Build tool
  "@vitejs/plugin-react": "^4.3.4",    // JSX support
  "@types/react": "^18.3.12",          // TypeScript types (IDE)
  "@types/react-dom": "^18.3.1"        // TypeScript types (IDE)
}
```

### Servicos externos (scripts)
- **BCB SGS API** — `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ID}/dados` (publica, sem auth)
- **BCB Focus API** — `https://olinda.bcb.gov.br/olinda/servico/Expectativas/...` (publica, OData)
- **AwesomeAPI** — `https://economia.awesomeapi.com.br/last/USD-BRL` (publica, real-time)
- **Yahoo Finance** — `https://query2.finance.yahoo.com/v8/finance/chart/{SYMBOL}` (publica, rate-limited)
- **ANBIMA Feed API** — `https://api-sandbox.anbima.com.br/feed/precos-indices/v1/...` (OAuth2, paga)

---

## 5. FONTES DE DADOS

### 5.1 cliente.json (Manual — Mensal)
**Origem**: Relatorio de performance XP Investimentos
**Frequencia**: Mensal (apos fechamento)
**Processo**: Assessor extrai dados do portal XP e edita o JSON

**Campos por conta (empresas[]):**
```
conta, nome, tipo (Private/Regular), patrimonio, rentMes, ganhoMes,
pctCDI, rentAno, pctCDIAno, rent2025, pctCDI2025, acumulado,
volatilidade, mesesPositivos, mesesNegativos, mesesAcimaCDI,
movimentacaoMes, mensal[], evolucaoPatrimonial[], estrategia[]
```

**Campos por posicao (fundos[]):**
```
conta, curto (nome), classe, tipo, taxa, liquidez, total,
pctCart, rentMes, pctCDIMes, gestora, cnpj, diasCorridos,
taxaAdmin, taxaPerf, segmento
```

### 5.2 macro.json (Auto — On-demand)
**Script**: `fetch-macro.mjs` | **Comando**: `npm run update-macro`
**Frequencia**: Sob demanda (idealmente diario ou antes de reuniao)

**Series BCB SGS utilizadas:**
| ID | Serie | Uso |
|---|---|---|
| 432 | Selic meta (% a.a.) | KPI macro, projecao FIP |
| 4389 | CDI anualizado | Benchmark de carteira |
| 4391 | CDI acumulado mes | Referencia mensal |
| 433 | IPCA variacao mensal | Indicador macro |
| 13522 | IPCA acumulado 12M | Context macro |
| 1 | Dolar PTAX venda | Cambio, hedge |

**Endpoints Focus:**
```
GET /Expectativas/versao/v1/odata/ExpectativasMercadoAnuais
  $filter: Indicador eq 'IPCA' and DataReferencia eq '2026'
GET /Expectativas/versao/v1/odata/ExpectativasReuniao
  $filter: Indicador eq 'Taxa Selic'
```

### 5.3 anbima.json (Auto/Mock)
**Script**: `fetch-anbima.mjs` | **Comando**: `npm run update-anbima`
**Auth**: OAuth2 client_credentials (Basic Auth → access_token)

**Endpoints ANBIMA Feed API:**
| Endpoint | Dados | Uso |
|---|---|---|
| `/titulos-publicos/curvas-juros` | ETTJ (Pre, IPCA, Implicita) | Grafico de curvas soberanas |
| `/titulos-publicos/mercado-secundario-TPF` | NTN-B, LFT, LTN quotes | Precos de referencia |
| `/debentures/curvas-credito` | Spread AAA/AA/A | Curvas de credito |
| `/debentures/mercado-secundario` | Debentures | Spread vs soberana |
| `/cri-cra/mercado-secundario` | CRI/CRA | Posicoes de credito |
| `/titulos-publicos/vna` | VNA IPCA/Selic | Valor nominal atualizado |

**Mock fallback**: Quando credenciais invalidas, gera dados simulados realistas:
- Pre: 14.85% → 13.70% (curva descendente)
- IPCA: 7.55% → 6.60%
- Credit spreads: AAA 0.40-0.72%, AA 0.65-1.10%, A 0.95-1.55%

---

## 6. LOGICA FINANCEIRA IMPLEMENTADA

### 6.1 Consolidacao multi-conta
```
totalPat = SUM(empresas[i].patrimonio)                    // R$ 26.204.602,78
wRent   = SUM(empresas[i].rentMes × patrimonio) / totalPat  // Rent. ponderada
wCDI    = SUM(empresas[i].pctCDI × patrimonio) / totalPat   // %CDI ponderado
```

### 6.2 Duration e DV01 (Tab 9)
**Duracao Macaulay estimada** (sem fluxos individuais):
```
prazoAnos = (vencimento - hoje) / 365
```

**Ajuste por indexador** (proxy para duration efetiva):
```
Indexador       Multiplicador    Logica
IPCA            × 0.82          NTN-B: duration modificada < Macaulay
Pre-fixado      × 0.95          LTN/NTN-F: quase 1:1
CDI+            × 0.15          Flutuante: resetado a cada cupom
Selic           × 0.08          LFT: duration proxima de zero
%CDI            × 0.10          % do CDI: similar a flutuante
Fundos          × 0.35          Proxy: prazo medio ponderado
```

**Duration Modificada:**
```
durMod = durMac / (1 + yield/200)
```

**DV01 (Dollar Value of 01):**
```
DV01 = durMod × valor × 0.0001   // Sensibilidade a 1bp
```

### 6.3 Spread vs Soberana
Calculo apenas para posicoes IPCA-indexed:
```
spreadVsCurva = taxaContratada - ettjRate(closestVertex)
wSpread = SUM(spreadVsCurva[i] × valor[i]) / SUM(valor_ipca)
```

### 6.4 Stress Test
**Cenarios paralelos** (choque instantaneo na curva):
```
-200bp, -100bp, -50bp, +50bp, +100bp, +200bp, +300bp
impacto = -totalDV01 × choqueBps
pctImpacto = impacto / totalPat × 100
```

### 6.5 Cenarios Historicos (multi-fator)
```
Cenario        Juros(bp)  Ibov(%)  Dolar(%)  Credito(bp)
Crise 2008     +300       -45      +35       +250
Crise 2015     +500       -13      +47       +180
COVID-19       -450       -47      +30       +400
Choque 2022    +200       -6       +5        +120
```

**Decomposicao do impacto:**
```
impJuros   = -totalDV01 × choque_juros
impBolsa   = exposicao_RV × (choque_ibov / 100)
impCredito = -totalCredito × (choque_credito/10000) × wDuration
impTotal   = impJuros + impBolsa + impCredito
```

### 6.6 Tax Alpha
**Equivalente bruto:**
```
Para isento: eqBruto = taxa / (1 - aliquota)
Aliquota: 22.5% (≤180d), 20% (≤360d), 17.5% (≤720d), 15% (>720d)
```

**Economia tributaria:**
```
economiaTributaria = SUM(fundo_isento.total × fundo_isento.rentMes/100 × aliquota_equivalente)
```

### 6.7 Custo & Concentracao
**TER ponderado:**
```
wER = SUM(taxaAdmin[i] × total[i]) / SUM(total[i])  // apenas fundos com custo
```

**HHI (Herfindahl-Hirschman) — Indice de Concentracao:**
```
HHI = SUM((total[i] / totalPat × 100)^2)
< 1500: Diversificado | 1500-2500: Moderado | > 2500: Concentrado

Intuicao: eleva o peso de cada ativo ao quadrado e soma.
Se 1 ativo = 100% → HHI = 10.000 (maximo).
Se 100 ativos iguais de 1% → HHI = 100 (minimo pratico).
Quanto menor, mais diversificado.
```

**KPI Dynamics (v1.1):**
Cada KPI exibe uma seta indicando a dinamica para o investidor:
```
TER Ponderado         → ↓ = melhor (custo total ponderado da carteira)
Custo Anual           → ↓ = melhor (impacto das taxas em R$)
Diversificacao (HHI)  → ↓ = melhor (indice de concentracao, alvo < 1.000)
Maior Posicao         → ↓ = melhor (alvo < 15%)
Posicoes sem Custo    → ↑ = melhor (quanto mais, menor o TER)
```

### 6.8 Simulacao FIP AG7
```
aporte = R$ 5.000.000 (fixo)
MOIC conservador: 2.5x → bruto = aporte × 2.5
MOIC otimista:    3.0x → bruto = aporte × 3.0
IR: 15% sobre ganho
Amortizacao: 40% em 1T/2028
Vencimento: 1T/2030

CDI (custo de oportunidade):
  cdiFactor = PROD(1 + selicEstimada[periodo], frac_periodo)
  cdiNet = aporte × cdiFactor - (ganho × 0.15)

Alpha = retornoLiqFIP - retornoLiqCDI
```

### 6.9 Timeline de Carrego (Asset Allocation)
```
Para cada mes de 2026:
  pool += pool × taxaMensal(selic_estimada)  // carrego CDI
  pool += vencimentos_do_mes × (1 + carrego_acumulado)
```

---

## 7. ESTRUTURA DO DASHBOARD (9 TABS)

### Tab 0 — Visao Geral
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes (5) | Texto destaque | Patrimonio, Rent Mes, Ganho, Rent Ano, Ganho Ano |
| Evolucao patrimonial | LineChart | evoTotal[] (12 meses) |
| Rentabilidade conta principal | BarChart | conta.mensal[] (12 meses, referencia CDI) |
| Performance por conta | Table | 7 contas × 8 colunas |

### Tab 1 — Alocacao
| Componente | Tipo | Dados |
|---|---|---|
| Por estrategia | HorizontalBar | byStrat (Pos Fixado, Inflacao, etc) |
| Por tipo de papel | HorizontalBar | byClass (Fundos, Titulos, CDB, etc) |
| Por conta | HorizontalBar | empresas por patrimonio |
| Tabela de fundos | Table | fundos[] agrupados por tipo |
| Perfil de estrategia | HorizontalBar | classes de investimento |

### Tab 2 — Cenario Macro
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes (8) | Texto | Selic, CDI, IPCA, Dolar, Ibov, S&P, Ouro, Bitcoin |
| Trajetoria Selic Focus | LineChart | focusSelicCurva[] |
| Tabela Focus | Table | Expectativas IPCA, PIB, Cambio, Selic |

### Tab 3 — Benchmarks
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes | Texto | Rent consolidada, %CDI, Ganho, Rent ano |
| Tabela por conta | Table | Private vs Regular, rent mes/ano, %CDI |
| Consolidado | BarChart | Barras por conta vs referencia |

### Tab 3 — Benchmark + Investment Mandate (T4)
| Componente | Tipo | Dados |
|---|---|---|
| Retorno vs benchmarks | Table | Portfolio vs CDI, Ibov, IPCA, Dolar |
| Ranking de contas | HorizontalBar | Performance mensal por conta |
| Investment Mandate | Cards semaforo | Return vs CDI, Volatility, Monthly, Positive Months, YTD, Accounts |
| Recomendacoes | Cards 3×2 | Concentracao, Duration, Juros, Estruturados, Soberano, Liquidez |

> **Nota**: T5 (KPIs editaveis) foi integrado ao T4 como Investment Mandate na v1.1.
> Valores de referencia agora sao dinamicos (computados dos dados, nao hardcoded).

### Tab 5 — Asset Allocation
| Componente | Tipo | Dados |
|---|---|---|
| Liquidez imediata | KPI boxes | Fundos D+0, LFTs, CDBs 100% CDI |
| Vencimentos 2026 | Table | Timeline de vencimentos |
| Carrego CDI projetado | LineChart (area) | Pool de liquidez com carrego |
| FIP AG7 | Table + LineChart | Simulacao MOIC 2.5x/3.0x vs CDI |

### Tab 6 — Tax Alpha
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes | Texto | Patrimonio isento, Economia IR, Come-cotas, IR medio |
| Composicao tributaria | HorizontalBar | Isento, Come-cotas, Tabela Regressiva, RV |
| Distribuicao por faixa | Table | Faixas de IR (22.5% a 15%) |
| Equivalente bruto | Table | Ativos isentos com taxa equivalente |
| Top 10 retorno bruto vs liquido | HorizontalBar | BarChart layout vertical |

### Tab 7 — Custo & Concentracao
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes | Texto | TER, Custo anual, HHI, Top 5, Posicoes sem custo |
| Composicao por faixa | HorizontalBar | Sem custo, ≤0.50%, 0.51-1.00%, >1.00% |
| Custo por classe | BarChart | Taxa admin media por classe |
| Detalhe por posicao | Table | Custo individual + alpha/custo |
| Top 20 posicoes | HorizontalBar | Barras de concentracao |
| Custo-beneficio | Card texto | Narrativa automatica |
| Concentracao | Card texto | HHI + analise automatica |

### Tab 8 — Curvas & Risco
| Componente | Tipo | Dados |
|---|---|---|
| KPI boxes | Texto | Duration, DV01, Spread, MtM |
| ETTJ | LineChart | Curvas Pre, IPCA, Implicita |
| Mapa de posicoes | ScatterChart | Duration × Yield (tamanho = patrimonio) |
| Posicoes renda fixa | Table | 28 posicoes com duration, DV01, spread |
| Credit spread | BarChart | Curvas AAA/AA/A por vertice |
| Stress test | Table + CSS bars | Cenarios -200bp a +300bp |
| Cenarios historicos | Cards | Crise 2008, 2015, COVID, 2022 |
| Glossario | Grid 3 colunas | 15 termos financeiros |

---

## 8. DESIGN SYSTEM

### Paleta de cores
```
Navy:       #1B2A4A    // Cor primaria, textos principais, headers
Dark Navy:  #0D1A30    // Acentos escuros
Steel:      #2C5282    // Secundaria, graficos
Teal:       #234E6F    // Terciaria
Slate:      #4A5568    // Texto corpo
Med Gray:   #718096    // Labels, subtitulos, eixos
Light Gray: #E2E8F0    // Bordas sutis
Very Light: #F7FAFC    // Backgrounds secundarios
White:      #FFFFFF    // Background principal
Green:      #276749    // Positivo, isentos
Red:        #9B2C2C    // Negativo, custos
Amber:      #B7791F    // Neutro, alertas, CDI reference
```

### Tipografia
```
Sans-serif: Inter (Google Fonts) — labels, subtitulos, corpo
Monospace:  JetBrains Mono — numeros, valores financeiros, KPIs
Serif:      Source Serif 4 — font-family do body (base)
```

### Principios de design (SCD — Storytelling com Dados)
1. **Gridlines quase invisiveis** — `strokeDasharray: "3 3"`, cor `#EDF2F7`
2. **Eixos sem linhas** — `axisLine={false}`, `tickLine={false}`, labels cinza
3. **Barras horizontais** em vez de pie charts (comparacao visual direta)
4. **Tabelas sem background** nos headers — bordas minimas cinza
5. **Cor estrategica** — cinza para estrutura, cor so para destaque (max 10%)
6. **Dados em primeiro plano** — bordas, grades e labels sao secundarios

### Componentes visuais reutilizaveis
```jsx
KPI      — Metric box com borderLeft colorido, label + valor + contexto
LPie     — Barras horizontais (substituiu PieChart) com % total
MinTip   — Tooltip compacto para graficos Recharts
PageHead — Header de pagina no modo relatorio (cliente, secao, pag)
Cover    — Capa do relatorio PDF (A4, centralizado)
```

---

## 9. REFERENCIAS DE MERCADO

| Referencia | Inspiracao |
|---|---|
| **Aladdin (BlackRock)** | Consolidacao multi-conta, analise de risco integrada |
| **Bloomberg PORT** | ETTJ, duration, stress test por cenario |
| **PIMCO Client Reports** | Design institucional, paleta navy/green, tipografia premium |
| **Sparta Asset Reports** | Layout de wealth report brasileiro, metricas de carteira |
| **XP Advisory** | Estrutura de contas Private/Regular, benchmarks CDI |
| **Storytelling com Dados (Knaflic)** | Principios de design visual: barras > pizza, cor estrategica, reduzir saturacao |

---

## 10. PASSO A PASSO PARA RECRIAR O PROJETO

### 10.1 Preparacao do ambiente
```bash
# Requisitos: Node.js 18+, npm
node -v   # v18.x ou superior
npm -v    # 9.x ou superior
```

### 10.2 Estrutura inicial
```bash
mkdir dash-institucional && cd dash-institucional
npm create vite@latest . -- --template react
npm install recharts
```

### 10.3 Configuracao
```bash
# vite.config.js — apenas plugin react
# Remover App.css, assets/ (desnecessarios)
# Criar src/data/ para JSONs
```

### 10.4 Dados
```bash
# 1. Criar src/data/cliente.json com dados do cliente XP
# 2. Copiar fetch-macro.mjs e fetch-anbima.mjs para raiz
# 3. Criar .env com credenciais ANBIMA (opcional)
# 4. Rodar:
npm run update-macro    # Gera macro.json
npm run update-anbima   # Gera anbima.json (mock sem credenciais)
```

### 10.5 Dashboard
```bash
# Criar src/AppCliente.jsx com:
# 1. Imports (React, Recharts, JSONs)
# 2. Paleta de cores (P), formatadores (fmt, fmtPct, fmtM)
# 3. Estilos base (card, stit, th, td)
# 4. Componentes reutilizaveis (KPI, LPie, MinTip)
# 5. Data processing (useMemo)
# 6. 9 tabs (T1 a T9) com logica financeira
# 7. Print mode (Cover, PageHead, PageBreak)
# 8. Render condicional (printMode ? relatorio : dashboard)
```

### 10.6 Execucao
```bash
npm run dev      # http://localhost:8791
npm run build    # Producao → dist/
```

### 10.7 Deploy
```bash
npx vercel       # Deploy automatico
```

---

## 11. RISCOS TECNICOS

### Criticos
| Risco | Impacto | Mitigacao |
|---|---|---|
| **Arquivo unico de ~2215 linhas** | Manutencao dificil, merge conflicts | Modularizar em componentes separados |
| **Dados manuais (cliente.json)** | Erro humano na digitacao | Criar validador de schema |
| **Sem testes automatizados** | Regressoes silenciosas | Adicionar Vitest + componentes de teste |
| **Bundle 714KB** | Performance em mobile | Code-splitting por tab |

### Moderados
| Risco | Impacto | Mitigacao |
|---|---|---|
| **APIs publicas sem SLA** | Dados macro indisponiveis | Cache local, fallback para ultimo dado |
| **ANBIMA sandbox limitado** | Dados ficticios em prod | Assinar Feed (R$ 686-1830/mes) |
| **Sem CI/CD** | Deploy manual | GitHub Actions + Vercel integration |
| **Sem observabilidade** | Erros nao detectados | Sentry ou LogRocket |

### Baixos
| Risco | Impacto | Mitigacao |
|---|---|---|
| **Recharts SVG pesado** | Print pode falhar com muitos pontos | Limitar dados em graficos |
| **Chrome-only print** | PDF quebra em Firefox/Safari | Documentar requisito Chrome |

---

## 12. AUDITORIA DE SEGURANCA

### Vulnerabilidades identificadas
| Item | Risco | Status | Recomendacao |
|---|---|---|---|
| **Credenciais ANBIMA em .env** | Exposicao se commitado | OK (.gitignored) | Manter .env no .gitignore |
| **Dados do cliente em JSON** | PII exposto no bundle | MEDIO | Considerar criptografia ou API backend |
| **Sem autenticacao** | Qualquer um acessa URL | ALTO | Adicionar auth (Vercel Password Protection ou Clerk) |
| **Yahoo Finance scraping** | Bloqueio por rate-limit | BAIXO | Implementar retry com backoff |
| **Sem HTTPS local** | Dados em transito | BAIXO | Vite serve HTTPS com cert local |

### Recomendacoes
1. **Nunca commitar .env** — ja configurado no .gitignore
2. **Proteger URL de deploy** — Vercel Password Protection (R$ 0, plano hobby)
3. **Considerar backend** para dados sensíveis se escalar para multi-cliente
4. **Rotacionar credenciais ANBIMA** periodicamente

---

## 13. MELHORES PRATICAS A IMPLEMENTAR

### Versionamento
- [ ] Inicializar repositorio Git (`git init`)
- [ ] Conectar ao GitHub (repo privado)
- [ ] Commitar com mensagens semanticas (feat:, fix:, docs:)
- [ ] Branch strategy: main (producao), dev (desenvolvimento)

### Modularizacao
- [ ] Extrair cada tab para arquivo separado (`T1_VisaoGeral.jsx`, etc)
- [ ] Criar `src/utils/formatters.js` para fmt, fmtPct, fmtM
- [ ] Criar `src/utils/calculations.js` para logica financeira
- [ ] Criar `src/styles/theme.js` para paleta P e estilos base

### Qualidade
- [ ] Adicionar ESLint + Prettier
- [ ] Adicionar Vitest para testes unitarios (calculos financeiros)
- [ ] Validador de schema para cliente.json (Zod ou Joi)

### Observabilidade
- [ ] Error boundary no React
- [ ] Logging de erros de fetch nos scripts
- [ ] Monitoramento de uptime (UptimeRobot, gratis)

---

## 14. CHECKLIST DE CONTINUIDADE

### Backup (3 camadas)
- [ ] **GitHub** — Repositorio privado, push diario
- [ ] **OneDrive** — Pasta atual (ja em uso)
- [ ] **Google Drive** — Backup semanal do projeto completo

### Documentacao
- [x] **SYSTEM_PLAYBOOK.md** — Este documento
- [ ] **CHANGELOG.md** — Registro de mudancas por versao
- [ ] **README.md** — Instrucoes de setup (atualizar)

### Replicabilidade
- [x] **package.json** com todas dependencias
- [x] **.env.example** com template de credenciais
- [x] **fetch scripts** para regenerar dados
- [ ] **Seed data** — cliente.json template vazio

### Monitoramento
- [ ] Verificar `npm run update-macro` mensalmente
- [ ] Verificar ANBIMA credentials (expiracao)
- [ ] Backup pre-deploy em branch separada

---

## 15. ROADMAP DE EVOLUCAO

### Fase 1 — Estabilizacao (Q1/2026)
- [ ] Modularizar AppCliente.jsx em componentes
- [ ] Adicionar autenticacao basica
- [ ] Criar CI/CD com GitHub Actions + Vercel
- [ ] Testes unitarios para calculos financeiros

### Fase 2 — Multi-Cliente (Q2/2026)
- [ ] Seletor de cliente na interface
- [ ] Multiplos cliente.json (ou micro-backend)
- [ ] Template de onboarding para novos clientes
- [ ] Historico de snapshots mensais

### Fase 3 — Inteligencia (Q3/2026)
- [ ] Alertas automaticos (concentracao > threshold)
- [ ] Sugestoes de rebalanceamento
- [ ] Simulador de cenarios interativo
- [ ] Integracao real ANBIMA Feed (producao)

### Fase 4 — Produto (Q4/2026)
- [ ] Backend Node.js + PostgreSQL
- [ ] API de integracao com XP/BTG
- [ ] Multi-tenancy (SaaS para advisors)
- [ ] White-label para escritorios parceiros

---

## SCRIPTS DE REFERENCIA RAPIDA

```bash
# Desenvolvimento
npm run dev                    # Servidor em http://localhost:8791

# Atualizar dados
npm run update-macro           # Macro: Selic, CDI, IPCA, Focus, FX
npm run update-anbima          # ANBIMA: ETTJ, TPF, credito (mock sem .env)
npm run update-all             # Ambos

# Build
npm run build                  # Gera dist/ para producao
npm run preview                # Serve o build localmente

# Deploy
npx vercel                     # Deploy no Vercel
```

---

---

## 16. CHANGELOG

### v1.1 — 15/03/2026

**Reconciliacao de dados (cliente.json):**
- Trend Pos-Fixado: R$ 2.456.721 → R$ 18.417,76 (era catch-all inflado)
- CDBs Banco XP: R$ 2.500.000 → R$ 3.346.908,98 (understated)
- COEs/Estrut.: R$ 1.312.745,97 → R$ 1.629.040,84 (consolidado multi-conta)
- XP MAP COEs: REMOVIDO (double-counted com COEs/Estrut.)
- Resultado: 42 ativos, total R$ 25.829.953,72, gap R$ 374.649 = caixa (1,43%)
- Fonte: 7 PDFs XPerformance ref. 27/02/2026

**KPI Dynamics (T8 — Custo & Concentracao):**
- Adicionadas setas de dinamica (↓ = melhor, ↑ = melhor) em todos os KPIs
- HHI renomeado para "Indice de concentracao" com explicacao acessivel
- Targets simbolicos: HHI < 1.000 e Maior Posicao < 15%

**Correcoes de hardcode:**
- Solis Antares e NTN-B: valores agora computados dinamicamente de `fundos[]`
- COEs na recomendacao: agora calculado via `fundos.filter(f => f.tipo === "COE")`
- "conta 3149413" → dinamico (diversas contas)

**Fonts:**
- index.html: DM Sans/Mono → Inter/JetBrains Mono/Source Serif 4 (match real)
- Removido `<link>` duplicado de fonts dentro do AppCliente.jsx

**T5 → T4 merge:**
- KPIs editaveis integrados ao Benchmark como Investment Mandate
- Tab count: 9 → 8

---

> **Nota**: Este documento deve ser atualizado a cada mudanca significativa no sistema.
> Responsavel: Equipe Patrimonium | Ultima revisao: 15/03/2026
