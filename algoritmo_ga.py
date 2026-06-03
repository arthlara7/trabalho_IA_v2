import random
from funcoes.calcula_custo_total import calcula_custo_total
from funcoes.gera_rota import gera_rota

class AlgoritmoGeneticoTSP:
    def __init__(self, num_cidades, matriz_distancias, tamanho_populacao=100,
                 taxa_mutacao=None, taxa_crossover=0.85, geracoes=500,
                 geracoes_sem_melhora_max=None):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias
        self.tamanho_populacao = tamanho_populacao
        # Taxa de mutação por posição: padrão = 1/n
        # Significa que em média 1 posição da rota é mutada por chamada
        self.taxa_mutacao = taxa_mutacao if taxa_mutacao is not None else 1.0 / num_cidades
        self.taxa_crossover = taxa_crossover
        self.geracoes = geracoes
        self.geracoes_sem_melhora_max = geracoes_sem_melhora_max

    def _selecao_torneio(self, populacao, custos, k=3):
        participantes = random.sample(list(zip(populacao, custos)), k)
        vencedor = min(participantes, key=lambda x: x[1])
        return vencedor[0]

    def _crossover_ox(self, pai1, pai2):
        tamanho = len(pai1)
        inicio, fim = sorted(random.sample(range(tamanho), 2))
        filho = [-1] * tamanho
        filho[inicio:fim] = pai1[inicio:fim]
        p2_filtrado = [cidade for cidade in pai2 if cidade not in filho[inicio:fim]]

        idx_insercao = fim
        for cidade in p2_filtrado:
            if idx_insercao == tamanho:
                idx_insercao = 0
            filho[idx_insercao] = cidade
            idx_insercao += 1
        return filho

    def _mutacao_swap(self, rota):
        
        #Mutação por posição: cada posição tem probabilidade taxa_mutacao de ser trocada com outra posição aleatória.
        #Pode haver múltiplos swaps por chamada.
        
        nova_rota = rota.copy()
        n = len(nova_rota)
        for i in range(n):
            if random.random() < self.taxa_mutacao:
                j = random.randrange(n)
                nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
        return nova_rota

    def executar(self):
        populacao = [gera_rota(self.num_cidades) for _ in range(self.tamanho_populacao)]
        melhor_rota_global = None
        melhor_custo_global = float('inf')
        historico_custos = []
        geracoes_sem_melhora = 0

        for _ in range(self.geracoes):
            custos = [calcula_custo_total(rota, self.matriz_distancias) for rota in populacao]
            melhor_custo_atual = min(custos)
            idx_melhor = custos.index(melhor_custo_atual)

            if melhor_custo_atual < melhor_custo_global:
                melhor_custo_global = melhor_custo_atual
                melhor_rota_global = populacao[idx_melhor].copy()
                geracoes_sem_melhora = 0
            else:
                geracoes_sem_melhora += 1

            historico_custos.append(melhor_custo_global)

            if (self.geracoes_sem_melhora_max is not None
                    and geracoes_sem_melhora >= self.geracoes_sem_melhora_max):
                break

            nova_populacao = [melhor_rota_global.copy()]
            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self._selecao_torneio(populacao, custos)
                pai2 = self._selecao_torneio(populacao, custos)

                if random.random() < self.taxa_crossover:
                    filho = self._crossover_ox(pai1, pai2)
                else:
                    filho = pai1.copy()

                filho = self._mutacao_swap(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao

        while len(historico_custos) < self.geracoes:
            historico_custos.append(melhor_custo_global)

        return melhor_rota_global, melhor_custo_global, historico_custos