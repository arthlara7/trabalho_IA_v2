import matplotlib.pyplot as plt

# Configurações globais de estética pra todos os gráficos
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'lines.linewidth': 1.8,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'figure.dpi': 100,
})


def _salva_figura(nome_base):
    """Salva a figura atual em PNG (alta res) e PDF (vetorial)."""
    plt.savefig(f'{nome_base}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{nome_base}.pdf', bbox_inches='tight')


def plot_convergencia_comparacao(hist_medio_ga, hist_medio_pso, titulo="Convergência: GA vs PSO"):
    """
    Plota a convergência média dos dois algoritmos.
    Se desvio for fornecido, mostra faixa sombreada de média ± desvio.
    """
    plt.figure(figsize=(10, 5))

    iteracoes = range(len(hist_medio_ga))
    iteracoes_pso = range(len(hist_medio_pso))

    # GA
    plt.plot(iteracoes, hist_medio_ga, label='GA (média)',
             color='#1f77b4', linewidth=2)
   

    # PSO
    plt.plot(iteracoes_pso, hist_medio_pso, label='PSO (média)',
             color='#ff7f0e', linewidth=2)
   

    plt.title(titulo)
    plt.xlabel('Iterações / Gerações')
    plt.ylabel('Custo (Distância Total)')
    plt.legend(loc='upper right', framealpha=0.9)
    plt.tight_layout()
    _salva_figura('grafico_convergencia_comparacao')
    plt.show()


def plot_rotas_comparacao(cidades, rota_ga, rota_pso,
                           titulo="Melhores Tours Encontrados"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    def desenha_rota(ax, rota, cor, subtitulo):
        x = [cidades[c][0] for c in rota] + [cidades[rota[0]][0]]
        y = [cidades[c][1] for c in rota] + [cidades[rota[0]][1]]
        ax.plot(x, y, marker='o', linestyle='-', color=cor,
                markerfacecolor='white', markeredgewidth=2, markersize=8)
        for i, cidade in enumerate(rota):
            ax.text(cidades[cidade][0] + 0.15, cidades[cidade][1] + 0.15,
                    str(cidade), fontsize=10, fontweight='bold')
        ax.set_title(subtitulo)
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.grid(True, linestyle='--', alpha=0.5)

    desenha_rota(ax1, rota_ga, '#d62728', "Algoritmo Genético (GA)")
    desenha_rota(ax2, rota_pso, '#9467bd', "Particle Swarm Optimization (PSO)")

    plt.suptitle(titulo, fontsize=14, fontweight='bold')
    plt.tight_layout()
    _salva_figura('grafico_rotas_comparacao')
    plt.show()

