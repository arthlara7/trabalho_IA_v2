from funcoes.cria_matriz_distancia import cria_matriz_distancia
from funcoes.cria_grafico import plot_convergencia_comparacao, plot_rotas_comparacao
from funcoes.analise_estatistica import analise_estatistica, imprime_estatisticas, calcula_historico_medio
from funcoes.ler_instancia import le_arquivo
from algoritmo_pso import AlgoritmoPSO_TSP
from algoritmo_ga import AlgoritmoGeneticoTSP


def main():
    # Lê a instância do arquivo
    num_cidades, cidades = le_arquivo("instancia.txt")
    matriz_distancias = cria_matriz_distancia(cidades)

    # Configurações dos experimentos
    iteracoes = 500
    tamanho_populacao = 100
    num_execucoes = 30

    print(f"Comparação GA vs PSO")
    print(f"  Cidades        : {num_cidades}")
    print(f"  Iterações      : {iteracoes}")
    print(f"  População      : {tamanho_populacao}")
    print(f"  Execuções p/alg: {num_execucoes}")
    print()

    # ===== Análise estatística GA =====
    print("Rodando GA...")
    stats_ga = analise_estatistica(
        AlgoritmoGeneticoTSP,
        num_execucoes=num_execucoes,
        num_cidades=num_cidades,
        matriz_distancias=matriz_distancias,
        tamanho_populacao=tamanho_populacao,
        taxa_mutacao=0.1,
        taxa_crossover=0.85,
        geracoes=iteracoes,
        geracoes_sem_melhora_max=100,  # para se ficar 100 gerações sem melhorar
    )
    imprime_estatisticas("GA", stats_ga)

    # ===== Análise estatística PSO =====
    print("\nRodando PSO...")
    stats_pso = analise_estatistica(
        AlgoritmoPSO_TSP,
        num_execucoes=num_execucoes,
        num_cidades=num_cidades,
        matriz_distancias=matriz_distancias,
        num_particulas=tamanho_populacao,
        iteracoes=iteracoes,
    )
    imprime_estatisticas("PSO", stats_pso)

    # ===== Gráficos =====
    # Histórico médio das 30 execuções (mais robusto que uma única execução)
    hist_medio_ga = calcula_historico_medio(stats_ga['historicos'])
    hist_medio_pso = calcula_historico_medio(stats_pso['historicos'])

    plot_convergencia_comparacao(hist_medio_ga, hist_medio_pso,
                                  titulo="Convergência Média (30 execuções)")
    plot_rotas_comparacao(cidades, stats_ga['melhor_rota'], stats_pso['melhor_rota'])


if __name__ == "__main__":
    main()