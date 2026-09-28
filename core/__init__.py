"""API pública da biblioteca de métodos numéricos."""

from .ajuste_curvas import (
    ResultadoAjuste,
    ajuste_exponencial,
    ajuste_linear,
    ajuste_quadratico,
)
from .expressoes import compilar_expressao
from .formatacao import imprimir_tabela
from .graficos import plotar
from .interpolacao import (
    ResultadoInterpolacao,
    erro_absoluto,
    gregory_newton,
    lagrange,
    limite_superior_erro,
    newton_diferencas_divididas,
    tabela_diferencas_divididas,
)
from .modelos import Funcao, Resultado
from .raizes import bisseccao, newton_raphson, secante, secante_amortecida
from .sistemas import newton_sistema

__all__ = [
    "Funcao",
    "Resultado",
    "ResultadoAjuste",
    "ResultadoInterpolacao",
    "ajuste_exponencial",
    "ajuste_linear",
    "ajuste_quadratico",
    "bisseccao",
    "compilar_expressao",
    "erro_absoluto",
    "gregory_newton",
    "imprimir_tabela",
    "lagrange",
    "limite_superior_erro",
    "newton_diferencas_divididas",
    "newton_raphson",
    "newton_sistema",
    "plotar",
    "secante",
    "secante_amortecida",
    "tabela_diferencas_divididas",
]
