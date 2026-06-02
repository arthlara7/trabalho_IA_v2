import argparse
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
from roda_experimento import rodar_experimento
from funcoes.salva_estatistica import salva_estatisticas_txt


def main():
    parser = argparse.ArgumentParser(
        description='Compara GA vs PSO para o Problema do Caixeiro Viajante'
    )
    parser.add_argument(
        'instancia', nargs='?', default=None,
        help='Caminho do arquivo de instância. '
             'Se omitido, roda todas em instancias/'
    )
    parser.add_argument(
        '--execucoes', type=int, default=30,
        help='Número de execuções por algoritmo (padrão: 30)'
    )
    parser.add_argument(
        '--iteracoes', type=int, default=500,
        help='Número máximo de iterações (padrão: 500)'
    )
    parser.add_argument(
        '--populacao', type=int, default=100,
        help='Tamanho da população (padrão: 100)'
    )

    args = parser.parse_args()

    if args.instancia:
        # Modo single: roda uma instância específica
        nome_base = os.path.basename(args.instancia).replace('.txt', '')
        pasta_resultados = os.path.join('resultados', nome_base)

        rodar_experimento(
            args.instancia,
            pasta_resultados,
            iteracoes=args.iteracoes,
            tamanho_populacao=args.populacao,
            num_execucoes=args.execucoes,
        )
    else:
        # Modo batch: roda todas as instâncias da pasta instancias/
        pasta_instancias = 'instancias'
        if not os.path.exists(pasta_instancias):
            print(f"ERRO: pasta '{pasta_instancias}/' não encontrada.")
            print("Crie a pasta e coloque arquivos .txt de instâncias dentro,")
            print("ou execute passando o caminho: python main.py arquivo.txt")
            return

        arquivos = sorted([
            f for f in os.listdir(pasta_instancias)
            if f.endswith('.txt')
        ])

        if not arquivos:
            print(f"Nenhum arquivo .txt encontrado em {pasta_instancias}/")
            return

        print(f"Rodando experimentos para {len(arquivos)} instância(s)...\n")

        for arquivo in arquivos:
            caminho = os.path.join(pasta_instancias, arquivo)
            nome_base = arquivo.replace('.txt', '')
            pasta_resultados = os.path.join('resultados', nome_base)

            rodar_experimento(
                caminho,
                pasta_resultados,
                iteracoes=args.iteracoes,
                tamanho_populacao=args.populacao,
                num_execucoes=args.execucoes,
            )
            print()


if __name__ == "__main__":
    main()