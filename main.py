import argparse
import os
from roda_experimento import rodar_experimento


def main():
    #Escolha de argumentos: pode-se escolher o nome da instância se quiser rodar somente uma, o numero de execuções, de iterações e da população
    #usando -- na frente do argumento, ex: python3 main.py instancias/instancia --execucoes 10 (ele vai realizar 10 execuções na instância)
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
        # Caso o usuário queira rodar uma instância somente, ele especifica com /instnacias/"nome da instancia"
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
        # Se não especificar a instância que quer rodar, roda todas 30x
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