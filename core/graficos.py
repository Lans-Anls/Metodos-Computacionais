"""Visualização de funções de uma variável e suas raízes."""
from __future__ import annotations

from typing import Optional, Sequence

from .modelos import Funcao


def _safe(f: Funcao, x: float) -> float:
    try:
        y = f(x)
        return float("nan") if isinstance(y, complex) else float(y)
    except (ValueError, ZeroDivisionError, OverflowError):
        return float("nan")


def plotar(f: Funcao, intervalo: tuple[float, float],
           raizes: Optional[Sequence[Optional[float]]] = None,
           n_pontos: int = 400, titulo: str = "", xlabel: str = "x",
           ylabel: str = "f(x)",
           pontos_extra: Optional[Sequence[tuple[float, str]]] = None,
           salvar: Optional[str] = None, mostrar: bool = False) -> None:
    """Traça a função e marca as raízes e os pontos extras fornecidos."""
    import numpy as np
    import matplotlib
    if not mostrar:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a, b = intervalo
    xs = np.linspace(a, b, n_pontos)
    ys = np.array([_safe(f, float(x)) for x in xs])

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(xs, ys, color="#1f77b4", lw=2, label=ylabel)
    ax.axhline(0, color="0.4", lw=1, ls="--")

    for raiz in raizes or []:
        if raiz is None:
            continue
        ax.plot(raiz, _safe(f, raiz), "o", color="crimson", ms=9, zorder=5)
        ax.annotate(f"raiz ≈ {raiz:.5f}", xy=(raiz, 0), xytext=(0, 20),
                    textcoords="offset points", ha="center",
                    color="crimson", fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color="crimson"))

    for ponto_x, rotulo in pontos_extra or []:
        ax.plot(ponto_x, _safe(f, ponto_x), "s", color="darkgreen", ms=8, zorder=5)
        ax.annotate(rotulo, xy=(ponto_x, _safe(f, ponto_x)), xytext=(0, -24),
                    textcoords="offset points", ha="center", color="darkgreen")

    ax.set_title(titulo, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()

    if salvar:
        fig.savefig(salvar, dpi=130)
        print(f"[gráfico salvo em: {salvar}]")
    if mostrar:
        plt.show()
    plt.close(fig)
