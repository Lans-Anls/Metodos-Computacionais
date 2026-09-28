"""Interpolação polinomial e análise do erro de interpolação."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass
class ResultadoInterpolacao:
    """Resultado comum aos métodos de interpolação polinomial."""

    metodo: str
    x: float
    valor: float
    grau: int
    coeficientes: list[float]
    tabela: list[dict]
    termos: list[float]

    def avaliar(self, x: float) -> float:
        """Avalia o polinômio na forma de potências usando Horner."""
        resultado = 0.0
        for coeficiente in reversed(self.coeficientes):
            resultado = resultado * x + coeficiente
        return resultado


def _validar_pontos(xs: Sequence[float], ys: Sequence[float]) -> tuple[list[float], list[float]]:
    if len(xs) != len(ys):
        raise ValueError("As listas de x e y devem ter o mesmo tamanho.")
    if len(xs) < 2:
        raise ValueError("Informe pelo menos dois pontos para interpolar.")
    pontos_x = [float(valor) for valor in xs]
    pontos_y = [float(valor) for valor in ys]
    if not all(math.isfinite(valor) for valor in pontos_x + pontos_y):
        raise ValueError("Os pontos devem conter somente valores finitos.")
    if len(set(pontos_x)) != len(pontos_x):
        raise ValueError("Os valores de x devem ser distintos.")
    return pontos_x, pontos_y


def _multiplicar_polinomios(a: list[float], b: list[float]) -> list[float]:
    produto = [0.0] * (len(a) + len(b) - 1)
    for indice_a, coeficiente_a in enumerate(a):
        for indice_b, coeficiente_b in enumerate(b):
            produto[indice_a + indice_b] += coeficiente_a * coeficiente_b
    return produto


def _coeficientes_lagrange(xs: list[float], ys: list[float]) -> list[float]:
    coeficientes = [0.0] * len(xs)
    for indice, (x_i, y_i) in enumerate(zip(xs, ys)):
        base = [1.0]
        denominador = 1.0
        for outro_indice, x_j in enumerate(xs):
            if outro_indice == indice:
                continue
            base = _multiplicar_polinomios(base, [-x_j, 1.0])
            denominador *= x_i - x_j
        for grau, coeficiente in enumerate(base):
            coeficientes[grau] += y_i * coeficiente / denominador
    return coeficientes


def lagrange(xs: Sequence[float], ys: Sequence[float], x: float) -> ResultadoInterpolacao:
    """Interpola um valor pelas bases polinomiais de Lagrange."""
    pontos_x, pontos_y = _validar_pontos(xs, ys)
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("O valor a interpolar deve ser finito.")

    termos = []
    tabela = []
    for indice, (x_i, y_i) in enumerate(zip(pontos_x, pontos_y)):
        numerador = 1.0
        denominador = 1.0
        for outro_indice, x_j in enumerate(pontos_x):
            if outro_indice == indice:
                continue
            numerador *= x - x_j
            denominador *= x_i - x_j
        base = numerador / denominador
        termo = y_i * base
        termos.append(termo)
        tabela.append({"i": indice, "x_i": x_i, "y_i": y_i,
                       "L_i(x)": base, "y_i L_i(x)": termo})

    return ResultadoInterpolacao(
        metodo="Lagrange",
        x=x,
        valor=sum(termos),
        grau=len(pontos_x) - 1,
        coeficientes=_coeficientes_lagrange(pontos_x, pontos_y),
        tabela=tabela,
        termos=termos,
    )


def tabela_diferencas_divididas(xs: Sequence[float], ys: Sequence[float]) -> list[list[float]]:
    """Constrói a tabela triangular de diferenças divididas de Newton."""
    pontos_x, pontos_y = _validar_pontos(xs, ys)
    tabela = [pontos_y]
    for ordem in range(1, len(pontos_x)):
        anterior = tabela[-1]
        coluna = [
            (anterior[indice + 1] - anterior[indice])
            / (pontos_x[indice + ordem] - pontos_x[indice])
            for indice in range(len(pontos_x) - ordem)
        ]
        tabela.append(coluna)
    return tabela


def newton_diferencas_divididas(xs: Sequence[float], ys: Sequence[float],
                                x: float) -> ResultadoInterpolacao:
    """Interpola um valor pela forma de Newton com diferenças divididas."""
    pontos_x, pontos_y = _validar_pontos(xs, ys)
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("O valor a interpolar deve ser finito.")
    tabela_dd = tabela_diferencas_divididas(pontos_x, pontos_y)
    coeficientes_newton = [coluna[0] for coluna in tabela_dd]

    termos = [coeficientes_newton[0]]
    produto = 1.0
    for ordem in range(1, len(pontos_x)):
        produto *= x - pontos_x[ordem - 1]
        termos.append(coeficientes_newton[ordem] * produto)

    tabela = []
    for indice, (x_i, y_i) in enumerate(zip(pontos_x, pontos_y)):
        linha = {"i": indice, "x_i": x_i, "f[x_i]": y_i}
        for ordem in range(1, len(pontos_x) - indice):
            linha[f"ordem_{ordem}"] = tabela_dd[ordem][indice]
        tabela.append(linha)

    coeficientes = [0.0] * len(pontos_x)
    produto_polinomial = [1.0]
    for ordem, coeficiente in enumerate(coeficientes_newton):
        for grau, valor in enumerate(produto_polinomial):
            coeficientes[grau] += coeficiente * valor
        if ordem < len(pontos_x) - 1:
            produto_polinomial = _multiplicar_polinomios(
                produto_polinomial, [-pontos_x[ordem], 1.0])

    return ResultadoInterpolacao(
        metodo="Newton (diferenças divididas)",
        x=x,
        valor=sum(termos),
        grau=len(pontos_x) - 1,
        coeficientes=coeficientes,
        tabela=tabela,
        termos=termos,
    )


def gregory_newton(xs: Sequence[float], ys: Sequence[float], x: float,
                   tolerancia: float = 1e-9) -> ResultadoInterpolacao:
    """Interpola por Gregory-Newton progressivo em nós igualmente espaçados."""
    pontos_x, pontos_y = _validar_pontos(xs, ys)
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("O valor a interpolar deve ser finito.")
    passo = pontos_x[1] - pontos_x[0]
    if passo == 0:
        raise ValueError("O espaçamento entre os pontos não pode ser zero.")
    for indice in range(1, len(pontos_x) - 1):
        espacamento = pontos_x[indice + 1] - pontos_x[indice]
        if not math.isclose(espacamento, passo, rel_tol=tolerancia, abs_tol=tolerancia):
            raise ValueError("Gregory-Newton requer valores de x igualmente espaçados.")

    diferencas = [pontos_y]
    while len(diferencas[-1]) > 1:
        anterior = diferencas[-1]
        diferencas.append([anterior[i + 1] - anterior[i]
                           for i in range(len(anterior) - 1)])

    u = (x - pontos_x[0]) / passo
    termos = [pontos_y[0]]
    produto = 1.0
    for ordem in range(1, len(pontos_x)):
        produto *= u - (ordem - 1)
        termos.append(produto * diferencas[ordem][0] / math.factorial(ordem))

    tabela = []
    for indice, (x_i, y_i) in enumerate(zip(pontos_x, pontos_y)):
        linha = {"i": indice, "x_i": x_i, "f[x_i]": y_i}
        for ordem in range(1, len(pontos_x) - indice):
            linha[f"delta_{ordem}"] = diferencas[ordem][indice]
        tabela.append(linha)

    return ResultadoInterpolacao(
        metodo="Gregory-Newton",
        x=x,
        valor=sum(termos),
        grau=len(pontos_x) - 1,
        coeficientes=_coeficientes_lagrange(pontos_x, pontos_y),
        tabela=tabela,
        termos=termos,
    )


def erro_absoluto(valor_exato: float, valor_interpolado: float) -> float:
    """Calcula a diferença absoluta entre o valor exato e o interpolado."""
    return abs(float(valor_exato) - float(valor_interpolado))


def limite_superior_erro(xs: Sequence[float], x: float, max_derivada: float) -> float:
    """Calcula |psi_n(x)| M_(n+1) / (n+1)! para os nós informados."""
    pontos_x = [float(valor) for valor in xs]
    if not pontos_x:
        raise ValueError("Informe ao menos um nó para calcular o limite do erro.")
    if len(set(pontos_x)) != len(pontos_x):
        raise ValueError("Os valores de x devem ser distintos.")
    x = float(x)
    max_derivada = float(max_derivada)
    if not all(math.isfinite(valor) for valor in pontos_x + [x, max_derivada]):
        raise ValueError("O cálculo do limite requer valores finitos.")
    psi = math.prod(x - x_i for x_i in pontos_x)
    return abs(psi) * abs(max_derivada) / math.factorial(len(pontos_x))
