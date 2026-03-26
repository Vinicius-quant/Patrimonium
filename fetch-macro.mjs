/**
 * ============================================================
 * SCRIPT DE ATUALIZAÇÃO AUTOMÁTICA DE DADOS MACRO
 * ============================================================
 *
 * Uso:  npm run update-macro
 *
 * Fontes:
 *   - Banco Central (SGS): Selic, CDI, IPCA, Câmbio (PTAX)
 *   - BCB Focus (OLINDA): Projeções de mercado (Boletim Focus)
 *   - Yahoo Finance: Ibovespa, Ouro, S&P500, DXY, Bitcoin, etc.
 *   - AwesomeAPI: Cotação do dólar em tempo real
 *
 * Séries BCB/SGS utilizadas:
 *   432   = Selic meta (% a.a.)
 *   4389  = CDI anualizado (% a.a., base 252)
 *   4391  = CDI acumulado no mês (% a.m.)
 *   433   = IPCA variação mensal (%)
 *   13522 = IPCA acumulado 12 meses (%)
 *   1     = Dólar PTAX compra (R$/US$)
 *
 * Focus API (OLINDA):
 *   ExpectativasMercadoAnuais → IPCA, Selic, PIB Total, Câmbio
 *   ExpectativasMercadoSelic  → Projeção por reunião do Copom
 *
 * O script gera/atualiza o arquivo:
 *   src/data/macro.json
 *
 * A dashboard importa esse JSON automaticamente.
 * ============================================================
 */

import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT = join(__dirname, 'src', 'data', 'macro.json');

// ── Helpers ──────────────────────────────────────────────────

async function fetchJSON(url, label) {
  try {
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn(`  ⚠ ${label}: ${e.message}`);
    return null;
  }
}

function formatDate(d) {
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`;
}

function dateRange(monthsBack) {
  const end = new Date();
  const start = new Date();
  start.setMonth(start.getMonth() - monthsBack);
  return { start: formatDate(start), end: formatDate(end) };
}

// ── BCB SGS API ─────────────────────────────────────────────

async function fetchBCBSeries(serieId, label, months = 24) {
  const { start, end } = dateRange(months);
  const url = `https://api.bcb.gov.br/dados/serie/bcdata.sgs.${serieId}/dados?formato=json&dataInicial=${start}&dataFinal=${end}`;
  console.log(`  📡 ${label} (série ${serieId})...`);
  return await fetchJSON(url, label);
}

// ── BCB Focus API (OLINDA) ──────────────────────────────────
// Expectativas anuais do mercado (Boletim Focus)
// Indicadores: 'IPCA', 'Selic', 'PIB Total', 'Câmbio'

async function fetchFocusAnual(indicator, year) {
  const url = `https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?$filter=Indicador eq '${indicator}' and DataReferencia eq '${year}'&$orderby=Data desc&$top=1&$format=json`;
  console.log(`  📡 Focus Anual: ${indicator} ${year}...`);
  return await fetchJSON(url, `Focus ${indicator}`);
}

// Selic por reunião do Copom
async function fetchFocusSelicReuniao(reuniao) {
  const url = `https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoSelic?$filter=Reuniao eq '${reuniao}' and baseCalculo eq 1&$orderby=Data desc&$top=1&$format=json`;
  console.log(`  📡 Focus Selic: ${reuniao}...`);
  return await fetchJSON(url, `Focus Selic ${reuniao}`);
}

// Todas as reuniões de um ano (para curva Selic)
async function fetchFocusSelicCurva(year) {
  const url = `https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoSelic?$filter=baseCalculo eq 1 and startswith(Reuniao,'R') and endswith(Reuniao,'/${year}')&$orderby=Data desc&$format=json`;
  console.log(`  📡 Focus Selic curva ${year}...`);
  return await fetchJSON(url, `Focus Selic curva ${year}`);
}

// ── Yahoo Finance (via query2) ──────────────────────────────

async function fetchYahoo(symbol, label) {
  const url = `https://query2.finance.yahoo.com/v8/finance/chart/${symbol}?range=1y&interval=1d`;
  console.log(`  📡 ${label} (${symbol})...`);
  try {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    const result = json?.chart?.result?.[0];
    const meta = result?.meta;
    if (!meta) return null;

    // Calcular YTD correto: achar o primeiro pregão do ano corrente
    let ytdPct = null;
    const timestamps = result?.timestamp;
    const closes = result?.indicators?.quote?.[0]?.close;
    if (timestamps && closes) {
      const currentYear = new Date().getFullYear();
      for (let i = 0; i < timestamps.length; i++) {
        const d = new Date(timestamps[i] * 1000);
        if (d.getFullYear() === currentYear && closes[i] != null) {
          ytdPct = parseFloat(((meta.regularMarketPrice / closes[i] - 1) * 100).toFixed(2));
          break;
        }
      }
    }

    return {
      price: meta.regularMarketPrice,
      prevClose: meta.chartPreviousClose,
      ytdPct,
      currency: meta.currency
    };
  } catch (e) {
    console.warn(`  ⚠ ${label}: ${e.message}`);
    return null;
  }
}

// ── AwesomeAPI (câmbio real-time) ───────────────────────────

async function fetchDolar() {
  console.log(`  📡 Dólar (AwesomeAPI)...`);
  return await fetchJSON('https://economia.awesomeapi.com.br/last/USD-BRL', 'Dólar');
}

// ── MAIN ────────────────────────────────────────────────────

async function main() {
  console.log('\n🔄 Atualizando dados macroeconômicos...\n');

  const now = new Date();
  const thisYear = now.getFullYear();
  const nextYear = thisYear + 1;

  const result = {
    _geradoEm: now.toISOString(),
    _fontes: [
      "Banco Central do Brasil (SGS)",
      "BCB Focus (Expectativas de Mercado)",
      "AwesomeAPI (Câmbio)",
      "Yahoo Finance (Bolsas)"
    ],
    selic: {},
    cdi: {},
    ipca: {},
    cambio: {},
    ibovespa: {},
    ouro: {},
    internacional: {},
    focus: {},
    focusSelicCurva: [],
    selicHistorico: [],
    ipcaHistorico: [],
    cdiMensal: [],
  };

  // ── 1. SELIC ────────────────────────────────────────────
  const selicData = await fetchBCBSeries(432, 'Selic Meta', 24);
  if (selicData?.length) {
    const last = selicData[selicData.length - 1];
    result.selic.atual = parseFloat(last.valor);
    result.selic.data = last.data;
    result.selicHistorico = selicData.map(d => ({ data: d.data, valor: parseFloat(d.valor) }));
  }

  // ── 2. CDI ──────────────────────────────────────────────
  // Serie 4389 = CDI anualizado (% a.a., base 252)
  const cdiAnual = await fetchBCBSeries(4389, 'CDI anualizado', 3);
  if (cdiAnual?.length) {
    result.cdi.anual = parseFloat(cdiAnual[cdiAnual.length - 1].valor);
  }

  // Serie 4391 = CDI acumulado no mês (% a.m.) — CORRIGIDO: era 4393 (swap DI)
  const cdiMensal = await fetchBCBSeries(4391, 'CDI acum. mensal', 24);
  if (cdiMensal?.length) {
    result.cdi.ultimoMes = parseFloat(cdiMensal[cdiMensal.length - 1].valor);
    result.cdi.dataMes = cdiMensal[cdiMensal.length - 1].data;
    result.cdiMensal = cdiMensal.map(d => ({ data: d.data, valor: parseFloat(d.valor) }));

    // CDI acumulado 12M (composto)
    // Pegar últimos 12 meses completos (excluir mês parcial se valor < 0.5)
    const completeMeses = cdiMensal.filter(d => parseFloat(d.valor) >= 0.5);
    const last12 = completeMeses.slice(-12);
    let acum = 1;
    last12.forEach(d => { acum *= (1 + parseFloat(d.valor) / 100); });
    result.cdi.acum12m = parseFloat(((acum - 1) * 100).toFixed(2));
  }

  // ── 3. IPCA ─────────────────────────────────────────────
  // Serie 433 = IPCA mensal (%)
  const ipcaMensal = await fetchBCBSeries(433, 'IPCA mensal', 24);
  if (ipcaMensal?.length) {
    const last = ipcaMensal[ipcaMensal.length - 1];
    result.ipca.mensal = parseFloat(last.valor);
    result.ipca.dataMes = last.data;
    result.ipcaHistorico = ipcaMensal.map(d => ({ data: d.data, valor: parseFloat(d.valor) }));
  }

  // Serie 13522 = IPCA acumulado 12 meses (fonte oficial BCB)
  const ipca12m = await fetchBCBSeries(13522, 'IPCA acum. 12M', 3);
  if (ipca12m?.length) {
    result.ipca.acum12m = parseFloat(ipca12m[ipca12m.length - 1].valor);
  }

  // ── 4. CÂMBIO ───────────────────────────────────────────
  const dolar = await fetchDolar();
  if (dolar?.USDBRL) {
    result.cambio.dolar = parseFloat(dolar.USDBRL.bid);
    result.cambio.varDia = parseFloat(dolar.USDBRL.pctChange);
    result.cambio.dataHora = dolar.USDBRL.create_date;
  }

  // PTAX para cálculo YTD correto (primeiro dia útil do ano até hoje)
  const ptaxYTD = await fetchBCBSeries(1, 'PTAX YTD', 4);
  if (ptaxYTD?.length) {
    // Achar primeiro valor do ano corrente
    const thisYearStr = String(thisYear);
    const ptaxThisYear = ptaxYTD.filter(d => d.data.endsWith(thisYearStr));
    if (ptaxThisYear.length >= 2) {
      const first = parseFloat(ptaxThisYear[0].valor);
      const last = parseFloat(ptaxThisYear[ptaxThisYear.length - 1].valor);
      result.cambio.varAno = parseFloat(((last / first - 1) * 100).toFixed(2));
    }
  }

  // ── 5. IBOVESPA ─────────────────────────────────────────
  const ibov = await fetchYahoo('^BVSP', 'Ibovespa');
  if (ibov) {
    result.ibovespa.pontos = ibov.price;
    // Usar YTD correto (primeiro pregão do ano), não chartPreviousClose (1 ano atrás)
    result.ibovespa.varAno = ibov.ytdPct ?? 0;
  }

  // ── 6. OURO ─────────────────────────────────────────────
  const gold = await fetchYahoo('GC=F', 'Ouro');
  if (gold) {
    result.ouro.usd = gold.price;
    result.ouro.varAno = gold.ytdPct ?? 0;
  }

  // ── 7. INTERNACIONAL ────────────────────────────────────
  const symbols = [
    { sym: '^GSPC', key: 'sp500', label: 'S&P 500' },
    { sym: 'DX-Y.NYB', key: 'dxy', label: 'DXY' },
    { sym: 'BTC-USD', key: 'bitcoin', label: 'Bitcoin' },
    { sym: '^TNX', key: 'us10y', label: 'US 10Y' },
    { sym: 'CL=F', key: 'oil', label: 'Petróleo WTI' },
    { sym: '^VIX', key: 'vix', label: 'VIX' },
  ];

  for (const { sym, key, label } of symbols) {
    const data = await fetchYahoo(sym, label);
    if (data) {
      result.internacional[key] = {
        price: data.price,
        varAno: data.ytdPct ?? 0,
        currency: data.currency
      };
    }
  }

  // ── 8. FOCUS — Expectativas Anuais ────────────────────
  // Indicador 'IPCA' (não 'Inflação')
  const focusIPCA = await fetchFocusAnual('IPCA', String(thisYear));
  if (focusIPCA?.value?.length) {
    result.focus.ipca = parseFloat(focusIPCA.value[0].Mediana);
    result.focus.ipcaData = focusIPCA.value[0].Data;
  }

  const focusIPCA2 = await fetchFocusAnual('IPCA', String(nextYear));
  if (focusIPCA2?.value?.length) {
    result.focus.ipcaProx = parseFloat(focusIPCA2.value[0].Mediana);
  }

  // Indicador 'PIB Total'
  const focusPIB = await fetchFocusAnual('PIB Total', String(thisYear));
  if (focusPIB?.value?.length) {
    result.focus.pib = parseFloat(focusPIB.value[0].Mediana);
  }

  const focusPIB2 = await fetchFocusAnual('PIB Total', String(nextYear));
  if (focusPIB2?.value?.length) {
    result.focus.pibProx = parseFloat(focusPIB2.value[0].Mediana);
  }

  // Indicador 'Câmbio' (NÃO 'Taxa de câmbio' — nome corrigido)
  const focusCambio = await fetchFocusAnual('Câmbio', String(thisYear));
  if (focusCambio?.value?.length) {
    result.focus.cambioFim = parseFloat(focusCambio.value[0].Mediana);
  }

  // Selic fim de ano — usar ExpectativasMercadoAnuais (NÃO ExpectativasMercadoSelic)
  // ExpectativasMercadoSelic retorna por reunião, não por ano
  const focusSelic = await fetchFocusAnual('Selic', String(thisYear));
  if (focusSelic?.value?.length) {
    result.focus.selicFim = parseFloat(focusSelic.value[0].Mediana);
    result.focus.selicData = focusSelic.value[0].Data;
  }

  const focusSelic2 = await fetchFocusAnual('Selic', String(nextYear));
  if (focusSelic2?.value?.length) {
    result.focus.selicProx = parseFloat(focusSelic2.value[0].Mediana);
  }

  // ── 9. CURVA SELIC (por reunião do Copom) ─────────────
  // Pegar todas as reuniões de 2026 e 2027 para montar a curva
  const selicCurva = [];

  // Adicionar ponto atual
  if (result.selic.atual) {
    selicCurva.push({ reuniao: 'Atual', mediana: result.selic.atual });
  }

  // Reuniões de 2026 (R2 a R8)
  for (let r = 2; r <= 8; r++) {
    const data = await fetchFocusSelicReuniao(`R${r}/${thisYear}`);
    if (data?.value?.length) {
      selicCurva.push({
        reuniao: `R${r}/${thisYear}`,
        mediana: parseFloat(data.value[0].Mediana),
        respondentes: data.value[0].numeroRespondentes,
      });
    }
  }

  // Reuniões de 2027 (R1 a R4 para projeção mais longa)
  for (let r = 1; r <= 4; r++) {
    const data = await fetchFocusSelicReuniao(`R${r}/${nextYear}`);
    if (data?.value?.length) {
      selicCurva.push({
        reuniao: `R${r}/${nextYear}`,
        mediana: parseFloat(data.value[0].Mediana),
        respondentes: data.value[0].numeroRespondentes,
      });
    }
  }

  result.focusSelicCurva = selicCurva;

  // ── SALVAR ──────────────────────────────────────────────
  writeFileSync(OUTPUT, JSON.stringify(result, null, 2), 'utf-8');

  console.log('\n✅ Dados salvos em src/data/macro.json');
  console.log('\n📊 Resumo:');
  console.log(`   Selic: ${result.selic.atual ?? '—'}% a.a.`);
  console.log(`   CDI anual: ${result.cdi.anual ?? '—'}% | mensal: ${result.cdi.ultimoMes ?? '—'}% | 12M: ${result.cdi.acum12m ?? '—'}%`);
  console.log(`   IPCA mensal: ${result.ipca.mensal ?? '—'}% | 12M: ${result.ipca.acum12m ?? '—'}%`);
  console.log(`   Dólar: R$ ${result.cambio.dolar ?? '—'} | YTD: ${result.cambio.varAno ?? '—'}%`);
  console.log(`   Ibovespa: ${result.ibovespa.pontos ?? '—'} pts | YTD: ${result.ibovespa.varAno ?? '—'}%`);
  console.log(`   Ouro: US$ ${result.ouro.usd ?? '—'}/oz`);
  console.log(`   Focus ${thisYear}: IPCA ${result.focus.ipca ?? '—'}% | Selic ${result.focus.selicFim ?? '—'}% | PIB ${result.focus.pib ?? '—'}% | Câmbio R$ ${result.focus.cambioFim ?? '—'}`);
  console.log(`   Focus ${nextYear}: IPCA ${result.focus.ipcaProx ?? '—'}% | Selic ${result.focus.selicProx ?? '—'}%`);
  console.log(`   Curva Selic: ${selicCurva.map(s => s.reuniao + ':' + s.mediana + '%').join(' → ')}`);
  console.log('');
}

main().catch(console.error);
