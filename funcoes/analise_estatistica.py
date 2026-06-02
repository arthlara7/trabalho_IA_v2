import time
import statistics

def analise_estatistica(algoritmo_classe, num_execucoes=30, **kwargs):
    """
    Executa um algoritmo várias vezes e retorna estatísticas.

    Parâmetros:
        algoritmo_classe: a classe do algoritmo (ex: AlgoritmoGeneticoTSP)
        num_execucoes: quantas vezes rodar (padrão 30)
        **kwargs: argumentos pra construir o algoritmo

    Retorna um dicionário com:
        media, desvio, melhor, pior, tempo_medio,
        melhor_rota, custos (lista de todos os custos),
        historicos (lista de listas com a convergência de cada execução)
    """
    custos = []
    tempos = []
    historicos = []
    melhor_rota = None
    melhor_custo = float('inf')

    for execucao in range(num_execucoes):
        instancia = algoritmo_classe(**kwargs)

        t0 = time.time()
        rota, custo, historico = instancia.executar()
        tempo = time.time() - t0

        custos.append(custo)
        tempos.append(tempo)
        historicos.append(historico)

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota

        # Feedback de progresso
        print(f"  Execução {execucao + 1:3d}/{num_execucoes}: "
              f"custo = {custo:.4f}, tempo = {tempo:.2f}s")

    return {
        'media': statistics.mean(custos),
        'desvio': statistics.stdev(custos) if len(custos) > 1 else 0.0,
        'melhor': min(custos),
        'pior': max(custos),
        'tempo_medio': statistics.mean(tempos),
        'tempo_total': sum(tempos),
        'melhor_rota': melhor_rota,
        'custos': custos,
        'historicos': historicos,
    }


def imprime_estatisticas(nome_algoritmo, stats):
    """Imprime as estatísticas de um algoritmo de forma formatada."""
    print("-" * 50)
    print(f"RESULTADOS {nome_algoritmo}")
    print("-" * 50)
    print(f"  Melhor custo encontrado : {stats['melhor']:.4f}")
    print(f"  Pior custo encontrado   : {stats['pior']:.4f}")
    print(f"  Média                   : {stats['media']:.4f}")
    print(f"  Desvio padrão           : {stats['desvio']:.4f}")
    print(f"  Tempo médio por execução: {stats['tempo_medio']:.4f} seg")
    print(f"  Tempo total             : {stats['tempo_total']:.2f} seg")
    print(f"  Melhor rota encontrada  : {stats['melhor_rota']}")
    print("-" * 50)


def calcula_historico_medio(historicos):
    """
    Calcula a média de convergência ao longo das iterações.
    Recebe uma lista de históricos (todos do mesmo tamanho)
    e retorna um único histórico médio.
    """
    num_execucoes = len(historicos)
    num_iteracoes = len(historicos[0])

    historico_medio = []
    for iteracao in range(num_iteracoes):
        soma = sum(hist[iteracao] for hist in historicos)
        historico_medio.append(soma / num_execucoes)

    return historico_medio