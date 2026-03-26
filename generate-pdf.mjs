/**
 * Patrimonium — PDF Generator
 *
 * Gera relatório PDF pixel-perfect via Puppeteer (headless Chrome).
 * Substitui Ctrl+P com controle total sobre:
 *   - Page breaks
 *   - Renderização de gráficos Recharts
 *   - Margens e tamanho A4
 *   - Numeração de páginas
 *   - Marca d'água (opcional)
 *
 * Uso:
 *   npm run pdf
 *   npm run pdf -- --watermark "CONFIDENCIAL"
 *   npm run pdf -- --output "relatorio-mar-26.pdf"
 */

import puppeteer from "puppeteer";
import { execSync, spawn } from "child_process";
import { existsSync, mkdirSync } from "fs";
import { resolve, join } from "path";

// ── Config ──────────────────────────────────────────────
const BASE_URL = "http://localhost";
const VITE_PORT = 5173; // fallback — tenta detectar
const OUTPUT_DIR = resolve("output");
const DEFAULT_NAME = "Patrimonium_Relatorio";

// ── Args ────────────────────────────────────────────────
const args = process.argv.slice(2);
const getArg = (flag) => {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : null;
};

const watermark = getArg("--watermark");
const outputName = getArg("--output") || `${DEFAULT_NAME}_${new Date().toISOString().slice(0, 10)}.pdf`;
const noServer = args.includes("--no-server");

// ── Helpers ─────────────────────────────────────────────
function log(msg) {
  const ts = new Date().toLocaleTimeString("pt-BR");
  console.log(`  [${ts}] ${msg}`);
}

async function findVitePort() {
  // Tenta portas comuns do Vite
  for (const port of [5173, 5174, 5175, 8791, 3000]) {
    try {
      const res = await fetch(`${BASE_URL}:${port}`, { signal: AbortSignal.timeout(1000) });
      if (res.ok) return port;
    } catch {}
  }
  return null;
}

async function startViteServer() {
  log("Iniciando Vite dev server...");
  const vite = spawn("node", ["node_modules/vite/bin/vite.js"], {
    stdio: "pipe",
    shell: true,
    cwd: resolve("."),
  });

  return new Promise((resolve, reject) => {
    let port = null;
    const timeout = setTimeout(() => reject(new Error("Vite não iniciou em 15s")), 15000);

    vite.stdout.on("data", (data) => {
      const str = data.toString();
      const match = str.match(/localhost:(\d+)/);
      if (match) {
        port = parseInt(match[1]);
        clearTimeout(timeout);
        log(`Vite rodando na porta ${port}`);
        resolve({ port, process: vite });
      }
    });

    vite.stderr.on("data", (data) => {
      const str = data.toString();
      if (str.includes("error")) {
        clearTimeout(timeout);
        reject(new Error("Vite error: " + str));
      }
    });
  });
}

// ── Main ────────────────────────────────────────────────
async function generatePDF() {
  console.log("\n  ╔══════════════════════════════════════════╗");
  console.log("  ║   Patrimonium · PDF Generator             ║");
  console.log("  ║   Arquitetura de Alocação de Capital     ║");
  console.log("  ╚══════════════════════════════════════════╝\n");

  // 1. Encontrar ou iniciar servidor
  let port = await findVitePort();
  let viteProcess = null;

  if (!port && !noServer) {
    const server = await startViteServer();
    port = server.port;
    viteProcess = server.process;
    // Dar tempo pro HMR estabilizar
    await new Promise(r => setTimeout(r, 2000));
  } else if (!port) {
    console.error("  ✗ Nenhum servidor encontrado. Rode 'npm run dev' primeiro.\n");
    process.exit(1);
  }

  log(`Servidor detectado em localhost:${port}`);

  // 2. Criar diretório de output
  if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });
  const outputPath = join(OUTPUT_DIR, outputName);

  // 3. Abrir Puppeteer
  log("Iniciando Chromium...");
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-gpu",
      "--font-render-hinting=none", // Melhora renderização de fontes
    ],
  });

  const page = await browser.newPage();

  // Viewport A4 portrait para renderizar 1:1 sem escala
  await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });

  // 4. Navegar para print mode
  const url = `${BASE_URL}:${port}/?print=1`;
  log(`Carregando ${url}`);
  await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });

  // 5. Esperar gráficos Recharts renderizarem
  log("Aguardando renderização dos gráficos...");
  await page.waitForSelector(".recharts-wrapper", { timeout: 10000 }).catch(() => {
    log("⚠ Nenhum gráfico Recharts encontrado — continuando...");
  });

  // Espera extra para animações e fontes
  await new Promise(r => setTimeout(r, 3000));

  // 6. Garantir que todas as fontes carregaram
  await page.evaluate(() => document.fonts.ready);
  log("Fontes carregadas");

  // 7. Adicionar marca d'água se solicitado
  if (watermark) {
    log(`Adicionando marca d'água: "${watermark}"`);
    await page.evaluate((text) => {
      const wm = document.createElement("div");
      wm.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        display: flex; align-items: center; justify-content: center;
        pointer-events: none; z-index: 99999;
        font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 700;
        color: rgba(11, 37, 69, 0.04); transform: rotate(-35deg);
        letter-spacing: 0.1em; text-transform: uppercase;
      `;
      wm.textContent = text;
      document.body.appendChild(wm);
    }, watermark);
  }

  // 8. Adicionar classe para estilos específicos do PDF
  await page.evaluate(() => {
    document.body.classList.add("print-ready");
  });

  // 9. Gerar PDF
  log("Gerando PDF...");
  await page.pdf({
    path: outputPath,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: false,
    margin: {
      top: "12mm",
      bottom: "18mm",
      left: "10mm",
      right: "10mm",
    },
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="width: 100%; font-family: 'Helvetica Neue', 'Arial', sans-serif; font-size: 7px; color: #A0AEC0; display: flex; justify-content: space-between; padding: 0 10mm;">
        <span>Patrimonium</span>
        <span></span>
        <span style="font-size: 6.5px;">Confidencial · Uso exclusivo do destinatário</span>
      </div>
    `,
    footerTemplate: `
      <div style="width: 100%; font-family: 'Helvetica Neue', 'Arial', sans-serif; font-size: 7px; color: #718096; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 10mm;">
        <span><strong style="color: #1B2A4A; font-size: 7.5px;">Patrimonium</strong></span>
        <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
        <span style="font-size: 6px;">Propriedade intelectual Patrimonium · Reprodução proibida</span>
      </div>
    `,
  });

  const fileSizeKB = Math.round((await import("fs")).statSync(outputPath).size / 1024);
  log(`PDF gerado: ${outputPath} (${fileSizeKB} KB)`);

  // 10. Cleanup
  await browser.close();
  if (viteProcess) {
    viteProcess.kill();
    log("Vite server encerrado");
  }

  console.log("\n  ✓ Relatório salvo em:");
  console.log(`    ${outputPath}\n`);
}

generatePDF().catch((err) => {
  console.error("\n  ✗ Erro:", err.message, "\n");
  process.exit(1);
});
