import math

def calcula_distancia(cidade_a: tuple, cidade_b: tuple):
    return math.sqrt((cidade_a[0] - cidade_b[0])**2 + (cidade_a[1] - cidade_b[1])**2)
