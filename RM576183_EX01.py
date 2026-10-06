# -*- coding: utf-8 -*-
# RM576183 - Exercício 01
# Bidu: votação do melhor dia para lives de mentoria financeira

num_colaboradores = int(input("Informe o número de colaboradores: "))

segunda = 0
terca = 0
quarta = 0
quinta = 0
sexta = 0

for _ in range(num_colaboradores):
    dia_valido = False

    while not dia_valido:
        dia = input(
            "Informe o dia da sua preferência (segunda-feira, terça-feira, "
            "quarta-feira, quinta-feira, sexta-feira): "
        ).strip().lower()

        if dia in ("segunda-feira", "segunda"):
            segunda += 1
            dia_valido = True
        elif dia in ("terça-feira", "terca-feira", "terça", "terca"):
            terca += 1
            dia_valido = True
        elif dia in ("quarta-feira", "quarta"):
            quarta += 1
            dia_valido = True
        elif dia in ("quinta-feira", "quinta"):
            quinta += 1
            dia_valido = True
        elif dia in ("sexta-feira", "sexta"):
            sexta += 1
            dia_valido = True
        else:
            print("Dia inválido. Use um dos dias informados no enunciado.")

maior_votacao = segunda
if terca > maior_votacao:
    maior_votacao = terca
if quarta > maior_votacao:
    maior_votacao = quarta
if quinta > maior_votacao:
    maior_votacao = quinta
if sexta > maior_votacao:
    maior_votacao = sexta

dias_empatados = []

if segunda == maior_votacao and maior_votacao > 0:
    dias_empatados.append("segunda-feira")
if terca == maior_votacao and maior_votacao > 0:
    dias_empatados.append("terça-feira")
if quarta == maior_votacao and maior_votacao > 0:
    dias_empatados.append("quarta-feira")
if quinta == maior_votacao and maior_votacao > 0:
    dias_empatados.append("quinta-feira")
if sexta == maior_votacao and maior_votacao > 0:
    dias_empatados.append("sexta-feira")

if len(dias_empatados) == 0:
    print("Nenhum voto válido foi registrado.")
elif len(dias_empatados) == 1:
    print(f"O dia escolhido pelos colaboradores é: {dias_empatados[0]}")
else:
    print("Houve empate entre os colaboradores nos dias:")
    for dia_escolhido in dias_empatados:
        print(dia_escolhido)
