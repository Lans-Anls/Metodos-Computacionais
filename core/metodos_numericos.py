"""
metodos_numericos.py
====================
Biblioteca genérica para localização de raízes de funções de uma variável.

Fornece três métodos clássicos — bissecção, Newton-Raphson e secante — que
devolvem a tabela completa de iterações, além de utilitários para imprimir a
tabela e traçar o gráfico da função com as raízes encontradas.

O código é independente do contexto das questões: basta passar qualquer f
(e, para Newton, a derivada f') que a mesma infraestrutura gera a tabela de
iterações e o gráfico, para qualquer problema.

Exemplo mínimo:
    from metodos_numericos import bisseccao, imprimir_tabela, plotar
    f = lambda x: x**2 - 2
    res = bisseccao(f, 0, 2, tol=1e-6)
    imprimir_tabela(res)
    plotar(f, (0, 2), raizes=[res.raiz], salvar="raiz.png")
"""
from __future__ import annotations

import sys

from .formatacao import imprimir_tabela
from .graficos import plotar
from .modelos import Funcao, Resultado
from .raizes import bisseccao, newton_raphson, secante, secante_amortecida


def usar_utf8() -> None:
    """Força saída UTF-8 no stdout (evita erros em consoles cp1252/redirecionados)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
