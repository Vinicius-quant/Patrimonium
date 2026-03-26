#!/usr/bin/env python3
"""
Gera PDF: Relatorio Consolidado — Racional de Desenvolvimento IA
Resume toda a mentoria, decisoes, diagnostico e roadmap discutidos na sessao.
Estilo premium: Navy #0B2545, Green #1C7C54, Orange #D4700A
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
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

W, H = A4
MARGIN = 18*mm

# ── Estilos ────────────────────────────────────────────────────────
def make_styles():
    s = {}
    s["cover_title"] = ParagraphStyle("ct", fontName="Helvetica-Bold",
        fontSize=26, leading=32, textColor=NAVY, alignment=TA_LEFT)
    s["cover_sub"] = ParagraphStyle("cs", fontName="Helvetica",
        fontSize=12, leading=17, textColor=DGRAY, alignment=TA_LEFT)
    s["cover_meta"] = ParagraphStyle("cm", fontName="Helvetica",
        fontSize=10, leading=15, textColor=NAVY, alignment=TA_LEFT)
    s["section_num"] = ParagraphStyle("sn", fontName="Helvetica-Bold",
        fontSize=10, leading=12, textColor=GREEN, spaceAfter=2*mm)
    s["section_title"] = ParagraphStyle("st", fontName="Helvetica-Bold",
        fontSize=18, leading=22, textColor=NAVY, spaceAfter=3*mm)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold",
        fontSize=12, leading=16, textColor=NAVY, spaceBefore=4*mm, spaceAfter=2*mm)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=GREEN, spaceBefore=3*mm, spaceAfter=2*mm)
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
    return s

ST = make_styles()

# ── Helpers ─────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, H - 12*mm, W - MARGIN, H - 12*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(NAVY)
    canvas.drawString(MARGIN, H - 10*mm, "Relatorio Consolidado  ·  Mentoria IA")
    canvas.drawRightString(W - MARGIN, H - 10*mm, "Confidencial  ·  Uso pessoal")
    canvas.setStrokeColor(MGRAY)
    canvas.line(MARGIN, 12*mm, W - MARGIN, 12*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DGRAY)
    canvas.drawString(MARGIN, 8*mm, "Patrimonium  ·  Assessoria de Investimentos")
    canvas.drawCentredString(W/2, 8*mm, f"Pagina {doc.page}")
    canvas.drawRightString(W - MARGIN, 8*mm, datetime.date.today().strftime("%d/%m/%Y"))
    canvas.restoreState()

def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GREEN)
    canvas.rect(0, H - 8*mm, W, 8*mm, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 6*mm, fill=1, stroke=0)
    canvas.restoreState()

def green_line():
    return HRFlowable(width="100%", thickness=2, color=GREEN,
                      spaceBefore=1*mm, spaceAfter=3*mm)

def navy_line():
    return HRFlowable(width="100%", thickness=0.5, color=MGRAY,
                      spaceBefore=2*mm, spaceAfter=2*mm)

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

# ── Build PDF ──────────────────────────────────────────────────────
def build():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Relatorio_Racional_IA_Patrimonium.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=18*mm, bottomMargin=18*mm,
        title="Relatorio Consolidado — Mentoria IA",
        author="Patrimonium"
    )

    story = []
    COL_W = W - 2*MARGIN

    # ═══════════════════════════════════════════════════════════════
    # CAPA
    # ═══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("RELATORIO CONSOLIDADO<br/>MENTORIA IA", ST["cover_title"]))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Sintese completa do racional de desenvolvimento em Inteligencia Artificial,<br/>"
        "diagnostico de perfil, decisoes estrategicas e roadmap de 24 semanas.",
        ST["cover_sub"]))
    story.append(Spacer(1, 20*mm))

    meta_data = [
        ["<b>Profissional:</b>", "Assessor de Investimentos"],
        ["<b>Empresa:</b>", "Patrimonium"],
        ["<b>Projeto de referencia:</b>", "Patrimonium — Arquitetura de Alocacao de Capital"],
        ["<b>Sessao de mentoria:</b>", "13-15 de marco de 2026"],
        ["<b>Gerado em:</b>", datetime.date.today().strftime("%d/%m/%Y")],
    ]
    for row in meta_data:
        story.append(Paragraph(f"{row[0]}  {row[1]}", ST["cover_meta"]))
        story.append(Spacer(1, 1*mm))

    story.append(Spacer(1, 25*mm))
    story.append(Paragraph(
        "<i>Este documento consolida todas as analises, decisoes e racionais "
        "da sessao de mentoria em IA. Serve como referencia para continuidade "
        "do desenvolvimento em novas sessoes de trabalho.</i>",
        ST["small"]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 1 — CONTEXTO DO PROJETO PRISMA
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 01", ST["section_num"]))
    story.append(Paragraph("Contexto: O Projeto Patrimonium", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Antes de iniciar a mentoria em IA, foi construido — inteiramente "
        "via orquestracao de IA — o Patrimonium, uma plataforma de alocacao de capital para wealth "
        "management. O projeto serviu como prova de conceito do potencial de "
        "orquestracao de IA.",
        ST["body"]))

    story.append(Paragraph("Metricas do Patrimonium:", ST["h2"]))

    patrimonium_headers = ["Metrica", "Valor"]
    patrimonium_rows = [
        ["Linhas de codigo (JSX)", "2.263"],
        ["Linhas de dados (JSON)", "5.533"],
        ["Total do projeto", "~9.400 linhas"],
        ["Modelos financeiros", "24 (Duration, DV01, HRP, Stress, etc.)"],
        ["Componentes Recharts", "64 graficos"],
        ["Tabelas financeiras", "17"],
        ["Operacoes com arrays", "178"],
        ["Tokens consumidos", "254,6 milhoes"],
        ["Custo estimado (API)", "~USD 117"],
        ["Sessoes de trabalho", "3 sessoes"],
        ["Total de mensagens", "2.558"],
    ]
    story.append(make_table(patrimonium_headers, patrimonium_rows,
        col_widths=[COL_W * 0.45, COL_W * 0.55]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Comparativo de sofisticacao:", ST["h2"]))

    comp_headers = ["Plataforma", "Feature match vs Patrimonium"]
    comp_rows = [
        ["XP Investimentos App", "9% — basicamente consulta de saldo"],
        ["BTG Wealth Dashboard", "17% — alocacao + benchmarks"],
        ["Bloomberg Terminal (funcoes base)", "48% — alocacao + risco + DV01"],
        ["Patrimonium", "100% — referencia completa"],
    ]
    story.append(make_table(comp_headers, comp_rows,
        col_widths=[COL_W * 0.45, COL_W * 0.55]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "O Patrimonium e um 'Bloomberg Lite' brasileiro. Nenhum assessor no Brasil "
        "tem uma ferramenta desse nivel feita sob medida. Plataforma proprietaria "
        "construida via orquestracao de IA para wealth management.",
        ST["quote"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 2 — DIAGNOSTICO DE PERFIL
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 02", ST["section_num"]))
    story.append(Paragraph("Diagnostico de Perfil", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Avaliacao baseada no historico de interacao com ferramentas de IA, "
        "nos projetos entregues e no perfil profissional como assessor "
        "da Patrimonium.",
        ST["body"]))

    diag_headers = ["Competencia", "Nota", "Justificativa"]
    diag_rows = [
        ["Prompt Engineering", "8.5", "Construiu sistema complexo via instrucoes iterativas"],
        ["Tooling IA", "9.0", "Top 1%% usuarios. 254M tokens, 24 modelos"],
        ["Python", "5.0", "Usa scripts mas nao programa autonomamente"],
        ["Machine Learning", "2.0", "Conceitual. Nunca treinou um modelo"],
        ["Estatistica", "4.0", "Medias ponderadas, desvio. Falta: regressao, Bayes"],
        ["Matematica Financeira", "7.5", "Duration, DV01, stress. Falta: derivativos"],
        ["Financas / Mercado", "8.0", "Opera diariamente. Falta: framework quant"],
        ["React / Frontend", "6.0", "Patrimonium inteiro em JSX — via IA"],
        ["Data Engineering", "5.5", "Pipeline BCB/ANBIMA. Falta: automacao"],
        ["Visao de Produto", "9.0", "Concebeu, definiu escopo, iterou. Product owner"],
    ]
    story.append(make_table(diag_headers, diag_rows,
        col_widths=[40*mm, 12*mm, COL_W - 52*mm]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<b><font color='#D4700A'>Nota composta: 6.5 / 10</font></b>  ·  "
        "Perfil: Estrategista de produto com execucao via IA. "
        "Meta: 8.5/10 em 12 meses.", ST["body_bold"]))

    story.append(Paragraph("Perfil sintetico:", ST["h2"]))
    story.append(Paragraph(
        "Perfil de profissional de mercado financeiro que ja usa IA no nivel de "
        "arquiteto — projetando sistemas complexos. O gap esta na base tecnica: "
        "Python, ML, estatistica. A mentoria foca em preencher esses gaps sem "
        "transformar em desenvolvedor, mas em alguem que valida, dirige e orquestra.",
        ST["body"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 3 — TESE ESTRATEGICA
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 03", ST["section_num"]))
    story.append(Paragraph("Tese Estrategica: O Que Aprender vs O Que a IA Fara", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "A pergunta central nao e 'o que aprender' mas 'o que permanece "
        "valioso quando a IA fizer 90%% da execucao'. A resposta define "
        "a prioridade de cada bloco do roadmap.",
        ST["body"]))

    story.append(Paragraph("Skills com prazo de validade (IA fara melhor em 2027):", ST["h3"]))
    expiring = [
        "Escrever codigo Python, React, SQL — 65%% sera IA-generated",
        "Treinar modelos de ML (AutoML, NAS)",
        "Gerar relatorios, PDFs, dashboards com um prompt",
        "Parsear documentos, extratos, CSVs",
    ]
    for item in expiring:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("Skills duraveis (IA amplifica mas nao substitui):", ST["h3"]))
    durable = [
        "<b>Julgamento</b> — Decidir o que construir, para quem, com que restricoes",
        "<b>Validacao</b> — Saber se o modelo e lixo ou ouro. IA alucina; quem valida ganha",
        "<b>Domain expertise</b> — HRP com constraint de liquidez para cliente conservadora",
        "<b>Orquestracao</b> — Projetar sistemas multi-agente, pipelines, MCP",
        "<b>Confianca do cliente</b> — Sentar na frente do cliente e explicar uma queda",
        "<b>Narrativa</b> — Transformar dados em historia. IA compila; voce convence",
    ]
    for item in durable:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Regra de ouro: Se a IA fara isso melhor em 2 anos, invista o minimo "
        "para validar. Se a IA nao fara, invista pesado. O roadmap foi "
        "calibrado com essa logica.",
        ST["quote"]))

    story.append(Paragraph("Framework de niveis de maturidade em IA:", ST["h2"]))
    mat_headers = ["Nivel", "Descricao", "Status"]
    mat_rows = [
        ["L1 — Perguntador", "Faz perguntas a ferramentas de IA", "Concluido"],
        ["L2 — Diretor", "Direciona com contexto preciso", "Concluido"],
        ["L3 — Arquiteto", "Projeta sistemas via IA (Patrimonium)", "Atual"],
        ["L4 — Orquestrador", "Multi-agente, pipelines, automacao", "Meta sem 22"],
        ["L5 — Plataforma", "Constroi produtos sobre APIs de IA", "Meta 2027"],
    ]
    story.append(make_table(mat_headers, mat_rows,
        col_widths=[35*mm, 55*mm, COL_W - 90*mm]))

    story.append(Paragraph("Projecao de posicionamento:", ST["h2"]))
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
    # SECAO 4 — ROADMAP RESUMIDO
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 04", ST["section_num"]))
    story.append(Paragraph("Roadmap: 24 Semanas, 124 Horas", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "O roadmap completo esta no documento 'Roadmap_IA_Patrimonium.pdf' "
        "com cronograma semana a semana. Abaixo, o resumo executivo de cada bloco.",
        ST["body"]))

    # Bloco 1
    story.append(Paragraph("<b><font color='#1C7C54'>BLOCO 1</font>  ·  "
        "Python + Estatistica  ·  Sem 1-6  ·  29h</b>", ST["h2"]))
    story.append(Paragraph(
        "Objetivo: Nao virar programador. Virar alguem que le, valida e dirige "
        "codigo. Python e a lingua franca da IA.", ST["body"]))
    b1 = [
        "Harvard CS50P (semanas 1-3): variaveis, funcoes, APIs",
        "IMPA ML (semanas 4-5): regressao, bias-variance, cross-validation",
        "Checkpoint (semana 6): script que baixa dados BCB, calcula media movel, plota",
    ]
    for item in b1:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("<b>Competencias:</b> Le Python, consome API REST, "
        "entende overfitting e cross-validation.", ST["body_bold"]))

    # Bloco 2
    story.append(Paragraph("<b><font color='#1C7C54'>BLOCO 2</font>  ·  "
        "Machine Learning Core  ·  Sem 7-12  ·  31h</b>", ST["h2"]))
    story.append(Paragraph(
        "Objetivo: Treinar um modelo real, validar, saber quando ML agrega "
        "vs quando e ruido.", ST["body"]))
    b2 = [
        "Andrew Ng ML Specialization (semanas 7-9): supervised, neural networks",
        "IMPA ML (semana 10): PCA, clustering, conformal prediction",
        "Projeto (semana 11): modelo preditivo de direcao da Selic",
        "Checkpoint (semana 12): validar modelo com cross-validation, documentar",
    ]
    for item in b2:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("<b>Competencias:</b> Treinou modelo end-to-end, "
        "le feature importance, distingue ML util de ruido.", ST["body_bold"]))

    # Bloco 3
    story.append(Paragraph("<b><font color='#1C7C54'>BLOCO 3</font>  ·  "
        "ML Financeiro + Portfolio  ·  Sem 13-18  ·  32h</b>", ST["h2"]))
    story.append(Paragraph(
        "Objetivo: Conectar ML ao wealth management. Implementar HRP. "
        "Domain expertise e o skill mais duravel.", ST["body"]))
    b3 = [
        "Lopez de Prado AFML (semanas 13-15): labeling, CV, HRP",
        "skfolio (semana 16): portfolio optimization pratico",
        "Harvard CS50 AI (semana 17): search, optimization",
        "Checkpoint (semana 18): integrar HRP no Patrimonium como nova tab",
    ]
    for item in b3:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("<b>Competencias:</b> Leu Lopez de Prado, "
        "implementou HRP, sabe explicar pro cliente.", ST["body_bold"]))

    # Bloco 4
    story.append(Paragraph("<b><font color='#1C7C54'>BLOCO 4</font>  ·  "
        "Orquestracao de IA  ·  Sem 19-22  ·  22h</b>", ST["h2"]))
    story.append(Paragraph(
        "Objetivo: Dominar multi-agente, MCP, APIs de IA. "
        "Em 2027: quem usa IA e commodity. Quem orquestra e arquiteto.", ST["body"]))
    b4 = [
        "Cursos de IA (semanas 19-21): APIs de IA, Prompt Engineering, MCP",
        "Checkpoint (semana 22): pipeline CSV -> IA -> JSON -> PDF -> email",
    ]
    for item in b4:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Paragraph("<b>Competencias:</b> Chama APIs de IA via Python, "
        "construiu MCP server, automatizou pipeline.", ST["body_bold"]))

    # Bloco 5
    story.append(Paragraph("<b><font color='#1C7C54'>BLOCO 5</font>  ·  "
        "Autoridade  ·  Sem 23-24  ·  10h</b>", ST["h2"]))
    story.append(Paragraph(
        "Objetivo: Parar de consumir e comecar a produzir. "
        "Posicionar-se como referencia em wealth + IA no Brasil.", ST["body"]))
    b5 = [
        "Artigo: 'Advisory com ML e IA — Case Patrimonium' (LinkedIn + Medium)",
        "Portfolio de competencias consolidado",
    ]
    for item in b5:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 5 — CURSO IMPA
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 05", ST["section_num"]))
    story.append(Paragraph("Curso IMPA ML — Analise e Recomendacao", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "O curso de Machine Learning do IMPA (Mestrado/Doutorado), ministrado "
        "pelo Prof. Paulo Orenstein (PhD Stanford, Google Research Award), esta "
        "disponivel integralmente no YouTube: 21 video-aulas, 38h43min total.",
        ST["body"]))

    story.append(Paragraph("Playlist: PLo4jXE-LdDTRLGDL59SkkLPBHVmYphuqI", ST["callout"]))

    story.append(Paragraph("Recomendacao de visualizacao seletiva (~16h de 38h):", ST["h2"]))

    impa_headers = ["Prioridade", "Aulas", "Topico", "Por que"]
    impa_rows = [
        ["ALTA", "1-3", "Regressao, bias-variance", "Fundamento de tudo"],
        ["ALTA", "7-8", "Cross-validation, Ridge, Lasso", "Validacao de modelos"],
        ["ALTA", "12-13", "Arvores, Random Forest", "Modelo mais usado no mercado"],
        ["MEDIA", "20-21", "PCA, clustering, conformal", "Reducao de dimensionalidade"],
        ["MEDIA", "15-16", "Redes neurais intro", "Contexto, nao execucao"],
        ["BAIXA", "4-6, 9-11", "Classificacao, SVM, kernel", "Complementar, se sobrar tempo"],
    ]
    story.append(make_table(impa_headers, impa_rows,
        col_widths=[22*mm, 15*mm, 42*mm, COL_W - 79*mm]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "O curso do IMPA e de nivel mestrado — mais rigido matematicamente que "
        "Andrew Ng. A recomendacao e assistir seletivamente: focar nas aulas "
        "de alta prioridade e usar as demais como referencia.",
        ST["quote"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 6 — RECURSOS COMPLETOS
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 06", ST["section_num"]))
    story.append(Paragraph("Recursos Completos", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph("Cursos (todos gratuitos):", ST["h2"]))
    ref_headers = ["Curso", "Instituicao", "Horas"]
    ref_rows = [
        ["CS50P — Intro to Python", "Harvard", "30h"],
        ["CS50 AI — Artificial Intelligence", "Harvard", "20h"],
        ["ML Specialization", "Stanford / Coursera", "40h"],
        ["Machine Learning (Mestrado)", "IMPA / Paulo Orenstein", "38h"],
        ["Practical Deep Learning", "Fast.ai / Jeremy Howard", "12h"],
        ["IA Tooling in Action", "Cursos IA", "3h"],
        ["Building with AI APIs", "Cursos IA", "5h"],
        ["MCP Intro + Advanced", "Cursos IA", "6h"],
        ["Prompt Engineering Tutorial", "Cursos IA", "6h"],
        ["Tool Use Course", "Cursos IA", "5h"],
        ["MIT 6.S191 — Intro Deep Learning", "MIT", "15h"],
    ]
    story.append(make_table(ref_headers, ref_rows,
        col_widths=[55*mm, 45*mm, COL_W - 100*mm]))

    story.append(Paragraph("Livros essenciais:", ST["h2"]))
    book_headers = ["Livro", "Autor", "Foco"]
    book_rows = [
        ["Intro to Statistical Learning (ISLP)", "Hastie, Tibshirani", "ML classico"],
        ["Advances in Financial ML", "Lopez de Prado", "ML financeiro"],
        ["ML & Data Science for Finance", "Tatsat, Puri", "Receitas Python"],
        ["Automate the Boring Stuff", "Al Sweigart", "Python iniciante"],
    ]
    story.append(make_table(book_headers, book_rows,
        col_widths=[50*mm, 35*mm, COL_W - 85*mm]))

    story.append(Paragraph("Pessoas a seguir:", ST["h2"]))
    people_headers = ["Nome", "Papel", "Relevancia"]
    people_rows = [
        ["Marcos Lopez de Prado", "Cornell, ex-AQR", "Pai do ML financeiro"],
        ["Paulo Orenstein", "IMPA, PhD Stanford", "Professor curso IMPA"],
        ["Andrew Ng", "Stanford", "Maior educador ML"],
        ["Jeremy Howard", "Fast.ai", "ML pratico, top-down"],
        ["Dario Amodei", "CEO AI Lab", "Direcao da IA"],
        ["Andrej Karpathy", "Ex-Tesla AI", "Tutoriais deep learning"],
    ]
    story.append(make_table(people_headers, people_rows,
        col_widths=[38*mm, 32*mm, COL_W - 70*mm]))

    story.append(Paragraph("Custos:", ST["h2"]))
    cost_headers = ["Componente", "Valor"]
    cost_rows = [
        ["Cursos online (Harvard, IMPA, Coursera, MIT)", "Gratuito"],
        ["Livros (Lopez de Prado + Tatsat)", "~R$ 450"],
        ["CFA Data Science Certificate (opcional, pos-trilha)", "~R$ 9.000"],
        ["TOTAL trilha core", "~R$ 450"],
        ["TOTAL com certificacao", "~R$ 9.450"],
    ]
    story.append(make_table(cost_headers, cost_rows,
        col_widths=[COL_W * 0.65, COL_W * 0.35]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 7 — DECISOES E PREMISSAS
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 07", ST["section_num"]))
    story.append(Paragraph("Decisoes e Premissas da Mentoria", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Registro das decisoes tomadas durante a sessao de mentoria, "
        "para referencia em sessoes futuras.",
        ST["body"]))

    story.append(Paragraph("1. Velocidade da IA vs profundidade de aprendizado", ST["h3"]))
    story.append(Paragraph(
        "Premissa: a IA evolui a cada 6 meses. Ate 2028, 65%% do codigo sera "
        "IA-generated. Portanto, o foco nao e dominar execucao (codigo, treino "
        "de modelo), mas sim validacao e orquestracao. O roadmap prioriza "
        "'saber avaliar' sobre 'saber fazer'.",
        ST["body"]))

    story.append(Paragraph("2. Perfil do profissional", ST["h3"]))
    story.append(Paragraph(
        "Perfil de assessor de investimentos. Nao e e nao pretende ser "
        "desenvolvedor. O objetivo e ser o profissional financeiro que "
        "mais sabe usar IA no Brasil — nao o melhor programador.",
        ST["body"]))

    story.append(Paragraph("3. Ritmo de 5h/semana", ST["h3"]))
    story.append(Paragraph(
        "Considerando a rotina de advisory, o ritmo e de 5 horas por semana. "
        "Total: 124 horas em 24 semanas (6 meses). Compativel com quem "
        "trabalha full-time no mercado financeiro.",
        ST["body"]))

    story.append(Paragraph("4. Priorizacao de cursos", ST["h3"]))
    story.append(Paragraph(
        "Harvard CS50P para Python (estruturado, exercicios), Andrew Ng para ML "
        "(didatico, pratico), IMPA para rigor matematico (seletivo), cursos de IA "
        "para orquestracao. Cursos gratuitos sempre que possivel.",
        ST["body"]))

    story.append(Paragraph("5. Conexao com o Patrimonium", ST["h3"]))
    story.append(Paragraph(
        "Cada bloco do roadmap termina com um checkpoint que conecta ao "
        "Patrimonium. Semana 6: script BCB. Semana 12: modelo Selic. Semana 18: "
        "tab HRP. Semana 22: pipeline automatizado. Nao e aprendizado "
        "abstrato — e aplicacao direta.",
        ST["body"]))

    story.append(Paragraph("6. Retroevolucao da IA", ST["h3"]))
    story.append(Paragraph(
        "A preocupacao com a evolucao constante da IA e central. O roadmap "
        "antecipa isso: os blocos 1-3 focam em fundamentos que nao mudam "
        "(estatistica, ML classico, financas). O bloco 4 foca em orquestracao, "
        "que e a camada que permanece relevante mesmo com IA mais poderosa.",
        ST["body"]))

    story.append(Paragraph("7. Meta de nota 8.5/10", ST["h3"]))
    story.append(Paragraph(
        "De 6.5 atual para 8.5 em 12 meses. Os maiores saltos serao em "
        "Python (5.0 -> 7.0), ML (2.0 -> 6.5) e Orquestracao (novo skill). "
        "Os pontos ja fortes (Prompt Eng 8.5, Visao de Produto 9.0, "
        "Tooling IA 9.0) se mantem e potencializam os novos.",
        ST["body"]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════
    # SECAO 8 — DOCUMENTOS GERADOS
    # ═══════════════════════════════════════════════════════════════
    story.append(Paragraph("SECAO 08", ST["section_num"]))
    story.append(Paragraph("Documentos Gerados nesta Sessao", ST["section_title"]))
    story.append(green_line())

    story.append(Paragraph(
        "Lista de todos os artefatos produzidos durante a sessao, "
        "com localizacao e descricao.",
        ST["body"]))

    docs_headers = ["Documento", "Localizacao", "Descricao"]
    docs_rows = [
        ["Roadmap_IA_Patrimonium.pdf", "output/", "Cronograma 24 sem, exercicios, competencias"],
        ["Patrimonium_Guia_Apresentacao.pdf", "output/", "Guia de apresentacao das 9 tabs do Patrimonium"],
        ["Relatorio_Racional_IA.pdf", "output/", "Este documento — consolidacao da mentoria"],
        ["generate-roadmap.py", "scripts/", "Script gerador do Roadmap PDF"],
        ["generate-guide.py", "scripts/", "Script gerador do Guia de Apresentacao"],
        ["generate-summary-report.py", "scripts/", "Script gerador deste relatorio"],
    ]
    story.append(make_table(docs_headers, docs_rows,
        col_widths=[48*mm, 20*mm, COL_W - 68*mm]))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Projeto Patrimonium — Estrutura de codigo:", ST["h2"]))

    code_headers = ["Arquivo", "Descricao"]
    code_rows = [
        ["src/AppCliente.jsx", "Componente principal — 2.263 linhas, 9 tabs"],
        ["src/data/cliente.json", "Dados do cliente — 5.533 linhas"],
        ["src/data/ettj.json", "Estrutura a Termo da Taxa de Juros"],
        ["src/data/focus.json", "Dados Focus BCB"],
        ["src/data/indices.json", "Indices de mercado"],
        ["public/index.html", "HTML base com fontes Inter"],
        ["package.json", "Dependencias React + Recharts"],
    ]
    story.append(make_table(code_headers, code_rows,
        col_widths=[45*mm, COL_W - 45*mm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Proximos passos sugeridos:", ST["h2"]))
    nexts = [
        "Iniciar Bloco 1 — CS50P semana 1 (variaveis, condicionais, loops)",
        "Implementar modo relatorio no Patrimonium",
        "Configurar ambiente Python local (VS Code + venv + jupyter)",
        "Acessar playlist IMPA ML e marcar aulas de alta prioridade",
        "Considerar adicionar API BCB ao Patrimonium para dados em tempo real",
    ]
    for item in nexts:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", ST["bullet"]))

    story.append(Spacer(1, 10*mm))

    # Closing
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY,
                            spaceBefore=5*mm, spaceAfter=3*mm))
    story.append(Paragraph(
        "<i>Relatorio Consolidado — Mentoria IA  ·  Patrimonium<br/>"
        "Documento confidencial. Uso pessoal.<br/>"
        f"Gerado em {datetime.date.today().strftime('%d/%m/%Y')}.</i>",
        ST["small"]))

    # ── Build ──────────────────────────────────────────────────────
    doc.build(story, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"  OK - PDF gerado: {os.path.abspath(out_path)}")
    print(f"      ({os.path.getsize(out_path) // 1024} KB)")

if __name__ == "__main__":
    build()
