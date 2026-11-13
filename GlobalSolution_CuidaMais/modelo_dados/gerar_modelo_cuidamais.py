# -*- coding: utf-8 -*-
"""Gera os modelos Lógico e Físico (Oracle) da plataforma Cuida+ (Global Solution).

Uma única definição de entidades/relacionamentos alimenta:
  - diagrama do Modelo Lógico   (modelo_logico.png)
  - diagrama do Modelo Físico   (modelo_fisico.png)
  - script DDL Oracle           (cuidamais_ddl.sql)

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
PDF_NAME = "Modelo_Logico_Fisico_CuidaMais.pdf"

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
        "IDOSO", "IDOSO", "T_CM_IDOSO",
        "Pessoa idosa atendida pela plataforma Cuida+ (usuário principal).",
        [
            pk("Id Idoso", "id_idoso"),
            Attr("Nome", "VARCHAR (100)", "nm_idoso", "VARCHAR2(100)"),
            Attr("CPF", "CHAR (11)", "nr_cpf", "CHAR(11)", uk=True),
            Attr("Data Nascimento", "DATE", "dt_nascimento", "DATE"),
            Attr("Telefone", "VARCHAR (15)", "nr_telefone", "VARCHAR2(15)"),
            Attr("Endereco", "VARCHAR (200)", "ds_endereco", "VARCHAR2(200)"),
            Attr("CEP", "CHAR (8)", "nr_cep", "CHAR(8)"),
            Attr("Acessibilidade", "VARCHAR (255)", "ds_acessibilidade", "VARCHAR2(255)", mandatory=False),
            Attr("Prefere Voz", "CHAR (1)", "st_prefere_voz", "CHAR(1)", default="'S'"),
            Attr("Data Cadastro", "DATE", "dt_cadastro", "DATE", default="SYSDATE"),
            Attr("Ativo", "CHAR (1)", "st_ativo", "CHAR(1)", default="'S'"),
        ],
        uniques=[("UK_IDOSO_CPF", ["nr_cpf"])],
        checks=[("CK_IDOSO_ATIVO", "st_ativo IN ('S', 'N')"),
                ("CK_IDOSO_VOZ", "st_prefere_voz IN ('S', 'N')")],
    ),
    Entity(
        "CUIDADOR", "CUIDADOR", "T_CM_CUIDADOR",
        "Familiar ou cuidador que acompanha um ou mais idosos.",
        [
            pk("Id Cuidador", "id_cuidador"),
            Attr("Nome", "VARCHAR (100)", "nm_cuidador", "VARCHAR2(100)"),
            Attr("E-mail", "VARCHAR (150)", "ds_email", "VARCHAR2(150)", uk=True),
            Attr("Telefone", "VARCHAR (15)", "nr_telefone", "VARCHAR2(15)"),
            Attr("Senha Hash", "VARCHAR (255)", "ds_senha_hash", "VARCHAR2(255)"),
            Attr("Data Cadastro", "DATE", "dt_cadastro", "DATE", default="SYSDATE"),
        ],
        uniques=[("UK_CUIDADOR_EMAIL", ["ds_email"])],
    ),
    Entity(
        "VINCULO", "VINCULO_CUIDADOR", "T_CM_VINCULO_CUIDADOR",
        "Associação N:N entre idoso e cuidador (parentesco e recebimento de alertas).",
        [
            pk("Id Vinculo", "id_vinculo"),
            Attr("Parentesco", "VARCHAR (30)", "ds_parentesco", "VARCHAR2(30)"),
            Attr("Recebe Alerta", "CHAR (1)", "st_recebe_alerta", "CHAR(1)", default="'S'"),
            Attr("Data Inicio", "DATE", "dt_inicio", "DATE", default="SYSDATE"),
        ],
        uniques=[("UK_VINCULO", ["id_idoso", "id_cuidador"])],
        checks=[("CK_VINCULO_ALERTA", "st_recebe_alerta IN ('S', 'N')")],
    ),
    Entity(
        "CATEGORIA", "CATEGORIA_SERVICO", "T_CM_CATEGORIA_SERVICO",
        "Domínio de categorias de prestadores (Saúde, Beleza, Farmácia, Mercado...).",
        [
            pk("Id Categoria", "id_categoria", "NUMBER(3)", "NUMERIC (3)"),
            Attr("Nome", "VARCHAR (50)", "nm_categoria", "VARCHAR2(50)", uk=True),
        ],
        uniques=[("UK_CATEGORIA_NOME", ["nm_categoria"])],
    ),
    Entity(
        "PRESTADOR", "PRESTADOR", "T_CM_PRESTADOR",
        "Médico, clínica, cabeleireiro ou comércio que publica sua agenda na plataforma.",
        [
            pk("Id Prestador", "id_prestador"),
            Attr("Nome", "VARCHAR (120)", "nm_prestador", "VARCHAR2(120)"),
            Attr("CPF/CNPJ", "VARCHAR (14)", "nr_documento", "VARCHAR2(14)", uk=True),
            Attr("E-mail", "VARCHAR (150)", "ds_email", "VARCHAR2(150)", uk=True),
            Attr("Telefone", "VARCHAR (15)", "nr_telefone", "VARCHAR2(15)"),
            Attr("Endereco", "VARCHAR (200)", "ds_endereco", "VARCHAR2(200)"),
            Attr("CEP", "CHAR (8)", "nr_cep", "CHAR(8)"),
            Attr("Senha Hash", "VARCHAR (255)", "ds_senha_hash", "VARCHAR2(255)"),
            Attr("Ativo", "CHAR (1)", "st_ativo", "CHAR(1)", default="'S'"),
        ],
        uniques=[("UK_PRESTADOR_DOC", ["nr_documento"]), ("UK_PRESTADOR_EMAIL", ["ds_email"])],
        checks=[("CK_PRESTADOR_ATIVO", "st_ativo IN ('S', 'N')")],
    ),
    Entity(
        "SERVICO", "SERVICO", "T_CM_SERVICO",
        "Serviço oferecido pelo prestador (consulta, corte de cabelo, entrega...).",
        [
            pk("Id Servico", "id_servico"),
            Attr("Nome", "VARCHAR (100)", "nm_servico", "VARCHAR2(100)"),
            Attr("Duracao (min)", "NUMERIC (3)", "nr_duracao_min", "NUMBER(3)"),
            Attr("Preco", "NUMERIC (8,2)", "vl_preco", "NUMBER(8,2)", mandatory=False),
            Attr("Atende em Casa", "CHAR (1)", "st_domicilio", "CHAR(1)", default="'N'"),
            Attr("Ativo", "CHAR (1)", "st_ativo", "CHAR(1)", default="'S'"),
        ],
        checks=[("CK_SERVICO_DURACAO", "nr_duracao_min > 0"),
                ("CK_SERVICO_PRECO", "vl_preco IS NULL OR vl_preco >= 0"),
                ("CK_SERVICO_DOMICILIO", "st_domicilio IN ('S', 'N')")],
    ),
    Entity(
        "HORARIO", "HORARIO_DISPONIVEL", "T_CM_HORARIO_DISPONIVEL",
        "Janela de horário publicada pelo prestador. L=Livre, R=Reservado, B=Bloqueado.",
        [
            pk("Id Horario", "id_horario", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Data/Hora Inicio", "DATE", "dh_inicio", "DATE"),
            Attr("Data/Hora Fim", "DATE", "dh_fim", "DATE"),
            Attr("Situacao (L/R/B)", "CHAR (1)", "st_horario", "CHAR(1)", default="'L'"),
        ],
        uniques=[("UK_HORARIO", ["id_prestador", "dh_inicio"])],
        checks=[("CK_HORARIO_PERIODO", "dh_fim > dh_inicio"),
                ("CK_HORARIO_SITUACAO", "st_horario IN ('L', 'R', 'B')")],
    ),
    Entity(
        "AGENDAMENTO", "AGENDAMENTO", "T_CM_AGENDAMENTO",
        "Compromisso marcado para o idoso (pela IA, pela web ou pelo cuidador).",
        [
            pk("Id Agendamento", "id_agendamento", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Data Solicitacao", "DATE", "dh_solicitacao", "DATE", default="SYSDATE"),
            Attr("Situacao", "CHAR (1)", "st_agendamento", "CHAR(1)", default="'P'"),
            Attr("Origem (V/W/C)", "CHAR (1)", "tp_origem", "CHAR(1)"),
            Attr("Observacao", "VARCHAR (255)", "ds_observacao", "VARCHAR2(255)", mandatory=False),
            Attr("Lembrete Enviado", "CHAR (1)", "st_lembrete", "CHAR(1)", default="'N'"),
        ],
        uniques=[("UK_AGENDAMENTO_HORARIO", ["id_horario"])],
        checks=[("CK_AGEND_SITUACAO", "st_agendamento IN ('P', 'C', 'R', 'X', 'F', 'N')"),
                ("CK_AGEND_ORIGEM", "tp_origem IN ('V', 'W', 'C')"),
                ("CK_AGEND_LEMBRETE", "st_lembrete IN ('S', 'N')")],
    ),
    Entity(
        "MEDICAMENTO", "MEDICAMENTO", "T_CM_MEDICAMENTO",
        "Medicamento em uso pelo idoso (cadastrado pelo próprio idoso ou pelo cuidador).",
        [
            pk("Id Medicamento", "id_medicamento"),
            Attr("Nome", "VARCHAR (100)", "nm_medicamento", "VARCHAR2(100)"),
            Attr("Dosagem", "VARCHAR (50)", "ds_dosagem", "VARCHAR2(50)"),
            Attr("Instrucao", "VARCHAR (255)", "ds_instrucao", "VARCHAR2(255)", mandatory=False),
            Attr("Data Inicio", "DATE", "dt_inicio", "DATE"),
            Attr("Data Fim", "DATE", "dt_fim", "DATE", mandatory=False),
            Attr("Ativo", "CHAR (1)", "st_ativo", "CHAR(1)", default="'S'"),
        ],
        checks=[("CK_MEDICAMENTO_DATAS", "dt_fim IS NULL OR dt_fim >= dt_inicio"),
                ("CK_MEDICAMENTO_ATIVO", "st_ativo IN ('S', 'N')")],
    ),
    Entity(
        "HORARIO_MED", "HORARIO_MEDICAMENTO", "T_CM_HORARIO_MEDICAMENTO",
        "Horário de dose programado (ex.: 08:00, todos os dias = '1111111').",
        [
            pk("Id Horario Med", "id_horario_med"),
            Attr("Hora Dose", "CHAR (5)", "hr_dose", "CHAR(5)"),
            Attr("Dias Semana", "CHAR (7)", "ds_dias_semana", "CHAR(7)", default="'1111111'"),
        ],
        uniques=[("UK_HORARIO_MED", ["id_medicamento", "hr_dose"])],
    ),
    Entity(
        "REGISTRO_DOSE", "REGISTRO_DOSE", "T_CM_REGISTRO_DOSE",
        "Histórico de cada dose: T=Tomada, E=Esquecida, A=Adiada, P=Pendente. Base da IA de adesão.",
        [
            pk("Id Registro", "id_registro", "NUMBER(14)", "NUMERIC (14)"),
            Attr("Data/Hora Prevista", "DATE", "dh_prevista", "DATE"),
            Attr("Data/Hora Confirmacao", "DATE", "dh_confirmacao", "DATE", mandatory=False),
            Attr("Situacao", "CHAR (1)", "st_dose", "CHAR(1)", default="'P'"),
            Attr("Forma Confirmacao", "CHAR (1)", "tp_confirmacao", "CHAR(1)", mandatory=False),
        ],
        uniques=[("UK_REGISTRO_DOSE", ["id_horario_med", "dh_prevista"])],
        checks=[("CK_DOSE_SITUACAO", "st_dose IN ('P', 'T', 'E', 'A')"),
                ("CK_DOSE_CONFIRMACAO", "tp_confirmacao IS NULL OR tp_confirmacao IN ('V', 'B', 'C')")],
    ),
    Entity(
        "ALERTA", "ALERTA", "T_CM_ALERTA",
        "Alerta enviado aos cuidadores. D=Dose esquecida, F=Falta, R=Risco (IA), A=Agendamento.",
        [
            pk("Id Alerta", "id_alerta", "NUMBER(12)", "NUMERIC (12)"),
            Attr("Tipo", "CHAR (1)", "tp_alerta", "CHAR(1)"),
            Attr("Mensagem", "VARCHAR (255)", "ds_mensagem", "VARCHAR2(255)"),
            Attr("Score Risco (IA)", "NUMERIC (3,2)", "nr_score_risco", "NUMBER(3,2)", mandatory=False),
            Attr("Data Geracao", "DATE", "dh_geracao", "DATE", default="SYSDATE"),
            Attr("Lido", "CHAR (1)", "st_lido", "CHAR(1)", default="'N'"),
        ],
        checks=[("CK_ALERTA_TIPO", "tp_alerta IN ('D', 'F', 'R', 'A')"),
                ("CK_ALERTA_SCORE", "nr_score_risco IS NULL OR nr_score_risco BETWEEN 0 AND 1"),
                ("CK_ALERTA_LIDO", "st_lido IN ('S', 'N')")],
    ),
    Entity(
        "INTERACAO_IA", "INTERACAO_IA", "T_CM_INTERACAO_IA",
        "Registro de cada conversa com a assistente: intenção identificada e resultado.",
        [
            pk("Id Interacao", "id_interacao", "NUMBER(14)", "NUMERIC (14)"),
            Attr("Data/Hora", "DATE", "dh_interacao", "DATE", default="SYSDATE"),
            Attr("Canal (W/Z)", "CHAR (1)", "tp_canal", "CHAR(1)"),
            Attr("Transcricao", "VARCHAR (4000)", "ds_transcricao", "VARCHAR2(4000)"),
            Attr("Intencao", "VARCHAR (30)", "ds_intencao", "VARCHAR2(30)"),
            Attr("Confianca", "NUMERIC (3,2)", "nr_confianca", "NUMBER(3,2)", mandatory=False),
            Attr("Resolvida", "CHAR (1)", "st_resolvida", "CHAR(1)", default="'N'"),
        ],
        checks=[("CK_INTERACAO_CANAL", "tp_canal IN ('W', 'Z')"),
                ("CK_INTERACAO_RESOLVIDA", "st_resolvida IN ('S', 'N')")],
    ),
]
ENT = {e.key: e for e in E}

R = [
    Rel("IDOSO", "VINCULO", "id_idoso", True, "possui"),
    Rel("CUIDADOR", "VINCULO", "id_cuidador", True, "acompanha"),
    Rel("CATEGORIA", "PRESTADOR", "id_categoria", True, "classifica"),
    Rel("PRESTADOR", "SERVICO", "id_prestador", True, "oferece"),
    Rel("PRESTADOR", "HORARIO", "id_prestador", True, "publica"),
    Rel("IDOSO", "AGENDAMENTO", "id_idoso", True, "marca"),
    Rel("SERVICO", "AGENDAMENTO", "id_servico", True, "é agendado"),
    Rel("HORARIO", "AGENDAMENTO", "id_horario", True, "reserva"),
    Rel("IDOSO", "MEDICAMENTO", "id_idoso", True, "utiliza"),
    Rel("CUIDADOR", "MEDICAMENTO", "id_cuidador", False, "cadastra"),
    Rel("MEDICAMENTO", "HORARIO_MED", "id_medicamento", True, "programa"),
    Rel("HORARIO_MED", "REGISTRO_DOSE", "id_horario_med", True, "gera"),
    Rel("IDOSO", "ALERTA", "id_idoso", True, "origina"),
    Rel("IDOSO", "INTERACAO_IA", "id_idoso", True, "conversa"),
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
        "-- Cuida+ - Modelo Físico (Oracle Database 19c+)",
        f"-- {RM} | Gerado por gerar_modelo_cuidamais.py",
        "-- Pode ser executado no SQL Developer ou importado no Oracle Data Modeler",
        "-- (File > Import > DDL File) para gerar os diagramas relacional/lógico.",
        "-- =====================================================================",
        "",
        "-- Remoção (ordem inversa das dependências) --------------------------",
    ]
    order = ["INTERACAO_IA", "ALERTA", "REGISTRO_DOSE", "HORARIO_MED", "MEDICAMENTO",
             "AGENDAMENTO", "HORARIO", "SERVICO", "PRESTADOR", "CATEGORIA", "VINCULO",
             "CUIDADOR", "IDOSO"]
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
    L.append("CREATE INDEX IX_HORARIO_LIVRE ON T_CM_HORARIO_DISPONIVEL (st_horario, dh_inicio);")
    L.append("CREATE INDEX IX_DOSE_PREVISTA ON T_CM_REGISTRO_DOSE (dh_prevista, st_dose);")
    L.append("")
    L.append("-- Dados de domínio ---------------------------------------------------")
    for cat in ["Saude", "Beleza e Estetica", "Farmacia", "Mercado", "Servicos Domesticos", "Bem-estar"]:
        L.append(f"INSERT INTO T_CM_CATEGORIA_SERVICO (nm_categoria) VALUES ('{cat}');")
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
    "CATEGORIA": (0, 0), "SERVICO": (1, 0), "PRESTADOR": (2, 0), "HORARIO": (3, 0),
    "INTERACAO_IA": (0, 1), "IDOSO": (1, 1), "AGENDAMENTO": (2, 1), "REGISTRO_DOSE": (4, 1),
    "ALERTA": (0, 2), "VINCULO": (1, 2), "CUIDADOR": (2, 2), "MEDICAMENTO": (3, 2), "HORARIO_MED": (4, 2),
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

    i = "IDOSO"
    r1 = y(i)                       # topo da linha 1
    r2 = y("VINCULO")               # topo da linha 2
    top_ch = y("PRESTADOR") - 35
    hy0 = y("PRESTADOR") + 45
    hy1 = r1 + 45
    hy2 = r2 + 45
    ag = "AGENDAMENTO"
    return {
        ("CATEGORIA", "PRESTADOR"): [(cx("CATEGORIA"), y("CATEGORIA")), (cx("CATEGORIA"), top_ch),
                                     (cx("PRESTADOR"), top_ch), (cx("PRESTADOR"), y("PRESTADOR"))],
        ("PRESTADOR", "SERVICO"): [(x("PRESTADOR"), hy0), (right("SERVICO"), hy0)],
        ("PRESTADOR", "HORARIO"): [(right("PRESTADOR"), hy0), (x("HORARIO"), hy0)],
        ("SERVICO", ag): [(cx("SERVICO"), bottom("SERVICO")), (cx("SERVICO"), r1 - 45),
                          (x(ag) + 80, r1 - 45), (x(ag) + 80, y(ag))],
        ("HORARIO", ag): [(cx("HORARIO"), bottom("HORARIO")), (cx("HORARIO"), r1 - 75),
                          (right(ag) - 80, r1 - 75), (right(ag) - 80, y(ag))],
        (i, ag): [(right(i), hy1), (x(ag), hy1)],
        (i, "INTERACAO_IA"): [(x(i), hy1), (right("INTERACAO_IA"), hy1)],
        (i, "VINCULO"): [(cx(i), bottom(i)), (cx(i), y("VINCULO"))],
        (i, "ALERTA"): [(x(i) + 60, bottom(i)), (x(i) + 60, r2 - 45), (cx("ALERTA"), r2 - 45),
                        (cx("ALERTA"), y("ALERTA"))],
        (i, "MEDICAMENTO"): [(right(i) - 60, bottom(i)), (right(i) - 60, r2 - 75), (cx("MEDICAMENTO"), r2 - 75),
                             (cx("MEDICAMENTO"), y("MEDICAMENTO"))],
        ("CUIDADOR", "VINCULO"): [(x("CUIDADOR"), hy2), (right("VINCULO"), hy2)],
        ("CUIDADOR", "MEDICAMENTO"): [(right("CUIDADOR"), hy2), (x("MEDICAMENTO"), hy2)],
        ("MEDICAMENTO", "HORARIO_MED"): [(right("MEDICAMENTO"), hy2), (x("HORARIO_MED"), hy2)],
        ("HORARIO_MED", "REGISTRO_DOSE"): [(cx("HORARIO_MED"), y("HORARIO_MED")),
                                           (cx("REGISTRO_DOSE"), bottom("REGISTRO_DOSE"))],
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
    legend_bottom = 140 + 260
    height = max(height, legend_bottom + MARGIN)
    fig = plt.figure(figsize=(cw / 100, height / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, cw)
    ax.set_ylim(height, 0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    if kind == "logical":
        title = "Cuida+ — Modelo Lógico (Entidade-Relacionamento)"
        sub = f"{RM} · Notação: pé-de-galinha (IE) · Tipos lógicos · Chaves estrangeiras representadas pelos relacionamentos"
    else:
        title = "Cuida+ — Modelo Físico (Oracle Database)"
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
    lx = cw - MARGIN - 470
    ly = boxes["HORARIO"][1]
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
    ddl_path = os.path.join(OUTPUT_DIR, "cuidamais_ddl.sql")
    with open(ddl_path, "w", encoding="utf-8") as f:
        f.write(build_ddl())
    print(f"DDL gerado: {ddl_path}")

    log_png = os.path.join(OUTPUT_DIR, "modelo_logico.png")
    phy_png = os.path.join(OUTPUT_DIR, "modelo_fisico.png")
    render("logical", log_png)
    render("physical", phy_png)
    print(f"Imagens geradas: {log_png}, {phy_png}")



if __name__ == "__main__":
    main()
