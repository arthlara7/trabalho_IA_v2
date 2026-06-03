# Comparação entre Algoritmo Genético e PSO para o TSP

Implementação e comparação de Algoritmo Genético (GA) e Otimização por
Enxame de Partículas (PSO) aplicados ao Problema do Caixeiro Viajante (TSP).

Trabalho da disciplina de Inteligência Artificial — UFSJ, 2026/1.

Docente: Edmilson Batista dos Santos

## Requisitos
- Python 3.8 ou superior
- Bibliotecas listadas em `requirements.txt`, sendo elas:
    * matplotlib>=3.5
    * scipy>=1.9
    * numpy>=1.22


## Instalação
```bash
pip install -r requirements.txt
```

## Como executar
**Rodar uma instância específica:**
```bash
python main.py instancias/instancia.txt
```

**Rodar todas as instâncias da pasta `instancias/` em sequência:**
```bash
python main.py
```

**Alterar o número de execuções para teste rápido (o padrão é 30):**
```bash
python main.py instancias/instancia.txt --execucoes 5
```

**Colocar outros parâmetros:**
```bash
python main.py instancias/instancia.txt --execucoes 30 --iteracoes 500 --populacao 100
```

**Ver todas as opções disponíveis:**
```bash
python main.py --help
```

## Saída
Para cada instância executada, o programa cria uma pasta em `resultados/<nome_da_instancia>/`
contendo:

- `estatisticas.txt` — resumo das métricas (média, desvio, melhor, pior, tempo)
- `grafico_convergencia_comparacao.pdf` e `.png` — convergência média do GA e PSO
- `grafico_rotas_comparacao.pdf` e `.png` — melhores rotas encontradas

O terminal exibe progresso execução por execução, estatísticas detalhadas
de cada algoritmo e o resultado do teste de Wilcoxon-Mann-Whitney.

## Estrutura do Projeto
```
.
├── main.py                       # script principal
├── algoritmo_ga.py               # Algoritmo Genético
├── algoritmo_pso.py              # Otimização por Enxame de Partículas
├── roda_experimento.py           # Função que roda o experimento, imprime e salva os dados
├── requirements.txt              # dependências Python
├── funcoes/
│   ├── ler_instancia.py          # leitura do arquivo de cidades
│   ├── calcula_dist_euclidiana.py# calcula a distância euclidiana entre cidades
│   ├── cria_matriz_distancia.py  # matriz de distâncias pré-computada
│   ├── calcula_custo_total.py    # função de avaliação (fitness)
│   ├── gera_rota.py              # geração de rotas aleatórias
│   ├── analise_estatistica.py    # estatísticas + Mann-Whitney
│   └── cria_grafico.py           # geração dos gráficos
├── instancias/                   # arquivos de entrada
│   ├── instancia.txt             # instância padrão (12 cidades)
│   ├── tsp_berlin52.txt          # TSPLIB - 52 cidades
│   ├── tsp_kroA100.txt           # TSPLIB - 100 cidades
│   └── tsp_eil101.txt            # TSPLIB - 101 cidades
└── resultados/                   # gerado automaticamente
```

## Formato do arquivo de instância

Os arquivos `.txt` em `instancias/` seguem o formato:
```
12
1 5
4 6
7 5
...
```
A primeira linha é o número total de cidades. As linhas seguintes contêm
as coordenadas `x y` de cada cidade, separadas por espaço.

## Algoritmos
**Algoritmo Genético (GA):**
- Representação: caminho (*path*)
- Seleção: torneio (k=3)
- Cruzamento: Order Crossover (OX), taxa 0,85
- Mutação: por posição, taxa 1/n
- Elitismo: 1 indivíduo

**Otimização por Enxame de Partículas (PSO):**
- Representação: caminho (*path*)
- Velocidade: sequência de swaps (*swap-based PSO*)
- Inércia: linearmente decrescente de 0,9 a 0,4
- Coeficientes: c1 = c2 = 1,5
- Clamping de velocidade: 50% do número de cidades
- Topologia: global (*Star*)

**Critério de parada (ambos):**
- Máximo de 500 iterações OU
- 100 iterações consecutivas sem melhora do melhor custo

## Instâncias TSPLIB
As instâncias `berlin52`, `kroA100` e `eil101` foram obtidas da biblioteca
TSPLIB. Os ótimos conhecidos são, respectivamente, 7.542, 21.282 e 629.

## Autores
- Artur Henrique Lara
- Bryan Luiz Veloso da Silva
- Cassiuscray Felipe dos Santos
- Pedro Henrique Faria Moura do Altíssimo

Departamento de Ciência da Computação - DCOMP — UFSJ