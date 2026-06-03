import random
from funcoes.calcula_custo_total import calcula_custo_total
from funcoes.gera_rota import gera_rota

class AlgoritmoPSO_TSP:
    def __init__(self, num_cidades, matriz_distancias, num_particulas=100,
                 iteracoes=500, w_max=0.9, w_min=0.4, c1=1.5, c2=1.5,
                 vmax_fator=0.5, iteracoes_sem_melhora_max=None):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias
        self.num_particulas = num_particulas
        self.iteracoes = iteracoes

        self.w_max = w_max
        self.w_min = w_min
        self.c1 = c1
        self.c2 = c2

        self.vmax = int(vmax_fator * num_cidades)
        self.iteracoes_sem_melhora_max = iteracoes_sem_melhora_max

    def _diferenca_rotas(self, rota_destino, rota_origem):
        origem = rota_origem.copy()
        swaps = []
        for i in range(len(rota_destino)):
            if origem[i] != rota_destino[i]:
                j = origem.index(rota_destino[i])
                origem[i], origem[j] = origem[j], origem[i]
                swaps.append((i, j))
        return swaps

    def _aplica_velocidade(self, rota, velocidade):
        nova_rota = rota.copy()
        for i, j in velocidade:
            nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
        return nova_rota

    def _multiplica_velocidade(self, velocidade, fator):
        if fator <= 0:
            return []

        nova_velocidade = []
        parte_inteira = int(fator)
        parte_fracionaria = fator - parte_inteira

        for swap in velocidade:
            for _ in range(parte_inteira):
                nova_velocidade.append(swap)
            if random.random() < parte_fracionaria:
                nova_velocidade.append(swap)

        return nova_velocidade

    def _clamp_velocidade(self, velocidade):
        if len(velocidade) > self.vmax:
            indices = sorted(random.sample(range(len(velocidade)), self.vmax))
            return [velocidade[i] for i in indices]
        return velocidade

    def executar(self):
        posicoes = [gera_rota(self.num_cidades) for _ in range(self.num_particulas)]
        velocidades = [[] for _ in range(self.num_particulas)]

        custos_iniciais = [calcula_custo_total(p, self.matriz_distancias)
                           for p in posicoes]

        pbest_pos = [p.copy() for p in posicoes]
        pbest_custos = custos_iniciais.copy()

        idx_melhor = pbest_custos.index(min(pbest_custos))
        gbest_pos = pbest_pos[idx_melhor].copy()
        gbest_custo = pbest_custos[idx_melhor]

        historico_custos = []
        iteracoes_sem_melhora = 0

        for iteracao in range(self.iteracoes):
            # Inércia decrescente: agora atinge exatamente w_min na última iteração
            if self.iteracoes > 1:
                w_atual = self.w_max - (self.w_max - self.w_min) * (iteracao / (self.iteracoes - 1))
            else:
                w_atual = self.w_max

            houve_melhora_nesta_iteracao = False

            for i in range(self.num_particulas):
                r1, r2 = random.random(), random.random()

                v_inercia = self._multiplica_velocidade(velocidades[i], w_atual)
                swaps_pbest = self._diferenca_rotas(pbest_pos[i], posicoes[i])
                v_cognitivo = self._multiplica_velocidade(swaps_pbest, self.c1 * r1)
                swaps_gbest = self._diferenca_rotas(gbest_pos, posicoes[i])
                v_social = self._multiplica_velocidade(swaps_gbest, self.c2 * r2)

                nova_velocidade = v_inercia + v_cognitivo + v_social
                nova_velocidade = self._clamp_velocidade(nova_velocidade)
                velocidades[i] = nova_velocidade

                posicoes[i] = self._aplica_velocidade(posicoes[i], velocidades[i])
                custo = calcula_custo_total(posicoes[i], self.matriz_distancias)

                if custo < pbest_custos[i]:
                    pbest_custos[i] = custo
                    pbest_pos[i] = posicoes[i].copy()

                if custo < gbest_custo:
                    gbest_custo = custo
                    gbest_pos = posicoes[i].copy()
                    houve_melhora_nesta_iteracao = True

            historico_custos.append(gbest_custo)

            # Critério de parada por estagnação
            if houve_melhora_nesta_iteracao:
                iteracoes_sem_melhora = 0
            else:
                iteracoes_sem_melhora += 1

            if (self.iteracoes_sem_melhora_max is not None
                    and iteracoes_sem_melhora >= self.iteracoes_sem_melhora_max):
                break

        # Padding do histórico (igual ao GA)
        while len(historico_custos) < self.iteracoes:
            historico_custos.append(gbest_custo)

        return gbest_pos, gbest_custo, historico_custos