"""
Patrimonium - Arquitetura de Alocacao de Capital
Guia de Apresentacao — Patrimonium
Roteiro para apresentacao de resultados ao cliente.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.platypus.flowables import Flowable
import os

NAVY = HexColor("#1B2A4A")
GREEN = HexColor("#276749")
STEEL = HexColor("#2C5282")
AMBER = HexColor("#B7791F")
RED = HexColor("#9B2C2C")
GRAY = HexColor("#718096")
LGRAY = HexColor("#E2E8F0")
VLIGHT = HexColor("#F7FAFC")
SLATE = HexColor("#4A5568")

W, H = A4
F = "Helvetica"
FB = "Helvetica-Bold"
FI = "Helvetica-Oblique"
MO = "Courier"

# Styles
S = {}
S["ct"] = ParagraphStyle("ct", fontName=FB, fontSize=28, leading=34, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6)
S["cs"] = ParagraphStyle("cs", fontName=F, fontSize=14, leading=18, textColor=STEEL, alignment=TA_LEFT, spaceAfter=24)
S["sn"] = ParagraphStyle("sn", fontName=FB, fontSize=10, leading=12, textColor=GREEN, letterSpacing=2)
S["st"] = ParagraphStyle("st", fontName=FB, fontSize=20, leading=26, textColor=NAVY, spaceBefore=4, spaceAfter=16)
S["h2"] = ParagraphStyle("h2", fontName=FB, fontSize=13, leading=18, textColor=NAVY, spaceBefore=18, spaceAfter=8)
S["h3"] = ParagraphStyle("h3", fontName=FB, fontSize=11, leading=15, textColor=STEEL, spaceBefore=14, spaceAfter=6)
S["bd"] = ParagraphStyle("bd", fontName=F, fontSize=10.5, leading=16, textColor=SLATE, alignment=TA_JUSTIFY, spaceAfter=8)
S["qt"] = ParagraphStyle("qt", fontName=FI, fontSize=10.5, leading=16, textColor=GRAY, spaceAfter=8, leftIndent=16)
S["bl"] = ParagraphStyle("bl", fontName=F, fontSize=10.5, leading=16, textColor=SLATE, spaceAfter=4, leftIndent=20, bulletIndent=8)
S["tl"] = ParagraphStyle("tl", fontName=FB, fontSize=9, leading=12, textColor=GREEN, letterSpacing=1.5)
S["tb"] = ParagraphStyle("tb", fontName=FI, fontSize=10, leading=15, textColor=NAVY, leftIndent=16, spaceAfter=10)


class ColorLine(Flowable):
    def __init__(self, w, h=2, color=GREEN):
        Flowable.__init__(self)
        self.width = w; self.height = h; self.color = color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LGRAY); canvas.setLineWidth(0.5)
    canvas.line(30*mm, H-14*mm, W-30*mm, H-14*mm)
    canvas.setFont(F, 7); canvas.setFillColor(GRAY)
    canvas.drawString(30*mm, H-12.5*mm, "Patrimonium")
    canvas.drawRightString(W-30*mm, H-12.5*mm, "Confidencial \xb7 Uso exclusivo do destinat\xe1rio")
    canvas.line(30*mm, 16*mm, W-30*mm, 16*mm)
    canvas.drawString(30*mm, 12*mm, "Patrimonium")
    canvas.drawCentredString(W/2, 12*mm, f"P\xe1gina {doc.page}")
    canvas.drawRightString(W-30*mm, 12*mm, "Propriedade intelectual Patrimonium")
    canvas.restoreState()


def build_pdf():
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "Patrimonium_Guia_Apresentacao.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=22*mm, bottomMargin=22*mm, leftMargin=30*mm, rightMargin=30*mm)
    uw = W - 60*mm
    st = []

    def sec(n, t, dur=None):
        st.append(Paragraph(f"SE\xc7\xc3O {n}", S["sn"]))
        st.append(Paragraph(t, S["st"]))
        st.append(ColorLine(uw, 2, GREEN))
        if dur: st.append(Spacer(1, 2*mm)); st.append(Paragraph(f"Tempo sugerido: {dur}", S["qt"]))
        st.append(Spacer(1, 4*mm))

    def h2(t): st.append(Paragraph(t, S["h2"]))
    def h3(t): st.append(Paragraph(t, S["h3"]))
    def bd(t): st.append(Paragraph(t, S["bd"]))
    def tip(l, t):
        st.append(Spacer(1, 2*mm))
        st.append(Paragraph(f"\u25b6 {l}", S["tl"]))
        st.append(Paragraph(t, S["tb"]))
    def bul(items):
        for i in items: st.append(Paragraph(f"\u2022&nbsp;&nbsp;{i}", S["bl"]))
    def sep():
        st.append(Spacer(1, 3*mm)); st.append(ColorLine(uw, 0.5, LGRAY)); st.append(Spacer(1, 3*mm))

    # ════════════════════ CAPA ════════════════════
    st.append(Spacer(1, 40*mm))
    st.append(ColorLine(uw, 3, GREEN))
    st.append(Spacer(1, 20*mm))
    st.append(Paragraph("GUIA DE APRESENTA\xc7\xc3O", S["ct"]))
    st.append(Paragraph("Patrimonium \u2014 Arquitetura de Aloca\xe7\xe3o de Capital", S["ct"]))
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph("Roteiro para apresenta\xe7\xe3o de resultados ao cliente.<br/>Metodologia, fontes de dados e fio condutor para cada se\xe7\xe3o do Patrimonium.", S["cs"]))
    st.append(Spacer(1, 20*mm))

    meta = Table([
        ["Cliente:", "[Nome do Cliente]"],
        ["Patrim\xf4nio:", "R$ 26.204.602"],
        ["Refer\xeancia:", "27/02/2026"],
        ["Patrimonium:", ""],
        ["Data do Guia:", "15/03/2026"],
    ], colWidths=[80, 200])
    meta.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), FB), ("FONTNAME", (1,0), (1,-1), F),
        ("FONTSIZE", (0,0), (-1,-1), 11), ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("TEXTCOLOR", (1,0), (1,-1), SLATE), ("LEADING", (0,0), (-1,-1), 18),
        ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    st.append(meta)

    st.append(Spacer(1, 30*mm))
    st.append(ColorLine(uw, 2, NAVY))
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph(
        "Este documento \xe9 de uso interno da Patrimonium para preparar a reuni\xe3o de apresenta\xe7\xe3o de resultados. "
        "Cont\xe9m o roteiro completo, metodologia de cada c\xe1lculo e as fontes de dados utilizadas no Patrimonium.",
        ParagraphStyle("disc", fontName=FI, fontSize=9, leading=14, textColor=GRAY, alignment=TA_JUSTIFY)
    ))
    st.append(PageBreak())

    # ════════════════════ SUMARIO ════════════════════
    st.append(Paragraph("SUM\xc1RIO", S["st"]))
    st.append(ColorLine(uw, 2, GREEN))
    st.append(Spacer(1, 8*mm))
    toc = [
        ("01", "Overview", "Vis\xe3o consolidada do patrim\xf4nio e performance"),
        ("02", "Asset Allocation", "Composi\xe7\xe3o da carteira por estrat\xe9gia, tipo e conta"),
        ("03", "Portfolio Strategy", "Liquidez, vencimentos, risco de reinvestimento e rotation"),
        ("04", "Benchmark", "Performance vs refer\xeancias e par\xe2metros do mandato"),
        ("05", "Tax Alpha", "Efici\xeancia fiscal, economia de IR e come-cotas"),
        ("06", "Hedge", "DV01, stress test, cen\xe1rios hist\xf3ricos e proje\xe7\xe3o Focus"),
        ("07", "Portfolio Efficiency", "TER, HHI e diversifica\xe7\xe3o"),
        ("08", "Macro View", "Cen\xe1rio macroecon\xf4mico e proje\xe7\xf5es Focus"),
        ("09", "Metodologia Geral", "Fontes de dados, c\xe1lculos base e premissas"),
    ]
    gc = GREEN.hexval()[2:]
    nc = NAVY.hexval()[2:]
    grc = GRAY.hexval()[2:]
    for n, t, d in toc:
        st.append(Paragraph(
            f'<font color="#{gc}">{n}</font>&nbsp;&nbsp;&nbsp;<font color="#{nc}"><b>{t}</b></font>'
            f'&nbsp;&nbsp;<font color="#{grc}">\u2014 {d}</font>',
            ParagraphStyle("toc", fontName=F, fontSize=11, leading=22, textColor=SLATE)
        ))
        st.append(ColorLine(uw, 0.5, LGRAY))
    st.append(PageBreak())

    # ════════════════════ 01 — OVERVIEW ════════════════════
    sec("01", "Overview \u2014 Vis\xe3o Geral", "3\u20134 minutos")

    h2("Abertura da reuni\xe3o")
    bd("Comece com o <b>patrim\xf4nio consolidado</b>. \xc9 o n\xfamero que ancora toda a conversa. "
       "Mostre os R$ 26,2 milh\xf5es distribu\xeddos em 7 contas (Private e Regular), depois des\xe7a para a rentabilidade.")

    tip("FALA SUGERIDA",
        "\u201c[Cliente], seu patrim\xf4nio consolidado est\xe1 em R$ 26,2 milh\xf5es. "
        "No m\xeas de fevereiro, a carteira rendeu X,XX%, equivalente a X% do CDI. "
        "Isso representou um ganho financeiro de R$ XXX mil.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>5 KPIs de cabe\xe7alho:</b> Patrim\xf4nio, Rent. M\xeas, Ganho R$, Rent. Ano e Ganho Ano.",
        "<b>Gr\xe1fico de evolu\xe7\xe3o patrimonial:</b> \xc1rea chart com 12 meses (Mar/25 a Fev/26).",
        "<b>Gr\xe1fico de rent. mensal:</b> Barras da conta principal com linha do CDI.",
        "<b>Tabela de performance:</b> Todas as 7 contas com rent., % CDI e risco.",
        "<b>Barra de consist\xeancia:</b> Meses positivos vs negativos por conta.",
    ])
    sep()
    h2("Metodologia dos c\xe1lculos")
    h3("Rentabilidade ponderada")
    bd("M\xe9dia ponderada pelo patrim\xf4nio de cada conta: "
       "<b>wRent = \u03a3(rentMes<sub>i</sub> \xd7 pat<sub>i</sub>) / \u03a3(pat<sub>i</sub>)</b>. "
       "Contas maiores t\xeam mais peso no resultado consolidado.")
    h3("% do CDI")
    bd("Mesma l\xf3gica: <b>wCDI = \u03a3(pctCDI<sub>i</sub> \xd7 pat<sub>i</sub>) / \u03a3(pat<sub>i</sub>)</b>. "
       "Se a carteira rendeu 1,10% e o CDI 1,00%, o % do CDI \xe9 110%. Acima de 100% = batendo o benchmark.")
    h3("Ganho financeiro")
    bd("Soma simples dos ganhos de cada conta: <b>\u03a3(ganhoMes<sub>i</sub>)</b>.")
    sep()
    h2("Fontes de dados")
    bul([
        "<b>Patrim\xf4nio e rentabilidade:</b> XP Investimentos (relat\xf3rio de carteira consolidada).",
        "<b>CDI:</b> CETIP/B3 \u2014 taxa DI over acumulada no per\xedodo.",
        "<b>Refer\xeancia:</b> Data de corte do relat\xf3rio (27/02/2026).",
    ])
    st.append(PageBreak())

    # ════════════════════ 02 — ASSET ALLOCATION ════════════════════
    sec("02", "Asset Allocation \u2014 Composi\xe7\xe3o", "3\u20134 minutos")

    h2("Fio condutor")
    bd("Ap\xf3s mostrar o resultado, explique <b>como</b> o patrim\xf4nio est\xe1 distribu\xeddo. "
       "Quest\xe3o central: <i>\u201cOnde est\xe1 o dinheiro e por qu\xea?\u201d</i>")
    tip("FALA SUGERIDA",
        "\u201cAgora vamos ver como seu patrim\xf4nio est\xe1 distribu\xeddo. "
        "A maior concentra\xe7\xe3o est\xe1 em p\xf3s-fixados, que representam X% da carteira. "
        "Com a Selic a 15%, p\xf3s-fixado entrega retorno consistente com risco m\xednimo.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>Perfil din\xe2mico:</b> Calculado pela aloca\xe7\xe3o (>60% p\xf3s = Conservador, >8% RV = Moderado-Agressivo).",
        "<b>3 gr\xe1ficos de barras:</b> Por estrat\xe9gia, por tipo de papel e por conta.",
        "<b>3 tabelas:</b> Fundos, Renda Fixa direta e Fundos Listados/A\xe7\xf5es.",
    ])
    sep()
    h2("Metodologia")
    h3("Classifica\xe7\xe3o por estrat\xe9gia")
    bd("Cada ativo \xe9 classificado pela XP em uma estrat\xe9gia (P\xf3s Fixado, IPCA+, Cr\xe9dito Privado, etc.). "
       "O Patrimonium consolida todas as contas, somando os valores de cada estrat\xe9gia.")
    h3("Perfil autom\xe1tico")
    bd("O perfil \xe9 inferido da aloca\xe7\xe3o real: >60% p\xf3s-fixado = \u201cConservador\u201d, >20% RV = \u201cAgressivo\u201d. "
       "Din\xe2mico e muda a cada m\xeas.")
    st.append(PageBreak())

    # ════════════════════ 03 — PORTFOLIO STRATEGY ════════════════════
    sec("03", "Portfolio Strategy \u2014 Liquidez e Vencimentos", "4\u20135 minutos")

    h2("Fio condutor")
    bd("Transi\xe7\xe3o: \u201cAgora que vimos a composi\xe7\xe3o, vamos ver a <b>liquidez</b> \u2014 "
       "quanto dinheiro est\xe1 dispon\xedvel e o que acontece ao longo de 2026.\u201d")
    tip("FALA SUGERIDA",
        "\u201cVoc\xea tem R$ X milh\xf5es dispon\xedveis para resgate imediato. "
        "Ao longo de 2026, mais R$ X milh\xf5es vencem e retornam ao caixa. "
        "Mas tem um ponto de aten\xe7\xe3o: a Selic vai cair, e o reinvestimento ser\xe1 a taxas menores.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>4 KPIs de liquidez:</b> Fundos D+0, LFTs, CDBs 100% CDI e Total Liquidez.",
        "<b>Cronograma de vencimentos:</b> Tabela com cada ativo que vence em 2026.",
        "<b>Gr\xe1fico de liquidez acumulada:</b> Pool crescendo ao longo do ano.",
        "<b>Risco de reinvestimento:</b> Impacto da queda da Selic.",
        "<b>FIP AG7:</b> Proposta de rotation \u2014 simulador com MOIC, TIR e alpha vs CDI.",
    ])
    sep()
    h2("Metodologia")
    h3("Pool de liquidez crescente")
    bd("Come\xe7amos com a liquidez imediata (fundos D+0 + LFTs + CDBs). A cada m\xeas, "
       "o pool <b>cresce pelo CDI mensal</b> (Selic Focus). Quando um ativo vence, entra no pool com carrego.")
    h3("Carrego mensal")
    bd("<b>taxaMensal = (1 + taxaAnual)<sup>1/12</sup> \u2212 1</b>. "
       "P\xf3s-fixados usam Selic Focus daquele m\xeas. IPCA+ usa IPCA 12M + spread. Prefixados usam taxa contratada.")
    h3("Risco de reinvestimento")
    bd("CDB 100% CDI a 15%, Selic cai para 12,125%: perda de R$ 28.750/ano por milh\xe3o reaplicado.")
    h3("Simula\xe7\xe3o FIP AG7")
    bd("Compara FIP AG7 (MOIC 2,5x e 3,0x) contra CDI carregado. "
       "CDI usa curva Focus (m\xe9dia 13,6% em 2026, 11,3% em 2027, 10,5% a partir de 2028). "
       "Alpha = diferen\xe7a l\xedquida de IR (15% em ambos).")
    st.append(PageBreak())

    # ════════════════════ 04 — BENCHMARK ════════════════════
    sec("04", "Benchmark \u2014 Performance e Mandato", "4\u20135 minutos")

    h2("Fio condutor")
    bd("Quest\xe3o central: \u201cEstamos batendo os benchmarks? Estamos dentro dos par\xe2metros combinados?\u201d "
       "Se\xe7\xe3o mais importante para demonstrar compet\xeancia e transpar\xeancia.")
    tip("FALA SUGERIDA",
        "\u201cSua carteira rendeu X% do CDI no m\xeas e X% no ano. Estamos acima do benchmark. "
        "Agora vou mostrar o mandato de investimento \u2014 os par\xe2metros que combinamos.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>Tabela de benchmarks:</b> Portf\xf3lio vs CDI, Ibovespa, IPCA e D\xf3lar (m\xeas, ano, 12M, 24M).",
        "<b>Ranking de contas:</b> Barras horizontais com linha do CDI.",
        "<b>6 cards do mandato:</b> Return vs CDI, Volatility, Monthly Return, Positive Months, YTD, Accounts vs CDI.",
        "<b>Recomenda\xe7\xf5es estrat\xe9gicas:</b> 6 cards com alertas e a\xe7\xf5es recomendadas.",
    ])
    sep()
    h2("Metodologia")
    h3("% do CDI")
    bd("<b>(rentabilidade do portf\xf3lio / rentabilidade do CDI) \xd7 100</b>. "
       "Portf\xf3lio 1,10% e CDI 1,00% = 110% do CDI.")
    h3("Mandato de investimento")
    bd("6 KPIs verificados contra metas. <b>Return vs CDI</b>: meta 100%. "
       "Acima = \u201cWithin Target\u201d (verde). 95\u2013100% = \u201cMonitoring\u201d. Abaixo = \u201cBelow Target\u201d.")
    h3("Volatilidade")
    bd("Desvio-padr\xe3o dos retornos mensais, anualizado. Meta m\xe1xima: 2,0%. "
       "Carteiras p\xf3s-fixadas costumam ficar abaixo de 1%.")
    st.append(PageBreak())

    # ════════════════════ 05 — TAX ALPHA ════════════════════
    sec("05", "Tax Alpha \u2014 Efici\xeancia Fiscal", "3\u20134 minutos")

    h2("Fio condutor")
    bd("Transi\xe7\xe3o: \u201cAl\xe9m de render bem, \xe9 importante pagar menos imposto. "
       "Vamos ver a efici\xeancia fiscal da carteira.\u201d")
    tip("FALA SUGERIDA",
        "\u201cDos R$ 26,2 milh\xf5es, X% est\xe1 em ativos isentos de IR \u2014 CRAs, CRIs, LCIs. "
        "Economia fiscal estimada de R$ XXX mil/ano. "
        "Os fundos com come-cotas custam R$ XXX mil em antecipa\xe7\xe3o.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>3 m\xe9tricas fiscais:</b> Economia IR (verde), Come-cotas drag (vermelho), IR m\xe9dio ponderado.",
        "<b>Composi\xe7\xe3o tribut\xe1ria:</b> Isento, come-cotas, regressiva, RV.",
        "<b>Faixas de IR:</b> Distribui\xe7\xe3o pela tabela regressiva (22,5% a 15%).",
        "<b>Gross Equivalent:</b> Rendimento bruto equivalente dos ativos isentos.",
        "<b>Come-cotas detalhado:</b> Drag por fundo, calculado semestralmente.",
        "<b>Bruto vs L\xedquido:</b> Retorno mensal bruto vs l\xedquido de IR.",
    ])
    sep()
    h2("Metodologia")
    h3("Economia fiscal")
    bd("<b>economiaIR = \u03a3(total<sub>isento</sub> \xd7 rentMes \xd7 12 \xd7 0,15)</b>. "
       "Quanto os isentos pagariam se tributados a 15%. Estimativa conservadora.")
    h3("Come-cotas drag")
    bd("Antecipa\xe7\xe3o semestral de 15%: <b>ganhoSemestral = total \xd7 ((1 + rentMes)<sup>6</sup> \u2212 1)</b>, "
       "depois <b>drag = ganhoSemestral \xd7 0,15 \xd7 2</b> (maio e novembro).")
    h3("Equivalente bruto")
    bd("<b>spreadEquiv = spread / (1 \u2212 al\xedquota)</b>. "
       "CRA IPCA + 6,20% isento = IPCA + 7,29% tributado a 15% = IPCA + 8,00% tributado a 22,5%.")
    h3("Retorno l\xedquido de IR")
    bd("<b>l\xedquido = rentMes \xd7 (1 \u2212 IR)</b>. Se retorno negativo, n\xe3o h\xe1 IR \u2014 l\xedquido = bruto.")
    st.append(PageBreak())

    # ════════════════════ 06 — HEDGE ════════════════════
    sec("06", "Hedge \u2014 Risco de Juros", "5\u20137 minutos")

    h2("Fio condutor")
    bd("Se\xe7\xe3o mais t\xe9cnica e mais reveladora. Quest\xe3o central: "
       "<i>\u201cSe os juros mudarem, quanto a carteira ganha ou perde?\u201d</i>")
    tip("FALA SUGERIDA",
        "\u201cA carteira tem sensibilidade moderada a juros. "
        "Se subirem 1,5%, impacto de R$ XXX mil negativos. Se ca\xedrem 1,5%, ganho de R$ XXX mil. "
        "O Focus projeta queda de 288 bps at\xe9 dezembro \u2014 se confirmado, a carteira ganha R$ XXX mil.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>Resumo de prote\xe7\xe3o:</b> Texto sobre sensibilidade da carteira.",
        "<b>4 KPIs:</b> Se Juros Subirem 1,5%, Se Ca\xedrem 1,5%, Prazo M\xe9dio, Cr\xe9dito Privado.",
        "<b>Tabela de stress (sim\xe9trica):</b> \xb10,5%, \xb11,0%, \xb11,5% + Proje\xe7\xe3o Focus.",
        "<b>Gr\xe1fico de barras:</b> Impacto por cen\xe1rio.",
        "<b>Callout Focus:</b> Impacto da proje\xe7\xe3o de corte na carteira.",
        "<b>Cen\xe1rios hist\xf3ricos:</b> Crise 2008, 2015, COVID-19, Choque 2022.",
        "<b>Gloss\xe1rio:</b> Termos t\xe9cnicos em linguagem simples.",
    ])
    sep()
    h2("Metodologia \u2014 Detalhada")

    h3("1. Duration e DV01")
    bd("<b>Duration</b> mede sensibilidade a juros. Maior duration = maior movimento de pre\xe7o.")
    bd("<b>Duration de Macaulay</b> simplificada por multiplicadores:")
    bul([
        "<b>P\xf3s-fixado (CDI, Selic):</b> durMac = prazo \xd7 0,08 \u2014 quase nenhuma sensibilidade.",
        "<b>CDI + spread alto:</b> durMac = prazo \xd7 0,15.",
        "<b>Prefixado:</b> durMac = prazo \xd7 0,95 \u2014 alta sensibilidade.",
        "<b>IPCA+:</b> durMac = prazo \xd7 0,82 \u2014 moderada-alta.",
        "<b>Fundos:</b> durMac = prazo \xd7 0,30 \xd7 0,35 \u2014 estimativa conservadora.",
    ])
    bd("<b>Duration Modificada:</b> durMod = durMac / (1 + yield/200).")
    bd("<b>DV01</b> = durMod \xd7 total \xd7 0,0001. "
       "Exemplo: R$ 1M com durMod = 3,0 \u2192 DV01 = R$ 300 por basis point.")
    sep()
    h3("2. Stress de juros")
    bd("<b>impacto = \u2212totalDV01 \xd7 \u0394bp</b>. "
       "Juros <b>sobem</b> = pre\xe7os <b>caem</b> (e vice-versa). "
       "Exemplo: totalDV01 = R$ 5.000, alta de 150 bps \u2192 \u2212R$ 750.000.")
    bd("Cen\xe1rios sim\xe9tricos (\xb10,5%, \xb11,0%, \xb11,5%) para visualizar risco e oportunidade.")
    sep()
    h3("3. Proje\xe7\xe3o Focus")
    bd("Boletim Focus (BCB): mediana de ~140 institui\xe7\xf5es. "
       "<b>Selic 15,00% \u2192 12,125%</b> at\xe9 dez/26 = corte de <b>288 bps</b>.")
    bd("Impacto na carteira: <b>totalDV01 \xd7 288</b> (positivo, juros caindo).")
    bd("<b>Na pr\xe1tica:</b> quando o Copom corta a Selic, t\xedtulos prefixados e IPCA+ "
       "comprados a taxas mais altas se valorizam no secund\xe1rio.")
    sep()
    h3("4. Cen\xe1rios Hist\xf3ricos")
    bd("4 crises com choques documentados: 2008, 2015, 2020, 2022. Para cada:")
    bul([
        "<b>Juros:</b> Varia\xe7\xe3o em bps \u2192 impacto via DV01.",
        "<b>Bolsa:</b> Queda Ibovespa \u2192 impacto = totalRV \xd7 (queda%/100).",
        "<b>Cr\xe9dito:</b> Abertura de spreads \u2192 \u2212totalCr\xe9dito \xd7 (spread/10000) \xd7 duration.",
        "<b>Total:</b> Soma dos 3 = perda estimada na carteira atual.",
    ])
    bd("Narrativa autom\xe1tica: \u201cMesmo no pior cen\xe1rio, a perda seria de X%\u201d \u2014 "
       "demonstrando prote\xe7\xe3o do p\xf3s-fixado.")
    st.append(PageBreak())

    # ════════════════════ 07 — PORTFOLIO EFFICIENCY ════════════════════
    sec("07", "Portfolio Efficiency \u2014 Custo e Concentra\xe7\xe3o", "3\u20134 minutos")

    h2("Fio condutor")
    bd("Transi\xe7\xe3o: \u201cAl\xe9m de impostos, temos os custos de gest\xe3o. "
       "Quanto a carteira paga em taxas e se o dinheiro est\xe1 bem diversificado.\u201d")
    tip("FALA SUGERIDA",
        "\u201cO custo total \xe9 de X,XX% ao ano = R$ XXX mil. "
        "A maior parte est\xe1 em ativos sem custo \u2014 renda fixa direta, t\xedtulos p\xfablicos, CDBs. "
        "Solis Antares e Riza cobram taxa alta mas entregam alpha \u2014 o fee se justifica.\u201d")
    sep()
    h2("Metodologia")
    h3("TER ponderado")
    bd("<b>TER = \u03a3(taxaAdmin<sub>i</sub> \xd7 total<sub>i</sub>) / \u03a3(total<sub>i</sub>)</b>. "
       "M\xe9dia ponderada da taxa de administra\xe7\xe3o.")
    h3("HHI (Herfindahl-Hirschman)")
    bd("<b>HHI = \u03a3(share<sub>i</sub><sup>2</sup>)</b>. "
       "&lt;1.500 = Diversificado. 1.500\u20132.500 = Moderado. &gt;2.500 = Concentrado. Ideal &lt;1.000.")
    h3("Alpha/Custo")
    bd("<b>alpha = rentAnual \u2212 CDIanual</b>, depois <b>alpha/custo = alpha / taxaAdmin</b>. "
       "&gt;1,0x = fundo entrega mais do que cobra. &lt;0 = perdendo para CDI e cobrando taxa.")
    st.append(PageBreak())

    # ════════════════════ 08 — MACRO VIEW ════════════════════
    sec("08", "Macro View \u2014 Cen\xe1rio Econ\xf4mico", "3\u20134 minutos")

    h2("Fio condutor")
    bd("Encerramento com vis\xe3o de mercado: \u201cPara fechar, o ambiente em que estamos operando "
       "e o que isso significa para as decis\xf5es de aloca\xe7\xe3o.\u201d")
    tip("FALA SUGERIDA",
        "\u201cO cen\xe1rio macro est\xe1 favor\xe1vel. Selic em 15%, Focus projeta queda para 12,1% at\xe9 dezembro. "
        "Janela para travar taxas boas agora, antes que caiam.\u201d")
    sep()
    h2("O que est\xe1 na tela")
    bul([
        "<b>5 indicadores:</b> Selic, CDI, IPCA, C\xe2mbio e Ibovespa.",
        "<b>Gr\xe1fico da Selic:</b> Proje\xe7\xe3o Focus com curva descendente at\xe9 Dez/26.",
        "<b>Tabela Focus:</b> IPCA, Selic, PIB e c\xe2mbio para 2026 e 2027.",
        "<b>6 cards de Leitura de Cen\xe1rio:</b> Atividade, Infla\xe7\xe3o, Emprego, Cr\xe9dito, Fiscal, Externo.",
    ])
    sep()
    h2("Fontes de dados")
    bul([
        "<b>Selic e CDI:</b> Banco Central do Brasil (API de s\xe9ries temporais).",
        "<b>IPCA:</b> IBGE \u2014 acumulado 12 meses.",
        "<b>Focus:</b> Boletim Focus (BCB) \u2014 mediana do mercado. Atualizado via <font face='Courier'>npm run update-macro</font>.",
        "<b>C\xe2mbio:</b> BCB \u2014 PTAX de fechamento.",
        "<b>Ibovespa:</b> B3.",
    ])
    h3("Curva Selic Focus")
    bd("Constru\xedda a partir das medianas Focus para cada reuni\xe3o do Copom. "
       "Script <font face='Courier'>update-macro.mjs</font> busca via API BCB e armazena em <font face='Courier'>src/data/macro.json</font>.")
    st.append(PageBreak())

    # ════════════════════ 09 — METODOLOGIA GERAL ════════════════════
    sec("09", "Metodologia Geral \u2014 Fontes e Premissas", "Refer\xeancia")

    h2("Fontes de dados")
    ft = Table([
        ["Dado", "Fonte", "Frequ\xeancia"],
        ["Carteira (posi\xe7\xf5es)", "XP Investimentos (consolidado)", "Mensal"],
        ["Rentabilidade e CDI", "XP Investimentos + CETIP/B3", "Mensal"],
        ["Selic, CDI, IPCA", "Banco Central do Brasil (API)", "Di\xe1ria/Mensal"],
        ["Focus (proje\xe7\xf5es)", "Boletim Focus (BCB)", "Semanal"],
        ["ETTJ (curva de juros)", "ANBIMA", "Di\xe1ria"],
        ["Taxas indicativas TPF", "ANBIMA", "Di\xe1ria"],
        ["Credit curves", "ANBIMA", "Di\xe1ria"],
        ["C\xe2mbio (PTAX)", "Banco Central do Brasil", "Di\xe1ria"],
        ["Ibovespa", "B3", "Di\xe1ria"],
    ], colWidths=[120, 200, 80])
    ft.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), FB), ("FONTNAME", (0,1), (-1,-1), F),
        ("FONTSIZE", (0,0), (-1,-1), 9), ("TEXTCOLOR", (0,0), (-1,0), white),
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,1), (-1,-1), SLATE),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("GRID", (0,0), (-1,-1), 0.5, LGRAY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, VLIGHT]),
    ]))
    st.append(ft); st.append(Spacer(1, 6*mm))

    sep()
    h2("Premissas e limita\xe7\xf5es")
    bul([
        "Rentabilidades s\xe3o <b>l\xedquidas de taxas de administra\xe7\xe3o</b> e <b>brutas de IR</b>, exceto onde indicado.",
        "A duration \xe9 estimada por aproxima\xe7\xe3o (multiplicadores por indexador), n\xe3o por fluxo de caixa.",
        "O DV01 assume paralelismo na curva (todos os v\xe9rtices se movem igualmente).",
        "Cen\xe1rios hist\xf3ricos usam choques reais, aplicados \xe0 carteira <b>atual</b> (n\xe3o \xe0 de \xe9poca).",
        "A proje\xe7\xe3o Focus \xe9 a <b>mediana do mercado</b> \u2014 n\xe3o \xe9 predi\xe7\xe3o.",
        "O come-cotas drag \xe9 estimado com base na rentabilidade mensal corrente, anualizada.",
        "O equivalente bruto assume al\xedquota constante.",
        "O FIP AG7 usa TIR de 23% a.a. e MOIC de 2,5x\u20133,0x \u2014 cen\xe1rios, n\xe3o garantias.",
    ])

    sep()
    h2("Fluxo de atualiza\xe7\xe3o")
    bd("O Patrimonium \xe9 alimentado por 3 arquivos JSON atualizados mensalmente:")
    bul([
        "<font face='Courier'>src/data/cliente.json</font> \u2014 Carteira, extra\xedda da XP.",
        "<font face='Courier'>src/data/macro.json</font> \u2014 Macro, via <font face='Courier'>npm run update-macro</font> (API BCB + B3).",
        "<font face='Courier'>src/data/anbima.json</font> \u2014 Curvas ETTJ, taxas indicativas e credit curves (ANBIMA).",
    ])

    sep()
    h2("Ordem recomendada de apresenta\xe7\xe3o")
    bd("Tempo total estimado: 25\u201335 minutos.")
    ot = Table([
        ["#", "Se\xe7\xe3o", "Tempo", "Objetivo"],
        ["1", "Overview", "3\u20134 min", "Ancorar no patrim\xf4nio e resultado"],
        ["2", "Asset Allocation", "3\u20134 min", "Mostrar onde est\xe1 o dinheiro"],
        ["3", "Portfolio Strategy", "4\u20135 min", "Liquidez, vencimentos e rotation"],
        ["4", "Benchmark", "4\u20135 min", "Performance vs refer\xeancias"],
        ["5", "Tax Alpha", "3\u20134 min", "Efici\xeancia fiscal"],
        ["6", "Hedge", "5\u20137 min", "Gest\xe3o de risco de juros"],
        ["7", "Portfolio Efficiency", "3\u20134 min", "Custos e diversifica\xe7\xe3o"],
        ["8", "Macro View", "3\u20134 min", "Contexto de mercado"],
    ], colWidths=[25, 110, 55, 210])
    ot.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), FB), ("FONTNAME", (0,1), (-1,-1), F),
        ("FONTSIZE", (0,0), (-1,-1), 9.5), ("TEXTCOLOR", (0,0), (-1,0), white),
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,1), (0,-1), GREEN),
        ("FONTNAME", (0,1), (0,-1), FB), ("TEXTCOLOR", (1,1), (-1,-1), SLATE),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("GRID", (0,0), (-1,-1), 0.5, LGRAY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, VLIGHT]),
    ]))
    st.append(ot)
    st.append(Spacer(1, 8*mm))

    sep()
    h2("Dicas finais")
    bul([
        "Comece sempre pelo patrim\xf4nio \u2014 \xe9 o n\xfamero que o cliente mais quer ouvir.",
        "Use os callouts verdes como \u201cpontos de valor\u201d \u2014 momentos de mostrar o que voc\xea faz pelo cliente.",
        "Nos cen\xe1rios hist\xf3ricos: \u201cMesmo na pior crise, a perda seria de X%\u201d.",
        "Na proje\xe7\xe3o Focus, conecte com a\xe7\xe3o: \u201cPor isso recomendamos travar taxas agora\u201d.",
        "Feche com a proposta de rotation (FIP AG7) ou com as recomenda\xe7\xf5es estrat\xe9gicas.",
        "O Patrimonium fica acess\xedvel para consulta posterior.",
    ])

    st.append(Spacer(1, 10*mm))
    st.append(ColorLine(uw, 2, NAVY))
    st.append(Spacer(1, 4*mm))
    st.append(Paragraph(
        "Patrimonium \u2014 Guia de Apresenta\xe7\xe3o<br/>"
        "Documento confidencial. Uso interno.<br/>"
        "Gerado em 15/03/2026.",
        ParagraphStyle("fin", fontName=FI, fontSize=9, leading=14, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=hf)
    print(f"\n  OK - PDF gerado: {path}")
    print(f"    ({os.path.getsize(path) // 1024} KB)\n")
    return path


if __name__ == "__main__":
    build_pdf()
