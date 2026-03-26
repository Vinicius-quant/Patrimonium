const path = require("path");
const fs = require("fs");
const g = require("child_process").execSync("npm root -g").toString().trim();
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat, TabStopType, TabStopPosition
} = require(path.join(g, "docx"));

// ── PALETTE ──
const NAVY = "1B2A4A";
const GREEN = "276749";
const STEEL = "2C5282";
const GRAY = "718096";
const LIGHT = "F7FAFC";
const WHITE = "FFFFFF";
const RED = "9B2C2C";
const AMBER = "B7791F";
const BORDER_CLR = "CBD5E0";

// ── HELPERS ──
const border = { style: BorderStyle.SINGLE, size: 1, color: BORDER_CLR };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

const PW = 9026; // A4 content width (1" margins)

function txt(text, opts = {}) {
  return new TextRun({ text, font: "Arial", size: opts.size || 20, color: opts.color || "333333", bold: opts.bold || false, italics: opts.italics || false, ...opts });
}

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, spacing: { before: level === HeadingLevel.HEADING_1 ? 360 : 240, after: 160 }, children: [txt(text, { bold: true, size: level === HeadingLevel.HEADING_1 ? 28 : 24, color: NAVY })] });
}

function para(runs, opts = {}) {
  const children = typeof runs === "string" ? [txt(runs)] : runs;
  return new Paragraph({ spacing: { after: opts.after || 120, before: opts.before || 0 }, alignment: opts.align || AlignmentType.LEFT, children, ...opts });
}

function cell(content, opts = {}) {
  const children = typeof content === "string"
    ? [para([txt(content, { size: opts.fontSize || 18, bold: opts.bold || false, color: opts.fontColor || "333333" })], { after: 40 })]
    : content;
  return new TableCell({
    borders,
    width: { size: opts.width || 1000, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: opts.vAlign || "center",
    children,
  });
}

function headerCell(content, width) {
  return cell(content, { width, shading: NAVY, bold: true, fontColor: WHITE, fontSize: 17 });
}

function dataRow(cells, colWidths, isAlt = false) {
  return new TableRow({
    children: cells.map((c, i) => cell(c, { width: colWidths[i], shading: isAlt ? LIGHT : WHITE, fontSize: 18 })),
  });
}

function table(headers, rows, colWidths) {
  const totalW = colWidths.reduce((s, w) => s + w, 0);
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i])) }),
      ...rows.map((r, idx) => dataRow(r, colWidths, idx % 2 === 1)),
    ],
  });
}

function bullet(text, opts = {}) {
  return new Paragraph({
    numbering: { reference: "bullets", level: opts.level || 0 },
    spacing: { after: 60 },
    children: [txt(text, { size: 20 })],
  });
}

function spacer(h = 200) {
  return new Paragraph({ spacing: { before: h, after: 0 }, children: [] });
}

function scoreBar(label, score) {
  const color = score >= 7 ? GREEN : score >= 5 ? AMBER : RED;
  return para([
    txt(label + ": ", { bold: true, size: 20, color: NAVY }),
    txt(score + "/10", { bold: true, size: 22, color }),
  ]);
}

// ── DOCUMENT ──
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, font: "Arial", color: NAVY }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, font: "Arial", color: STEEL }, paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ]},
      { reference: "numbers", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ]},
    ],
  },
  sections: [
    // ═══ COVER PAGE ═══
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
      },
      children: [
        spacer(3000),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("AUDITORIA TECNICA", { size: 44, bold: true, color: NAVY })] }),
        spacer(100),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("PATRIMONIUM", { size: 56, bold: true, color: GREEN })] }),
        spacer(200),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [txt("Arquitetura de Alocacao de Capital", { size: 24, color: GRAY, italics: true })] }),
        spacer(600),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("Relatorio de Varredura Completa", { size: 22, color: STEEL })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("Codigo-fonte, Arquitetura, Riscos e Prontidao", { size: 20, color: GRAY })] }),
        spacer(1200),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("Data: 18/03/2026", { size: 20, color: GRAY })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [txt("Classificacao: CONFIDENCIAL", { size: 18, bold: true, color: RED })] }),
      ],
    },
    // ═══ CONTENT ═══
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 4 } },
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            children: [
              txt("PATRIMONIUM", { size: 16, bold: true, color: NAVY }),
              txt("\tAuditoria Tecnica — Marco 2026", { size: 14, color: GRAY }),
            ],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: BORDER_CLR, space: 4 } },
            children: [
              txt("Confidencial — ", { size: 14, color: GRAY }),
              txt("Pagina ", { size: 14, color: GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 14, color: GRAY }),
            ],
          })],
        }),
      },
      children: [
        // ── 1. VISAO GERAL ──
        heading("1. VISAO GERAL DO PROJETO"),
        para([txt("O que faz: ", { bold: true, color: NAVY }), txt("Dashboard institucional que consolida carteiras de investimentos de clientes de alta renda, puxando dados de multiplas plataformas (XP, Itau, XP Internacional) e apresentando em relatorio visual com analise de risco, eficiencia tributaria, cenarios macro e planejamento financeiro.")]),
        para([txt("Problema que resolve: ", { bold: true, color: NAVY }), txt("Assessores de investimento gastam horas montando relatorios em Excel/PowerPoint. Este sistema gera automaticamente um relatorio de qualidade institucional (nivel PIMCO/BlackRock) em segundos.")]),
        para([txt("Produto final: ", { bold: true, color: NAVY }), txt("Relatorio PDF personalizado por cliente + dashboard interativo na web.")]),
        para([txt("Classificacao: ", { bold: true, color: NAVY }), txt("Web App SPA + Ferramenta de Geracao de Relatorios. Nao e SaaS ainda — e uma ferramenta interna com potencial de virar produto.")]),

        // ── 2. ARQUITETURA ──
        heading("2. ARQUITETURA COMPLETA"),
        para([txt("Tipo: ", { bold: true, color: NAVY }), txt("Monolito front-end multi-tenant (3 instancias independentes)")]),
        heading("Fluxo de Funcionamento", HeadingLevel.HEADING_2),
        bullet("PDFs da XP (manual) sao parseados e convertidos em cliente.json"),
        bullet("APIs (BCB/ANBIMA/Yahoo) alimentam macro.json + anbima.json via scripts Node.js"),
        bullet("React SPA (AppCliente.jsx) processa os JSONs e renderiza 8-10 tabs de analise"),
        bullet("Puppeteer converte o dashboard em PDF A4 profissional"),
        heading("Pontos Criticos", HeadingLevel.HEADING_2),
        bullet("Arquivo unico de 2.300-3.000 linhas — qualquer erro quebra o sistema inteiro"),
        bullet("Dados estaticos em JSON — nao ha pipeline automatizado de extracao dos PDFs da XP"),
        bullet("3 copias do mesmo codigo (root, client-b, client-c) sao forks manuais"),
        bullet("Sem backend — nao escala para multiplos clientes sem copiar pasta"),

        // ── 3. MAPA DE ARQUIVOS ──
        new Paragraph({ children: [new PageBreak()] }),
        heading("3. MAPA DE ARQUIVOS"),
        table(
          ["Arquivo", "Linguagem", "Essencial?", "Funcao"],
          [
            ["src/AppCliente.jsx", "React/JSX", "CORE", "Dashboard inteiro — 2.287 linhas, todas as tabs"],
            ["src/data/cliente.json", "JSON", "CORE", "Dados do cliente — patrimonio, fundos, RF, estrategia"],
            ["src/data/macro.json", "JSON", "CORE", "Dados macro — Selic, CDI, IPCA, cambio, Focus"],
            ["src/data/anbima.json", "JSON", "Secundario", "Curvas ANBIMA — ETTJ, credito, VNA"],
            ["fetch-macro.mjs", "Node.js", "Essencial", "Puxa dados de 5 APIs (BCB, Yahoo, Awesome)"],
            ["fetch-anbima.mjs", "Node.js", "Secundario", "OAuth2 com ANBIMA"],
            ["scripts/generate-pdf.mjs", "Node.js", "Essencial", "Puppeteer gera PDF A4"],
            ["client-b/", "Pasta", "Fork", "Copia para cliente B (3.010 linhas)"],
            ["client-c/", "Pasta", "Fork", "Copia para cliente C (2.332 linhas)"],
            [".gitignore", "Config", "Seguranca", "Protege dados sensiveis do Git"],
            [".env", "Config", "Seguranca", "Credenciais ANBIMA (so placeholders)"],
            ["README.md", "Markdown", "Documentacao", "Instrucoes de setup e atualizacao"],
          ],
          [2200, 1200, 1200, 4426],
        ),

        // ── 4. STACK TECNOLOGICO ──
        new Paragraph({ children: [new PageBreak()] }),
        heading("4. STACK TECNOLOGICO"),
        table(
          ["Tecnologia", "Para que serve", "Boa escolha?"],
          [
            ["React 18", "Biblioteca de UI — componentes reativos", "Excelente"],
            ["Vite 6", "Build tool — hot reload rapido", "Melhor da categoria"],
            ["Recharts 2.13", "Graficos React declarativos", "OK (Nivo seria melhor)"],
            ["Puppeteer 24", "Chrome headless para PDF", "Solucao correta"],
            ["Node.js (fetch)", "Data pipeline — BCB, Yahoo, ANBIMA", "Simples e funcional"],
            ["CSS-in-JS (inline)", "Estilizacao toda inline no JSX", "Anti-pattern critico"],
            ["JSON estatico", "Banco de dados em arquivos", "Funciona, nao escala"],
          ],
          [2400, 4226, 2400],
        ),
        spacer(100),
        para([txt("Banco de dados: ", { bold: true, color: NAVY }), txt("Nenhum. Dados vivem em JSONs estaticos.")]),
        para([txt("Linguagens: ", { bold: true, color: NAVY }), txt("JavaScript/JSX (React), Node.js, Python (scripts auxiliares), HTML5, CSS3")]),

        // ── 5. LOGICA DO SISTEMA ──
        heading("5. LOGICA DO SISTEMA (CORE)"),
        para([txt("Coracao: ", { bold: true, color: NAVY }), txt("AppCliente.jsx — um unico componente React que importa 3 JSONs, processa via useMemo, e renderiza 8-10 tabs.")]),
        heading("Fluxo de Dados", HeadingLevel.HEADING_2),
        bullet("JSON estatico entra via import"),
        bullet("useMemo calcula totais, medias ponderadas, agrupamentos por estrategia/classe/conta"),
        bullet("State (tab ativa) controla qual aba e exibida"),
        bullet("JSX renderiza graficos (Recharts) e tabelas"),
        bullet("Print mode (?print=1 na URL) exibe todas as tabs em sequencia com CSS A4"),
        bullet("Puppeteer ou Ctrl+P gera PDF final"),
        heading("Tabs por Funcao", HeadingLevel.HEADING_2),
        table(
          ["Tab", "Funcao Principal"],
          [
            ["T1 — Overview", "KPIs consolidados, evolucao patrimonial, rentabilidade"],
            ["T2 — Asset Allocation", "Barras por estrategia/tipo/conta, tabela detalhada"],
            ["T3 — Macro View", "Indicadores BCB, curva Selic, inflacao"],
            ["T4 — Benchmark", "Comparativo CDI vs carteira"],
            ["T5 — Portfolio Strategy", "Patrimonio consolidado XP + externo"],
            ["T6 — Tax Alpha", "Eficiencia tributaria, come-cotas, gross equivalent"],
            ["T7 — Portfolio Efficiency", "Custos, concentracao, stress test"],
            ["T8 — Hedge", "Projecao Focus, impacto de Selic na carteira"],
            ["T9 — Financial Planning", "Simulacao 60 meses BRL/USD (so client-b)"],
          ],
          [3000, 6026],
        ),

        // ── 6. QUALIDADE DO CODIGO ──
        new Paragraph({ children: [new PageBreak()] }),
        heading("6. QUALIDADE DO CODIGO"),
        table(
          ["Criterio", "Nota", "Justificativa"],
          [
            ["Organizacao", "3/10", "Arquivo monolitico de 2.300+ linhas sem componentes separados"],
            ["Clareza", "6/10", "Variaveis bem nomeadas, mas funcoes T1-T10 sao enormes"],
            ["Padronizacao", "4/10", "CSS inline inconsistente, mistura de patterns"],
            ["Escalabilidade", "2/10", "Copiar pasta inteira para cada cliente = anti-pattern"],
            ["Manutenibilidade", "3/10", "Mudar algo global exige editar 3 arquivos"],
            ["Testes", "0/10", "Zero testes unitarios ou de integracao"],
            ["Tipagem", "2/10", "@types instalados mas sem TypeScript real"],
          ],
          [2200, 1000, 5826],
        ),
        spacer(100),
        scoreBar("NOTA GERAL DE QUALIDADE", 3.5),
        para([txt("Justificativa: ", { bold: true }), txt("O codigo funciona e produz resultado visual impressionante, mas a arquitetura e insustentavel. Um arquivo de 3.000 linhas com CSS inline, sem testes, sem componentizacao, copiado manualmente para cada cliente — isso e prototipo, nao produto.")]),

        // ── 7. RISCOS E PROBLEMAS ──
        heading("7. RISCOS E PROBLEMAS"),
        heading("Criticos", HeadingLevel.HEADING_2),
        bullet("3 copias do mesmo codigo — qualquer bugfix precisa ser replicado em 3 lugares. Ja existem divergencias."),
        bullet("Arquivo de 3.000 linhas — um typo na linha 1.500 quebra o dashboard inteiro."),
        bullet("Zero testes — nao ha como saber se uma mudanca quebrou algo sem testar manualmente."),
        bullet("Dados manuais — o pipeline PDF da XP para cliente.json e manual. Erro de digitacao compromete o relatorio."),
        heading("Altos", HeadingLevel.HEADING_2),
        bullet("CSS inline em tudo — impossivel implementar temas ou personalizacao por cliente."),
        bullet("Sem TypeScript — erros de tipo so aparecem em runtime."),
        bullet("Recharts sem key props — warnings constantes no console."),
        bullet("Print CSS fragil — quebras de pagina dependem de Chrome/OS/resolucao."),
        heading("Medios", HeadingLevel.HEADING_2),
        bullet("Python + Node misturados — scripts Python sao secundarios mas adicionam complexidade."),
        bullet("node_modules triplicado — 3 copias das mesmas dependencias (~500MB+)."),
        bullet("Sem CI/CD — deploy e manual."),
        bullet("Sem versionamento de dados — se macro.json for corrompido, nao ha rollback."),

        // ── 8. BACKUP E PRESERVACAO ──
        heading("8. BACKUP E PRESERVACAO"),
        table(
          ["Check", "Status", "Detalhe"],
          [
            ["Codigo completo?", "OK", "Todos os fontes presentes"],
            ["Dados completos?", "OK", "3 cliente.json + macro + anbima"],
            ["Git inicializado?", "ATENCAO", "Sim, mas ZERO commits"],
            [".gitignore correto?", "OK", "Protege dados sensiveis"],
            ["Risco de perda?", "ALTO", "OneDrive sync pode corromper, sem historico"],
          ],
          [2400, 1600, 5026],
        ),
        spacer(100),
        heading("Acoes para Backup 100%", HeadingLevel.HEADING_2),
        bullet("Fazer o primeiro commit AGORA — 42 arquivos staged esperando"),
        bullet("Verificar que cliente.json NAO sera commitado (esta no .gitignore)"),
        bullet("Adicionar client-c/src/data/cliente.json ao .gitignore"),
        bullet("Remover dist/ do staging se estiver la"),
        bullet("Criar backup local dos JSONs de dados em pasta separada"),

        // ── 9. PRONTIDAO GITHUB ──
        heading("9. PRONTIDAO PARA GITHUB"),
        table(
          ["Item", "Status", "Acao"],
          [
            ["Estrutura de pastas", "ATENCAO", "Funcional mas nao ideal — 3 projetos soltos"],
            ["README.md", "OK", "Existe, precisa atualizar com client-b e client-c"],
            [".gitignore", "ATENCAO", "Falta client-c/src/data/cliente.json"],
            ["Arquivos sensiveis", "OK", ".env so tem placeholders"],
            ["Primeiro commit", "CRITICO", "Nao existe — tudo staged mas nunca commitado"],
            ["Branch strategy", "CRITICO", "Inexistente"],
            ["node_modules", "OK", "Excluido pelo .gitignore"],
          ],
          [2600, 1600, 4826],
        ),

        // ── 10. TRADUCAO EXECUTIVA ──
        new Paragraph({ children: [new PageBreak()] }),
        heading("10. TRADUCAO EXECUTIVA"),
        new Paragraph({
          spacing: { before: 200, after: 200 },
          border: { left: { style: BorderStyle.SINGLE, size: 12, color: GREEN, space: 8 } },
          indent: { left: 300 },
          children: [
            txt("Patrimonium e um sistema proprietario de relatorios institucionais para wealth management. Ele consolida carteiras de multiplas plataformas — XP, Itau, conta internacional — e gera automaticamente um relatorio de 15-20 paginas com analise de alocacao, eficiencia tributaria, cenarios de juros e planejamento financeiro de longo prazo.", { size: 20, italics: true, color: STEEL }),
          ],
        }),
        new Paragraph({
          spacing: { after: 200 },
          border: { left: { style: BorderStyle.SINGLE, size: 12, color: GREEN, space: 8 } },
          indent: { left: 300 },
          children: [
            txt("O diferencial: o que uma plataforma como SmartBrain faz em dados brutos, o Patrimonium faz em inteligencia consultiva. Cada relatorio tem opiniao — identifica riscos de concentracao, sugere rotacoes tributarias, projeta cenarios com e sem aportes. Nao e um extrato; e um argumento de investimento.", { size: 20, italics: true, color: STEEL }),
          ],
        }),
        new Paragraph({
          spacing: { after: 200 },
          border: { left: { style: BorderStyle.SINGLE, size: 12, color: GREEN, space: 8 } },
          indent: { left: 300 },
          children: [
            txt("Hoje atende 3 clientes-piloto com patrimonio consolidado acima de R$ 30M. A base tecnica existe. O que falta e engenharia de produto para escalar de 3 para 300 clientes.", { size: 20, italics: true, color: STEEL }),
          ],
        }),

        // ── 11. VEREDITO FINAL ──
        heading("11. VEREDITO FINAL"),
        table(
          ["Criterio", "Nota"],
          [
            ["Qualidade visual do output", "9/10"],
            ["Qualidade do codigo", "3.5/10"],
            ["Arquitetura", "2/10"],
            ["Seguranca", "7/10"],
            ["Documentacao", "7/10"],
            ["Prontidao para producao", "3/10"],
            ["NOTA GERAL", "5/10"],
          ],
          [6000, 3026],
        ),
        spacer(200),
        para([txt("Nivel do desenvolvedor: ", { bold: true, color: NAVY }), txt("Intermediario com visao de produto avancada. Sabe o QUE construir (excepcional), mas o COMO precisa de refatoracao seria.")]),
        para([txt("Vendavel como produto? ", { bold: true, color: NAVY }), txt("Sim, com refatoracao. O output visual ja compete com solucoes de mercado. A arquitetura nao.")]),
        spacer(200),
        heading("Top 5 Melhorias para Virar Premium", HeadingLevel.HEADING_2),
        new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 80 }, children: [txt("Componentizar", { bold: true }), txt(" — quebrar o monolito em ~20 componentes (Header, KPICard, BarChart, TabContent, etc.)")] }),
        new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 80 }, children: [txt("Unificar clientes", { bold: true }), txt(" — um unico codebase com cliente.json como parametro, nao 3 pastas separadas")] }),
        new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 80 }, children: [txt("Adicionar TypeScript", { bold: true }), txt(" — eliminar erros de runtime")] }),
        new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 80 }, children: [txt("Parser automatico de PDFs", { bold: true }), txt(" — extracao automatizada dos relatorios XP para JSON")] }),
        new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 80 }, children: [txt("Backend minimo", { bold: true }), txt(" — Node/Express ou Supabase para servir dados por cliente sem copiar codigo")] }),

        // ── ESTATISTICAS ──
        spacer(300),
        new Paragraph({
          spacing: { after: 0 },
          border: { top: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 8 } },
          children: [],
        }),
        para([txt("ESTATISTICAS DO CODIGO", { bold: true, size: 22, color: NAVY })], { before: 100 }),
        table(
          ["Metrica", "Valor"],
          [
            ["Total linhas JSX (3 clientes)", "7.629"],
            ["Total linhas scripts (Node+Python)", "2.724"],
            ["Dependencias de producao", "3 (React, ReactDOM, Recharts)"],
            ["Dependencias de dev", "4 (Vite, plugin-react, types, Puppeteer)"],
            ["Arquivos de codigo", "51"],
            ["APIs externas integradas", "5 (BCB SGS, BCB Olinda, Yahoo, Awesome, ANBIMA)"],
            ["Clientes ativos", "3 pilotos"],
            ["Patrimonio consolidado coberto", "> R$ 30M"],
          ],
          [4500, 4526],
        ),
      ],
    },
  ],
});

// ── GENERATE ──
const OUT = path.join("C:\\Users\\vinic\\OneDrive\\Dash Institucional", "AUDITORIA_TECNICA_PATRIMONIUM.docx");
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("Generated:", OUT, "(" + (buf.length / 1024).toFixed(0) + " KB)");
});
