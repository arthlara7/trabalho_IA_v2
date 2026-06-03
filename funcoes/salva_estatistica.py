# Salva resumo das estatísticas em arquivo texto.

def salva_estatisticas_txt(caminho, nome_instancia, num_cidades, stats_ga, stats_pso, resultado_teste):

    with open(caminho, 'w') as f:
        f.write(f"INSTÂNCIA: {nome_instancia} ({num_cidades} cidades)\n")
        f.write("=" * 60 + "\n\n")

        for nome, stats in [("GA", stats_ga), ("PSO", stats_pso)]:
            f.write(f"--- {nome} ---\n")
            f.write(f"  Melhor   : {stats['melhor']:.4f}\n")
            f.write(f"  Pior     : {stats['pior']:.4f}\n")
            f.write(f"  Média    : {stats['media']:.4f}\n")
            f.write(f"  Desvio   : {stats['desvio']:.4f}\n")
            f.write(f"  Tempo méd: {stats['tempo_medio']:.4f} seg\n")
            f.write(f"  Melhor rota: {stats['melhor_rota']}\n\n")

        if resultado_teste:
            f.write("--- Mann-Whitney ---\n")
            f.write(f"  Estatística U: {resultado_teste['estatistica']:.4f}\n")
            f.write(f"  p-valor      : {resultado_teste['p_valor']:.6f}\n")
            f.write(f"  Significativo: {resultado_teste['significativo']}\n")
