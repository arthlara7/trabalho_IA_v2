def le_arquivo(caminho:str):
    with open(caminho, "r") as arquivo:      
        cidades = []
        num_cidades = int(arquivo.readline())
        while True:
            linha = arquivo.readline()
            if not linha:
                break
            valores = linha.split()
            n = [int(valor) for valor in valores]
            cidades.append(tuple(n))
    return num_cidades, cidades