# -*- coding: utf-8 -*-
"""Gera PDF da atividade de Casos de Uso - Fintech FinControl."""

from __future__ import annotations

import os
import tempfile

import matplotlib.pyplot as plt
from fpdf import FPDF
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle

FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\ariali.ttf"
OUTPUT_DIR = r"C:\Users\wfix_\OneDrive\Documentos\Automation\FIAP\FIAP"
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Atividade_Casos_de_Uso_Fintech.pdf")


def create_use_case_diagram(image_path: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Limite do sistema
    system_box = FancyBboxPatch(
        (3.2, 0.6),
        8.3,
        6.8,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        linewidth=1.5,
        edgecolor="#333333",
        facecolor="#F8FBFF",
    )
    ax.add_patch(system_box)
    ax.text(7.35, 7.15, "FinControl", ha="center", va="center", fontsize=13, weight="bold")
    ax.text(7.35, 6.85, "Sistema de Controle Financeiro Pessoal", ha="center", va="center", fontsize=9)

    use_cases = [
        (7.35, 6.0, "Registrar Gasto"),
        (7.35, 5.0, "Categorizar Gasto"),
        (7.35, 4.0, "Visualizar Resumo Mensal"),
        (7.35, 3.0, "Editar ou Excluir Gasto"),
        (7.35, 2.0, "Filtrar Gastos"),
        (7.35, 1.0, "Autenticar-se"),
    ]

    ellipse_width = 4.8
    ellipse_height = 0.72
    actor_x = 1.35
    actor_y = 4.0

    # Ator principal (stick figure simplificado)
    ax.add_patch(Circle((actor_x, actor_y + 1.0), 0.28, fill=False, linewidth=1.5, edgecolor="#222222"))
    ax.plot([actor_x, actor_x], [actor_y + 0.72, actor_y + 0.15], color="#222222", linewidth=1.5)
    ax.plot([actor_x - 0.45, actor_x + 0.45], [actor_y + 0.55, actor_y + 0.55], color="#222222", linewidth=1.5)
    ax.plot([actor_x, actor_x - 0.35], [actor_y + 0.15, actor_y - 0.45], color="#222222", linewidth=1.5)
    ax.plot([actor_x, actor_x + 0.35], [actor_y + 0.15, actor_y - 0.45], color="#222222", linewidth=1.5)
    ax.text(actor_x, actor_y - 0.85, "Usuário do\nAplicativo", ha="center", va="top", fontsize=10, weight="bold")

    for cx, cy, label in use_cases:
        ellipse = Ellipse(
            (cx, cy),
            ellipse_width,
            ellipse_height,
            linewidth=1.4,
            edgecolor="#1F4E79",
            facecolor="#FFFFFF",
        )
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, ha="center", va="center", fontsize=9.5)

        # Associação ator -> caso de uso
        ax.plot(
            [actor_x + 0.35, cx - ellipse_width / 2],
            [actor_y + 0.55, cy],
            color="#555555",
            linewidth=1.0,
        )

    ax.set_title(
        "Diagrama de Casos de Uso – FinControl (MVP)",
        fontsize=14,
        weight="bold",
        pad=16,
    )

    plt.tight_layout()
    plt.savefig(image_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


class AtividadePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial", "", FONT_REGULAR)
        self.add_font("Arial", "B", FONT_BOLD)
        self.add_font("Arial", "I", FONT_ITALIC)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def section_title(self, title: str) -> None:
        self.ln(2)
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 240, 255)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def field(self, label: str, value: str) -> None:
        self.set_font("Arial", "B", 10)
        self.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 10)
        self.multi_cell(self.epw, 5, value)
        self.ln(1)

    def numbered_list(self, items: list[str]) -> None:
        self.set_font("Arial", "", 10)
        for i, item in enumerate(items, 1):
            self.set_x(self.l_margin)
            self.multi_cell(self.epw, 5, f"{i}. {item}")
            self.ln(0.5)


def build_pdf(output_path: str, diagram_path: str) -> None:
    pdf = AtividadePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        0,
        10,
        "Casos de Uso – Fintech FinControl",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C",
    )
    pdf.set_font("Arial", "", 10)
    pdf.cell(
        0,
        6,
        "Atividade – Capítulo 8 | Organização financeira pessoal (MVP)",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C",
    )
    pdf.ln(4)

    pdf.section_title("1. Diagrama de Casos de Uso")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "O diagrama abaixo apresenta o ator principal Usuário do Aplicativo e seis casos de uso "
        "compatíveis com o escopo do FinControl, seguindo a notação UML com elipses, ator e "
        "associações entre eles.",
    )
    pdf.ln(2)
    pdf.image(diagram_path, x=10, w=190)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Atores identificados:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(pdf.epw, 5, "- Usuário do Aplicativo (ator principal)")
    pdf.ln(1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Casos de uso identificados:", new_x="LMARGIN", new_y="NEXT")
    pdf.numbered_list(
        [
            "Registrar Gasto",
            "Categorizar Gasto",
            "Visualizar Resumo Mensal",
            "Editar ou Excluir Gasto",
            "Filtrar Gastos",
            "Autenticar-se",
        ]
    )

    pdf.add_page()
    pdf.section_title("2. Documento Descritivo do Caso de Uso")

    pdf.field(
        "Nome do Caso de Uso:",
        "Registrar Gasto",
    )
    pdf.field(
        "Breve descrição:",
        "Permite que o usuário do aplicativo registre uma despesa informando valor, data, "
        "descrição e, quando aplicável, categoria. Esse caso de uso é fundamental para construir "
        "o histórico financeiro e alimentar demais funcionalidades do FinControl, como resumos "
        "e filtros.",
    )
    pdf.field(
        "Atores envolvidos:",
        "Usuário do Aplicativo (ator principal).\nSistema FinControl (ator secundário, responsável "
        "por validar, persistir e exibir os dados).",
    )
    pdf.field(
        "Pré-condições:",
        "- O usuário deve estar autenticado no aplicativo.\n"
        "- O usuário deve possuir acesso à funcionalidade de lançamentos.\n"
        "- O sistema deve estar disponível para receber novos registros.",
    )
    pdf.field(
        "Pós-condições:",
        "- O gasto é armazenado com sucesso no histórico financeiro do usuário.\n"
        "- O resumo de gastos do período é atualizado.\n"
        "- O usuário visualiza confirmação do registro realizado.",
    )

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Fluxo principal:", new_x="LMARGIN", new_y="NEXT")
    pdf.numbered_list(
        [
            "O usuário acessa a tela de lançamentos do FinControl.",
            "O usuário seleciona a opção Registrar Gasto.",
            "O sistema exibe o formulário de cadastro de despesa.",
            "O usuário informa valor, data, descrição e categoria (se disponível).",
            "O usuário confirma o registro.",
            "O sistema valida os dados informados.",
            "O sistema salva o gasto no histórico financeiro.",
            "O sistema exibe mensagem de sucesso e atualiza a listagem de movimentações.",
        ]
    )
    pdf.ln(1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Fluxos alternativos:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "FA1 – Cancelamento do registro", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "3a. Durante o preenchimento, o usuário cancela a operação.\n"
        "4a. O sistema descarta as informações não confirmadas.\n"
        "5a. O sistema retorna à tela anterior sem registrar o gasto.",
    )
    pdf.ln(1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "FA2 – Registro sem categoria obrigatória", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "4a. O usuário informa os campos obrigatórios, mas não seleciona categoria.\n"
        "5a. O sistema permite salvar o gasto com categoria padrão \"Outros\".\n"
        "6a. O fluxo retorna ao passo 7 do fluxo principal.",
    )
    pdf.ln(1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Exceções:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "E1 – Dados inválidos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "6a. O sistema identifica valor ausente, zero, negativo ou data inválida.\n"
        "7a. O sistema exibe mensagem de erro indicando o campo incorreto.\n"
        "8a. O usuário corrige os dados e o fluxo retorna ao passo 5.",
    )
    pdf.ln(1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "E2 – Falha ao salvar o registro", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "7a. Ocorre indisponibilidade do serviço ou erro de persistência.\n"
        "8a. O sistema informa que não foi possível concluir o registro.\n"
        "9a. O usuário pode tentar novamente ou retornar à tela anterior.",
    )

    pdf.output(output_path)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        diagram = os.path.join(tmp, "diagrama_casos_de_uso.png")
        create_use_case_diagram(diagram)
        build_pdf(OUTPUT_PDF, diagram)
    print(f"PDF gerado: {OUTPUT_PDF}")
