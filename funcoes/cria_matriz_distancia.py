from funcoes.calcula_dist_euclidiana import calcula_distancia

def cria_matriz_distancia(cidades: list):
    n = len(cidades)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matriz[i][j] = calcula_distancia(cidades[i], cidades[j])
    return matriz