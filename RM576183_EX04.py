# -*- coding: utf-8 -*-
# RM576183 - Exercício 04
# Cálculo de IR sobre resgate de investimentos (CDB, LCI, LCA)

print("Escolha o tipo de investimento:")
print("1. CDB")
print("2. LCI")
print("3. LCA")

tipo_investimento_valido = False

while not tipo_investimento_valido:
    tipo_investimento = int(input("Digite o tipo de investimento (1, 2 ou 3): "))

    if tipo_investimento == 1 or tipo_investimento == 2 or tipo_investimento == 3:
        tipo_investimento_valido = True
    else:
        print("Tipo de investimento inválido. Digite 1, 2 ou 3.")

valor_resgate = float(input("Digite o valor a ser resgatado: "))
dias_investidos = int(input("Digite o número de dias que o valor permaneceu investido: "))

imposto_renda = 0.0

if tipo_investimento == 1:
    if dias_investidos <= 180:
        aliquota = 22.5
    elif dias_investidos <= 360:
        aliquota = 20
    elif dias_investidos <= 720:
        aliquota = 17.5
    else:
        aliquota = 15

    imposto_renda = valor_resgate * (aliquota / 100)

print(f"O valor do imposto de renda a ser pago é: R$ {imposto_renda:.2f}")
