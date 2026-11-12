# -*- coding: utf-8 -*-
"""Gera as telas (protótipo desktop 1600x900) da plataforma web Cuida+.

Cada função desenha uma tela em coordenadas de pixel (origem no canto
superior esquerdo) e salva um PNG em alta resolução nesta pasta.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Wedge

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900

plt.rcParams["font.family"] = ["Segoe UI", "Segoe UI Symbol", "DejaVu Sans"]

# Paleta (contraste AA para textos sobre fundos claros)
BG = "#F3F6F5"
SIDE = "#0E4F4A"
SIDE_ACTIVE = "#16766E"
PRIMARY = "#0F766E"
PRIMARY_L = "#DDF4EF"
ACCENT = "#B45309"
ACCENT_L = "#FEF3C7"
DANGER = "#B91C1C"
DANGER_L = "#FEE2E2"
OK = "#15803D"
OK_L = "#DCFCE7"
INK = "#1F2937"
MUTED = "#5B6472"
CARD = "#FFFFFF"
BORDER = "#DADFE3"
BLUE = "#1D4ED8"
BLUE_L = "#DBEAFE"


# --------------------------------------------------------------------------- #
# Primitivas
# --------------------------------------------------------------------------- #

def new():
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc=BG, ec="none", zorder=0))
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print("Tela gerada:", path)


def rr(ax, x, y, w, h, fc=CARD, ec=BORDER, r=12, lw=1.2, z=1, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec if ec else "none", lw=lw, zorder=z, ls=ls))


def tx(ax, x, y, s, size=16, color=INK, weight="normal", ha="left", va="center", z=5, **kw):
    # size em "px" do canvas -> pontos (1 px = 0,72 pt nesta figura)
    ax.text(x, y, s, fontsize=size * 0.72, color=color, weight=weight, ha=ha, va=va, zorder=z, **kw)


def button(ax, x, y, w, h, label, fc=PRIMARY, fg="white", size=18, r=10, ec=None, weight="bold", z=3):
    rr(ax, x, y, w, h, fc=fc, ec=ec, r=r, z=z)
    tx(ax, x + w / 2, y + h / 2, label, size=size, color=fg, weight=weight, ha="center", z=z + 1)


def badge(ax, x, y, label, fc, fg, size=13, pad=12, h=26, z=4):
    w = len(label) * size * 0.58 + 2 * pad
    rr(ax, x, y, w, h, fc=fc, ec=None, r=h / 2, z=z)
    tx(ax, x + w / 2, y + h / 2, label, size=size, color=fg, weight="bold", ha="center", z=z + 1)
    return w


def circle(ax, cx, cy, r, fc, ec="none", z=3, lw=1):
    ax.add_patch(Circle((cx, cy), r, fc=fc, ec=ec, zorder=z, lw=lw))


def mic(ax, cx, cy, s=1.0, color="white", z=6):
    """Ícone de microfone desenhado com formas simples."""
    rr(ax, cx - 9 * s, cy - 20 * s, 18 * s, 28 * s, fc=color, ec=None, r=9 * s, z=z)
    ax.add_patch(Wedge((cx, cy + 2 * s), 15 * s, 0, 180, width=3 * s, fc=color, ec="none", zorder=z,
                       transform=ax.transData))
    # o eixo y é invertido: o "arco" de 0-180 graus fica para baixo, como no ícone real
    ax.plot([cx, cx], [cy + 17 * s, cy + 24 * s], color=color, lw=3 * s, zorder=z, solid_capstyle="round")
    ax.plot([cx - 8 * s, cx + 8 * s], [cy + 25 * s, cy + 25 * s], color=color, lw=3 * s, zorder=z,
            solid_capstyle="round")


def avatar(ax, cx, cy, r, initials, fc=PRIMARY_L, fg=PRIMARY):
    circle(ax, cx, cy, r, fc, z=4)
    tx(ax, cx, cy, initials, size=r * 0.8, color=fg, weight="bold", ha="center", z=5)


def logo(ax, x, y, light=True):
    c = "white" if light else PRIMARY
    circle(ax, x + 18, y, 18, "#2DD4BF" if light else PRIMARY, z=4)
    tx(ax, x + 18, y + 1, "+", size=28, color=SIDE if light else "white", weight="bold", ha="center", z=5)
    tx(ax, x + 46, y, "Cuida+", size=28, color=c, weight="bold", z=5)


def sidebar(ax, items, active, role, user, initials):
    ax.add_patch(Rectangle((0, 0), 270, H, fc=SIDE, ec="none", zorder=1))
    logo(ax, 28, 50)
    tx(ax, 30, 92, role.upper(), size=12.5, color="#9FD9D1", weight="bold")
    y = 130
    for icon, label in items:
        if label == active:
            rr(ax, 16, y, 238, 58, fc=SIDE_ACTIVE, ec=None, r=10, z=2)
            ax.add_patch(Rectangle((16, y + 10), 5, 38, fc="#5EEAD4", ec="none", zorder=3))
        tx(ax, 44, y + 29, icon, size=21, color="white", ha="center")
        tx(ax, 68, y + 29, label, size=19, color="white", weight="bold" if label == active else "normal")
        y += 66
    # usuário logado
    ax.plot([24, 246], [H - 100, H - 100], color="#2B6F69", lw=1, zorder=2)
    avatar(ax, 52, H - 52, 24, initials, fc="#CCFBF1", fg=SIDE)
    tx(ax, 86, H - 62, user, size=16, color="white", weight="bold")
    tx(ax, 86, H - 39, "Sair", size=14, color="#9FD9D1")


def topbar(ax, title, subtitle=None):
    ax.add_patch(Rectangle((270, 0), W - 270, 84, fc=CARD, ec="none", zorder=1))
    ax.plot([270, W], [84, 84], color=BORDER, lw=1, zorder=2)
    tx(ax, 306, 34 if subtitle else 42, title, size=26, weight="bold")
    if subtitle:
        tx(ax, 306, 62, subtitle, size=15, color=MUTED)
    # barra de acessibilidade (presente em todas as telas)
    x = W - 452
    for label, w in [("A−", 46), ("A+", 46), ("◐  Alto contraste", 168), ("🔊  Ouvir tela", 140)]:
        rr(ax, x, 24, w, 38, fc=BG, ec=BORDER, r=8, z=2)
        tx(ax, x + w / 2, 43, label, size=14.5, color=INK, weight="bold", ha="center")
        x += w + 8


def card(ax, x, y, w, h, title=None, action=None, z=1):
    rr(ax, x, y, w, h, fc=CARD, ec=BORDER, r=14, z=z)
    if title:
        tx(ax, x + 24, y + 34, title, size=20, weight="bold", z=z + 3)
    if action:
        tx(ax, x + w - 24, y + 34, action, size=15, color=PRIMARY, weight="bold", ha="right", z=z + 3)


def annotate(ax, n, x, y):
    """Marcador numerado usado na legenda das telas (fluxo de interação)."""
    circle(ax, x, y, 15, ACCENT, ec="white", z=9, lw=2)
    tx(ax, x, y + 1, str(n), size=15, color="white", weight="bold", ha="center", z=10)


IDOSO_NAV = [("⌂", "Início"), ("✚", "Meus remédios"), ("▦", "Compromissos"),
             ("☏", "Marcar horário"), ("♥", "Minha família")]
CUIDADOR_NAV = [("⌂", "Painel"), ("✚", "Medicamentos"), ("▦", "Agenda da Maria"),
                ("⚠", "Alertas"), ("⚙", "Configurações")]
PREST_NAV = [("▦", "Agenda"), ("✉", "Solicitações"), ("✂", "Serviços"),
             ("◷", "Disponibilidade"), ("★", "Avaliações")]


# --------------------------------------------------------------------------- #
# Telas
# --------------------------------------------------------------------------- #

def tela_01_acesso():
    fig, ax = new()
    # faixa esquerda institucional
    ax.add_patch(Rectangle((0, 0), 620, H, fc=SIDE, ec="none", zorder=1))
    logo(ax, 70, 110)
    tx(ax, 70, 210, "Cuidado, lembretes e\nagendamentos em um\nsó lugar.", size=40, color="white",
       weight="bold", va="top", linespacing=1.25)
    tx(ax, 70, 430, "A Cuida+ conversa com você, lembra a hora\ndos remédios e marca horários com médicos,\n"
       "salões e comércios do seu bairro.", size=19, color="#CDEDE8", va="top", linespacing=1.5)
    for i, (ic, t) in enumerate([("🔊", "Funciona por voz"), ("🔒", "Dados protegidos (LGPD)"),
                                 ("♥", "Família sempre informada")]):
        yy = 600 + i * 54
        circle(ax, 92, yy, 20, "#16766E", z=3)
        tx(ax, 92, yy, ic, size=17, color="white", ha="center")
        tx(ax, 126, yy, t, size=19, color="white", weight="bold")

    # área de escolha de perfil
    rr(ax, W - 452, 24, 46, 38, fc=CARD, ec=BORDER, r=8, z=2)
    x = W - 452
    for label, w in [("A−", 46), ("A+", 46), ("◐  Alto contraste", 168), ("🔊  Ouvir tela", 140)]:
        rr(ax, x, 24, w, 38, fc=CARD, ec=BORDER, r=8, z=2)
        tx(ax, x + w / 2, 43, label, size=14.5, weight="bold", ha="center")
        x += w + 8

    tx(ax, 700, 140, "Olá! Quem está acessando?", size=36, weight="bold")
    tx(ax, 700, 186, "Escolha uma opção. Você também pode dizer em voz alta: “Sou a Maria”.", size=19, color=MUTED)

    perfis = [
        ("☺", "Sou idoso(a)", "Entrar com meu telefone e um código\nenviado por SMS ou WhatsApp.", PRIMARY, PRIMARY_L),
        ("♥", "Sou familiar ou cuidador", "Acompanhar remédios, compromissos\ne receber alertas.", BLUE, BLUE_L),
        ("✂", "Sou prestador de serviço", "Médicos, clínicas, salões e comércios:\npublique sua agenda.", ACCENT, ACCENT_L),
    ]
    y = 240
    for i, (ic, t, d, c, cl) in enumerate(perfis):
        sel = i == 0
        rr(ax, 700, y, 820, 150, fc=CARD, ec=c if sel else BORDER, r=16, lw=3 if sel else 1.2, z=2)
        circle(ax, 778, y + 75, 46, cl, z=3)
        tx(ax, 778, y + 75, ic, size=40, color=c, ha="center", weight="bold")
        tx(ax, 850, y + 52, t, size=28, weight="bold")
        tx(ax, 850, y + 100, d, size=17.5, color=MUTED, linespacing=1.35)
        tx(ax, 1480, y + 75, "›", size=54, color=c, ha="center", weight="bold")
        y += 172
    annotate(ax, 1, 700, 240)
    rr(ax, 700, 768, 820, 70, fc=PRIMARY_L, ec=None, r=14, z=2)
    mic(ax, 748, 800, 0.9, PRIMARY)
    tx(ax, 790, 803, "Prefere falar? Toque aqui e diga quem você é — a Cuida+ te guia pela voz.",
       size=18, color=PRIMARY, weight="bold")
    save(fig, "tela_01_acesso.png")


def tela_02_inicio_idoso():
    fig, ax = new()
    sidebar(ax, IDOSO_NAV, "Início", "Área do idoso", "Maria Aparecida", "MA")
    topbar(ax, "Bom dia, Dona Maria!", "Quinta-feira, 12 de novembro  ·  São Paulo, 24 °C")

    # botão principal de voz
    rr(ax, 306, 112, 1258, 150, fc=PRIMARY, ec=None, r=18, z=1)
    circle(ax, 400, 187, 54, "#15958B", z=2)
    circle(ax, 400, 187, 40, "white", z=3)
    mic(ax, 400, 190, 1.05, PRIMARY)
    tx(ax, 480, 160, "Falar com a Cuida", size=34, color="white", weight="bold")
    tx(ax, 480, 210, "Toque no botão e peça, por exemplo: “marque um corte de cabelo na terça de manhã”.",
       size=18.5, color="#D5F5EF")
    annotate(ax, 1, 306, 112)

    # remédios de hoje
    card(ax, 306, 290, 640, 580, "Remédios de hoje", "Ver todos ›")
    remedios = [
        ("08:00", "Losartana 50 mg", "1 comprimido em jejum", "tomou", "Tomei às 08:05"),
        ("12:30", "Metformina 850 mg", "1 comprimido após o almoço", "agora", None),
        ("20:00", "Sinvastatina 20 mg", "1 comprimido à noite", "depois", "Às 20:00"),
        ("22:00", "Colírio Timolol", "1 gota em cada olho", "depois", "Às 22:00"),
    ]
    y = 350
    for hora, nome, inst, st, info in remedios:
        fc = {"tomou": OK_L, "agora": ACCENT_L, "depois": CARD}[st]
        ec = {"tomou": "#86EFAC", "agora": "#F59E0B", "depois": BORDER}[st]
        rr(ax, 326, y, 600, 112, fc=fc, ec=ec, r=12, lw=2 if st == "agora" else 1.2, z=2)
        tx(ax, 348, y + 38, hora, size=26, weight="bold")
        tx(ax, 460, y + 38, nome, size=21, weight="bold")
        tx(ax, 460, y + 76, inst, size=16.5, color=MUTED)
        if st == "tomou":
            tx(ax, 906, y + 38, "✓  " + info, size=16, color=OK, weight="bold", ha="right")
        elif st == "agora":
            button(ax, 742, y + 52, 168, 46, "✓  Já tomei", fc=OK, size=18)
            tx(ax, 906, y + 30, "É agora!", size=16, color=ACCENT, weight="bold", ha="right")
        else:
            tx(ax, 906, y + 38, info, size=16, color=MUTED, ha="right")
        y += 126
    annotate(ax, 2, 326, 476)

    # compromissos
    card(ax, 970, 290, 594, 400, "Próximos compromissos", "Ver agenda ›")
    comps = [
        ("SEX", "13", "10:00", "Consulta — Cardiologista", "Dra. Ana Lima · Clínica Vida", "Confirmado", OK, OK_L),
        ("TER", "17", "09:30", "Corte de cabelo", "Salão Bela Vida · 800 m de casa", "Confirmado", OK, OK_L),
        ("QUI", "19", "15:00", "Entrega da farmácia", "Drogaria Bem Estar · em casa", "Aguardando", ACCENT, ACCENT_L),
    ]
    y = 346
    for dia, num, hora, t, d, st, c, cl in comps:
        rr(ax, 990, y, 80, 92, fc=PRIMARY_L, ec=None, r=10, z=2)
        tx(ax, 1030, y + 28, dia, size=15, color=PRIMARY, weight="bold", ha="center")
        tx(ax, 1030, y + 62, num, size=30, color=PRIMARY, weight="bold", ha="center")
        tx(ax, 1090, y + 22, hora + "  ·  " + t, size=18.5, weight="bold")
        tx(ax, 1090, y + 52, d, size=16, color=MUTED)
        badge(ax, 1090, y + 66, st, cl, c, size=12.5)
        y += 110
    # ajuda / família
    rr(ax, 970, 712, 594, 158, fc=BLUE_L, ec=None, r=14, z=1)
    tx(ax, 994, 750, "♥  Sua filha Carla acompanha sua rotina", size=19, color=BLUE, weight="bold")
    tx(ax, 994, 786, "Ela recebe um aviso se algum remédio for esquecido.", size=16, color=INK)
    button(ax, 994, 812, 250, 44, "☏  Ligar para Carla", fc=BLUE, size=17)
    button(ax, 1260, 812, 280, 44, "Pedir ajuda agora", fc=DANGER, size=17)
    save(fig, "tela_02_inicio_idoso.png")


def tela_03_assistente():
    fig, ax = new()
    sidebar(ax, IDOSO_NAV, "Marcar horário", "Área do idoso", "Maria Aparecida", "MA")
    topbar(ax, "Conversa com a Cuida", "Assistente de voz · você fala, a Cuida entende e marca para você")

    # área da conversa
    card(ax, 306, 110, 860, 760)

    def bubble(y, text, me, h=None, w=None):
        lines = text.count("\n") + 1
        h = h or 20 + lines * 28
        w = w or 520
        x = 1146 - w if me else 326
        rr(ax, x, y, w, h, fc=PRIMARY if me else BG, ec=None, r=16, z=2)
        tx(ax, x + 22, y + h / 2, text, size=19, color="white" if me else INK, linespacing=1.4)
        return y + h + 16

    tx(ax, 736, 138, "Hoje, 09:12", size=14, color=MUTED, ha="center")
    y = bubble(158, "🔊  “Quero cortar o cabelo terça\nde manhã, perto de casa.”", True, w=430)
    y = bubble(y, "Claro, Dona Maria! Encontrei 2 horários\nna terça-feira (17/11) pela manhã:", False, w=470)
    # opções
    opts = [("1", "Salão Bela Vida", "Terça 17/11 · 09:30", "800 m de casa · R$ 45,00 · ★ 4,8", True),
            ("2", "Studio Cabelo & Cia", "Terça 17/11 · 10:30", "1,2 km · R$ 50,00 · atende em casa", False)]
    for n, nome, quando, det, sel in opts:
        rr(ax, 326, y, 600, 84, fc=CARD, ec=PRIMARY if sel else BORDER, r=12, lw=2.5 if sel else 1.2, z=2)
        circle(ax, 368, y + 42, 22, PRIMARY if sel else PRIMARY_L, z=3)
        tx(ax, 368, y + 42, n, size=22, color="white" if sel else PRIMARY, weight="bold", ha="center")
        tx(ax, 408, y + 27, f"{nome}  —  {quando}", size=19, weight="bold")
        tx(ax, 408, y + 59, det, size=16, color=MUTED)
        y += 94
    annotate(ax, 1, 326, 342)
    y = bubble(y + 2, "🔊  “Pode ser o primeiro.”", True, w=330)
    # confirmação
    rr(ax, 326, y, 640, 140, fc=ACCENT_L, ec="#F59E0B", r=14, lw=2, z=2)
    tx(ax, 350, y + 30, "Posso confirmar?", size=20, color=ACCENT, weight="bold")
    tx(ax, 350, y + 64, "Corte de cabelo no Salão Bela Vida, terça, 17/11, às 09:30.", size=18)
    button(ax, 350, y + 86, 220, 42, "✓  Sim, pode marcar", fc=OK, size=17)
    button(ax, 584, y + 86, 170, 42, "Outro horário", fc=CARD, fg=INK, ec=BORDER, size=17)
    annotate(ax, 2, 326, y)

    # barra de entrada por voz
    rr(ax, 326, 800, 820, 54, fc=BG, ec=BORDER, r=27, z=2)
    tx(ax, 356, 827, "Fale ou digite sua mensagem…", size=17, color=MUTED)
    circle(ax, 1112, 827, 24, PRIMARY, z=3)
    mic(ax, 1112, 829, 0.62, "white")

    # painel "o que a IA entendeu" (transparência)
    card(ax, 1190, 110, 374, 470, "O que a Cuida entendeu")
    tx(ax, 1214, 168, "Transparência: você vê o que foi\ncompreendido antes de confirmar.", size=14.5,
       color=MUTED, va="top", linespacing=1.4)
    campos = [("Pedido", "Agendar serviço"), ("Serviço", "Corte de cabelo"), ("Dia", "Terça-feira, 17/11"),
              ("Período", "Manhã (08h–12h)"), ("Preferência", "Perto de casa (≤ 2 km)"),
              ("Confiança", "94%")]
    y = 236
    for k, v in campos:
        tx(ax, 1214, y, k, size=14.5, color=MUTED)
        tx(ax, 1214, y + 26, v, size=18, weight="bold")
        y += 56
    annotate(ax, 3, 1190, 110)
    card(ax, 1190, 600, 374, 270, "Depois de marcar")
    for i, t in enumerate(["✓  Lembrete 1 dia antes", "✓  Lembrete 1 hora antes", "✓  Aviso para a Carla",
                           "✓  Salão recebe o pedido"]):
        tx(ax, 1214, 662 + i * 46, t, size=18, color=OK, weight="bold")
    save(fig, "tela_03_assistente_ia.png")


def tela_04_confirmacao():
    fig, ax = new()
    sidebar(ax, IDOSO_NAV, "Compromissos", "Área do idoso", "Maria Aparecida", "MA")
    topbar(ax, "Horário marcado!", "Agendamento confirmado pelo prestador")
    card(ax, 430, 120, 1010, 740)
    circle(ax, 935, 230, 70, OK_L, z=3)
    circle(ax, 935, 230, 50, OK, z=4)
    tx(ax, 935, 232, "✓", size=58, color="white", weight="bold", ha="center")
    tx(ax, 935, 345, "Pronto, Dona Maria! Seu horário está marcado.", size=32, weight="bold", ha="center")
    tx(ax, 935, 390, "O Salão Bela Vida confirmou o seu pedido.", size=20, color=MUTED, ha="center")

    rr(ax, 520, 430, 830, 210, fc=BG, ec=None, r=14, z=2)
    info = [("✂", "Serviço", "Corte de cabelo feminino (40 min)"),
            ("▦", "Quando", "Terça-feira, 17 de novembro, às 09:30"),
            ("⌖", "Onde", "Salão Bela Vida — Rua das Flores, 120 (800 m)"),
            ("$", "Valor", "R$ 45,00 — pagamento no local")]
    y = 466
    for ic, k, v in info:
        tx(ax, 560, y, ic, size=22, color=PRIMARY, ha="center", weight="bold")
        tx(ax, 596, y, k, size=17, color=MUTED)
        tx(ax, 720, y, v, size=20, weight="bold")
        y += 46

    rr(ax, 520, 660, 830, 78, fc=PRIMARY_L, ec=None, r=14, z=2)
    tx(ax, 548, 686, "⏰  Vou te lembrar na segunda às 18h e na terça às 08:30.", size=18.5, color=PRIMARY,
       weight="bold")
    tx(ax, 548, 716, "♥  Sua filha Carla também foi avisada.", size=18.5, color=PRIMARY, weight="bold")
    button(ax, 520, 766, 260, 60, "Ver meus compromissos", fc=PRIMARY, size=18)
    button(ax, 796, 766, 230, 60, "⌖  Como chegar", fc=CARD, fg=INK, ec=BORDER, size=18)
    button(ax, 1042, 766, 308, 60, "Cancelar ou remarcar", fc=CARD, fg=DANGER, ec=BORDER, size=18)
    annotate(ax, 1, 520, 660)
    save(fig, "tela_04_confirmacao.png")


def tela_05_lembrete():
    fig, ax = new()
    sidebar(ax, IDOSO_NAV, "Meus remédios", "Área do idoso", "Maria Aparecida", "MA")
    topbar(ax, "Meus remédios", "Lembrete em tela cheia com som e voz")
    # fundo esmaecido
    ax.add_patch(Rectangle((270, 84), W - 270, H - 84, fc="#0B1F1D", alpha=0.55, ec="none", zorder=6))
    # modal
    rr(ax, 470, 130, 930, 700, fc=CARD, ec=None, r=24, z=7)
    rr(ax, 470, 130, 930, 120, fc=ACCENT_L, ec=None, r=24, z=7)
    ax.add_patch(Rectangle((470, 210), 930, 40, fc=ACCENT_L, ec="none", zorder=7))
    tx(ax, 935, 192, "⏰  Hora do remédio, Dona Maria!", size=36, color=ACCENT, weight="bold", ha="center", z=8)
    # pílula
    rr(ax, 560, 300, 150, 66, fc="#FDE68A", ec="#B45309", r=33, lw=2, z=8)
    ax.add_patch(Rectangle((635, 302), 2, 62, fc="#B45309", ec="none", zorder=9))
    tx(ax, 760, 300, "Metformina 850 mg", size=34, weight="bold", va="top", z=8)
    tx(ax, 760, 352, "1 comprimido  ·  depois do almoço  ·  12:30", size=21, color=MUTED, va="top", z=8)
    rr(ax, 560, 410, 750, 66, fc=BLUE_L, ec=None, r=12, z=8)
    tx(ax, 588, 443, "🔊  Você também pode responder falando: “já tomei” ou “me lembre depois”.",
       size=17.5, color=BLUE, weight="bold", z=8)
    button(ax, 560, 510, 750, 92, "✓   Já tomei", fc=OK, size=32, r=16, z=8)
    button(ax, 560, 620, 368, 76, "⏰  Lembrar em 15 min", fc=CARD, fg=INK, ec=BORDER, size=21, r=14, z=8)
    button(ax, 942, 620, 368, 76, "✕  Não vou tomar", fc=CARD, fg=DANGER, ec=BORDER, size=21, r=14, z=8)
    tx(ax, 935, 750, "Se não houver resposta em 30 minutos, a Cuida liga para você\ne, depois, avisa a Carla.",
       size=16.5, color=MUTED, ha="center", z=8, linespacing=1.4)
    annotate(ax, 1, 560, 510)
    save(fig, "tela_05_lembrete_remedio.png")


def tela_06_cuidador():
    fig, ax = new()
    sidebar(ax, CUIDADOR_NAV, "Painel", "Área da família", "Carla Souza", "CS")
    topbar(ax, "Acompanhando: Maria Aparecida, 74 anos", "Atualizado agora · últimos 7 dias")

    kpis = [("Adesão aos remédios", "89%", "▲ 4 p.p. vs semana anterior", OK),
            ("Doses esquecidas", "3", "todas no horário das 20:00", DANGER),
            ("Compromissos na semana", "3", "2 confirmados · 1 aguardando", PRIMARY),
            ("Conversas com a Cuida", "17", "5 agendamentos por voz", BLUE)]
    x = 306
    for t, v, d, c in kpis:
        card(ax, x, 108, 302, 148)
        tx(ax, x + 22, 140, t, size=16, color=MUTED)
        tx(ax, x + 22, 190, v, size=44, color=c, weight="bold")
        tx(ax, x + 22, 234, d, size=14, color=MUTED)
        x += 318

    # gráfico de adesão por dia
    card(ax, 306, 278, 700, 330, "Doses tomadas por dia")
    dias = ["Qui", "Sex", "Sáb", "Dom", "Seg", "Ter", "Qua"]
    tomadas = [4, 3, 4, 4, 3, 4, 3]
    total = 4
    base, top = 560, 380
    for i, (d, t) in enumerate(zip(dias, tomadas)):
        bx = 350 + i * 92
        rr(ax, bx, top, 52, base - top, fc="#EEF2F2", ec=None, r=6, z=2)
        h = (base - top) * t / total
        rr(ax, bx, base - h, 52, h, fc=OK if t == total else "#F59E0B", ec=None, r=6, z=3)
        tx(ax, bx + 26, base - h - 14, f"{t}/4", size=14, weight="bold", ha="center")
        tx(ax, bx + 26, base + 22, d, size=15, color=MUTED, ha="center")
    rr(ax, 700, 305, 14, 14, fc=OK, ec=None, r=3, z=3)
    tx(ax, 722, 312, "Todas as doses", size=14, color=MUTED)
    rr(ax, 836, 305, 14, 14, fc="#F59E0B", ec=None, r=3, z=3)
    tx(ax, 858, 312, "Alguma esquecida", size=14, color=MUTED)

    # alerta da IA
    card(ax, 1030, 278, 534, 330)
    rr(ax, 1030, 278, 534, 64, fc=DANGER_L, ec=None, r=14, z=2)
    ax.add_patch(Rectangle((1030, 320), 534, 22, fc=DANGER_L, ec="none", zorder=2))
    tx(ax, 1054, 310, "⚠  Alerta inteligente da Cuida", size=20, color=DANGER, weight="bold")
    badge(ax, 1410, 297, "Risco: 0,72", "white", DANGER, size=13)
    tx(ax, 1054, 362, "Padrão identificado:", size=16, color=MUTED, va="top")
    tx(ax, 1054, 390, "3 das últimas 5 doses das 20:00 (Sinvastatina)\nforam esquecidas — sempre em dias com\n"
       "consulta ou saída de casa à tarde.", size=17, va="top", linespacing=1.4)
    tx(ax, 1054, 488, "Sugestões:", size=16, color=MUTED, va="top")
    button(ax, 1054, 520, 236, 44, "Mudar para 19:30", fc=PRIMARY, size=16)
    button(ax, 1302, 520, 238, 44, "☏  Ligar para mãe", fc=CARD, fg=INK, ec=BORDER, size=16)
    annotate(ax, 1, 1030, 278)

    # histórico recente
    card(ax, 306, 630, 1258, 240, "Atividade recente", "Ver histórico completo ›")
    rows = [("Hoje 12:31", "✓ Metformina 850 mg tomada (confirmação por voz)", OK),
            ("Hoje 09:14", "▦ Corte de cabelo marcado pela assistente — Salão Bela Vida, 17/11 09:30", PRIMARY),
            ("Ontem 20:32", "✕ Sinvastatina 20 mg não confirmada — ligação automática sem resposta", DANGER),
            ("Ontem 08:05", "✓ Losartana 50 mg tomada (botão “Já tomei”)", OK)]
    y = 690
    for t, d, c in rows:
        tx(ax, 330, y, t, size=15.5, color=MUTED)
        tx(ax, 480, y, d, size=17, color=c, weight="bold")
        ax.plot([330, 1540], [y + 22, y + 22], color="#EEF0F2", lw=1, zorder=2)
        y += 44
    save(fig, "tela_06_painel_familia.png")


def tela_07_cadastro_medicamento():
    fig, ax = new()
    sidebar(ax, CUIDADOR_NAV, "Medicamentos", "Área da família", "Carla Souza", "CS")
    topbar(ax, "Novo medicamento", "Para: Maria Aparecida")
    card(ax, 306, 108, 840, 762)

    def field(x, y, w, label, value, hint=None):
        tx(ax, x, y, label, size=16, weight="bold")
        rr(ax, x, y + 18, w, 52, fc=CARD, ec=BORDER, r=8, z=2)
        tx(ax, x + 16, y + 44, value, size=18)
        if hint:
            tx(ax, x, y + 88, hint, size=14, color=MUTED)

    field(338, 150, 500, "Nome do medicamento *", "Sinvastatina")
    field(860, 150, 254, "Dosagem *", "20 mg")
    field(338, 260, 776, "Instrução para a Dona Maria (a Cuida lê em voz alta)",
          "1 comprimido à noite, com água", "Use frases curtas e simples.")
    tx(ax, 338, 392, "Horários *", size=16, weight="bold")
    x = 338
    for h in ["20:00"]:
        rr(ax, x, 410, 120, 50, fc=PRIMARY_L, ec=PRIMARY, r=25, z=2, lw=1.5)
        tx(ax, x + 60, 435, h + "  ✕", size=17, color=PRIMARY, weight="bold", ha="center")
        x += 132
    rr(ax, x, 410, 190, 50, fc=CARD, ec=BORDER, r=25, z=2, ls="--")
    tx(ax, x + 95, 435, "+ Adicionar horário", size=16, color=PRIMARY, weight="bold", ha="center")

    tx(ax, 338, 498, "Dias da semana", size=16, weight="bold")
    x = 338
    for d in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]:
        rr(ax, x, 516, 90, 48, fc=PRIMARY, ec=None, r=10, z=2)
        tx(ax, x + 45, 540, d, size=16, color="white", weight="bold", ha="center")
        x += 100
    field(338, 600, 370, "Início do tratamento *", "12/11/2026")
    field(744, 600, 370, "Término (opcional)", "Uso contínuo")
    button(ax, 338, 790, 260, 56, "Salvar medicamento", fc=PRIMARY, size=18)
    button(ax, 614, 790, 160, 56, "Cancelar", fc=CARD, fg=INK, ec=BORDER, size=18)
    annotate(ax, 1, 318, 435)

    # pré-visualização do lembrete
    card(ax, 1170, 108, 394, 470, "Como a Dona Maria verá")
    rr(ax, 1194, 170, 346, 230, fc=ACCENT_L, ec="#F59E0B", r=14, z=2)
    tx(ax, 1367, 204, "⏰  Hora do remédio!", size=20, color=ACCENT, weight="bold", ha="center")
    tx(ax, 1367, 246, "Sinvastatina 20 mg", size=22, weight="bold", ha="center")
    tx(ax, 1367, 280, "1 comprimido à noite, com água", size=15, color=MUTED, ha="center")
    button(ax, 1218, 312, 298, 62, "✓  Já tomei", fc=OK, size=22, r=12)
    tx(ax, 1194, 432, "Se não confirmar:", size=16, weight="bold")
    for i, t in enumerate(["30 min → a Cuida liga para ela", "60 min → você recebe um alerta",
                           "Padrões são analisados pela IA"]):
        tx(ax, 1194, 470 + i * 34, "•  " + t, size=15.5, color=MUTED)
    card(ax, 1170, 600, 394, 270, "Medicamentos ativos")
    for i, (n, h) in enumerate([("Losartana 50 mg", "08:00"), ("Metformina 850 mg", "12:30"),
                                ("Colírio Timolol", "22:00")]):
        yy = 664 + i * 62
        tx(ax, 1194, yy, n, size=17, weight="bold")
        badge(ax, 1460, yy - 13, h, PRIMARY_L, PRIMARY, size=13)
        ax.plot([1194, 1540], [yy + 30, yy + 30], color="#EEF0F2", lw=1, zorder=2)
    save(fig, "tela_07_cadastro_medicamento.png")


def tela_08_prestador_agenda():
    fig, ax = new()
    sidebar(ax, PREST_NAV, "Agenda", "Área do prestador", "Salão Bela Vida", "BV")
    topbar(ax, "Agenda da semana", "16 a 21 de novembro  ·  Salão Bela Vida")

    # calendário semanal
    card(ax, 306, 108, 860, 762)
    dias = ["Seg 16", "Ter 17", "Qua 18", "Qui 19", "Sex 20", "Sáb 21"]
    horas = ["08:00", "09:30", "11:00", "13:30", "15:00", "16:30"]
    gx, gy, cw, ch = 400, 170, 124, 108
    for i, d in enumerate(dias):
        tx(ax, gx + i * cw + cw / 2, 140, d, size=16, weight="bold", ha="center",
           color=PRIMARY if d == "Ter 17" else INK)
    grid = {
        (1, 1): ("R", "Maria A.", "via voz"),
        (0, 0): ("R", "João P.", ""), (2, 2): ("R", "Lúcia M.", ""), (4, 1): ("R", "Rosa T.", ""),
        (3, 3): ("B", "Bloqueado", ""), (5, 0): ("R", "Ana C.", ""), (5, 1): ("R", "Célia R.", ""),
        (1, 4): ("P", "Pendente", "Sr. Antônio"),
    }
    for r, h in enumerate(horas):
        tx(ax, 380, gy + r * ch + 22, h, size=14.5, color=MUTED, ha="right")
        for c in range(len(dias)):
            x0, y0 = gx + c * cw + 4, gy + r * ch + 4
            st = grid.get((c, r))
            if st is None:
                rr(ax, x0, y0, cw - 8, ch - 8, fc="#F6FBFA", ec="#CDE7E2", r=8, z=2, ls="--")
                tx(ax, x0 + (cw - 8) / 2, y0 + (ch - 8) / 2, "Livre", size=14, color="#5E9E95", ha="center")
            else:
                k, a, b = st
                fc, ec, fg = {"R": (PRIMARY_L, PRIMARY, PRIMARY), "B": ("#EEF0F2", "#C9CED4", MUTED),
                              "P": (ACCENT_L, "#F59E0B", ACCENT)}[k]
                rr(ax, x0, y0, cw - 8, ch - 8, fc=fc, ec=ec, r=8, z=2, lw=2 if (c, r) == (1, 1) else 1.2)
                tx(ax, x0 + 10, y0 + 26, a, size=15, color=fg, weight="bold")
                if b:
                    tx(ax, x0 + 10, y0 + 54, b, size=13.5, color=fg)
    annotate(ax, 2, gx + cw + 4, gy + ch + 4)
    # legenda
    lx = 400
    for lab, fc, ec in [("Reservado", PRIMARY_L, PRIMARY), ("Pendente", ACCENT_L, "#F59E0B"),
                        ("Livre", "#F6FBFA", "#CDE7E2"), ("Bloqueado", "#EEF0F2", "#C9CED4")]:
        rr(ax, lx, 832, 18, 18, fc=fc, ec=ec, r=4, z=2)
        tx(ax, lx + 26, 841, lab, size=14, color=MUTED)
        lx += 150

    # solicitações pendentes
    card(ax, 1190, 108, 374, 450, "Novas solicitações", "1 pendente")
    rr(ax, 1210, 166, 334, 372, fc=ACCENT_L, ec="#F59E0B", r=12, z=2)
    avatar(ax, 1248, 206, 24, "AS", fc="white", fg=ACCENT)
    tx(ax, 1284, 196, "Antônio Silva, 81", size=17, weight="bold")
    tx(ax, 1284, 222, "Pedido pela assistente de voz", size=13.5, color=MUTED)
    for i, (k, v) in enumerate([("Serviço", "Corte masculino (30 min)"), ("Quando", "Ter 17/11 · 15:00"),
                                ("Obs.", "Usa andador — precisa de\nacesso sem degraus")]):
        tx(ax, 1230, 266 + i * 50, k, size=14, color=MUTED, va="top")
        tx(ax, 1310, 266 + i * 50, v, size=15.5, weight="bold", va="top", linespacing=1.3)
    rr(ax, 1230, 410, 294, 50, fc="white", ec=None, r=8, z=3)
    tx(ax, 1244, 435, "♿  Dica de atendimento: fale devagar\n     e confirme o horário em voz alta.", size=12.5,
       color=BLUE, z=4, linespacing=1.3)
    button(ax, 1230, 474, 140, 46, "✓ Confirmar", fc=OK, size=16)
    button(ax, 1384, 474, 140, 46, "Recusar", fc=CARD, fg=DANGER, ec=BORDER, size=16)
    annotate(ax, 1, 1190, 108)

    card(ax, 1190, 580, 374, 290, "Resumo do mês")
    for i, (k, v, c) in enumerate([("Agendamentos pela Cuida+", "38", PRIMARY),
                                   ("Comparecimento", "95%", OK),
                                   ("Novos clientes 60+", "12", BLUE)]):
        yy = 650 + i * 70
        tx(ax, 1214, yy, k, size=16, color=MUTED)
        tx(ax, 1540, yy, v, size=30, color=c, weight="bold", ha="right")
    save(fig, "tela_08_agenda_prestador.png")


def tela_09_prestador_servicos():
    fig, ax = new()
    sidebar(ax, PREST_NAV, "Disponibilidade", "Área do prestador", "Salão Bela Vida", "BV")
    topbar(ax, "Serviços e disponibilidade", "O que você oferece e quando a Cuida+ pode marcar")

    card(ax, 306, 108, 1258, 330, "Meus serviços", "+ Novo serviço")
    cols = [("Serviço", 330), ("Duração", 760), ("Preço", 900), ("Atende em casa", 1040), ("Ativo", 1250),
            ("", 1420)]
    for c, x in cols:
        tx(ax, x, 180, c, size=15, color=MUTED, weight="bold")
    ax.plot([330, 1540], [200, 200], color=BORDER, lw=1, zorder=2)
    servs = [("Corte feminino", "40 min", "R$ 45,00", False, True),
             ("Corte masculino", "30 min", "R$ 35,00", True, True),
             ("Escova", "45 min", "R$ 50,00", False, True),
             ("Coloração", "90 min", "R$ 120,00", False, False)]
    y = 236
    for n, d, p, casa, ativo in servs:
        tx(ax, 330, y, n, size=18, weight="bold")
        tx(ax, 760, y, d, size=17)
        tx(ax, 900, y, p, size=17)
        for xx, on in [(1040, casa), (1250, ativo)]:
            rr(ax, xx, y - 14, 54, 28, fc=PRIMARY if on else "#C9CED4", ec=None, r=14, z=2)
            circle(ax, xx + (40 if on else 14), y, 11, "white", z=3)
        tx(ax, 1420, y, "Editar", size=16, color=PRIMARY, weight="bold")
        ax.plot([330, 1540], [y + 26, y + 26], color="#EEF0F2", lw=1, zorder=2)
        y += 52
    annotate(ax, 1, 306, 108)

    card(ax, 306, 460, 830, 410, "Horário de atendimento")
    dias = [("Segunda", "08:00 – 18:00", True), ("Terça", "08:00 – 18:00", True),
            ("Quarta", "08:00 – 18:00", True), ("Quinta", "08:00 – 12:00", True),
            ("Sexta", "08:00 – 18:00", True), ("Sábado", "08:00 – 14:00", True), ("Domingo", "Fechado", False)]
    y = 548
    for d, h, on in dias:
        rr(ax, 330, y - 14, 54, 28, fc=PRIMARY if on else "#C9CED4", ec=None, r=14, z=2)
        circle(ax, 330 + (40 if on else 14), y, 11, "white", z=3)
        tx(ax, 404, y, d, size=17, weight="bold")
        rr(ax, 560, y - 20, 220, 40, fc=BG if on else CARD, ec=BORDER, r=8, z=2)
        tx(ax, 580, y, h, size=16, color=INK if on else MUTED)
        y += 45
    tx(ax, 830, 524, "Intervalo entre atendimentos", size=15, color=MUTED)
    rr(ax, 830, 544, 280, 44, fc=BG, ec=BORDER, r=8, z=2)
    tx(ax, 848, 566, "10 minutos", size=16)
    tx(ax, 830, 618, "Antecedência mínima", size=15, color=MUTED)
    rr(ax, 830, 638, 280, 44, fc=BG, ec=BORDER, r=8, z=2)
    tx(ax, 848, 660, "2 horas", size=16)
    button(ax, 830, 790, 280, 52, "Salvar e publicar agenda", fc=PRIMARY, size=17)
    annotate(ax, 2, 306, 460)

    card(ax, 1160, 460, 404, 410, "Preferências de atendimento")
    prefs = [("Aceitar agendamento pela IA", True), ("Confirmar automaticamente", False),
             ("Receber observações de\nacessibilidade", True), ("Avisar por WhatsApp", True)]
    y = 530
    for t, on in prefs:
        tx(ax, 1184, y, t, size=16.5, linespacing=1.3)
        rr(ax, 1486, y - 14, 54, 28, fc=PRIMARY if on else "#C9CED4", ec=None, r=14, z=2)
        circle(ax, 1486 + (40 if on else 14), y, 11, "white", z=3)
        y += 70
    rr(ax, 1184, 790, 356, 58, fc=BLUE_L, ec=None, r=10, z=2)
    tx(ax, 1200, 819, "♿  Acesso sem degraus declarado", size=15.5, color=BLUE, weight="bold")
    save(fig, "tela_09_servicos_prestador.png")


def main():
    tela_01_acesso()
    tela_02_inicio_idoso()
    tela_03_assistente()
    tela_04_confirmacao()
    tela_05_lembrete()
    tela_06_cuidador()
    tela_07_cadastro_medicamento()
    tela_08_prestador_agenda()
    tela_09_prestador_servicos()


if __name__ == "__main__":
    main()
