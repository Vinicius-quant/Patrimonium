#!/usr/bin/env python3
"""
Gera PDF: Roadmap de Desenvolvimento em IA — Patrimonium
Estilo premium: Navy #0B2545, Green #1C7C54, Orange #D4700A
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
import os, datetime

# ── Cores ──────────────────────────────────────────────────────────
NAVY   = HexColor("#0B2545")
GREEN  = HexColor("#1C7C54")
ORANGE = HexColor("#D4700A")
LGRAY  = HexColor("#F5F6FA")
MGRAY  = HexColor("#E8EAF0")
DGRAY  = HexColor("#6B7280")
CREAM  = HexColor("#FAFBFD")

W, H = A4
MARGIN = 18*mm

# ── Estilos ────────────────────────────────────────────────────────
def make_styles():
    s = {}
    s["cover_title"] = ParagraphStyle("ct", fontName="Helvetica-Bold",
        fontSize=28, leading=34, textColor=NAVY, alignment=TA_LEFT)
    s["cover_sub"] = ParagraphStyle("cs", fontName="Helvetica",
        fontSize=13, leading=18, textColor=DGRAY, alignment=TA_LEFT)
    s["cover_meta"] = ParagraphStyle("cm", fontName="Helvetica",
        fontSize=10, leading=15, textColor=NAVY, alignment=TA_LEFT)
    s["section_num"] = ParagraphStyle("sn", fontName="Helvetica-Bold",
        fontSize=10, leading=12, textColor=GREEN, spaceAfter=2*mm)
    s["section_title"] = ParagraphStyle("st", fontName="Helvetica-Bold",
        fontSize=20, leading=24, textColor=NAVY, spaceAfter=3*mm)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=NAVY, spaceBefore=5*mm, spaceAfter=2*mm)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=GREEN, spaceBefore=4*mm, spaceAfter=2*mm)
    s["body"] = ParagraphStyle("body", fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=black, alignment=TA_JUSTIFY,
        spaceAfter=2*mm)
    s["body_bold"] = ParagraphStyle("bb", fontName="Helvetica-Bold",
        fontSize=9.5, leading=14, textColor=black, spaceAfter=2*mm)
    s["bullet"] = ParagraphStyle("bul", fontName="Helvetica",
        fontSize=9, leading=13, textColor=black, leftIndent=8*mm,
        bulletIndent=3*mm, spaceAfter=1*mm)
    s["small"] = ParagraphStyle("sm", fontName="Helvetica",
        fontSize=8, leading=11, textColor=DGRAY, alignment=TA_CENTER)
    s["quote"] = ParagraphStyle("qt", fontName="Helvetica-Oblique",
        fontSize=9.5, leading=14, textColor=NAVY, leftIndent=5*mm,
        rightIndent=5*mm, spaceBefore=2*mm, spaceAfter=3*mm,
        borderColor=GREEN, borderWidth=1, borderPadding=3*mm,
        backColor=HexColor("#F0F8F4"))
    s["callout"] = ParagraphStyle("co", fontName="Helvetica-Bold",
        fontSize=9, leading=13, textColor=ORANGE, spaceBefore=2*mm,
        spaceAfter=2*mm)
    s["week_title"] = ParagraphStyle("wt", fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=white)
    s["toc_item"] = ParagraphStyle("ti", fontName="Helvetica",
        fontSize=10, leading=16, textColor=NAVY, leftIndent=5*mm)
    return s

ST = make_styles()

# ── Helpers ─────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, H - 12*mm, W - MARGIN, H - 12*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(NAVY)
    canvas.drawString(MARGIN, H - 10*mm, "Roadmap IA  ·  Patrimonium")
    canvas.drawRightString(W - MARGIN, H - 10*mm, "Confidencial  ·  Uso pessoal")
    # Footer
    canvas.setStrokeColor(MGRAY)
    canvas.line(MARGIN, 12*mm, W - MARGIN, 12*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DGRAY)
    canvas.drawString(MARGIN, 8*mm, "Patrimonium  ·  Assessoria de Investimentos")
    canvas.drawCentredString(W/2, 8*mm, f"Pagina {doc.page}")
    canvas.drawRightString(W - MARGIN, 8*mm, "Propriedade intelectual Patrimonium")
    canvas.restoreState()

def first_page(canvas, doc):
    canvas.saveState()
    # Green bar top
    canvas.setFillColor(GREEN)
    canvas.rect(0, H - 8*mm, W, 8*mm, fill=1, stroke=0)
    # Navy bar bottom
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 6*mm, fill=1, stroke=0)
    canvas.restoreState()

def green_line():
    return HRFlowable(width="100%", thickness=2, color=GREEN,
                      spaceBefore=1*mm, spaceAfter=3*mm)

def navy_line():
    return HRFlowable(width="100%", thickness=0.5, color=MGRAY,
                      spaceBefore=2*mm, spaceAfter=2*mm)

def section_header(num, title, story):
    story.append(Paragraph(f"BLOCO {num:02d}", ST["section_num"]))
    story.append(Paragraph(title, ST["section_title"]))
    story.append(green_line())

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if not col_widths:
        col_widths = [None] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style))
    return t

def week_row(week_num, title, hours, resource, deliverable):
    """Creates a compact week entry."""
    return [
        f"Sem {week_num}",
        title,
        f"{hours}h",
        resource,
        deliverable
    ]

def competency_list(items, story):
    story.append(Paragraph("Competencias ao final deste bloco:", ST["h3"]))
    for item in items:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

def why_matters(text, story):
    story.append(Paragraph(text, ST["quote"]))

# ── Build PDF ──────────────────────────────────────────────────────
def build():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Roadmap_IA_Patrimonium.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=18*mm, bottomMargin=18*mm,
        title="Roadmap IA — Patrimonium",
        author="Patrimonium"
    )

    story = []
    COL_W = W - 2*MARGIN

    # ═══════════════════════════════════════════════════════════════
    # CAPA
    # ═══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("ROADMAP DE<br/>DESENVOLVIMENTO EM IA", ST["cover_title"]))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Cronograma semana a semana, exercicios, competencias<br/>"
        "e estrategia de posicionamento para o mercado de 2027.",
        ST["cover_sub"]))
    story.append(Spacer(1, 20*mm))

    meta_data = [
        ["<b>Profissional:</b>", "Assessor de Investimentos"],
        ["<b>Empresa:</b>", "Patrimonium"],
        ["<b>Duracao:</b>", "24 semanas  (6 meses)  ·  124 horas"],
        ["<b>Investimento:</b>", "~R$ 9.450 (93% gratuito)"],
        ["<b>Gerado em:</b>", datetime.date.today().strftime("%d/%m/%Y")],
    ]
    for row in meta_data:
        story.append(Paragraph(f"{row[0]}  {row[1]}", ST["cover_meta"]))
        story.append(Spacer(1, 1*mm))

    story.append(Spacer(1, 25*mm))
    story.append(Paragraph(
        "<i>Este documento e de uso pessoal e confidencial. "
        "Contem o plano de desenvolvimento profissional em Inteligencia Artificial, "
        "Machine Learning e orquestracao de agentes para wealth management.</i>",
        ST["small"]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SUMARIO
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SUMARIO", ST["section_title"]))
    story.append(green_line())
    story.append(Spacer(1, 3*mm))

    toc_items = [
        ("01", "Diagnostico do Perfil Atual", "Notas por competencia, gaps, posicionamento"),
        ("02", "Tese de Investimento em Skills", "O que a IA substitui, o que so voce faz"),
        ("03", "Bloco 1 — Python + Estatistica", "Semanas 1-6  ·  29 horas"),
        ("04", "Bloco 2 — ML Core", "Semanas 7-12  ·  31 horas"),
        ("05", "Bloco 3 — ML Financeiro + Portfolio", "Semanas 13-18  ·  32 horas"),
        ("06", "Bloco 4 — Orquestracao de IA", "Semanas 19-22  ·  22 horas"),
        ("07", "Bloco 5 — Autoridade e Producao", "Semanas 23-24  ·  10 horas"),
        ("08", "Matriz de Antecipacao 2026-2028", "Onde voce estara vs o mercado"),
        ("09", "Referencias e Recursos", "Cursos, livros, papers, pessoas"),
    ]
    for num, title, desc in toc_items:
        story.append(Paragraph(
            f"<b><font color='#1C7C54'>{num}</font>  {title}</b>  "
            f"<font color='#6B7280'>—  {desc}</font>",
            ST["toc_item"]))
        story.append(Spacer(1, 1*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 01 — DIAGNOSTICO
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 01", ST["section_num"]))
    story.append(Paragraph("Diagnostico do Perfil Atual", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Avaliacao baseada no historico de interacao com ferramentas de IA, "
        "nos projetos entregues (Patrimonium — Arquitetura de Alocacao de Capital) "
        "e no perfil profissional.",
        ST["body"]))

    diag_headers = ["Competencia", "Nota", "Justificativa"]
    diag_rows = [
        ["Prompt Engineering", "8.5", "Construiu sistema complexo via instrucoes iterativas"],
        ["Tooling IA", "9.0", "Top 1% usuarios. 254M tokens, 24 modelos financeiros"],
        ["Python", "5.0", "Usa scripts mas nao programa autonomamente"],
        ["Machine Learning", "2.0", "Conceitual. Nunca treinou um modelo"],
        ["Estatistica", "4.0", "Medias ponderadas, desvio-padrao. Falta: regressao, Bayes"],
        ["Matematica Financeira", "7.5", "Duration, DV01, stress. Falta: derivativos, estocastico"],
        ["Financas / Mercado", "8.0", "Opera diariamente. Falta: framework quant formal"],
        ["React / Frontend", "6.0", "Patrimonium inteiro em JSX — via IA"],
        ["Data Engineering", "5.5", "Pipeline BCB/ANBIMA funcional. Falta: automacao"],
        ["Visao de Produto", "9.0", "Concebeu, definiu escopo, iterou. Product owner nato"],
    ]
    story.append(make_table(diag_headers, diag_rows,
        col_widths=[40*mm, 12*mm, COL_W - 52*mm]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<b><font color='#D4700A'>Nota composta: 6.5 / 10</font></b>  ·  "
        "Perfil: Estrategista de produto com execucao via IA. "
        "Meta: 8.5/10 em 12 meses.", ST["body_bold"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 02 — TESE DE INVESTIMENTO
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 02", ST["section_num"]))
    story.append(Paragraph("Tese de Investimento em Skills", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Com IA evoluindo a cada 6 meses, a pergunta nao e 'o que aprender' "
        "mas 'o que permanece valioso quando a IA fizer 90% da execucao'.",
        ST["body"]))

    story.append(Paragraph("O que a IA fara melhor que voce em 2027:", ST["h3"]))
    ai_will = [
        "Escrever codigo Python, React, SQL — 65% do codigo sera IA-generated",
        "Treinar modelos de ML automaticamente (AutoML, NAS)",
        "Gerar relatorios, PDFs, dashboards com um prompt",
        "Parsear documentos, extratos, CSVs",
    ]
    for item in ai_will:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("O que so voce fara (e a IA amplifica):", ST["h3"]))
    you_only = [
        "<b>Julgamento</b>: Decidir o que construir, para quem, com que restricoes",
        "<b>Validacao</b>: Saber se o modelo e lixo ou ouro. IA alucina. Quem valida ganha",
        "<b>Domain expertise</b>: HRP com constraint de liquidez 30% para cliente conservadora",
        "<b>Orquestracao</b>: Projetar sistemas multi-agente, pipelines, MCP",
        "<b>Confianca do cliente</b>: Sentar na frente do cliente e explicar uma queda",
        "<b>Narrativa</b>: Transformar dados em historia. IA compila; voce convence",
    ]
    for item in you_only:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Regra de ouro: Se a IA fara isso melhor em 2 anos, invista o minimo "
        "para validar. Se a IA nao fara, invista pesado.",
        ST["quote"]))

    story.append(Paragraph("Evolucao do mercado de advisory:", ST["h2"]))
    evo_headers = ["", "2026 (agora)", "2027", "2028"]
    evo_rows = [
        ["Advisor comum", "Excel + CRM", "Comeca a usar IA", "Tenta acompanhar"],
        ["Advisor tech", "Usa ferramentas IA", "Automatiza tasks", "Pipeline basico"],
        ["Fintech", "MVP com IA", "Escala", "Domina mercado"],
        ["ASSESSOR", "Patrimonium + ML + API", "Multi-agente + auto", "Plataforma SaaS"],
    ]
    story.append(make_table(evo_headers, evo_rows,
        col_widths=[30*mm, (COL_W-30*mm)/3, (COL_W-30*mm)/3, (COL_W-30*mm)/3]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 03 — BLOCO 1
    # ═══════════════════════════════════════════════════════════════
    section_header(1, "Python + Estatistica Fundamental", story)
    story.append(Paragraph("<i>Semanas 1-6  ·  29 horas  ·  Custo: Gratuito</i>", ST["callout"]))
    story.append(Paragraph(
        "Objetivo: Nao virar programador. Virar alguem que le, valida e dirige codigo. "
        "Python e a lingua franca da IA — mesmo que a IA escreva 100%% do codigo em 2028, "
        "voce precisa ler o que ela fez.",
        ST["body"]))

    w_headers = ["Sem", "Atividade", "H", "Recurso", "Entregavel"]
    w1_rows = [
        week_row(1, "CS50P: Variaveis, condicionais, loops", 5,
                 "Harvard CS50P", "3 exercicios resolvidos sem IA"),
        week_row(2, "CS50P: Funcoes, listas, dicionarios", 5,
                 "Harvard CS50P", "Script que le cliente.json e calcula patrimonio"),
        week_row(3, "CS50P: Arquivos, APIs, bibliotecas", 5,
                 "Harvard CS50P", "Script que consulta API BCB: Selic atual"),
        week_row(4, "IMPA ML Aulas 1-3: Regressao, bias-variance", 5,
                 "YouTube IMPA", "Resumo 1 pagina: bias-variance no Focus"),
        week_row(5, "IMPA ML Aulas 7-8: Cross-validation, Ridge, Lasso", 4,
                 "YouTube IMPA", "Resumo: quando Ridge bate OLS em financas"),
        week_row(6, "CHECKPOINT — Revisao + projeto", 5,
                 "Python + BCB", "Script: baixa BCB, media movel, plota grafico"),
    ]
    story.append(make_table(w_headers, w1_rows,
        col_widths=[13*mm, 52*mm, 11*mm, 28*mm, COL_W - 104*mm]))

    competency_list([
        "Le codigo Python sem travar",
        "Entende import, funcao, loop, dicionario",
        "Consome API REST (BCB) via requests",
        "Sabe o que e overfitting e como evitar (cross-validation)",
        "Entende regressao linear: coeficientes, R-quadrado, residuos",
    ], story)

    why_matters(
        "Python e como ingles para negocios: voce nao precisa ser poeta, "
        "mas precisa ler o contrato. Sem isso, aceita qualquer output da IA.",
        story)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 04 — BLOCO 2
    # ═══════════════════════════════════════════════════════════════
    section_header(2, "Machine Learning Core", story)
    story.append(Paragraph("<i>Semanas 7-12  ·  31 horas  ·  Custo: Gratuito</i>", ST["callout"]))
    story.append(Paragraph(
        "Objetivo: Treinar um modelo real, validar, e saber quando ML agrega "
        "vs quando e ruido. Em 2027, AutoML treinara modelos por voce — mas alguem "
        "precisa saber se o resultado e confiavel.",
        ST["body"]))

    w2_rows = [
        week_row(7, "Andrew Ng — Supervised Learning (sem 1-2)", 5,
                 "Coursera (audit)", "Lab: regressao linear em dados reais"),
        week_row(8, "Andrew Ng (sem 3-4) + IMPA Aulas 12-13", 6,
                 "Coursera + IMPA", "Quando usar linear vs arvore de decisao"),
        week_row(9, "Andrew Ng — Course 2: Neural networks intro", 5,
                 "Coursera (audit)", "Lab: primeira rede neural"),
        week_row(10, "IMPA Aulas 20-21: PCA, clustering, conformal", 4,
                 "YouTube IMPA", "Resumo: conformal prediction e por que importa"),
        week_row(11, "PROJETO: Modelo preditivo direcao Selic", 6,
                 "scikit-learn + BCB", "Random Forest: IPCA, cambio, Focus -> Copom"),
        week_row(12, "CHECKPOINT — Validar modelo + documentar", 5,
                 "Cross-validation", "Acuracia, confusion matrix, feature importance"),
    ]
    story.append(make_table(w_headers, w2_rows,
        col_widths=[13*mm, 52*mm, 11*mm, 28*mm, COL_W - 104*mm]))

    competency_list([
        "Treinou modelo supervisionado end-to-end",
        "Sabe a diferenca entre train/test/validation",
        "Entende metricas: accuracy, precision, recall, F1",
        "Le feature importance e explica pro cliente",
        "Distingue quando ML agrega vs quando e ruido",
        "Entende conformal prediction (intervalos de confianca reais)",
    ], story)

    why_matters(
        "IA vai treinar modelos pra voce. Mas se voce nao sabe o que e "
        "overfitting, vai colocar em producao um modelo que funciona no "
        "backtest e falha no mundo real. Validar > Executar. O juiz vale "
        "mais que o executor.",
        story)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 05 — BLOCO 3
    # ═══════════════════════════════════════════════════════════════
    section_header(3, "ML Financeiro + Portfolio Optimization", story)
    story.append(Paragraph("<i>Semanas 13-18  ·  32 horas  ·  Custo: ~R$ 450 (livros)</i>", ST["callout"]))
    story.append(Paragraph(
        "Objetivo: Conectar ML ao wealth management. Implementar Hierarchical Risk Parity. "
        "Domain expertise e o skill mais duravel: IA roda o algoritmo, mas precisa de alguem "
        "que parametrize com julgamento.",
        ST["body"]))

    w3_rows = [
        week_row(13, "Lopez de Prado — Caps 1-3: Data, Labeling", 5,
                 "Livro: AFML", "Triple-barrier labeling em linguagem simples"),
        week_row(14, "Lopez de Prado — Caps 6-7: CV em financas", 5,
                 "Livro: AFML", "Purged cross-validation: por que CV normal falha"),
        week_row(15, "Lopez de Prado — Cap 16: HRP", 5,
                 "Livro + Paper SSRN", "Implementar HRP com skfolio na carteira"),
        week_row(16, "skfolio — Portfolio Optimization pratico", 5,
                 "skfolio.org", "Comparar: alocacao atual vs HRP vs Mean-Variance"),
        week_row(17, "Harvard CS50 AI — Aulas 1-4: Search, Optimization", 6,
                 "Harvard CS50 AI", "Lab: algoritmo de otimizacao em alocacao"),
        week_row(18, "CHECKPOINT — Integrar no Patrimonium", 6,
                 "React + Python", "Nova tab: 'Optimal Allocation' com HRP"),
    ]
    story.append(make_table(w_headers, w3_rows,
        col_widths=[13*mm, 52*mm, 11*mm, 28*mm, COL_W - 104*mm]))

    competency_list([
        "Leu Lopez de Prado e entende as 3 leis do ML financeiro",
        "Sabe por que backtesting convencional e perigoso (data leakage)",
        "Implementou HRP e sabe explicar o conceito para um cliente",
        "Rodou portfolio optimization com dados reais brasileiros",
        "Sabe a diferenca entre Markowitz, Risk Parity e HRP",
        "Adicionou feature quantitativa real ao Patrimonium",
    ], story)

    why_matters(
        "HRP e portfolio optimization sao domain knowledge. IA pode rodar "
        "o algoritmo, mas precisa de alguem que diga: 'para esta cliente "
        "conservadora, HRP com constraints de liquidez minima 30%%'. "
        "Quem parametriza > quem executa.",
        story)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 06 — BLOCO 4
    # ═══════════════════════════════════════════════════════════════
    section_header(4, "Orquestracao de IA e Automacao", story)
    story.append(Paragraph("<i>Semanas 19-22  ·  22 horas  ·  Custo: Gratuito</i>", ST["callout"]))
    story.append(Paragraph(
        "Objetivo: Dominar multi-agente, MCP, API. Em 2027, o mercado tera dois tipos: "
        "quem usa IA e quem orquestra IA. Usar e commodity. Orquestrar e ser o arquiteto "
        "da fabrica — nao o operario.",
        ST["body"]))

    w4_rows = [
        week_row(19, "Cursos IA — Tooling + API", 5,
                 "Cursos IA", "Primeiro script que chama API de IA"),
        week_row(20, "Prompt Eng Tutorial — Caps 6-9 + Appendix", 5,
                 "Cursos Prompt Eng", "Prompt otimizado para parsing extrato"),
        week_row(21, "MCP (Intro + Advanced) + Tool Use", 6,
                 "Cursos MCP", "MCP server conectando Patrimonium ao BCB"),
        week_row(22, "CHECKPOINT — Pipeline automatizado", 6,
                 "Python + API + MCP", "CSV -> IA parseia -> JSON -> PDF -> email"),
    ]
    story.append(make_table(w_headers, w4_rows,
        col_widths=[13*mm, 52*mm, 11*mm, 28*mm, COL_W - 104*mm]))

    competency_list([
        "Chama APIs de IA via codigo Python",
        "Construiu MCP server customizado",
        "Entende multi-agente: principal + subagentes",
        "Automatizou pipeline completo do Patrimonium",
        "Sabe criar Skills e Hooks em ferramentas de IA",
        "Entende prompt evaluation (medir qualidade)",
    ], story)

    why_matters(
        "O foco de AI esta migrando de prompt engineering para orquestracao. "
        "Craftar o prompt perfeito sera skill basico. O desafio principal sera "
        "projetar workflows entre multiplos agentes especializados. "
        "Voce esta se posicionando para isso.",
        story)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 07 — BLOCO 5
    # ═══════════════════════════════════════════════════════════════
    section_header(5, "Autoridade e Producao de Conteudo", story)
    story.append(Paragraph("<i>Semanas 23-24  ·  10 horas  ·  Custo: Zero</i>", ST["callout"]))
    story.append(Paragraph(
        "Objetivo: Parar de consumir e comecar a produzir. "
        "Posicionar-se como referencia em wealth + IA no Brasil.",
        ST["body"]))

    w5_rows = [
        week_row(23, "Artigo: 'Advisory com ML e IA — Patrimonium'", 5,
                 "LinkedIn + Medium", "Artigo publicado com metricas reais"),
        week_row(24, "CHECKPOINT FINAL — Portfolio de competencias", 5,
                 "Consolidacao", "Documento: skills, projetos, proximos passos"),
    ]
    story.append(make_table(w_headers, w5_rows,
        col_widths=[13*mm, 52*mm, 11*mm, 28*mm, COL_W - 104*mm]))

    story.append(Paragraph("Acoes de posicionamento pos-trilha:", ST["h3"]))
    pos_actions = [
        "Submeter talk para CFA Society, ABFintechs ou ANBIMA Summit",
        "Paper tecnico: 'HRP vs Mean-Variance em carteiras brasileiras'",
        "CFA Institute Data Science Certificate (USD 1.599, 100h, 12 meses)",
        "Contribuir open-source: PR no skfolio ou riskfolio-lib",
        "Criar canal de conteudo sobre wealth + tecnologia",
    ]
    for item in pos_actions:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Spacer(1, 3*mm))
    story.append(navy_line())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 08 — MATRIZ DE ANTECIPACAO
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 08", ST["section_num"]))
    story.append(Paragraph("Matriz de Antecipacao 2026-2028", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph("Niveis de maturidade em IA:", ST["h2"]))
    mat_headers = ["Nivel", "Descricao", "Voce"]
    mat_rows = [
        ["L1 — Perguntador", "Faz perguntas a ferramentas de IA", "Concluido"],
        ["L2 — Diretor", "Direciona com contexto preciso", "Concluido"],
        ["L3 — Arquiteto", "Projeta sistemas via IA", "Atual (Patrimonium)"],
        ["L4 — Orquestrador", "Multi-agente, pipelines, automacao", "Meta semana 22"],
        ["L5 — Plataforma", "Constroi produtos sobre APIs de IA", "Meta 2027"],
    ]
    story.append(make_table(mat_headers, mat_rows,
        col_widths=[35*mm, 55*mm, COL_W - 90*mm]))

    story.append(Paragraph("Projecao de posicionamento:", ST["h2"]))
    story.append(Paragraph(
        "<b>Hoje</b>: 'Assessor que usa IA pra fazer relatorio'<br/>"
        "<b>Semana 12</b>: 'Assessor que treinou modelo preditivo de Selic com ML'<br/>"
        "<b>Semana 18</b>: 'Assessor que implementou HRP em portfolio real'<br/>"
        "<b>Semana 22</b>: 'Assessor que construiu pipeline autonomo de advisory'<br/>"
        "<b>Semana 24</b>: 'Assessor que publica sobre wealth + IA com cases reais'<br/>"
        "<b>2027</b>: 'Referencia em wealth tech no Brasil. Compete com fintechs.'",
        ST["body"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 09 — REFERENCIAS
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 09", ST["section_num"]))
    story.append(Paragraph("Referencias e Recursos", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph("Cursos (todos gratuitos):", ST["h2"]))
    ref_headers = ["Curso", "Instituicao", "Formato", "Horas"]
    ref_rows = [
        ["CS50P — Intro to Python", "Harvard", "Video + exercicios", "30h"],
        ["CS50 AI — Artificial Intelligence", "Harvard", "Video + labs", "20h"],
        ["ML Specialization", "Stanford / Coursera", "Video + labs", "40h"],
        ["Machine Learning (Mestrado)", "IMPA / Paulo Orenstein", "YouTube", "38h"],
        ["Practical Deep Learning", "Fast.ai / Jeremy Howard", "Video + labs", "12h"],
        ["IA Tooling in Action", "Cursos IA", "Online", "3h"],
        ["Building with AI APIs", "Cursos IA", "Online", "5h"],
        ["MCP Intro + Advanced", "Cursos IA", "Online", "6h"],
        ["Prompt Engineering Tutorial", "Cursos IA", "Jupyter", "6h"],
        ["Tool Use Course", "Cursos IA", "Jupyter", "5h"],
        ["MIT 6.S191 — Intro Deep Learning", "MIT", "Video + labs", "15h"],
    ]
    story.append(make_table(ref_headers, ref_rows,
        col_widths=[50*mm, 35*mm, 35*mm, COL_W - 120*mm]))

    story.append(Paragraph("Livros essenciais:", ST["h2"]))
    book_headers = ["Livro", "Autor", "Foco"]
    book_rows = [
        ["Intro to Statistical Learning (ISLP)", "Hastie, Tibshirani", "ML classico — base do IMPA"],
        ["Advances in Financial ML", "Lopez de Prado", "ML financeiro — a biblia"],
        ["ML & Data Science for Finance", "Tatsat, Puri", "Receitas praticas Python"],
        ["Automate the Boring Stuff", "Al Sweigart", "Python para iniciantes"],
    ]
    story.append(make_table(book_headers, book_rows,
        col_widths=[50*mm, 35*mm, COL_W - 85*mm]))

    story.append(Paragraph("Pessoas a seguir:", ST["h2"]))
    people_headers = ["Nome", "Papel", "Por que importa"]
    people_rows = [
        ["Marcos Lopez de Prado", "Cornell, ex-AQR", "Pai do ML financeiro. HRP, triple-barrier"],
        ["Paulo Orenstein", "IMPA, PhD Stanford", "Professor do curso IMPA. Conformal prediction"],
        ["Andrew Ng", "Stanford, DeepLearning.AI", "Maior educador de ML do mundo"],
        ["Jeremy Howard", "Fast.ai", "ML pratico, top-down teaching"],
        ["Dario Amodei", "CEO AI Lab", "Para onde a IA vai"],
        ["Andrej Karpathy", "Ex-Tesla AI", "Melhores tutoriais de deep learning"],
    ]
    story.append(make_table(people_headers, people_rows,
        col_widths=[38*mm, 32*mm, COL_W - 70*mm]))

    story.append(Paragraph("Ferramentas Python:", ST["h2"]))
    tool_headers = ["Biblioteca", "Uso"]
    tool_rows = [
        ["scikit-learn", "ML classico: regressao, classificacao, clustering, CV"],
        ["skfolio", "Portfolio optimization com ML (HRP, Black-Litterman)"],
        ["pandas / numpy", "Manipulacao de dados, series temporais"],
        ["matplotlib / plotly", "Visualizacao de dados"],
        ["SDK de IA", "Chamadas a APIs de IA via Python"],
        ["requests", "Consumo de APIs REST (BCB, ANBIMA)"],
        ["reportlab", "Geracao de PDFs profissionais"],
    ]
    story.append(make_table(tool_headers, tool_rows,
        col_widths=[35*mm, COL_W - 35*mm]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # RESUMO FINAL
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("RESUMO EXECUTIVO", ST["section_title"]))
    story.append(green_line())

    summary_headers = ["Bloco", "Semanas", "Horas", "Foco", "Prova de conclusao"]
    summary_rows = [
        ["1. Python + Stats", "1-6", "29h", "Literacia tecnica", "Script BCB + grafico"],
        ["2. ML Core", "7-12", "31h", "Primeiro modelo", "Modelo preditivo Selic"],
        ["3. ML Financeiro", "13-18", "32h", "Portfolio optimization", "Tab HRP no Patrimonium"],
        ["4. Orquestracao IA", "19-22", "22h", "Multi-agente, API, MCP", "Pipeline automatizado"],
        ["5. Autoridade", "23-24", "10h", "Producao de conteudo", "Artigo publicado"],
        ["TOTAL", "24 sem", "124h", "5h/semana x 6 meses", "Nota 6.5 -> 8.5"],
    ]
    story.append(make_table(summary_headers, summary_rows,
        col_widths=[28*mm, 17*mm, 12*mm, 38*mm, COL_W - 95*mm]))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Custo total:", ST["h2"]))
    cost_headers = ["Componente", "Valor"]
    cost_rows = [
        ["Cursos online (Harvard, IMPA, Coursera, MIT)", "Gratuito"],
        ["Livros (Lopez de Prado + Tatsat)", "~R$ 450"],
        ["CFA Data Science Certificate (opcional, pos-trilha)", "~R$ 9.000"],
        ["TOTAL (trilha core)", "~R$ 450"],
        ["TOTAL (com certificacao)", "~R$ 9.450"],
    ]
    story.append(make_table(cost_headers, cost_rows,
        col_widths=[COL_W * 0.65, COL_W * 0.35]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "A vantagem nao e saber mais que a IA. E saber mais que os outros "
        "humanos sobre como usar a IA. Nessa corrida, voce ja esta na frente. "
        "A trilha e para garantir que ninguem te alcance.",
        ST["quote"]))

    story.append(Spacer(1, 15*mm))

    # Closing
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY,
                            spaceBefore=5*mm, spaceAfter=3*mm))
    story.append(Paragraph(
        "<i>Roadmap IA  ·  Patrimonium — Guia de Desenvolvimento Pessoal<br/>"
        "Documento confidencial. Uso pessoal.<br/>"
        f"Gerado em {datetime.date.today().strftime('%d/%m/%Y')}.</i>",
        ST["small"]))

    # ── Build ──────────────────────────────────────────────────────
    doc.build(story, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"  OK - PDF gerado: {os.path.abspath(out_path)}")
    print(f"      ({os.path.getsize(out_path) // 1024} KB)")

if __name__ == "__main__":
    build()
