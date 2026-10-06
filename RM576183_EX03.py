# -*- coding: utf-8 -*-
# RM576183 - Exercício 03
# Tabela de dívida, juros e parcelas - produto de crédito Fintech

valor_divida = float(input("Digite o valor da dívida: "))

indice = 0
while indice < 5:
    if indice == 0:
        numero_parcelas = 1
        percentual_juros = 0
    elif indice == 1:
        numero_parcelas = 3
        percentual_juros = 10
    elif indice == 2:
        numero_parcelas = 6
        percentual_juros = 15
    elif indice == 3:
        numero_parcelas = 9
        percentual_juros = 20
    else:
        numero_parcelas = 12
        percentual_juros = 25

    juros = valor_divida * (percentual_juros / 100)
    total = valor_divida + juros
    valor_parcela = total / numero_parcelas

    total_formatado = f"{total:.2f}".replace(".", ",")
    juros_formatado = f"{juros:.2f}".replace(".", ",")
    parcela_formatada = f"{valor_parcela:.2f}".replace(".", ",")

    print(
        f"Total:R$ {total_formatado} Juros:R$ {juros_formatado} "
        f"Número de parcelas:{numero_parcelas} Valor da Parcela:R$ {parcela_formatada}"
    )

    indice += 1
