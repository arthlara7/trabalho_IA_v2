import os
from funcoes.cria_matriz_distancia import cria_matriz_distancia
from funcoes.cria_grafico import (
    plot_convergencia_comparacao,
    plot_rotas_comparacao,
)
from funcoes.analise_estatistica import (
    analise_estatistica,
    imprime_estatisticas,
    calcula_historico_medio,
    teste_mann_whitney,
)
from funcoes.ler_instancia import le_arquivo
from algoritmo_pso import AlgoritmoPSO_TSP
from algoritmo_ga import AlgoritmoGeneticoTSP
from funcoes.salva_estatistica import salva_estatisticas_txt

def rodar_experimento(caminho_instancia, pasta_resultados,
                       iteracoes=500, tamanho_populacao=100,
                       num_execucoes=30, parada_estagnacao=100):
    """Roda GA vs PSO para uma única instância e salva resultados."""

    # Cria pasta de resultados se não existir
    os.makedirs(pasta_resultados, exist_ok=True)

    num_cidades, cidades = le_arquivo(caminho_instancia)
    matriz_distancias = cria_matriz_distancia(cidades)

    nome_instancia = os.path.basename(caminho_instancia).replace('.txt', '')

    print("=" * 60)
    print(f"INSTÂNCIA: {nome_instancia} ({num_cidades} cidades)")
    print("=" * 60)
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
    resultado_teste = teste_mann_whitney(
        stats_ga['custos'], stats_pso['custos'], "GA", "PSO"
    )

    # ===== Salva estatísticas em arquivo =====
    caminho_stats = os.path.join(pasta_resultados, 'estatisticas.txt')
    salva_estatisticas_txt(caminho_stats, nome_instancia, num_cidades,
                            stats_ga, stats_pso, resultado_teste)

    # ===== Gráficos =====
    hist_medio_ga = calcula_historico_medio(stats_ga['historicos'])
    hist_medio_pso = calcula_historico_medio(stats_pso['historicos'])

    print(f"\nSalvando gráficos em {pasta_resultados}/")

    # Os gráficos salvam na pasta atual; mudamos o diretório temporariamente
    diretorio_original = os.getcwd()
    os.chdir(pasta_resultados)
    try:
        plot_convergencia_comparacao(
            hist_medio_ga, hist_medio_pso, titulo=f"Convergência - {nome_instancia} ({num_cidades} cidades)"
        )
        plot_rotas_comparacao(
            cidades, stats_ga['melhor_rota'], stats_pso['melhor_rota'],
            titulo=f"Melhores Rotas - {nome_instancia}"
        )
    
    finally:
        os.chdir(diretorio_original)
