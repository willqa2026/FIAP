# -*- coding: utf-8 -*-
"""Gera os modelos Lógico e Físico (Oracle) do FinControl.

Uma única definição de entidades/relacionamentos alimenta:
  - diagrama do Modelo Lógico   (modelo_logico.png)
  - diagrama do Modelo Físico   (modelo_fisico.png)
  - script DDL Oracle           (fincontrol_ddl.sql)
  - PDF de entrega              (RM576183_Modelo_Logico_Fisico_FinControl.pdf)

Assim os dois modelos permanecem coerentes entre si.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from fpdf import FPDF
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RM = "RM576183"
PDF_NAME = f"{RM}_Modelo_Logico_Fisico_FinControl.pdf"

# --------------------------------------------------------------------------- #
# Definição do modelo
# --------------------------------------------------------------------------- #


@dataclass
class Attr:
    logical: str          # nome no modelo lógico
    ltype: str            # tipo lógico
    column: str           # nome da coluna física
    ptype: str            # tipo físico Oracle
    pk: bool = False
    uk: bool = False
    mandatory: bool = True
    default: str | None = None


@dataclass
class Entity:
    key: str
    logical: str
    table: str
    comment: str
    attrs: list[Attr]
    uniques: list[tuple[str, list[str]]] = field(default_factory=list)
    checks: list[tuple[str, str]] = field(default_factory=list)

    @property
    def pk(self) -> Attr:
        return next(a for a in self.attrs if a.pk)


@dataclass
class Rel:
    parent: str
    child: str
    fk_column: str
    mandatory: bool       # o filho exige o pai?
    label: str            # verbo (lado pai -> filho)


def pk(logical, column, ptype="NUMBER(10)", ltype="NUMERIC (10)"):
    return Attr(logical, ltype, column, ptype, pk=True)


E = [
    Entity(
        "USUARIO", "USUARIO", "T_USUARIO",
        "Usuário do aplicativo FinControl (autenticação e dono dos dados).",
        [
            pk("Id Usuario", "id_usuario"),
            Attr("Nome", "VARCHAR (100)", "nm_usuario", "VARCHAR2(100)"),
            Attr("E-mail", "VARCHAR (150)", "ds_email", "VARCHAR2(150)", uk=True),
            Attr("Senha Hash", "VARCHAR (255)", "ds_senha_hash", "VARCHAR2(255)"),
            Attr("CPF", "CHAR (11)", "nr_cpf", "CHAR(11)", uk=True),
            Attr("Data Nascimento", "DATE", "dt_nascimento", "DATE", mandatory=False),
            Attr("Data Cadastro", "DATE", "dt_cadastro", "DATE", default="SYSDATE"),
            Attr("Ativo", "CHAR (1)", "st_ativo", "CHAR(1)", default="'S'"),
        ],
        uniques=[("UK_USUARIO_EMAIL", ["ds_email"]), ("UK_USUARIO_CPF", ["nr_cpf"])],
        checks=[("CK_USUARIO_ATIVO", "st_ativo IN ('S', 'N')")],
    ),
    Entity(
        "FORMA_PAGAMENTO", "FORMA_PAGAMENTO", "T_FORMA_PAGAMENTO",
        "Domínio de formas de pagamento (Pix, Débito, Crédito, Dinheiro, Boleto).",
        [
            pk("Id Forma Pagamento", "id_forma_pagamento", "NUMBER(3)", "NUMERIC (3)"),
            Attr("Nome", "VARCHAR (30)", "nm_forma_pagamento", "VARCHAR2(30)", uk=True),
        ],
        uniques=[("UK_FORMA_PAGAMENTO_NOME", ["nm_forma_pagamento"])],
    ),
    Entity(
        "CATEGORIA", "CATEGORIA", "T_CATEGORIA",
        "Categoria de receita ou despesa. Sem usuário = categoria padrão do sistema.",
        [
            pk("Id Categoria", "id_categoria", "NUMBER(6)", "NUMERIC (6)"),
            Attr("Nome", "VARCHAR (50)", "nm_categoria", "VARCHAR2(50)"),
            Attr("Tipo (R/D)", "CHAR (1)", "tp_categoria", "CHAR(1)"),
        ],
        uniques=[("UK_CATEGORIA", ["id_usuario", "nm_categoria", "tp_categoria"])],
        checks=[("CK_CATEGORIA_TIPO", "tp_categoria IN ('R', 'D')")],
    ),
    Entity(
        "DESPESA", "DESPESA", "T_DESPESA",
        "Gasto registrado pelo usuário (US01, US02, US04, US05).",
        [
            pk("Id Despesa", "id_despesa", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Valor", "NUMERIC (12,2)", "vl_despesa", "NUMBER(12,2)"),
            Attr("Data", "DATE", "dt_despesa", "DATE"),
            Attr("Descricao", "VARCHAR (100)", "ds_despesa", "VARCHAR2(100)"),
            Attr("Observacao", "VARCHAR (255)", "ds_observacao", "VARCHAR2(255)", mandatory=False),
        ],
        checks=[("CK_DESPESA_VALOR", "vl_despesa > 0")],
    ),
    Entity(
        "RECEITA", "RECEITA", "T_RECEITA",
        "Entrada de dinheiro do usuário (salário, freelance, rendimentos etc.).",
        [
            pk("Id Receita", "id_receita", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Valor", "NUMERIC (12,2)", "vl_receita", "NUMBER(12,2)"),
            Attr("Data", "DATE", "dt_receita", "DATE"),
            Attr("Descricao", "VARCHAR (100)", "ds_receita", "VARCHAR2(100)"),
            Attr("Recorrente", "CHAR (1)", "st_recorrente", "CHAR(1)", default="'N'"),
        ],
        checks=[
            ("CK_RECEITA_VALOR", "vl_receita > 0"),
            ("CK_RECEITA_RECORRENTE", "st_recorrente IN ('S', 'N')"),
        ],
    ),
    Entity(
        "ORCAMENTO", "ORCAMENTO", "T_ORCAMENTO",
        "Limite mensal de gastos (geral ou por categoria) usado no Resumo Mensal (US03).",
        [
            pk("Id Orcamento", "id_orcamento"),
            Attr("Ano", "NUMERIC (4)", "nr_ano", "NUMBER(4)"),
            Attr("Mes", "NUMERIC (2)", "nr_mes", "NUMBER(2)"),
            Attr("Valor Limite", "NUMERIC (12,2)", "vl_limite", "NUMBER(12,2)"),
        ],
        uniques=[("UK_ORCAMENTO", ["id_usuario", "id_categoria", "nr_ano", "nr_mes"])],
        checks=[
            ("CK_ORCAMENTO_MES", "nr_mes BETWEEN 1 AND 12"),
            ("CK_ORCAMENTO_VALOR", "vl_limite > 0"),
        ],
    ),
    Entity(
        "DIVIDA", "DIVIDA", "T_DIVIDA",
        "Dívida/financiamento contratado pelo usuário (produto de crédito).",
        [
            pk("Id Divida", "id_divida"),
            Attr("Descricao", "VARCHAR (100)", "ds_divida", "VARCHAR2(100)"),
            Attr("Credor", "VARCHAR (100)", "nm_credor", "VARCHAR2(100)"),
            Attr("Valor Principal", "NUMERIC (12,2)", "vl_principal", "NUMBER(12,2)"),
            Attr("Percentual Juros", "NUMERIC (5,2)", "pc_juros", "NUMBER(5,2)"),
            Attr("Qtd Parcelas", "NUMERIC (3)", "qt_parcelas", "NUMBER(3)"),
            Attr("Data Contratacao", "DATE", "dt_contratacao", "DATE"),
        ],
        checks=[
            ("CK_DIVIDA_VALOR", "vl_principal > 0"),
            ("CK_DIVIDA_JUROS", "pc_juros >= 0"),
            ("CK_DIVIDA_PARCELAS", "qt_parcelas > 0"),
        ],
    ),
    Entity(
        "PARCELA_DIVIDA", "PARCELA_DIVIDA", "T_PARCELA_DIVIDA",
        "Parcela de uma dívida. Data de pagamento nula = parcela em aberto.",
        [
            pk("Id Parcela", "id_parcela", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Numero Parcela", "NUMERIC (3)", "nr_parcela", "NUMBER(3)"),
            Attr("Valor Parcela", "NUMERIC (12,2)", "vl_parcela", "NUMBER(12,2)"),
            Attr("Data Vencimento", "DATE", "dt_vencimento", "DATE"),
            Attr("Data Pagamento", "DATE", "dt_pagamento", "DATE", mandatory=False),
        ],
        uniques=[("UK_PARCELA_DIVIDA", ["id_divida", "nr_parcela"])],
        checks=[("CK_PARCELA_VALOR", "vl_parcela > 0")],
    ),
    Entity(
        "TIPO_INVESTIMENTO", "TIPO_INVESTIMENTO", "T_TIPO_INVESTIMENTO",
        "Domínio de tipos de investimento (CDB, LCI, LCA, Tesouro, Poupança).",
        [
            pk("Id Tipo Investimento", "id_tipo_investimento", "NUMBER(3)", "NUMERIC (3)"),
            Attr("Nome", "VARCHAR (50)", "nm_tipo_investimento", "VARCHAR2(50)", uk=True),
            Attr("Isento IR", "CHAR (1)", "st_isento_ir", "CHAR(1)"),
        ],
        uniques=[("UK_TIPO_INVESTIMENTO_NOME", ["nm_tipo_investimento"])],
        checks=[("CK_TIPO_INV_ISENTO", "st_isento_ir IN ('S', 'N')")],
    ),
    Entity(
        "INVESTIMENTO", "INVESTIMENTO", "T_INVESTIMENTO",
        "Aplicação financeira do usuário; resgate usado no cálculo de IR.",
        [
            pk("Id Investimento", "id_investimento"),
            Attr("Nome", "VARCHAR (100)", "nm_investimento", "VARCHAR2(100)"),
            Attr("Instituicao", "VARCHAR (100)", "nm_instituicao", "VARCHAR2(100)"),
            Attr("Valor Aplicado", "NUMERIC (12,2)", "vl_aplicado", "NUMBER(12,2)"),
            Attr("Rentabilidade a.a.", "NUMERIC (5,2)", "pc_rentabilidade_aa", "NUMBER(5,2)", mandatory=False),
            Attr("Data Aplicacao", "DATE", "dt_aplicacao", "DATE"),
            Attr("Data Vencimento", "DATE", "dt_vencimento", "DATE", mandatory=False),
            Attr("Data Resgate", "DATE", "dt_resgate", "DATE", mandatory=False),
            Attr("Valor Resgate", "NUMERIC (12,2)", "vl_resgate", "NUMBER(12,2)", mandatory=False),
        ],
        checks=[
            ("CK_INVESTIMENTO_VALOR", "vl_aplicado > 0"),
            ("CK_INVESTIMENTO_VENC", "dt_vencimento IS NULL OR dt_vencimento >= dt_aplicacao"),
            ("CK_INVESTIMENTO_RESGATE", "dt_resgate IS NULL OR dt_resgate >= dt_aplicacao"),
        ],
    ),
    Entity(
        "META", "META_FINANCEIRA", "T_META_FINANCEIRA",
        "Meta de planejamento financeiro (ex.: reserva de emergência, viagem).",
        [
            pk("Id Meta", "id_meta"),
            Attr("Nome", "VARCHAR (100)", "nm_meta", "VARCHAR2(100)"),
            Attr("Descricao", "VARCHAR (255)", "ds_meta", "VARCHAR2(255)", mandatory=False),
            Attr("Valor Objetivo", "NUMERIC (12,2)", "vl_objetivo", "NUMBER(12,2)"),
            Attr("Data Inicio", "DATE", "dt_inicio", "DATE"),
            Attr("Data Limite", "DATE", "dt_limite", "DATE", mandatory=False),
        ],
        checks=[
            ("CK_META_VALOR", "vl_objetivo > 0"),
            ("CK_META_DATAS", "dt_limite IS NULL OR dt_limite > dt_inicio"),
        ],
    ),
    Entity(
        "APORTE", "APORTE_META", "T_APORTE_META",
        "Valor guardado para uma meta. Saldo da meta = soma dos aportes.",
        [
            pk("Id Aporte", "id_aporte", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Valor", "NUMERIC (12,2)", "vl_aporte", "NUMBER(12,2)"),
            Attr("Data", "DATE", "dt_aporte", "DATE"),
        ],
        checks=[("CK_APORTE_VALOR", "vl_aporte > 0")],
    ),
]
ENT = {e.key: e for e in E}

R = [
    Rel("USUARIO", "CATEGORIA", "id_usuario", False, "personaliza"),
    Rel("USUARIO", "DESPESA", "id_usuario", True, "registra"),
    Rel("USUARIO", "RECEITA", "id_usuario", True, "recebe"),
    Rel("USUARIO", "ORCAMENTO", "id_usuario", True, "planeja"),
    Rel("USUARIO", "DIVIDA", "id_usuario", True, "contrai"),
    Rel("USUARIO", "INVESTIMENTO", "id_usuario", True, "aplica"),
    Rel("USUARIO", "META", "id_usuario", True, "define"),
    Rel("CATEGORIA", "DESPESA", "id_categoria", True, "classifica"),
    Rel("CATEGORIA", "RECEITA", "id_categoria", True, "classifica"),
    Rel("CATEGORIA", "ORCAMENTO", "id_categoria", False, "limita"),
    Rel("FORMA_PAGAMENTO", "DESPESA", "id_forma_pagamento", True, "paga"),
    Rel("DIVIDA", "PARCELA_DIVIDA", "id_divida", True, "possui"),
    Rel("TIPO_INVESTIMENTO", "INVESTIMENTO", "id_tipo_investimento", True, "classifica"),
    Rel("META", "APORTE", "id_meta", True, "recebe"),
]


def fk_name(rel: Rel) -> str:
    return f"FK_{ENT[rel.child].logical}_{ENT[rel.parent].logical}"


def physical_columns(e: Entity) -> list[tuple[str, str, str]]:
    """(marcador, coluna, tipo) — PK, FKs, demais colunas."""
    cols = []
    fks = [r for r in R if r.child == e.key]
    for a in e.attrs:
        if a.pk:
            cols.append(("P *", a.column, a.ptype))
    for r in fks:
        parent_pk = ENT[r.parent].pk
        cols.append((f"F {'*' if r.mandatory else ' '}", r.fk_column, parent_pk.ptype))
    for a in e.attrs:
        if not a.pk:
            mark = ("U " if a.uk else "  ") + ("*" if a.mandatory else " ")
            cols.append((mark, a.column, a.ptype))
    return cols


def physical_constraints(e: Entity) -> list[str]:
    out = [f"PK_{e.logical} ({e.pk.column})"]
    out += [f"{n} ({', '.join(c)})" for n, c in e.uniques]
    out += [f"{fk_name(r)} ({r.fk_column})" for r in R if r.child == e.key]
    return out


def logical_attrs(e: Entity) -> list[tuple[str, str, str]]:
    out = []
    for a in e.attrs:
        mark = ("P " if a.pk else "U " if a.uk else "  ") + ("*" if a.mandatory else " ")
        out.append((mark, a.logical, a.ltype))
    return out


# --------------------------------------------------------------------------- #
# DDL Oracle
# --------------------------------------------------------------------------- #


def build_ddl() -> str:
    L = [
        "-- =====================================================================",
        "-- FinControl - Modelo Físico (Oracle Database 19c+)",
        f"-- {RM} | Gerado por gerar_modelo_fincontrol.py",
        "-- Pode ser executado no SQL Developer ou importado no Oracle Data Modeler",
        "-- (File > Import > DDL File) para gerar os diagramas relacional/lógico.",
        "-- =====================================================================",
        "",
        "-- Remoção (ordem inversa das dependências) --------------------------",
    ]
    order = ["APORTE", "META", "INVESTIMENTO", "TIPO_INVESTIMENTO", "PARCELA_DIVIDA",
             "DIVIDA", "ORCAMENTO", "RECEITA", "DESPESA", "CATEGORIA", "FORMA_PAGAMENTO", "USUARIO"]
    for k in order:
        L.append(f"-- DROP TABLE {ENT[k].table} CASCADE CONSTRAINTS;")
    L.append("")

    for e in E:
        L.append(f"CREATE TABLE {e.table} (")
        lines = []
        for mark, col, typ in physical_columns(e):
            attr = next((a for a in e.attrs if a.column == col), None)
            s = f"    {col:<22} {typ:<14}"
            if attr and attr.pk:
                s += " GENERATED BY DEFAULT AS IDENTITY"
            if attr and attr.default:
                s += f" DEFAULT {attr.default}"
            if "*" in mark:
                s += " NOT NULL"
            lines.append(s.rstrip())
        L.append(",\n".join(lines))
        L.append(");")
        L.append("")
        L.append(f"ALTER TABLE {e.table} ADD CONSTRAINT PK_{e.logical} PRIMARY KEY ({e.pk.column});")
        for n, cols in e.uniques:
            L.append(f"ALTER TABLE {e.table} ADD CONSTRAINT {n} UNIQUE ({', '.join(cols)});")
        for n, expr in e.checks:
            L.append(f"ALTER TABLE {e.table} ADD CONSTRAINT {n} CHECK ({expr});")
        L.append(f"COMMENT ON TABLE {e.table} IS '{e.comment.replace(chr(39), chr(39)*2)}';")
        L.append("")

    L.append("-- Chaves estrangeiras -----------------------------------------------")
    for r in R:
        c, p = ENT[r.child], ENT[r.parent]
        L.append(
            f"ALTER TABLE {c.table} ADD CONSTRAINT {fk_name(r)}\n"
            f"    FOREIGN KEY ({r.fk_column}) REFERENCES {p.table} ({p.pk.column});"
        )
    L.append("")
    L.append("-- Índices para as FKs (consultas por usuário, filtros por período) --")
    for r in R:
        c = ENT[r.child]
        L.append(f"CREATE INDEX IX_{c.logical}_{r.fk_column.upper()[3:]} ON {c.table} ({r.fk_column});")
    L.append("CREATE INDEX IX_DESPESA_DATA ON T_DESPESA (id_usuario, dt_despesa);")
    L.append("CREATE INDEX IX_RECEITA_DATA ON T_RECEITA (id_usuario, dt_receita);")
    L.append("")
    L.append("-- Dados de domínio ---------------------------------------------------")
    for fp in ["Pix", "Cartao de Debito", "Cartao de Credito", "Dinheiro", "Boleto"]:
        L.append(f"INSERT INTO T_FORMA_PAGAMENTO (nm_forma_pagamento) VALUES ('{fp}');")
    for nome, isento in [("CDB", "N"), ("LCI", "S"), ("LCA", "S"), ("Tesouro Direto", "N"), ("Poupanca", "S")]:
        L.append(f"INSERT INTO T_TIPO_INVESTIMENTO (nm_tipo_investimento, st_isento_ir) VALUES ('{nome}', '{isento}');")
    for cat in ["Alimentacao", "Transporte", "Moradia", "Saude", "Educacao", "Lazer", "Compras", "Outros"]:
        L.append(f"INSERT INTO T_CATEGORIA (nm_categoria, tp_categoria) VALUES ('{cat}', 'D');")
    for cat in ["Salario", "Freelance", "Rendimentos", "Outros"]:
        L.append(f"INSERT INTO T_CATEGORIA (nm_categoria, tp_categoria) VALUES ('{cat}', 'R');")
    L.append("COMMIT;")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# Desenho dos diagramas
# --------------------------------------------------------------------------- #

HEADER_H = 30
ROW_H = 19
PAD = 8
FS = 10.5          # fonte das linhas (pt)
MARGIN = 30
GAP = 120
BOX_W = {"logical": 340, "physical": 450}


def col_x(kind: str) -> list[float]:
    return [MARGIN + i * (BOX_W[kind] + GAP) for i in range(5)]


def canvas_w(kind: str) -> float:
    return 2 * MARGIN + 5 * BOX_W[kind] + 4 * GAP

INK = "#1A1A1A"
MUTED = "#555555"
LINE = "#2F4F6F"
LOG_HEAD = "#DCE9F7"
LOG_BODY = "#F7FBFF"
PHY_HEAD = "#E3F1E3"
PHY_BODY = "#FAFFFA"
BORDER = "#3B5B7A"

LAYOUT = {  # (coluna, linha)
    "FORMA_PAGAMENTO": (0, 0), "DESPESA": (1, 0), "CATEGORIA": (2, 0),
    "RECEITA": (3, 0), "ORCAMENTO": (4, 0),
    "PARCELA_DIVIDA": (0, 1), "DIVIDA": (1, 1), "USUARIO": (2, 1),
    "META": (3, 1), "APORTE": (4, 1),
    "TIPO_INVESTIMENTO": (1, 2), "INVESTIMENTO": (2, 2),
}

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]


def box_height(n_rows: int, n_cons: int) -> float:
    h = HEADER_H + PAD + n_rows * ROW_H + PAD
    if n_cons:
        h += 6 + n_cons * ROW_H + PAD
    return h


def compute_boxes(kind: str) -> tuple[dict, float]:
    heights = {}
    for e in E:
        if kind == "logical":
            heights[e.key] = box_height(len(logical_attrs(e)), 0)
        else:
            heights[e.key] = box_height(len(physical_columns(e)), len(physical_constraints(e)))
    row_top = [140.0]
    for row in range(3):
        tallest = max(heights[k] for k, (c, r) in LAYOUT.items() if r == row)
        row_top.append(row_top[-1] + tallest + 120)
    xs = col_x(kind)
    boxes = {}
    for k, (c, r) in LAYOUT.items():
        boxes[k] = (xs[c], row_top[r], BOX_W[kind], heights[k])
    return boxes, row_top[3] - 120 + MARGIN


def routes(b: dict) -> dict:
    """Pontos (x, y) de cada relacionamento: do pai até o filho."""
    def x(k): return b[k][0]
    def y(k): return b[k][1]
    def w(k): return b[k][2]
    def h(k): return b[k][3]
    def cx(k): return x(k) + w(k) / 2
    def right(k): return x(k) + w(k)
    def bottom(k): return y(k) + h(k)

    u = "USUARIO"
    ch1 = y(u) - 40     # canal entre linha 0 e linha 1
    ch2 = y(u) - 70
    top_ch = y("CATEGORIA") - 35
    hy0 = y("CATEGORIA") + 45
    hy1 = y(u) + 45
    hy2 = y("INVESTIMENTO") + 45
    return {
        ("USUARIO", "CATEGORIA"): [(cx(u), y(u)), (cx(u), bottom("CATEGORIA"))],
        ("USUARIO", "DESPESA"): [(x(u) + 60, y(u)), (x(u) + 60, ch1), (cx("DESPESA"), ch1),
                                 (cx("DESPESA"), bottom("DESPESA"))],
        ("USUARIO", "RECEITA"): [(right(u) - 110, y(u)), (right(u) - 110, ch2), (cx("RECEITA"), ch2),
                                 (cx("RECEITA"), bottom("RECEITA"))],
        ("USUARIO", "ORCAMENTO"): [(right(u) - 40, y(u)), (right(u) - 40, ch1), (cx("ORCAMENTO"), ch1),
                                   (cx("ORCAMENTO"), bottom("ORCAMENTO"))],
        ("USUARIO", "DIVIDA"): [(x(u), hy1), (right("DIVIDA"), hy1)],
        ("USUARIO", "META"): [(right(u), hy1), (x("META"), hy1)],
        ("USUARIO", "INVESTIMENTO"): [(cx(u), bottom(u)), (cx(u), y("INVESTIMENTO"))],
        ("CATEGORIA", "DESPESA"): [(x("CATEGORIA"), hy0), (right("DESPESA"), hy0)],
        ("CATEGORIA", "RECEITA"): [(right("CATEGORIA"), hy0), (x("RECEITA"), hy0)],
        ("CATEGORIA", "ORCAMENTO"): [(cx("CATEGORIA") + 60, y("CATEGORIA")), (cx("CATEGORIA") + 60, top_ch),
                                     (cx("ORCAMENTO"), top_ch), (cx("ORCAMENTO"), y("ORCAMENTO"))],
        ("FORMA_PAGAMENTO", "DESPESA"): [(right("FORMA_PAGAMENTO"), hy0), (x("DESPESA"), hy0)],
        ("DIVIDA", "PARCELA_DIVIDA"): [(x("DIVIDA"), hy1), (right("PARCELA_DIVIDA"), hy1)],
        ("TIPO_INVESTIMENTO", "INVESTIMENTO"): [(right("TIPO_INVESTIMENTO"), hy2), (x("INVESTIMENTO"), hy2)],
        ("META", "APORTE"): [(right("META"), hy1), (x("APORTE"), hy1)],
    }


def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = (dx * dx + dy * dy) ** 0.5 or 1
    return dx / n, dy / n


def draw_end(ax, tip, toward, many: bool, mandatory: bool):
    """Notação pé-de-galinha (IE). tip = ponto na borda; toward = vetor p/ dentro da caixa."""
    ux, uy = toward
    px, py = -uy, ux
    if many:
        base = (tip[0] - ux * 16, tip[1] - uy * 16)
        for s in (-1, 0, 1):
            ax.plot([base[0], tip[0] + px * 9 * s], [base[1], tip[1] + py * 9 * s], color=LINE, lw=1.4, zorder=4)
        mark_at = 24
    else:
        b = (tip[0] - ux * 9, tip[1] - uy * 9)
        ax.plot([b[0] - px * 8, b[0] + px * 8], [b[1] - py * 8, b[1] + py * 8], color=LINE, lw=1.6, zorder=4)
        mark_at = 17
    c = (tip[0] - ux * (mark_at + 4), tip[1] - uy * (mark_at + 4))
    if mandatory:
        ax.plot([c[0] - px * 8, c[0] + px * 8], [c[1] - py * 8, c[1] + py * 8], color=LINE, lw=1.6, zorder=4)
    else:
        ax.add_patch(Circle(c, 5.5, facecolor="white", edgecolor=LINE, lw=1.4, zorder=5))


def draw_relationship(ax, pts, rel: Rel, show_label: bool):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=LINE, lw=1.4, zorder=3, solid_joinstyle="miter")
    # lado do pai: exatamente um (obrigatório) ou zero/um (opcional)
    draw_end(ax, pts[0], _unit(pts[1], pts[0]), many=False, mandatory=rel.mandatory)
    # lado do filho: zero ou muitos
    draw_end(ax, pts[-1], _unit(pts[-2], pts[-1]), many=True, mandatory=False)
    if show_label:
        segs = list(zip(pts[:-1], pts[1:]))
        a, b = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if abs(a[1] - b[1]) < 1:      # segmento horizontal: rótulo acima da linha
            my -= 12
        ax.text(mx, my, rel.label, fontsize=9, style="italic", color=MUTED, ha="center", va="center",
                zorder=6, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))


def draw_box(ax, x, y, w, h, title, rows, cons, head_fc, body_fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=6",
                                fc=body_fc, ec=BORDER, lw=1.4, zorder=2))
    ax.add_patch(Rectangle((x + 1, y + 1), w - 2, HEADER_H - 1, fc=head_fc, ec="none", zorder=2))
    ax.plot([x, x + w], [y + HEADER_H, y + HEADER_H], color=BORDER, lw=1.2, zorder=3)
    ax.text(x + w / 2, y + HEADER_H / 2, title, fontsize=11.5, weight="bold", color=INK,
            ha="center", va="center", zorder=4)
    ry = y + HEADER_H + PAD + ROW_H / 2
    for mark, name, typ in rows:
        bold = mark.startswith("P")
        ax.text(x + 10, ry, mark, fontsize=FS, family="monospace", color="#8B1A1A" if bold else MUTED,
                weight="bold", va="center", zorder=4)
        ax.text(x + 46, ry, name, fontsize=FS, color=INK, weight="bold" if bold else "normal",
                va="center", zorder=4)
        ax.text(x + w - 10, ry, typ, fontsize=FS - 0.5, color=MUTED, ha="right", va="center", zorder=4)
        ry += ROW_H
    if cons:
        sep = ry - ROW_H / 2 + PAD / 2 + 3
        ax.plot([x + 6, x + w - 6], [sep, sep], color=BORDER, lw=0.8, ls=(0, (3, 2)), zorder=3)
        ry = sep + 3 + PAD / 2 + ROW_H / 2
        for c in cons:
            icon = "PK" if c.startswith("PK") else "UK" if c.startswith("UK") else "FK"
            ax.text(x + 10, ry, icon, fontsize=FS - 1.5, family="monospace", color="#8B1A1A",
                    weight="bold", va="center", zorder=4)
            ax.text(x + 40, ry, c, fontsize=FS - 1, color=MUTED, va="center", zorder=4)
            ry += ROW_H


def draw_legend(ax, x, y, kind):
    items = [
        ("P", "Chave primária (identificador único)"),
        ("U", "Chave única (alternativa)"),
        ("*", "Obrigatório (NOT NULL); sem * = opcional"),
    ]
    if kind == "physical":
        items.insert(1, ("F", "Chave estrangeira"))
    w, h = 470, 36 + len(items) * 20 + 92
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=6",
                                fc="white", ec="#AAAAAA", lw=1, zorder=2))
    ax.text(x + 14, y + 18, "Legenda", fontsize=11, weight="bold", va="center", zorder=4)
    ry = y + 44
    for k, t in items:
        ax.text(x + 18, ry, k, fontsize=FS, family="monospace", weight="bold", color="#8B1A1A", va="center", zorder=4)
        ax.text(x + 46, ry, t, fontsize=FS - 0.5, va="center", zorder=4)
        ry += 20
    # exemplos de cardinalidade
    samples = [(True, "1 e somente 1  ——  0 ou muitos"), (False, "0 ou 1  ——  0 ou muitos")]
    for mand, label in samples:
        ry += 6
        p0, p1 = (x + 18, ry + 8), (x + 168, ry + 8)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=LINE, lw=1.4, zorder=3)
        draw_end(ax, p0, (-1, 0), many=False, mandatory=mand)
        draw_end(ax, p1, (1, 0), many=True, mandatory=False)
        ax.text(x + 190, ry + 8, label, fontsize=FS - 0.5, va="center", zorder=4)
        ry += 30


def render(kind: str, path: str) -> None:
    boxes, height = compute_boxes(kind)
    cw = canvas_w(kind)
    legend_bottom = boxes["INVESTIMENTO"][1] + 200
    height = max(height, legend_bottom + MARGIN)
    fig = plt.figure(figsize=(cw / 100, height / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, cw)
    ax.set_ylim(height, 0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    if kind == "logical":
        title = "FinControl — Modelo Lógico (Entidade-Relacionamento)"
        sub = f"{RM} · Notação: pé-de-galinha (IE) · Tipos lógicos · Chaves estrangeiras representadas pelos relacionamentos"
    else:
        title = "FinControl — Modelo Físico (Oracle Database)"
        sub = f"{RM} · Tabelas, colunas e tipos Oracle · PK / FK / UK com nome de constraint"
    ax.text(MARGIN, 40, title, fontsize=22, weight="bold", color=INK, va="center")
    ax.text(MARGIN, 76, sub, fontsize=12, color=MUTED, va="center")

    for (p, c), pts in routes(boxes).items():
        rel = next(r for r in R if r.parent == p and r.child == c)
        draw_relationship(ax, pts, rel, show_label=(kind == "logical"))

    for e in E:
        x, y, w, h = boxes[e.key]
        if kind == "logical":
            draw_box(ax, x, y, w, h, e.logical, logical_attrs(e), [], LOG_HEAD, LOG_BODY)
        else:
            draw_box(ax, x, y, w, h, e.table, physical_columns(e), physical_constraints(e), PHY_HEAD, PHY_BODY)

    # legenda no espaço livre da última linha (colunas 3-4)
    lx = col_x(kind)[3]
    ly = boxes["INVESTIMENTO"][1]
    draw_legend(ax, lx, ly, kind)

    fig.savefig(path, dpi=220, facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# PDF
# --------------------------------------------------------------------------- #


def build_pdf(images: list[tuple[str, str]], output: str) -> None:
    from PIL import Image

    pdf = FPDF(orientation="L", unit="mm", format="A3")
    pdf.set_auto_page_break(False)
    pw, ph, m = 420, 297, 8
    for title, img in images:
        pdf.add_page()
        iw, ih = Image.open(img).size
        scale = min((pw - 2 * m) / iw, (ph - 2 * m) / ih)
        w, h = iw * scale, ih * scale
        pdf.image(img, x=(pw - w) / 2, y=(ph - h) / 2, w=w, h=h, title=title)
    pdf.output(output)


def main() -> None:
    ddl_path = os.path.join(OUTPUT_DIR, "fincontrol_ddl.sql")
    with open(ddl_path, "w", encoding="utf-8") as f:
        f.write(build_ddl())
    print(f"DDL gerado: {ddl_path}")

    log_png = os.path.join(OUTPUT_DIR, "modelo_logico.png")
    phy_png = os.path.join(OUTPUT_DIR, "modelo_fisico.png")
    render("logical", log_png)
    render("physical", phy_png)
    print(f"Imagens geradas: {log_png}, {phy_png}")

    pdf_path = os.path.join(OUTPUT_DIR, PDF_NAME)
    build_pdf([("Modelo Lógico", log_png), ("Modelo Físico", phy_png)], pdf_path)
    print(f"PDF gerado: {pdf_path}")


if __name__ == "__main__":
    main()
