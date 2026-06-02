import time
import statistics


def analise_estatistica(algoritmo_classe, num_execucoes=30, **kwargs):
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
        'tempos': tempos,
        'historicos': historicos,
    }


def imprime_estatisticas(nome_algoritmo, stats):
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
    num_execucoes = len(historicos)
    num_iteracoes = len(historicos[0])

    historico_medio = []
    for iteracao in range(num_iteracoes):
        soma = sum(hist[iteracao] for hist in historicos)
        historico_medio.append(soma / num_execucoes)

    return historico_medio


def calcula_historico_desvio(historicos):
    """Calcula o desvio padrão em cada iteração ao longo das execuções."""
    num_execucoes = len(historicos)
    num_iteracoes = len(historicos[0])

    historico_desvio = []
    for iteracao in range(num_iteracoes):
        valores = [hist[iteracao] for hist in historicos]
        if num_execucoes > 1:
            historico_desvio.append(statistics.stdev(valores))
        else:
            historico_desvio.append(0.0)

    return historico_desvio


def teste_mann_whitney(custos_a, custos_b, nome_a="A", nome_b="B", alfa=0.05):
    """
    Teste de Wilcoxon-Mann-Whitney para comparar dois conjuntos de resultados.
    Hipótese nula: as duas amostras vêm da mesma distribuição.
    Se p-valor < alfa, rejeitamos H0 → diferença significativa.
    """
    try:
        from scipy.stats import mannwhitneyu
    except ImportError:
        print("\n[AVISO] scipy não instalado. Instale com: pip install scipy")
        return None

    # Teste bilateral (two-sided): testa se há diferença em qualquer direção
    stat, p_valor = mannwhitneyu(custos_a, custos_b, alternative='two-sided')

    media_a = statistics.mean(custos_a)
    media_b = statistics.mean(custos_b)

    print("\n" + "=" * 50)
    print("TESTE DE WILCOXON-MANN-WHITNEY")
    print("=" * 50)
    print(f"  {nome_a}: média = {media_a:.4f}")
    print(f"  {nome_b}: média = {media_b:.4f}")
    print(f"  Estatística U: {stat:.4f}")
    print(f"  p-valor      : {p_valor:.6f}")
    print(f"  Nível de significância (α): {alfa}")

    if p_valor < alfa:
        if media_a < media_b:
            vencedor = nome_a
        else:
            vencedor = nome_b
        print(f"  → Diferença estatisticamente significativa (p < {alfa})")
        print(f"  → {vencedor} apresentou melhor desempenho médio")
    else:
        print(f"  → Diferença NÃO significativa (p ≥ {alfa})")
        print(f"  → Não há evidência de que um algoritmo seja melhor que o outro")

    print("=" * 50)

    return {
        'estatistica': stat,
        'p_valor': p_valor,
        'significativo': p_valor < alfa,
        'media_a': media_a,
        'media_b': media_b,
    }