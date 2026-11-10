# -*- coding: utf-8 -*-
"""Gera 6 telas desktop de referência (FinControl) e PDF só com imagens."""

from __future__ import annotations

import os
from typing import Literal

import matplotlib.pyplot as plt
from fpdf import FPDF
from matplotlib.patches import FancyBboxPatch, Rectangle

OUTPUT_DIR = r"C:\Users\wfix_\OneDrive\Documentos\Automation\FIAP\FIAP"
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "RM576183_Atividade_Telas_FinControl_REFERENCIA.pdf")

W, H = 1440, 900
SIDEBAR_W = 240

PRIMARY = "#1F4E79"
BG = "#F5F7FA"
CARD = "#FFFFFF"
BORDER = "#E0E4EA"
TEXT = "#1A1A1A"
MUTED = "#6B7280"
SUCCESS = "#2E7D32"
DANGER = "#C62828"
ACTIVE_BG = "#E8EEF5"

MENU_ITEMS = ["Início", "Gastos", "Categorias", "Resumo", "Configurações"]

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]


def _fig_ax():
    fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=100)
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    return fig, ax


def _round_rect(ax, x, y, w, h, radius=8, fc=CARD, ec=BORDER, lw=1, zorder=1):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def _text(ax, x, y, s, size=14, color=TEXT, weight="normal", ha="left", va="top"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


def _button(ax, x, y, w, label, kind: Literal["primary", "secondary", "danger"] = "primary"):
    if kind == "primary":
        fc, ec, tc = PRIMARY, PRIMARY, "#FFFFFF"
    elif kind == "danger":
        fc, ec, tc = DANGER, DANGER, "#FFFFFF"
    else:
        fc, ec, tc = CARD, PRIMARY, PRIMARY
    _round_rect(ax, x, y, w, 40, radius=8, fc=fc, ec=ec, lw=1.5)
    _text(ax, x + w / 2, y + 20, label, size=13, color=tc, weight="bold", ha="center", va="center")


def _field(ax, x, y, w, label, placeholder="", value=""):
    _text(ax, x, y, label, size=12, color=MUTED)
    _round_rect(ax, x, y + 18, w, 40, radius=8, fc=CARD, ec=BORDER)
    content = value if value else placeholder
    color = TEXT if value else MUTED
    _text(ax, x + 12, y + 38, content, size=13, color=color, va="center")


def _sidebar(ax, active: str):
    ax.add_patch(Rectangle((0, 0), SIDEBAR_W, H, facecolor=CARD, edgecolor=BORDER, linewidth=1, zorder=0))
    ax.plot([SIDEBAR_W, SIDEBAR_W], [0, H], color=BORDER, linewidth=1, zorder=2)
    _text(ax, 24, 32, "FinControl", size=18, weight="bold", color=PRIMARY)
    _text(ax, 24, 54, "Controle financeiro", size=11, color=MUTED)
    y = 96
    for item in MENU_ITEMS:
        is_active = item == active
        if is_active:
            ax.add_patch(Rectangle((0, y), 4, 48, facecolor=PRIMARY, edgecolor="none", zorder=3))
            _round_rect(ax, 8, y + 4, SIDEBAR_W - 16, 40, radius=8, fc=ACTIVE_BG, ec="none")
        _text(ax, 48, y + 24, item, size=14, weight="bold" if is_active else "normal", color=PRIMARY if is_active else TEXT, va="center")
        y += 52


def _content_bg(ax):
    ax.add_patch(Rectangle((SIDEBAR_W, 0), W - SIDEBAR_W, H, facecolor=BG, edgecolor="none", zorder=0))


def save_screen(fig, path: str) -> None:
    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=100, bbox_inches="tight", pad_inches=0, facecolor=BG)
    plt.close(fig)


def screen_login(path: str) -> None:
    fig, ax = _fig_ax()
    cx, card_w = W / 2, 400
    card_x = cx - card_w / 2
    card_y = 240
    _round_rect(ax, card_x, card_y, card_w, 420, radius=12, fc=CARD, ec=BORDER)
    _text(ax, cx, card_y + 48, "FinControl", size=24, weight="bold", ha="center")
    _text(ax, cx, card_y + 78, "Entre na sua conta", size=14, color=MUTED, ha="center")
    _field(ax, card_x + 32, card_y + 110, card_w - 64, "E-mail", placeholder="seu@email.com")
    _field(ax, card_x + 32, card_y + 200, card_w - 64, "Senha", placeholder="••••••••")
    _text(ax, card_x + card_w - 32, card_y + 268, "Esqueci minha senha", size=12, color=PRIMARY, ha="right")
    _button(ax, card_x + 32, card_y + 300, card_w - 64, "Entrar")
    _text(ax, cx, card_y + 380, "Não tem conta? Criar conta", size=13, color=MUTED, ha="center")
    save_screen(fig, path)


def screen_register(path: str) -> None:
    fig, ax = _fig_ax()
    _sidebar(ax, "Gastos")
    _content_bg(ax)
    ox = SIDEBAR_W + 40
    _text(ax, ox, 40, "Novo gasto", size=28, weight="bold")
    _text(ax, ox, 72, "Gastos › Registrar", size=12, color=MUTED)
    col_w = 520
    _round_rect(ax, ox, 100, col_w, 200, radius=12)
    _text(ax, ox + 24, 124, "Valor e data", size=16, weight="bold")
    _field(ax, ox + 24, 150, 220, "Valor (R$)", placeholder="0,00")
    _field(ax, ox + 260, 150, 220, "Data", value="15/10/2026")
    _field(ax, ox + 24, 230, col_w - 48, "Forma de pagamento", value="Pix")

    _round_rect(ax, ox, 320, col_w, 200, radius=12)
    _text(ax, ox + 24, 344, "Detalhes", size=16, weight="bold")
    _field(ax, ox + 24, 370, col_w - 48, "Descrição", placeholder="Ex.: Supermercado")
    _field(ax, ox + 24, 450, col_w - 48, "Observação (opcional)", placeholder="")

    rx = ox + col_w + 32
    _round_rect(ax, rx, 100, 320, 280, radius=12)
    _text(ax, rx + 24, 124, "Categoria", size=16, weight="bold")
    _field(ax, rx + 24, 160, 272, "Categoria", value="Selecione…")
    _text(
        ax,
        rx + 24,
        240,
        "Você pode alterar depois\nem Categorias.",
        size=12,
        color=MUTED,
    )

    _button(ax, ox + col_w + 32 - 120, 820, 120, "Cancelar", kind="secondary")
    _button(ax, ox + col_w + 32 - 120 + 136, 820, 160, "Salvar gasto")
    save_screen(fig, path)


def screen_list_filters(path: str) -> None:
    fig, ax = _fig_ax()
    _sidebar(ax, "Gastos")
    _content_bg(ax)
    ox = SIDEBAR_W + 40
    _text(ax, ox, 40, "Gastos", size=28, weight="bold")
    _button(ax, W - 40 - 160, 28, 160, "+ Novo gasto")

    _round_rect(ax, ox, 88, W - ox - 40, 120, radius=12)
    _text(ax, ox + 24, 112, "Filtros", size=14, weight="bold")
    fw = 180
    _field(ax, ox + 24, 130, fw, "Data inicial", value="01/10/2026")
    _field(ax, ox + 24 + fw + 16, 130, fw, "Data final", value="31/10/2026")
    _field(ax, ox + 24 + 2 * (fw + 16), 130, fw, "Categoria", value="Todas")
    _field(ax, ox + 24 + 3 * (fw + 16), 130, 140, "Valor mín.", placeholder="0")
    _field(ax, ox + 24 + 3 * (fw + 16) + 156, 130, 140, "Valor máx.", placeholder="9999")
    _button(ax, W - 40 - 280, 168, 120, "Limpar filtros", kind="secondary")
    _button(ax, W - 40 - 144, 168, 144, "Aplicar filtros")

    ty = 232
    tw = W - ox - 40
    _round_rect(ax, ox, ty, tw, 420, radius=12)
    headers = ["Data", "Descrição", "Categoria", "Valor", "Ações"]
    col_x = [ox + 24, ox + 140, ox + 380, ox + 560, ox + 720]
    for i, h in enumerate(headers):
        _text(ax, col_x[i], ty + 24, h, size=12, weight="bold", color=MUTED)
    ax.plot([ox + 16, ox + tw - 16], [ty + 48, ty + 48], color=BORDER, linewidth=1)

    rows = [
        ("05/10/2026", "Supermercado", "Alimentação", "R$ 342,90"),
        ("08/10/2026", "Uber", "Transporte", "R$ 28,50"),
        ("10/10/2026", "Aluguel", "Moradia", "R$ 1.800,00"),
        ("12/10/2026", "Farmácia", "Saúde", "R$ 89,90"),
        ("14/10/2026", "Streaming", "Lazer", "R$ 55,90"),
    ]
    ry = ty + 64
    for date, desc, cat, val in rows:
        _text(ax, col_x[0], ry, date, size=13)
        _text(ax, col_x[1], ry, desc, size=13)
        _text(ax, col_x[2], ry, cat, size=13)
        _text(ax, col_x[3], ry, val, size=13, weight="bold")
        _text(ax, col_x[4], ry, "Editar   Excluir", size=12, color=PRIMARY)
        ax.plot([ox + 16, ox + tw - 16], [ry + 22, ry + 22], color=BORDER, linewidth=0.8)
        ry += 56

    _text(ax, ox + 24, ty + 392, "Mostrando 24 de 156 gastos", size=12, color=MUTED)
    _text(ax, ox + tw - 120, ty + 392, "1  2  3  ›", size=12, color=PRIMARY, ha="right")
    save_screen(fig, path)


def screen_edit_delete(path: str) -> None:
    fig, ax = _fig_ax()
    _sidebar(ax, "Gastos")
    _content_bg(ax)
    ox = SIDEBAR_W + 40
    _text(ax, ox, 40, "Editar gasto", size=28, weight="bold")

    list_w = 360
    _round_rect(ax, ox, 88, list_w, 720, radius=12)
    _field(ax, ox + 16, 104, list_w - 32, "Buscar", placeholder="Buscar gasto…")
    items = [
        ("05/10 — Supermercado", "R$ 342,90", True),
        ("08/10 — Uber", "R$ 28,50", False),
        ("10/10 — Aluguel", "R$ 1.800,00", False),
        ("12/10 — Farmácia", "R$ 89,90", False),
    ]
    iy = 200
    for title, val, selected in items:
        ec = PRIMARY if selected else BORDER
        lw = 2 if selected else 1
        _round_rect(ax, ox + 16, iy, list_w - 32, 72, radius=8, fc=ACTIVE_BG if selected else CARD, ec=ec, lw=lw)
        _text(ax, ox + 32, iy + 20, title, size=13, weight="bold" if selected else "normal")
        _text(ax, ox + 32, iy + 44, val, size=13, color=MUTED)
        iy += 84

    px = ox + list_w + 32
    pw = W - px - 40
    _round_rect(ax, px, 88, pw, 720, radius=12)
    _text(ax, px + 24, 112, "Dados do gasto selecionado", size=18, weight="bold")
    _field(ax, px + 24, 150, 280, "Valor (R$)", value="342,90")
    _field(ax, px + 320, 150, 280, "Data", value="05/10/2026")
    _field(ax, px + 24, 240, pw - 48, "Descrição", value="Supermercado")
    _field(ax, px + 24, 330, 280, "Categoria", value="Alimentação")

    _round_rect(ax, px + 24, 430, pw - 48, 48, radius=8, fc="#FFF8E1", ec="#FFE082")
    _text(ax, px + 40, 454, "Excluir remove o gasto permanentemente.", size=12, color="#795548", va="center")

    _button(ax, px + 24, 820, 140, "Excluir gasto", kind="danger")
    _button(ax, px + pw - 24 - 280, 820, 120, "Cancelar", kind="secondary")
    _button(ax, px + pw - 24 - 140, 820, 140, "Salvar alterações")
    save_screen(fig, path)


def screen_summary(path: str) -> None:
    fig, ax = _fig_ax()
    _sidebar(ax, "Resumo")
    _content_bg(ax)
    ox = SIDEBAR_W + 40
    _text(ax, ox, 40, "Resumo mensal", size=28, weight="bold")
    _round_rect(ax, ox + 320, 32, 220, 40, radius=8)
    _text(ax, ox + 430, 52, "‹  Outubro 2026  ›", size=14, ha="center", va="center")

    kpi_y = 96
    kpi_w = (W - ox - 40 - 32) / 3
    kpis = [("Total gasto", "R$ 4.280,00", TEXT), ("Orçamento", "R$ 5.000,00", TEXT), ("Saldo", "R$ 720,00", SUCCESS)]
    for i, (title, val, color) in enumerate(kpis):
        kx = ox + i * (kpi_w + 16)
        _round_rect(ax, kx, kpi_y, kpi_w, 100, radius=12)
        _text(ax, kx + 24, kpi_y + 28, title, size=13, color=MUTED)
        _text(ax, kx + 24, kpi_y + 62, val, size=22, weight="bold", color=color)

    chart_y = 220
    chart_w = (W - ox - 40) * 0.58
    side_w = (W - ox - 40) * 0.42 - 16
    _round_rect(ax, ox, chart_y, chart_w, 400, radius=12)
    _text(ax, ox + 24, chart_y + 28, "Gastos por categoria", size=16, weight="bold")
    bars = [("Alimentação", 0.85), ("Moradia", 0.95), ("Transporte", 0.35), ("Lazer", 0.25), ("Outros", 0.15)]
    by = chart_y + 70
    for label, frac in bars:
        _text(ax, ox + 24, by, label, size=12, color=MUTED)
        bar_x = ox + 160
        bar_w = 400 * frac
        _round_rect(ax, bar_x, by - 8, bar_w, 20, radius=4, fc=PRIMARY, ec="none")
        _round_rect(ax, bar_x + bar_w + 8, by - 8, 400 - bar_w, 20, radius=4, fc=BORDER, ec="none")
        by += 52

    sx = ox + chart_w + 24
    _round_rect(ax, sx, chart_y, side_w, 400, radius=12)
    _text(ax, sx + 24, chart_y + 28, "Top categorias", size=16, weight="bold")
    tops = [("Moradia", "42%"), ("Alimentação", "28%"), ("Transporte", "12%"), ("Lazer", "8%"), ("Outros", "10%")]
    ty = chart_y + 72
    for label, pct in tops:
        _text(ax, sx + 24, ty, label, size=13)
        _text(ax, sx + side_w - 48, ty, pct, size=13, weight="bold", ha="right")
        _round_rect(ax, sx + 24, ty + 16, side_w - 48, 6, radius=3, fc=BORDER, ec="none")
        fill_w = (side_w - 48) * (int(pct[:-1]) / 100)
        _round_rect(ax, sx + 24, ty + 16, fill_w, 6, radius=3, fc=PRIMARY, ec="none")
        ty += 56

    _button(ax, ox, 660, 200, "Ver gastos do mês")
    _button(ax, ox + 216, 660, 160, "Exportar PDF", kind="secondary")
    save_screen(fig, path)


def screen_categorize(path: str) -> None:
    fig, ax = _fig_ax()
    _sidebar(ax, "Categorias")
    _content_bg(ax)
    ox = SIDEBAR_W + 40
    _text(ax, ox, 40, "Categorizar gasto", size=28, weight="bold")
    _text(ax, ox, 72, "Selecione a categoria para o gasto abaixo", size=14, color=MUTED)

    _round_rect(ax, ox, 100, W - ox - 40, 72, radius=12, fc=ACTIVE_BG, ec=PRIMARY, lw=1.5)
    _text(ax, ox + 24, 136, "Supermercado  ·  R$ 342,90  ·  05/10/2026", size=15, weight="bold", va="center")

    cats = [
        "Alimentação",
        "Transporte",
        "Moradia",
        "Saúde",
        "Educação",
        "Lazer",
        "Compras",
        "Outros",
    ]
    gx, gy = ox, 200
    cw, ch, gap = 160, 120, 24
    cols = 4
    for i, name in enumerate(cats):
        col = i % cols
        row = i // cols
        cx = gx + col * (cw + gap)
        cy = gy + row * (ch + gap)
        selected = name == "Alimentação"
        ec = PRIMARY if selected else BORDER
        lw = 2.5 if selected else 1
        fc = ACTIVE_BG if selected else CARD
        _round_rect(ax, cx, cy, cw, ch, radius=12, fc=fc, ec=ec, lw=lw)
        _round_rect(ax, cx + 56, cy + 24, 48, 48, radius=24, fc=BORDER, ec="none")
        _text(ax, cx + cw / 2, cy + 92, name, size=13, weight="bold" if selected else "normal", ha="center")

    nx = gx + 3 * (cw + gap)
    ny = gy + 2 * (ch + gap)
    _round_rect(ax, nx, ny, cw, ch, radius=12, fc=BG, ec=BORDER, lw=1.5)
    ax.plot([nx + 40, nx + cw - 40], [ny + ch / 2, ny + ch / 2], color=MUTED, linestyle="--", linewidth=1)
    ax.plot([nx + cw / 2, nx + cw / 2], [ny + 40, ny + ch - 40], color=MUTED, linestyle="--", linewidth=1)
    _text(ax, nx + cw / 2, ny + ch - 24, "Nova categoria", size=12, color=MUTED, ha="center")

    _button(ax, ox, 820, 120, "Voltar", kind="secondary")
    _button(ax, W - 40 - 200, 820, 200, "Confirmar categoria")
    save_screen(fig, path)


def build_pdf(image_paths: list[str], output_path: str) -> None:
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    page_w = 297
    page_h = 210
    for img_path in image_paths:
        pdf.add_page()
        margin = 5
        avail_w = page_w - 2 * margin
        avail_h = page_h - 2 * margin
        img_w_px, img_h_px = W, H
        scale = min(avail_w / (img_w_px * 0.264583), avail_h / (img_h_px * 0.264583))
        draw_w = img_w_px * 0.264583 * scale
        draw_h = img_h_px * 0.264583 * scale
        x = (page_w - draw_w) / 2
        y = (page_h - draw_h) / 2
        pdf.image(img_path, x=x, y=y, w=draw_w, h=draw_h)
    pdf.output(output_path)


def main() -> None:
    screens = [
        ("01_login.png", screen_login),
        ("02_registrar_gasto.png", screen_register),
        ("03_listar_filtrar.png", screen_list_filters),
        ("04_editar_excluir.png", screen_edit_delete),
        ("05_resumo_mensal.png", screen_summary),
        ("06_categorizar.png", screen_categorize),
    ]
    paths: list[str] = []
    for filename, draw_fn in screens:
        out = os.path.join(OUTPUT_DIR, filename)
        draw_fn(out)
        paths.append(out)
        print(f"Imagem gerada: {out}")

    build_pdf(paths, OUTPUT_PDF)
    print(f"PDF gerado: {OUTPUT_PDF}")
    print(
        "\nUse estas imagens como referência no Figma. "
        "Para a entrega oficial, exporte as telas criadas no Figma em um PDF só com as imagens."
    )


if __name__ == "__main__":
    main()
