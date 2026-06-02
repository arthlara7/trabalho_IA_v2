from funcoes.cria_matriz_distancia import cria_matriz_distancia
from funcoes.cria_grafico import plot_convergencia_comparacao, plot_rotas_comparacao
from funcoes.analise_estatistica import (
    analise_estatistica,
    imprime_estatisticas,
    calcula_historico_medio,
    calcula_historico_desvio,
    teste_mann_whitney,
)
from funcoes.ler_instancia import le_arquivo
from algoritmo_pso import AlgoritmoPSO_TSP
from algoritmo_ga import AlgoritmoGeneticoTSP


def main():
    num_cidades, cidades = le_arquivo("instancia.txt")
    matriz_distancias = cria_matriz_distancia(cidades)

    iteracoes = 500
    tamanho_populacao = 100
    num_execucoes = 30
    parada_estagnacao = 100

    print(f"Comparação GA vs PSO")
    print(f"  Cidades              : {num_cidades}")
    print(f"  Iterações máx        : {iteracoes}")
    print(f"  População            : {tamanho_populacao}")
    print(f"  Execuções por algor. : {num_execucoes}")
    print(f"  Parada por estagnação: {parada_estagnacao} iterações")
    print()

    # ===== GA =====
    print("Rodando GA...")
    stats_ga = analise_estatistica(
        AlgoritmoGeneticoTSP,
        num_execucoes=num_execucoes,
        num_cidades=num_cidades,
        matriz_distancias=matriz_distancias,
        tamanho_populacao=tamanho_populacao,
        taxa_crossover=0.85,
        geracoes=iteracoes,
        geracoes_sem_melhora_max=parada_estagnacao,
    )
    imprime_estatisticas("GA", stats_ga)

    # ===== PSO =====
    print("\nRodando PSO...")
    stats_pso = analise_estatistica(
        AlgoritmoPSO_TSP,
        num_execucoes=num_execucoes,
        num_cidades=num_cidades,
        matriz_distancias=matriz_distancias,
        num_particulas=tamanho_populacao,
        iteracoes=iteracoes,
        iteracoes_sem_melhora_max=parada_estagnacao,
    )
    imprime_estatisticas("PSO", stats_pso)

    # ===== Teste estatístico =====
    teste_mann_whitney(stats_ga['custos'], stats_pso['custos'], "GA", "PSO")

    # ===== Gráficos =====
    hist_medio_ga = calcula_historico_medio(stats_ga['historicos'])
    hist_desvio_ga = calcula_historico_desvio(stats_ga['historicos'])
    hist_medio_pso = calcula_historico_medio(stats_pso['historicos'])
    hist_desvio_pso = calcula_historico_desvio(stats_pso['historicos'])

    print("\nGerando gráficos...")

    plot_convergencia_comparacao(
        hist_medio_ga, hist_medio_pso,
        hist_desvio_ga, hist_desvio_pso,
        titulo="Convergência Média (30 execuções) com Desvio Padrão"
    )

    plot_rotas_comparacao(cidades, stats_ga['melhor_rota'], stats_pso['melhor_rota'])

    print("\nGráficos salvos em PNG e PDF na pasta atual.")


if __name__ == "__main__":
    main()