import random
from funcoes.calcula_custo_total import calcula_custo_total
from funcoes.gera_rota import gera_rota


class AlgoritmoPSO_TSP:
    def __init__(self, num_cidades, matriz_distancias, num_particulas=100,
                 iteracoes=500, w_max=0.9, w_min=0.4, c1=1.5, c2=1.5,
                 vmax_fator=0.5):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias
        self.num_particulas = num_particulas
        self.iteracoes = iteracoes

        # Coeficientes do PSO
        self.w_max = w_max  # Inércia inicial (mais exploração)
        self.w_min = w_min  # Inércia final (mais explotação)
        self.c1 = c1        # Componente cognitivo (memória pessoal)
        self.c2 = c2        # Componente social (influência do enxame)

        # Tamanho máximo da velocidade = vmax_fator * num_cidades
        # Limita quantos swaps uma partícula pode aplicar de uma vez
        self.vmax = int(vmax_fator * num_cidades)

    # ---------- Operações de velocidade (sequência de swaps) ----------

    def _diferenca_rotas(self, rota_destino, rota_origem):
        """
        Retorna a sequência de swaps que transforma rota_origem em rota_destino.
        Cada swap é uma tupla (i, j) significando 'troque as posições i e j'.
        """
        origem = rota_origem.copy()  # não modifica o original
        swaps = []
        for i in range(len(rota_destino)):
            if origem[i] != rota_destino[i]:
                # Encontra onde está a cidade que deveria estar na posição i
                j = origem.index(rota_destino[i])
                # Aplica o swap em origem
                origem[i], origem[j] = origem[j], origem[i]
                swaps.append((i, j))
        return swaps

    def _aplica_velocidade(self, rota, velocidade):
        """Aplica uma sequência de swaps a uma rota."""
        nova_rota = rota.copy()
        for i, j in velocidade:
            nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
        return nova_rota

    def _multiplica_velocidade(self, velocidade, fator):
        """
        Mantém cada swap com probabilidade igual ao fator.
        Se fator > 1, pode duplicar alguns swaps.
        """
        if fator <= 0:
            return []

        nova_velocidade = []
        # Para fator entre 0 e 1: mantém com essa probabilidade
        # Para fator > 1: mantém parte inteira + parte fracionária probabilística
        parte_inteira = int(fator)
        parte_fracionaria = fator - parte_inteira

        for swap in velocidade:
            # Adiciona o swap "parte_inteira" vezes
            for _ in range(parte_inteira):
                nova_velocidade.append(swap)
            # Mais uma vez com probabilidade da parte fracionária
            if random.random() < parte_fracionaria:
                nova_velocidade.append(swap)

        return nova_velocidade

    def _clamp_velocidade(self, velocidade):
        """Limita o tamanho da velocidade a vmax."""
        if len(velocidade) > self.vmax:
            # Amostra aleatória dos swaps, mantendo a ordem
            indices = sorted(random.sample(range(len(velocidade)), self.vmax))
            return [velocidade[i] for i in indices]
        return velocidade

    # ---------- Loop principal ----------

    def executar(self):
        # Inicializa partículas como rotas aleatórias
        posicoes = [gera_rota(self.num_cidades) for _ in range(self.num_particulas)]

        # Velocidade inicial = lista vazia de swaps
        velocidades = [[] for _ in range(self.num_particulas)]

        # Calcula custos iniciais ANTES do loop (correção pedida)
        custos_iniciais = [calcula_custo_total(p, self.matriz_distancias)
                           for p in posicoes]

        # pBest inicializado corretamente com posições e custos atuais
        pbest_pos = [p.copy() for p in posicoes]
        pbest_custos = custos_iniciais.copy()

        # gBest = melhor pBest inicial
        idx_melhor = pbest_custos.index(min(pbest_custos))
        gbest_pos = pbest_pos[idx_melhor].copy()
        gbest_custo = pbest_custos[idx_melhor]

        historico_custos = []

        for iteracao in range(self.iteracoes):
            # Inércia decrescente: vai de w_max no início pra w_min no final
            w_atual = self.w_max - (self.w_max - self.w_min) * (iteracao / self.iteracoes)

            for i in range(self.num_particulas):
                # ---------- Atualização da velocidade ----------
                # v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
                # Cada parte é uma sequência de swaps

                r1, r2 = random.random(), random.random()

                # Inércia: mantém parte da velocidade anterior
                v_inercia = self._multiplica_velocidade(velocidades[i], w_atual)

                # Cognitivo: trocas que aproximam da pbest
                swaps_pbest = self._diferenca_rotas(pbest_pos[i], posicoes[i])
                v_cognitivo = self._multiplica_velocidade(swaps_pbest, self.c1 * r1)

                # Social: trocas que aproximam da gbest
                swaps_gbest = self._diferenca_rotas(gbest_pos, posicoes[i])
                v_social = self._multiplica_velocidade(swaps_gbest, self.c2 * r2)

                # Nova velocidade = concatenação das três
                nova_velocidade = v_inercia + v_cognitivo + v_social

                # Clamping: limita o tamanho máximo
                nova_velocidade = self._clamp_velocidade(nova_velocidade)

                velocidades[i] = nova_velocidade

                # ---------- Atualização da posição ----------
                posicoes[i] = self._aplica_velocidade(posicoes[i], velocidades[i])

                # ---------- Avaliação ----------
                custo = calcula_custo_total(posicoes[i], self.matriz_distancias)

                # Atualiza pBest
                if custo < pbest_custos[i]:
                    pbest_custos[i] = custo
                    pbest_pos[i] = posicoes[i].copy()

                # Atualiza gBest
                if custo < gbest_custo:
                    gbest_custo = custo
                    gbest_pos = posicoes[i].copy()

            historico_custos.append(gbest_custo)

        return gbest_pos, gbest_custo, historico_custos