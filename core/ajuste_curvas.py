"""Ajustes de curvas pelo método dos mínimos quadrados."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class ResultadoAjuste:
    """Resultado comum aos modelos ajustados por mínimos quadrados."""

    modelo: str
    coeficientes: list[float]
    r_quadrado: float
    soma_quadrados_residuos: float
    tabela: list[dict]

    def avaliar(self, x: float) -> float:
        """Avalia o modelo ajustado no ponto informado."""
        if self.modelo == "exponencial":
            amplitude, taxa = self.coeficientes
            return amplitude * math.exp(taxa * x)
        return sum(coeficiente * x ** grau
                   for grau, coeficiente in enumerate(self.coeficientes))


def _validar_dados(xs: Sequence[float], ys: Sequence[float],
                   minimo: int) -> tuple[np.ndarray, np.ndarray]:
    if len(xs) != len(ys):
        raise ValueError("As listas de x e y devem ter o mesmo tamanho.")
    if len(xs) < minimo:
        raise ValueError(f"O ajuste requer pelo menos {minimo} pontos.")
    pontos_x = np.asarray(xs, dtype=float)
    pontos_y = np.asarray(ys, dtype=float)
    if not np.all(np.isfinite(pontos_x)) or not np.all(np.isfinite(pontos_y)):
        raise ValueError("Os dados devem conter somente valores finitos.")
    if len(np.unique(pontos_x)) < minimo:
        raise ValueError("Não há valores distintos de x suficientes para o ajuste.")
    return pontos_x, pontos_y


def _resultado_polinomial(modelo: str, xs: np.ndarray, ys: np.ndarray,
                          coeficientes: np.ndarray) -> ResultadoAjuste:
    previstos = sum(coeficiente * xs ** grau
                    for grau, coeficiente in enumerate(coeficientes))
    return _montar_resultado(modelo, xs, ys, previstos, coeficientes.tolist())


def _montar_resultado(modelo: str, xs: np.ndarray, ys: np.ndarray,
                      previstos: np.ndarray, coeficientes: list[float]) -> ResultadoAjuste:
    residuos = ys - previstos
    sq_residuos = float(np.sum(residuos ** 2))
    sq_total = float(np.sum((ys - np.mean(ys)) ** 2))
    if math.isclose(sq_total, 0.0, abs_tol=1e-15):
        r_quadrado = 1.0 if math.isclose(sq_residuos, 0.0, abs_tol=1e-15) else 0.0
    else:
        r_quadrado = 1.0 - sq_residuos / sq_total
    tabela = [
        {"i": indice, "x_i": float(x), "y_i": float(y),
         "y_estimado": float(estimado), "residuo": float(residuo)}
        for indice, (x, y, estimado, residuo)
        in enumerate(zip(xs, ys, previstos, residuos))
    ]
    return ResultadoAjuste(modelo, coeficientes, r_quadrado, sq_residuos, tabela)


def ajuste_linear(xs: Sequence[float], ys: Sequence[float]) -> ResultadoAjuste:
    """Ajusta y = a0 + a1*x por mínimos quadrados."""
    pontos_x, pontos_y = _validar_dados(xs, ys, minimo=2)
    matriz = np.column_stack((np.ones(len(pontos_x)), pontos_x))
    coeficientes, *_ = np.linalg.lstsq(matriz, pontos_y, rcond=None)
    return _resultado_polinomial("linear", pontos_x, pontos_y, coeficientes)


def ajuste_quadratico(xs: Sequence[float], ys: Sequence[float]) -> ResultadoAjuste:
    """Ajusta y = a0 + a1*x + a2*x² por mínimos quadrados."""
    pontos_x, pontos_y = _validar_dados(xs, ys, minimo=3)
    matriz = np.column_stack((np.ones(len(pontos_x)), pontos_x, pontos_x ** 2))
    coeficientes, *_ = np.linalg.lstsq(matriz, pontos_y, rcond=None)
    return _resultado_polinomial("quadrático", pontos_x, pontos_y, coeficientes)


def ajuste_exponencial(xs: Sequence[float], ys: Sequence[float]) -> ResultadoAjuste:
    """Ajusta y = a*exp(b*x) pela linearização ln(y) = ln(a) + b*x."""
    pontos_x, pontos_y = _validar_dados(xs, ys, minimo=2)
    if np.any(pontos_y <= 0):
        raise ValueError("O ajuste exponencial requer todos os valores de y positivos.")
    matriz = np.column_stack((np.ones(len(pontos_x)), pontos_x))
    coeficientes_log, *_ = np.linalg.lstsq(matriz, np.log(pontos_y), rcond=None)
    amplitude = math.exp(float(coeficientes_log[0]))
    taxa = float(coeficientes_log[1])
    previstos = amplitude * np.exp(taxa * pontos_x)
    return _montar_resultado(
        "exponencial", pontos_x, pontos_y, previstos, [amplitude, taxa])
