import matplotlib.pyplot as plt

def plot_convergencia_comparacao(hist_ga, hist_pso, titulo="Convergência: GA vs PSO"):
    plt.figure(figsize=(10, 5))
    plt.plot(hist_ga, label='Custo Melhor Rota (GA)', color='blue', linewidth=2)
    plt.plot(hist_pso, label='Custo Melhor Rota (PSO)', color='orange', linewidth=2)
    plt.title(titulo)
    plt.xlabel('Iterações / Gerações')
    plt.ylabel('Custo (Distância)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig('grafico_convergencia_comparacao.png', dpi=300)
    plt.show()

def plot_rotas_comparacao(cidades, rota_ga, rota_pso, titulo="Melhores Tours Encontrados"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    def desenha_rota(ax, rota, cor, subtitulo):
        x = [cidades[c][0] for c in rota] + [cidades[rota[0]][0]]
        y = [cidades[c][1] for c in rota] + [cidades[rota[0]][1]]
        ax.plot(x, y, marker='o', linestyle='-', color=cor, markerfacecolor='white', markeredgewidth=2)
        for i, cidade in enumerate(rota):
            ax.text(cidades[cidade][0] + 0.1, cidades[cidade][1] + 0.1, str(cidade), fontsize=10)
        ax.set_title(subtitulo)
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.grid(True, linestyle='--', alpha=0.5)

    desenha_rota(ax1, rota_ga, 'red', "Algoritmo Genético (GA)")
    desenha_rota(ax2, rota_pso, 'purple', "Particle Swarm Optimization (PSO)")
    
    plt.suptitle(titulo, fontsize=14)
    plt.tight_layout()
    plt.savefig('grafico_rotas_comparacao.png', dpi=300)
    plt.show()