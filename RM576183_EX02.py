# -*- coding: utf-8 -*-
# RM576183 - Exercício 02
# Tabela de preço à vista e parcelado para compra de veículo

preco_carro = float(input("Digite o preço do carro: "))

preco_vista = preco_carro * 0.80
print(f"O preço final á vista com desconto 20% é:{preco_vista}")

parcelas = 6
while parcelas <= 60:
    percentual_acrescimo = (parcelas // 6) * 3
    preco_final = preco_carro * (1 + percentual_acrescimo / 100)
    valor_parcela = preco_final / parcelas

    preco_final_formatado = f"{preco_final:.2f}".replace(".", ",")
    valor_parcela_formatado = f"{valor_parcela:.2f}".replace(".", ",")

    print(
        f"O preço final parcelado em {parcelas} é de R$ {preco_final_formatado} "
        f"com parcelas de R$ {valor_parcela_formatado}"
    )

    parcelas += 6
