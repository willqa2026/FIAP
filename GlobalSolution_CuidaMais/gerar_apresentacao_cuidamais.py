# -*- coding: utf-8 -*-
"""Monta a apresentação da Global Solution (Cuida+) em PowerPoint (.pptx).

Pré-requisito: rodar antes
  - telas/gerar_telas_cuidamais.py        (protótipo)
  - modelo_dados/gerar_modelo_cuidamais.py (modelos lógico/físico + DDL)

A exportação para PDF é feita pelo PowerPoint (ver exportar_pdf.ps1).
"""

from __future__ import annotations

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

BASE = os.path.dirname(os.path.abspath(__file__))
TELAS = os.path.join(BASE, "telas")
MODELO = os.path.join(BASE, "modelo_dados")
OUT = os.path.join(BASE, "GS_CuidaMais_RM576183.pptx")

# Link do vídeo pitch: substitua após publicar no YouTube e exporte o PDF novamente.
VIDEO_URL = "https://www.youtube.com/watch?v=RcjY4MZFVf0"

INTEGRANTES = [("Will Pereira", "RM576183")]
FONT = "Segoe UI"


def rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


SIDE = rgb("0E4F4A")
PRIMARY = rgb("0F766E")
PRIMARY_L = rgb("DDF4EF")
MINT = rgb("5EEAD4")
ACCENT = rgb("B45309")
ACCENT_L = rgb("FEF3C7")
DANGER = rgb("B91C1C")
OK = rgb("15803D")
BLUE = rgb("1D4ED8")
BLUE_L = rgb("DBEAFE")
INK = rgb("1F2937")
MUTED = rgb("5B6472")
BG = rgb("F3F6F5")
WHITE = rgb("FFFFFF")
BORDER = rgb("DADFE3")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def box(slide, x, y, w, h, fill=WHITE, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None, lw=1.0):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    s.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def text(slide, x, y, w, h, content, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=1.1, space_after=4, shape=None):
    """content: str | list de parágrafos. Parágrafo: str ou lista de runs (texto, {bold,color,size})."""
    if shape is None:
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    else:
        tb = shape
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.04))
    paras = content if isinstance(content, list) else [content]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        para.space_after = Pt(space_after)
        runs = p if isinstance(p, list) else [(p, {})]
        for t, st in runs:
            r = para.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(st.get("size", size))
            f.bold = st.get("bold", bold)
            f.italic = st.get("italic", False)
            f.color.rgb = st.get("color", color)
    return tb


def bullets(slide, x, y, w, h, items, size=16, color=INK, bullet="•", bcolor=PRIMARY, space_after=8):
    paras = []
    for it in items:
        if isinstance(it, tuple):
            head, rest = it
            paras.append([(bullet + "  ", {"color": bcolor, "bold": True}), (head, {"bold": True}), (rest, {})])
        else:
            paras.append([(bullet + "  ", {"color": bcolor, "bold": True}), (it, {})])
    return text(slide, x, y, w, h, paras, size=size, color=color, space_after=space_after)


def notes(slide, t):
    slide.notes_slide.notes_text_frame.text = t


page = {"n": 0}


def new_slide(title=None, kicker=None, dark=False):
    s = prs.slides.add_slide(BLANK)
    page["n"] += 1
    box(s, 0, 0, SW, SH, fill=SIDE if dark else WHITE)
    if title:
        box(s, 0, 0, 0.16, SH, fill=PRIMARY)
        if kicker:
            text(s, 0.6, 0.32, 10, 0.35, kicker.upper(), size=12, color=PRIMARY, bold=True)
        text(s, 0.6, 0.6, 12.2, 0.8, title, size=30, bold=True, color=INK)
    if not dark:
        text(s, 0.6, 7.03, 8, 0.3, "Cuida+  ·  Global Solution 2026 — CitizenTech  ·  FIAP 1TDS", size=10, color=MUTED)
        text(s, 11.9, 7.03, 0.9, 0.3, str(page["n"]), size=10, color=MUTED, align=PP_ALIGN.RIGHT)
    return s


def card(slide, x, y, w, h, title=None, body=None, fill=WHITE, line=BORDER, title_color=INK, size=14,
         icon=None, icon_fill=PRIMARY_L, icon_color=PRIMARY, title_size=17):
    box(slide, x, y, w, h, fill=fill, line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    ty = y + 0.2
    tx_ = x + 0.25
    if icon:
        c = box(slide, x + 0.25, y + 0.22, 0.55, 0.55, fill=icon_fill, shape=MSO_SHAPE.OVAL)
        text(slide, 0, 0, 0, 0, icon, size=18, bold=True, color=icon_color, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, shape=c)
        tx_ = x + 0.95
    if title:
        text(slide, tx_, ty + (0.08 if icon else 0), x + w - tx_ - 0.2, 0.5, title, size=title_size, bold=True,
             color=title_color)
    if body:
        by = y + (0.9 if icon else 0.7)
        if isinstance(body, list) and body and isinstance(body[0], (str, tuple)) and not isinstance(body[0], list):
            bullets(slide, x + 0.25, by, w - 0.45, h - (by - y) - 0.1, body, size=size, space_after=4)
        else:
            text(slide, x + 0.25, by, w - 0.45, h - (by - y) - 0.1, body, size=size, color=MUTED)


def image_fit(slide, path, x, y, w, h, border=True):
    from PIL import Image
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    ww, hh = iw * scale, ih * scale
    px, py = x + (w - ww) / 2, y + (h - hh) / 2
    if border:
        box(slide, px - 0.03, py - 0.03, ww + 0.06, hh + 0.06, fill=BORDER)
    slide.shapes.add_picture(path, Inches(px), Inches(py), Inches(ww), Inches(hh))
    return px, py, ww, hh


def arrow(slide, x1, y1, x2, y2, color=PRIMARY, w=2.25):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    from lxml import etree
    tail = etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd")
    tail.set("type", "triangle")
    tail.set("w", "med")
    tail.set("len", "med")
    return c


def pill(slide, x, y, w, h, label, fill, color, size=12):
    s = box(slide, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    text(slide, 0, 0, 0, 0, label, size=size, bold=True, color=color, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, shape=s)


def number_dot(slide, x, y, n, fill=ACCENT, size=13, d=0.38):
    c = box(slide, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL)
    text(slide, 0, 0, 0, 0, str(n), size=size, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, shape=c)


def logo(slide, x, y, size=40, light=True):
    c = box(slide, x, y, size / 72 * 1.05, size / 72 * 1.05, fill=rgb("2DD4BF") if light else PRIMARY,
            shape=MSO_SHAPE.OVAL)
    text(slide, 0, 0, 0, 0, "+", size=size * 0.8, bold=True, color=SIDE if light else WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=c)
    text(slide, x + size / 72 * 1.2, y - 0.08, 5, size / 72 * 1.4, "Cuida+", size=size, bold=True,
         color=WHITE if light else PRIMARY)


# --------------------------------------------------------------------------- #
# 1. Capa
# --------------------------------------------------------------------------- #
s = new_slide(dark=True)
box(s, 7.2, 0, 6.133, SH, fill=rgb("0B3F3B"))
logo(s, 0.8, 0.8, size=44)
text(s, 0.8, 2.05, 6.3, 1.6, "Autonomia e cuidado para a pessoa idosa, com uma assistente que conversa, "
     "lembra e agenda.", size=26, bold=True, color=WHITE, spacing=1.05)
text(s, 0.8, 3.75, 6.2, 0.8, "Plataforma web CitizenTech que conecta idosos, famílias e prestadores de "
     "serviço do bairro.", size=15, color=rgb("CDEDE8"))
text(s, 0.8, 4.75, 6, 0.35, "INTEGRANTE", size=12, bold=True, color=MINT)
y = 5.12
for nome, rm in INTEGRANTES:
    text(s, 0.8, y, 4.2, 0.4, nome, size=18, bold=True, color=WHITE)
    text(s, 4.6, y, 2, 0.4, rm, size=18, color=rgb("CDEDE8"))
    y += 0.45
text(s, 0.8, 6.55, 6.4, 0.4, "FIAP · 1TDS · Global Solution 2026 — Desafio CitizenTech", size=12,
     color=rgb("9FD9D1"))
image_fit(s, os.path.join(TELAS, "tela_02_inicio_idoso.png"), 7.6, 1.2, 5.35, 3.1, border=False)
image_fit(s, os.path.join(TELAS, "tela_03_assistente_ia.png"), 7.6, 4.15, 5.35, 3.1, border=False)
notes(s, "Capa: nome da solução, integrante e RM (requisito do enunciado).")

# --------------------------------------------------------------------------- #
# 2. Identificação da solução
# --------------------------------------------------------------------------- #
s = new_slide("Identificação da solução", "1 · Identificação")
card(s, 0.6, 1.6, 3.9, 5.1, "Nome", None, fill=PRIMARY_L, line=None, title_color=PRIMARY)
logo(s, 0.9, 2.45, size=34, light=False)
text(s, 0.85, 3.4, 3.4, 3.2, ["Cuida+ é uma plataforma web com assistente de voz baseada em inteligência "
                              "artificial.",
                              "O nome reforça a ideia de “mais cuidado”, sem tirar a autonomia de quem é cuidado."],
     size=15, color=INK, space_after=10)
card(s, 4.75, 1.6, 8.0, 2.2, "Objetivo", None)
text(s, 5.0, 2.2, 7.5, 1.5, "Ajudar pessoas idosas a viverem com mais autonomia e segurança: a plataforma "
     "conversa por voz, lembra os horários dos remédios e dos compromissos e marca horários diretamente na "
     "agenda de médicos, salões e comércios do bairro — mantendo a família informada.", size=15, color=INK)
card(s, 4.75, 4.0, 8.0, 2.7, "Público beneficiado", None)
pubs = [("☺", "Pessoas idosas (60+)", "que moram sozinhas, tomam remédios de uso\ncontínuo e têm dificuldade com apps.", PRIMARY, PRIMARY_L),
        ("♥", "Familiares e cuidadores", "que acompanham à distância e precisam saber\nse está tudo bem.", BLUE,
         BLUE_L),
        ("✂", "Pequenos prestadores", "médicos, clínicas, salões, farmácias e comércios\nque atendem o público 60+.",
         ACCENT, ACCENT_L)]
y = 4.6
for ic, t, d, c, cl in pubs:
    o = box(s, 5.0, y, 0.5, 0.5, fill=cl, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, ic, size=16, bold=True, color=c, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=o)
    text(s, 5.65, y + 0.05, 2.6, 0.6, t, size=14, bold=True)
    text(s, 8.2, y - 0.02, 4.5, 0.65, d, size=12, color=MUTED, spacing=1.0)
    y += 0.7

# --------------------------------------------------------------------------- #
# 3. Problema e oportunidade
# --------------------------------------------------------------------------- #
s = new_slide("O problema: envelhecer com autonomia e segurança", "2 · Problema e oportunidade")
stats = [("32,1 mi", "de pessoas com 60 anos ou mais no Brasil — alta de 56% em relação a 2010.",
          "IBGE, Censo 2022", PRIMARY),
         ("18%", "dos idosos usam 5 ou mais medicamentos por dia (polifarmácia); 93% usam ao menos um de uso "
          "contínuo.", "Ramos et al., PNAUM, Rev. Saúde Pública, 2016", ACCENT),
         ("≈ 50%", "é a adesão média a tratamentos de doenças crônicas — metade das doses não é tomada como "
          "prescrito.", "OMS, Adherence to long-term therapies, 2003", DANGER),
         ("30%", "dos idosos ainda não usam internet — apps complexos excluem parte do público.",
          "IBGE, PNAD Contínua TIC 2024 (69,8% conectados)", BLUE)]
x = 0.6
for big, d, src, c in stats:
    box(s, x, 1.65, 2.95, 2.75, fill=BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    text(s, x + 0.22, 1.8, 2.6, 0.8, big, size=38, bold=True, color=c)
    text(s, x + 0.22, 2.65, 2.55, 1.2, d, size=13, color=INK, spacing=1.0)
    text(s, x + 0.22, 3.92, 2.6, 0.4, src, size=9.5, color=MUTED)
    x += 3.08
text(s, 0.6, 4.65, 12, 0.4, "Por que isso importa", size=17, bold=True, color=PRIMARY)
bullets(s, 0.6, 5.05, 6.0, 1.9, [
    ("Remédios esquecidos ", "agravam hipertensão e diabetes e geram internações evitáveis."),
    ("Agendar é difícil: ", "telefone ocupado, apps com letras pequenas, muitos passos."),
], size=14)
bullets(s, 6.75, 5.05, 6.0, 1.9, [
    ("A família se preocupa à distância ", "e não sabe se a rotina está sendo cumprida."),
    ("Oportunidade: ", "uma IA conversacional por voz remove a barreira digital — o idoso só precisa falar."),
], size=14)
notes(s, "Fontes: IBGE Censo 2022 (32.113.490 pessoas 60+); Ramos LR et al. Rev Saúde Pública 2016;50(supl 2):9s; "
         "WHO 2003 Adherence to long-term therapies; IBGE PNAD Contínua TIC 2024.")

# --------------------------------------------------------------------------- #
# 4. Quem é impactado (persona + dores)
# --------------------------------------------------------------------------- #
s = new_slide("Quem convive com o problema", "2 · Problema e oportunidade")
box(s, 0.6, 1.6, 4.3, 5.2, fill=PRIMARY_L, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
o = box(s, 0.9, 1.9, 1.1, 1.1, fill=PRIMARY, shape=MSO_SHAPE.OVAL)
text(s, 0, 0, 0, 0, "MA", size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=o)
text(s, 2.15, 1.98, 2.7, 0.5, "Dona Maria, 74", size=20, bold=True, color=INK)
text(s, 2.15, 2.45, 2.7, 0.6, "Persona principal · mora sozinha em São Paulo", size=12, color=MUTED)
bullets(s, 0.9, 3.25, 3.8, 3.5, [
    "Hipertensa e diabética: 4 remédios em horários diferentes.",
    "Usa celular para WhatsApp e ligações; não instala apps novos.",
    "Prefere falar a digitar; tem dificuldade de leitura com letra pequena.",
    "A filha Carla mora em outro bairro e liga todo dia para conferir.",
], size=13.5, space_after=7)
dores = [
    ("Pessoa idosa", ["Esquece doses ou toma em dobro", "Não consegue marcar consulta por telefone",
                      "Perde compromissos e se sente dependente"], PRIMARY, PRIMARY_L, "☺"),
    ("Família / cuidador", ["Não sabe se a mãe tomou o remédio", "Precisa agendar tudo por ela",
                            "Descobre problemas só depois"], BLUE, BLUE_L, "♥"),
    ("Prestador local", ["Faltas de pacientes e clientes 60+", "Atendimento por telefone toma tempo",
                         "Não sabe de necessidades especiais antes"], ACCENT, ACCENT_L, "✂"),
]
y = 1.6
for t, items, c, cl, ic in dores:
    box(s, 5.15, y, 7.6, 1.62, fill=WHITE, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    o = box(s, 5.4, y + 0.3, 0.6, 0.6, fill=cl, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, ic, size=18, bold=True, color=c, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shape=o)
    text(s, 6.25, y + 0.18, 6.3, 0.4, "Principais dificuldades — " + t, size=15, bold=True, color=c)
    bullets(s, 6.25, y + 0.58, 6.3, 1.0, items, size=13, bcolor=c, space_after=1)
    y += 1.76

# --------------------------------------------------------------------------- #
# 5. Como funciona (ecossistema)
# --------------------------------------------------------------------------- #
s = new_slide("Como a plataforma web funciona", "3 · Proposta de solução web")
# centro
c = box(s, 4.9, 2.75, 3.55, 2.2, fill=SIDE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
text(s, 5.0, 2.9, 3.35, 0.5, "Plataforma web Cuida+", size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
text(s, 5.0, 3.4, 3.35, 1.5, ["Assistente de IA (voz + texto)", "Agenda unificada de horários",
                              "Lembretes e alertas", "Banco de dados Oracle"],
     size=12.5, color=rgb("CDEDE8"), align=PP_ALIGN.CENTER, space_after=2)
actors = [
    (0.6, 1.65, "☺  Pessoa idosa", "Fala com a assistente, confirma doses e\ncompromissos em telas simples.",
     PRIMARY, PRIMARY_L),
    (0.6, 4.75, "♥  Família / cuidador", "Cadastra remédios, acompanha a adesão e\nrecebe alertas inteligentes.",
     BLUE, BLUE_L),
    (9.0, 1.65, "✂  Prestadores locais", "Publicam serviços e horários livres;\nconfirmam agendamentos.", ACCENT,
     ACCENT_L),
    (9.0, 4.75, "☏  Canais de apoio", "WhatsApp e ligação automática para quem\ntem pouca conectividade.",
     MUTED, BG),
]
for x, y, t, d, col, cl in actors:
    box(s, x, y, 3.75, 1.45, fill=cl, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    text(s, x + 0.2, y + 0.15, 3.4, 0.4, t, size=15, bold=True, color=col)
    text(s, x + 0.2, y + 0.6, 3.45, 0.85, d, size=12, color=INK, spacing=1.0)
arrow(s, 4.35, 2.4, 4.9, 3.1)
arrow(s, 4.35, 5.45, 4.9, 4.6)
arrow(s, 9.0, 2.4, 8.45, 3.1)
arrow(s, 9.0, 5.45, 8.45, 4.6)
text(s, 0.6, 6.35, 12.2, 0.6, [[("Fluxo central: ", {"bold": True, "color": PRIMARY}),
                                ("idoso pede por voz → IA entende e busca horários livres → idoso confirma → "
                                 "prestador aceita → lembretes automáticos → família acompanha.", {})]], size=14)

# --------------------------------------------------------------------------- #
# 6. Funcionalidades principais
# --------------------------------------------------------------------------- #
s = new_slide("Principais funcionalidades", "3 · Proposta de solução web")
funcs = [
    ("🎙", "Assistente de voz Cuida", "Entende pedidos falados (“marque um corte terça de manhã”), propõe opções e "
     "só marca após confirmação.", "Resolve: barreira digital"),
    ("✚", "Lembretes de remédios", "Alerta em tela cheia, com som e voz; “Já tomei” por botão ou fala; "
     "ligação automática se não houver resposta.", "Resolve: doses esquecidas"),
    ("▦", "Agenda pessoal", "Consultas, serviços e entregas em um só lugar, com lembrete 1 dia e 1 hora "
     "antes.", "Resolve: compromissos perdidos"),
    ("⌂", "Agenda dos prestadores", "Médicos, salões e comércios publicam serviços e horários livres; a IA reserva "
     "sem ligações.", "Resolve: dificuldade de agendar"),
    ("♥", "Painel da família", "Adesão aos remédios, histórico, compromissos e alertas inteligentes de risco.",
     "Resolve: preocupação à distância"),
    ("♿", "Acessibilidade total", "Fonte ajustável, alto contraste, leitura de tela em voz alta e "
     "observações de acessibilidade para o prestador.", "Resolve: exclusão de quem tem limitações"),
]
for i, (ic, t, d, r) in enumerate(funcs):
    x = 0.6 + (i % 3) * 4.1
    y = 1.6 + (i // 3) * 2.65
    card(s, x, y, 3.9, 2.45, t, None, icon=ic)
    text(s, x + 0.25, y + 0.95, 3.45, 1.1, d, size=12.5, color=INK, spacing=1.0)
    pill(s, x + 0.25, y + 1.95, 3.4, 0.33, r, PRIMARY_L, PRIMARY, size=11)

# --------------------------------------------------------------------------- #
# 7. Benefícios e CitizenTech
# --------------------------------------------------------------------------- #
s = new_slide("Benefícios e conexão com o conceito de CitizenTech", "3 · Proposta de solução web")
bens = [("Para a pessoa idosa", ["Mais autonomia: agenda sozinha, só falando",
                                 "Mais segurança na rotina de remédios",
                                 "Menos dependência e isolamento"], PRIMARY, PRIMARY_L),
        ("Para a família", ["Tranquilidade: vê a rotina em tempo real",
                            "Alertas só quando importa (não vigilância)",
                            "Menos tempo gasto agendando por terceiros"], BLUE, BLUE_L),
        ("Para os prestadores", ["Menos faltas com lembretes automáticos",
                                 "Novos clientes 60+ sem telefone ocupado",
                                 "Sabem antes das necessidades de acessibilidade"], ACCENT, ACCENT_L)]
for i, (t, items, c, cl) in enumerate(bens):
    x = 0.6 + i * 4.1
    box(s, x, 1.6, 3.9, 2.55, fill=cl, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    text(s, x + 0.25, 1.75, 3.5, 0.45, t, size=16, bold=True, color=c)
    bullets(s, x + 0.25, 2.25, 3.5, 1.9, items, size=13, bcolor=c, bullet="✓", space_after=5)
text(s, 0.6, 4.4, 12, 0.4, "Por que é uma CitizenTech", size=17, bold=True, color=PRIMARY)
cts = [("Nasce de uma necessidade real", " do cidadão idoso, não de uma tecnologia em busca de uso."),
       ("Inclusiva e acessível", ": voz, alto contraste, fonte grande e WhatsApp/ligação para quem tem pouca "
                                 "conectividade."),
       ("Conecta o ecossistema local", ": comunidade, família e pequenos negócios do bairro em uma mesma "
                                       "plataforma."),
       ("Protege dados (LGPD)", ": consentimento do idoso, dados de saúde mínimos e acesso só de quem ele "
                                "autoriza.")]
bullets(s, 0.6, 4.85, 12.1, 2.1, cts, size=14, space_after=6)

# --------------------------------------------------------------------------- #
# 8. Jornada do usuário
# --------------------------------------------------------------------------- #
s = new_slide("Jornada principal: da fala ao compromisso cumprido", "4 · Protótipo da plataforma web")
steps = [("1", "Acessa", "Escolhe o perfil ou diz quem é", "Tela 1"),
         ("2", "Pede por voz", "“Quero cortar o cabelo terça de manhã”", "Telas 2 e 3"),
         ("3", "Confirma", "A IA mostra o que entendeu e 2 opções", "Tela 3"),
         ("4", "Prestador aceita", "Pedido chega na agenda do salão", "Tela 8"),
         ("5", "Lembretes", "Compromisso e remédios no horário", "Telas 4 e 5"),
         ("6", "Família avisada", "Painel e alertas inteligentes", "Telas 6 e 7")]
x = 0.6
for i, (n, t, d, tela) in enumerate(steps):
    box(s, x, 2.0, 1.9, 2.9, fill=BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    number_dot(s, x + 0.7, 2.2, n, fill=PRIMARY, size=18, d=0.5)
    text(s, x + 0.05, 2.85, 1.8, 0.5, t, size=14, bold=True, align=PP_ALIGN.CENTER)
    text(s, x + 0.12, 3.35, 1.66, 1.0, d, size=11.5, color=MUTED, align=PP_ALIGN.CENTER, spacing=1.0)
    pill(s, x + 0.3, 4.35, 1.3, 0.32, tela, PRIMARY_L, PRIMARY, size=10.5)
    if i < len(steps) - 1:
        arrow(s, x + 1.92, 3.45, x + 2.08, 3.45, color=MUTED, w=1.75)
    x += 2.1
text(s, 0.6, 5.3, 12.2, 1.5, [
    [("Telas do idoso: ", {"bold": True, "color": PRIMARY}),
     ("poucos elementos por tela, botões grandes, texto mínimo de 18 px e voz em todas as etapas.", {})],
    [("Telas da família e do prestador: ", {"bold": True, "color": PRIMARY}),
     ("mais densas em informação, focadas em acompanhamento e gestão.", {})],
    [("Os números laranja ", {"bold": True, "color": ACCENT}),
     ("nas telas a seguir indicam a ordem das principais interações.", {})]], size=14, space_after=6)

# --------------------------------------------------------------------------- #
# 9-17. Telas do protótipo
# --------------------------------------------------------------------------- #
telas = [
    ("tela_01_acesso.png", "Tela 1 — Acesso e escolha de perfil", "Todos os perfis",
     ["Três perfis claros: idoso, família e prestador.",
      "Idoso entra com telefone + código (sem senha).",
      "Barra de acessibilidade em todas as telas.",
      "Entrada também por voz."],
     ["Escolha do perfil com cartões grandes e ícones."]),
    ("tela_02_inicio_idoso.png", "Tela 2 — Início do idoso", "Pessoa idosa",
     ["Botão principal “Falar com a Cuida”.",
      "Remédios do dia por cor: tomado, agora, depois.",
      "Próximos compromissos com status.",
      "Atalho para a família e pedido de ajuda."],
     ["Pede um serviço por voz.", "Confirma a dose com “Já tomei”."]),
    ("tela_03_assistente_ia.png", "Tela 3 — Conversa com a assistente (IA)", "Pessoa idosa",
     ["A fala é transcrita e interpretada.",
      "A IA consulta horários livres reais.",
      "Mostra só 2 opções para não confundir.",
      "Nada é marcado sem confirmação."],
     ["Escolhe uma das opções.", "Confirma o agendamento.", "Vê o que a IA entendeu (transparência)."]),
    ("tela_04_confirmacao.png", "Tela 4 — Agendamento confirmado", "Pessoa idosa",
     ["Resumo em linguagem simples.",
      "Lembretes programados automaticamente.",
      "Família avisada.",
      "Atalhos: como chegar, remarcar."],
     ["Lembretes e aviso à família gerados pelo sistema."]),
    ("tela_05_lembrete_remedio.png", "Tela 5 — Lembrete de medicamento", "Pessoa idosa",
     ["Alerta em tela cheia, com som e voz.",
      "Resposta por botão ou fala.",
      "Sem resposta: ligação automática e depois alerta à família.",
      "Cada resposta alimenta o histórico."],
     ["“Já tomei” registra a dose no REGISTRO_DOSE."]),
    ("tela_06_painel_familia.png", "Tela 6 — Painel da família", "Família / cuidador",
     ["Indicadores da semana: adesão e doses esquecidas.",
      "Gráfico diário de doses.",
      "Alerta inteligente com score de risco.",
      "Histórico de atividades."],
     ["A IA identifica o padrão e sugere ações."]),
    ("tela_07_cadastro_medicamento.png", "Tela 7 — Cadastro de medicamento", "Família / cuidador",
     ["Nome, dosagem e instrução em linguagem simples.",
      "Vários horários e dias da semana.",
      "Prévia do lembrete que o idoso verá.",
      "Lista dos remédios ativos."],
     ["Define os horários das doses."]),
    ("tela_08_agenda_prestador.png", "Tela 8 — Agenda do prestador", "Prestador de serviço",
     ["Agenda semanal: livre, reservado, pendente, bloqueado.",
      "Solicitações feitas pela IA, com observações de acessibilidade.",
      "Confirmar ou recusar com um clique.",
      "Resumo do mês."],
     ["Confirma a solicitação recebida.", "Horário reservado via assistente de voz."]),
    ("tela_09_servicos_prestador.png", "Tela 9 — Serviços e disponibilidade", "Prestador de serviço",
     ["Cadastro de serviços: duração, preço, atendimento em casa.",
      "Horários de funcionamento geram os horários livres.",
      "Preferências: aceitar IA, confirmação automática.",
      "Acessibilidade do local declarada."],
     ["Cadastra os serviços.", "Publica a disponibilidade."]),
]
for fname, title, perfil, feats, steps_ in telas:
    s = new_slide(title, "4 · Protótipo da plataforma web")
    pill(s, 10.55, 0.72, 2.2, 0.38, perfil, PRIMARY_L, PRIMARY, size=11.5)
    image_fit(s, os.path.join(TELAS, fname), 0.6, 1.55, 9.0, 5.3)
    text(s, 9.95, 1.55, 2.9, 0.4, "Destaques", size=15, bold=True, color=PRIMARY)
    bullets(s, 9.95, 1.95, 2.9, 2.8, feats, size=12, space_after=5)
    text(s, 9.95, 4.75, 2.9, 0.4, "Interações", size=15, bold=True, color=ACCENT)
    y = 5.15
    for i, st in enumerate(steps_):
        number_dot(s, 9.95, y, i + 1, size=11, d=0.32)
        text(s, 10.35, y - 0.03, 2.5, 0.55, st, size=11.5, spacing=1.0)
        y += 0.55

# --------------------------------------------------------------------------- #
# 18-20. Modelagem de dados
# --------------------------------------------------------------------------- #
s = new_slide("Modelo lógico (Entidade-Relacionamento)", "5 · Modelagem de dados")
image_fit(s, os.path.join(MODELO, "modelo_logico.png"), 0.45, 1.45, 12.45, 5.5)
s = new_slide("Modelo físico relacional (Oracle Database)", "5 · Modelagem de dados")
image_fit(s, os.path.join(MODELO, "modelo_fisico.png"), 0.45, 1.45, 12.45, 5.5)

s = new_slide("Como o modelo sustenta as funcionalidades", "5 · Modelagem de dados")
grupos = [
    ("Pessoas", "IDOSO · CUIDADOR · VINCULO_CUIDADOR",
     "Um idoso pode ter vários cuidadores e um cuidador pode acompanhar vários idosos (N:N). O vínculo define "
     "quem recebe alertas.", PRIMARY, PRIMARY_L),
    ("Agenda e prestadores", "CATEGORIA_SERVICO · PRESTADOR · SERVICO · HORARIO_DISPONIVEL · AGENDAMENTO",
     "O prestador publica horários; o AGENDAMENTO reserva um horário (UK em id_horario impede dois "
     "agendamentos no mesmo horário).", ACCENT, ACCENT_L),
    ("Medicamentos", "MEDICAMENTO · HORARIO_MEDICAMENTO · REGISTRO_DOSE",
     "Cada dose prevista gera um registro (tomada, esquecida, adiada). É o histórico que alimenta lembretes, "
     "indicadores e a IA de adesão.", OK, rgb("DCFCE7")),
    ("Inteligência artificial", "INTERACAO_IA · ALERTA",
     "Guarda a intenção identificada em cada conversa (auditoria e melhoria da IA) e os alertas com score de "
     "risco enviados à família.", BLUE, BLUE_L),
]
for i, (t, ents, d, c, cl) in enumerate(grupos):
    x = 0.6 + (i % 2) * 6.15
    y = 1.55 + (i // 2) * 2.2
    box(s, x, y, 5.95, 2.0, fill=cl, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    text(s, x + 0.25, y + 0.15, 5.5, 0.4, t, size=16, bold=True, color=c)
    text(s, x + 0.25, y + 0.55, 5.5, 0.5, ents, size=10.5, bold=True, color=INK, spacing=1.0)
    text(s, x + 0.25, y + 1.08, 5.5, 0.9, d, size=12.5, color=INK, spacing=1.0)
text(s, 0.6, 6.0, 12.2, 0.9, [
    [("13 tabelas · 14 relacionamentos · ", {"bold": True, "color": PRIMARY}),
     ("PKs com IDENTITY, FKs nomeadas, UKs e CHECKs de domínio (status, datas, valores). Script DDL Oracle "
      "(cuidamais_ddl.sql) importável no Oracle Data Modeler.", {})]], size=13)

# --------------------------------------------------------------------------- #
# 21-22. Inteligência artificial
# --------------------------------------------------------------------------- #
s = new_slide("IA 1 — Assistente de agendamento por voz", "6 · Aplicação de inteligência artificial")
text(s, 0.6, 1.5, 12.2, 0.7, [[("Necessidade atendida: ", {"bold": True, "color": PRIMARY}),
                               ("idosos com pouca familiaridade digital conseguem marcar serviços sozinhos, "
                                "apenas falando — sem formulários, menus ou ligações.", {})]], size=15)
pipe = [("Voz → texto", "Reconhecimento de fala (STT) transcreve o pedido.", "🎙"),
        ("Entende o pedido", "Modelo de linguagem (LLM) identifica intenção e extrai serviço, dia, período e "
                             "preferências.", "✦"),
        ("Busca na agenda", "Consulta HORARIO_DISPONIVEL filtrando categoria, distância do CEP e período.", "⌕"),
        ("Propõe e confirma", "Oferece até 2 opções em voz e texto e pede confirmação explícita.", "✓"),
        ("Registra e lembra", "Grava AGENDAMENTO e INTERACAO_IA e programa os lembretes.", "⏰")]
x = 0.6
for i, (t, d, ic) in enumerate(pipe):
    box(s, x, 2.4, 2.3, 2.35, fill=BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    o = box(s, x + 0.85, 2.55, 0.6, 0.6, fill=PRIMARY, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, ic, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
         shape=o)
    text(s, x + 0.1, 3.25, 2.1, 0.4, t, size=14, bold=True, align=PP_ALIGN.CENTER)
    text(s, x + 0.12, 3.65, 2.06, 1.1, d, size=11, color=MUTED, align=PP_ALIGN.CENTER, spacing=1.0)
    if i < len(pipe) - 1:
        arrow(s, x + 2.32, 3.55, x + 2.48, 3.55, color=MUTED, w=1.75)
    x += 2.5
card(s, 0.6, 5.0, 4.0, 1.85, "Integração na experiência", None, title_size=14)
text(s, 0.85, 5.45, 3.6, 1.4, "Botão “Falar com a Cuida” na tela inicial (Tela 2), conversa com o painel “O que a "
     "Cuida entendeu” (Tela 3) e canal WhatsApp.", size=11.5, color=INK, spacing=1.0)
card(s, 4.75, 5.0, 4.0, 1.85, "Benefícios", None, title_size=14)
text(s, 5.0, 5.45, 3.6, 1.4, "Autonomia do idoso, agendamento em menos de 2 minutos, menos ligações para o "
     "prestador e menos erros (a IA confere conflitos com outros compromissos).", size=11.5, color=INK, spacing=1.0)
card(s, 8.9, 5.0, 3.85, 1.85, "Dados necessários", None, title_size=14)
text(s, 9.15, 5.45, 3.45, 1.4, "Áudio/texto do pedido, CEP do idoso, serviços e horários livres dos prestadores, "
     "compromissos já marcados e preferências.", size=11.5, color=INK, spacing=1.0)

s = new_slide("IA 2 — Monitor preditivo de adesão aos medicamentos", "6 · Aplicação de inteligência artificial")
text(s, 0.6, 1.5, 12.2, 0.7, [[("Necessidade atendida: ", {"bold": True, "color": PRIMARY}),
                               ("antecipar o esquecimento de remédios antes que vire rotina — e avisar a família "
                                "só quando importa.", {})]], size=15)
card(s, 0.6, 2.3, 6.0, 2.75, "Como funciona", None)
bullets(s, 0.85, 2.85, 5.6, 2.2, [
    ("Modelo de classificação ", "(ex.: regressão logística ou árvores de decisão) treinado com o histórico de "
                                 "doses."),
    ("Calcula diariamente um score de risco ", "(0 a 1) por horário de dose."),
    ("Score ≥ 0,70 ", "gera um ALERTA do tipo “R” com o padrão encontrado e sugestões de ação."),
], size=12.5, space_after=6)
card(s, 6.75, 2.3, 6.0, 2.75, "Dados utilizados (já presentes no modelo)", None)
bullets(s, 7.0, 2.85, 5.6, 2.2, [
    ("REGISTRO_DOSE: ", "atrasos, esquecimentos e forma de confirmação."),
    ("HORARIO_MEDICAMENTO: ", "horário e dias da dose."),
    ("AGENDAMENTO: ", "dias com compromissos fora de casa."),
    ("INTERACAO_IA: ", "frequência de uso da assistente."),
], size=12.5, space_after=5)
box(s, 0.6, 5.25, 7.4, 1.6, fill=rgb("FEE2E2"), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
text(s, 0.85, 5.35, 7.0, 0.4, "Exemplo (Tela 6)", size=14, bold=True, color=DANGER)
text(s, 0.85, 5.75, 7.0, 1.1, "“3 das últimas 5 doses das 20:00 foram esquecidas, sempre em dias com saída de "
     "casa à tarde.” → Sugestões: mudar o lembrete para 19:30 ou ligar para a mãe.", size=12.5, color=INK,
     spacing=1.0)
card(s, 8.15, 5.25, 4.6, 1.6, "IA responsável", None, title_size=14)
text(s, 8.4, 5.68, 4.2, 1.15, "Não faz diagnóstico nem altera receitas; apenas sugere. A decisão é sempre "
     "humana. Dados mínimos e consentidos (LGPD).", size=11.5, color=INK, spacing=1.0)

# --------------------------------------------------------------------------- #
# 23. Impacto e indicadores
# --------------------------------------------------------------------------- #
s = new_slide("Impacto esperado e indicadores", "7 · Impacto esperado e indicadores")
rows = [("Indicador", "Como medir (dados da plataforma)", "Meta no piloto (6 meses)"),
        ("Adesão aos medicamentos", "Doses “tomadas” ÷ doses previstas (REGISTRO_DOSE)", "≥ 85% (referência OMS ≈ 50%)"),
        ("Autonomia no agendamento", "% de agendamentos com origem “voz/web” feitos pelo próprio idoso",
         "≥ 60% dos agendamentos"),
        ("Faltas em compromissos", "Agendamentos com situação “N” ÷ total realizados", "< 10%"),
        ("Tempo para agendar", "Da primeira fala à confirmação (INTERACAO_IA)", "< 2 minutos"),
        ("Resposta da família", "Alertas de risco lidos em até 24 h (ALERTA.st_lido)", "≥ 90%"),
        ("Satisfação", "Pesquisa por voz após 30 dias de uso (nota de 1 a 5)", "≥ 4,5")]
tbl = s.shapes.add_table(len(rows), 3, Inches(0.6), Inches(1.55), Inches(12.15), Inches(4.3)).table
widths = [3.3, 5.6, 3.25]
for i, wdt in enumerate(widths):
    tbl.columns[i].width = Inches(wdt)
for r, row in enumerate(rows):
    for ci, val in enumerate(row):
        cell = tbl.cell(r, ci)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY if r == 0 else (BG if r % 2 == 0 else WHITE)
        cell.margin_left = cell.margin_right = Inches(0.12)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = val
        run.font.name = FONT
        run.font.size = Pt(13 if r else 13.5)
        run.font.bold = r == 0 or ci == 0
        run.font.color.rgb = WHITE if r == 0 else (PRIMARY if ci == 2 else INK)
text(s, 0.6, 6.1, 12.2, 0.8, [[("Resultados esperados: ", {"bold": True, "color": PRIMARY}),
                               ("menos complicações por doses esquecidas, mais autonomia e convívio social para o "
                                "idoso, tranquilidade para a família e menos faltas para o comércio local. Todos os "
                                "indicadores são calculados a partir das tabelas do modelo de dados.", {})]],
     size=13)

# --------------------------------------------------------------------------- #
# 24. ODS
# --------------------------------------------------------------------------- #
s = new_slide("Conexão com os Objetivos de Desenvolvimento Sustentável", "7 · Impacto · ODS da ONU")
ods = [("3", "Saúde e bem-estar", rgb("4C9F38"),
        "Meta 3.4 — reduzir a mortalidade prematura por doenças crônicas não transmissíveis.",
        "Maior adesão a tratamentos de hipertensão e diabetes e acompanhamento contínuo da rotina de saúde."),
       ("10", "Redução das desigualdades", rgb("DD1367"),
        "Meta 10.2 — promover a inclusão social de todos, independentemente da idade ou deficiência.",
        "A voz remove a barreira digital: quem não domina apps passa a acessar serviços sozinho."),
       ("11", "Cidades e comunidades sustentáveis", rgb("FD9D24"),
        "Meta 11.3 — urbanização inclusiva e participativa.",
        "Conecta o idoso aos serviços do próprio bairro, fortalece o comércio local e reduz deslocamentos "
        "perdidos.")]
for i, (n, t, c, meta, how) in enumerate(ods):
    x = 0.6 + i * 4.1
    box(s, x, 1.6, 3.9, 1.35, fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, x + 0.2, 1.62, 1.2, 1.3, n, size=54, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 1.45, 1.7, 2.35, 1.2, ["ODS " + n, t], size=15, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE,
         space_after=0)
    box(s, x, 3.1, 3.9, 3.7, fill=BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    text(s, x + 0.25, 3.25, 3.45, 1.2, meta, size=12.5, bold=True, color=INK, spacing=1.0)
    text(s, x + 0.25, 4.45, 3.45, 0.4, "Como a Cuida+ contribui", size=13, bold=True, color=PRIMARY)
    text(s, x + 0.25, 4.85, 3.45, 1.9, how, size=13, color=INK, spacing=1.05)

# --------------------------------------------------------------------------- #
# 25. Diferenciais e viabilidade
# --------------------------------------------------------------------------- #
s = new_slide("Diferenciais e viabilidade", "Inovação e impacto social")
difs = [("Dois lados conectados", "A IA não só lembra: ela agenda de verdade, porque os prestadores publicam suas "
                                  "agendas na mesma plataforma."),
        ("Voz em primeiro lugar", "Pensada para quem não usa apps: fala, WhatsApp e ligação automática."),
        ("Família sem vigilância", "Alertas só quando há risco real, preservando a autonomia do idoso."),
        ("Acessibilidade de ponta a ponta", "Inclusive para o prestador, que recebe as necessidades do cliente "
                                            "antes do atendimento.")]
y = 1.6
for t, d in difs:
    box(s, 0.6, y, 0.12, 1.0, fill=PRIMARY)
    text(s, 0.9, y - 0.02, 6.0, 0.4, t, size=15, bold=True, color=INK)
    text(s, 0.9, y + 0.38, 6.0, 0.7, d, size=12.5, color=MUTED, spacing=1.0)
    y += 1.3
card(s, 7.3, 1.6, 5.45, 2.55, "Modelo de sustentação", None, fill=PRIMARY_L, line=None, title_color=PRIMARY)
bullets(s, 7.55, 2.2, 5.0, 1.9, [("Gratuito ", "para o idoso e a família."),
                                 ("Assinatura mensal acessível ", "para prestadores (agenda + clientes 60+)."),
                                 ("Parcerias ", "com UBS, prefeituras e operadoras de saúde.")], size=13)
card(s, 7.3, 4.35, 5.45, 2.45, "Viabilidade técnica", None)
bullets(s, 7.55, 4.95, 5.0, 1.9, ["Web responsiva + banco Oracle.",
                                  "IA com serviços de mercado (voz e linguagem) via API.",
                                  "Piloto em um bairro: 50 idosos e 20 prestadores."], size=13)

# --------------------------------------------------------------------------- #
# 26. Referências
# --------------------------------------------------------------------------- #
s = new_slide("Referências", "Fontes")
refs = [
    "IBGE. Censo Demográfico 2022: população por idade e sexo. Rio de Janeiro: IBGE, 2023.",
    "IBGE. PNAD Contínua — Acesso à Internet e à televisão e posse de telefone móvel celular para uso pessoal "
    "2024. Rio de Janeiro: IBGE, 2025.",
    "RAMOS, L. R. et al. Polifarmácia e polimorbidade em idosos no Brasil: um desafio em saúde pública. "
    "Revista de Saúde Pública, v. 50, supl. 2, 9s, 2016 (PNAUM).",
    "WORLD HEALTH ORGANIZATION. Adherence to long-term therapies: evidence for action. Genebra: WHO, 2003.",
    "ONU. Objetivos de Desenvolvimento Sustentável — Agenda 2030 (ODS 3, 10 e 11). Disponível em: "
    "brasil.un.org/pt-br/sdgs.",
    "UN-HABITAT. International Guidelines on People-Centred Smart Cities. Nairóbi: UN-Habitat. Disponível em: unhabitat.org.",
    "BRASIL. Lei nº 13.709/2018 — Lei Geral de Proteção de Dados Pessoais (LGPD).",
    "BRASIL. Lei nº 10.741/2003 — Estatuto da Pessoa Idosa.",
]
bullets(s, 0.6, 1.6, 12.2, 5.2, refs, size=13.5, space_after=9)

# --------------------------------------------------------------------------- #
# 27. Encerramento + vídeo
# --------------------------------------------------------------------------- #
s = new_slide(dark=True)
logo(s, 0.8, 0.8, size=40)
text(s, 0.8, 2.0, 11.5, 1.0, "Obrigado!", size=48, bold=True, color=WHITE)
text(s, 0.8, 3.0, 11.5, 0.6, "Cuidado com autonomia: a tecnologia fala a língua de quem mais precisa.",
     size=20, color=rgb("CDEDE8"))
box(s, 0.8, 3.95, 11.7, 1.35, fill=rgb("0B3F3B"), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
text(s, 1.1, 4.05, 11, 0.4, "▶  VÍDEO PITCH (YOUTUBE)", size=13, bold=True, color=MINT)
link = text(s, 1.1, 4.5, 11, 0.6, VIDEO_URL, size=22, bold=True, color=WHITE)
link.click_action.hyperlink.address = VIDEO_URL  # link no objeto: o texto continua branco
y = 5.75
for nome, rm in INTEGRANTES:
    text(s, 0.8, y, 5, 0.4, nome, size=16, bold=True, color=WHITE)
    text(s, 4.6, y, 2, 0.4, rm, size=16, color=rgb("CDEDE8"))
    y += 0.42

prs.save(OUT)
print("Apresentação gerada:", OUT, "-", len(prs.slides), "slides")
