def calcula_custo_total(rota: list, matriz_distancia: list):
    acumulador = 0.0
    n = len(rota)
    for i in range(n):
        if i == n - 1:
            acumulador += matriz_distancia[rota[i]][rota[0]]
        else:
            acumulador += matriz_distancia[rota[i]][rota[i+1]]
    return acumulador