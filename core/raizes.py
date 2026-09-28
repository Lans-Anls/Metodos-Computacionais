"""Métodos iterativos para raízes de funções de uma variável."""
from __future__ import annotations

from typing import Callable, Optional

from .modelos import Funcao, Resultado


def bisseccao(f: Funcao, a: float, b: float, tol: float = 1e-6,
              max_iter: int = 100) -> Resultado:
    """Método da bissecção no intervalo [a, b] (requer f(a)·f(b) < 0)."""
    colunas = ["n", "a", "f(a)", "b", "f(b)", "xm", "f(xm)", "erro"]
    a, b = float(a), float(b)
    fa, fb = f(a), f(b)
    if fa == 0:
        return Resultado("bissecção", a, True, 0, colunas, [], "f(a) = 0")
    if fb == 0:
        return Resultado("bissecção", b, True, 0, colunas, [], "f(b) = 0")
    if fa * fb > 0:
        return Resultado("bissecção", None, False, 0, colunas, [],
                         "sem troca de sinal em [a, b] (f(a)·f(b) > 0)")

    tabela: list[dict] = []
    raiz = None
    xm_ant = None
    convergiu = False
    for n in range(1, max_iter + 1):
        xm = (a + b) / 2
        fxm = f(xm)
        erro = abs(xm - xm_ant) if xm_ant is not None else abs(b - a) / 2
        tabela.append({"n": n, "a": a, "f(a)": fa, "b": b, "f(b)": fb,
                       "xm": xm, "f(xm)": fxm, "erro": erro})
        raiz = xm
        if fxm == 0 or erro < tol:
            convergiu = True
            break
        if fa * fxm < 0:
            b, fb = xm, fxm
        else:
            a, fa = xm, fxm
        xm_ant = xm

    motivo = "" if convergiu else "máximo de iterações atingido"
    return Resultado("bissecção", raiz, convergiu, len(tabela), colunas, tabela, motivo)


def newton_raphson(f: Funcao, df: Funcao, x0: float, tol: float = 1e-6,
                   max_iter: int = 100) -> Resultado:
    """Método de Newton-Raphson a partir de x0 (usa a derivada df)."""
    colunas = ["n", "x", "f(x)", "f'(x)", "erro", "erro_rel"]
    tabela: list[dict] = []
    x = float(x0)
    x_ant = None
    raiz = x
    convergiu = False
    motivo = ""
    for n in range(0, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        erro = abs(x - x_ant) if x_ant is not None else None
        erro_rel = abs((x - x_ant) / x) if (x_ant is not None and x != 0) else None
        tabela.append({"n": n, "x": x, "f(x)": fx, "f'(x)": dfx,
                       "erro": erro, "erro_rel": erro_rel})
        raiz = x
        if erro is not None and (erro < tol or abs(fx) < tol):
            convergiu = True
            break
        if dfx == 0:
            motivo = "derivada nula (f'(x) = 0)"
            break
        x_ant = x
        x = x - fx / dfx

    if not convergiu and not motivo:
        motivo = "máximo de iterações atingido"
    return Resultado("Newton-Raphson", raiz, convergiu, len(tabela) - 1, colunas, tabela, motivo)


def secante(f: Funcao, x0: float, x1: float, tol: float = 1e-6,
            max_iter: int = 100) -> Resultado:
    """Método da secante a partir de x0 e x1 (tol = erro relativo, fração)."""
    colunas = ["n", "x(n-1)", "x(n)", "x(n+1)", "f(x(n+1))", "erro_rel_%"]
    tabela: list[dict] = []
    x_prev, x_cur = float(x0), float(x1)
    try:
        f_prev, f_cur = f(x_prev), f(x_cur)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        return Resultado("secante", None, False, 0, colunas, [],
                         f"f indefinida no ponto inicial: {exc}")

    raiz = None
    convergiu = False
    motivo = ""
    for n in range(1, max_iter + 1):
        denom = f_cur - f_prev
        if denom == 0:
            motivo = "denominador nulo (f(xn) = f(xn-1))"
            break
        x_next = x_cur - f_cur * (x_cur - x_prev) / denom
        erro_rel = abs((x_next - x_cur) / x_next) * 100 if x_next != 0 else None
        try:
            f_next = f(x_next)
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            tabela.append({"n": n, "x(n-1)": x_prev, "x(n)": x_cur,
                           "x(n+1)": x_next, "f(x(n+1))": float("nan"),
                           "erro_rel_%": erro_rel})
            motivo = f"função indefinida em x(n+1) = {x_next:.4g} — método divergiu"
            raiz = None
            break
        tabela.append({"n": n, "x(n-1)": x_prev, "x(n)": x_cur, "x(n+1)": x_next,
                       "f(x(n+1))": f_next, "erro_rel_%": erro_rel})
        raiz = x_next
        if erro_rel is not None and erro_rel < tol * 100:
            convergiu = True
            break
        x_prev, f_prev = x_cur, f_cur
        x_cur, f_cur = x_next, f_next

    if not convergiu and not motivo:
        motivo = "máximo de iterações atingido"
    return Resultado("secante", raiz, convergiu, len(tabela), colunas, tabela, motivo)


def secante_amortecida(f: Funcao, x0: float, x1: float, tol: float = 1e-6,
                       max_iter: int = 100,
                       valido: Optional[Callable[[float], bool]] = None,
                       max_recuos: int = 60) -> Resultado:
    """Executa a secante com recuos para respeitar restrições de domínio."""
    colunas = ["n", "x(n-1)", "x(n)", "x(n+1)", "f(x(n+1))", "recuos", "erro_rel_%"]

    def avaliar(x: float) -> float:
        if valido is not None and not valido(x):
            raise ValueError("fora do domínio definido por `valido`")
        return f(x)

    x_prev, x_cur = float(x0), float(x1)
    try:
        f_prev, f_cur = avaliar(x_prev), avaliar(x_cur)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        return Resultado("secante amortecida", None, False, 0, colunas, [],
                         f"f indefinida no ponto inicial: {exc}")

    tabela: list[dict] = []
    raiz = None
    convergiu = False
    motivo = ""
    for n in range(1, max_iter + 1):
        denom = f_cur - f_prev
        if denom == 0:
            motivo = "denominador nulo (f(xn) = f(xn-1))"
            break
        x_next = x_cur - f_cur * (x_cur - x_prev) / denom
        f_next = None
        recuos = 0
        while recuos <= max_recuos:
            try:
                f_next = avaliar(x_next)
                break
            except (ValueError, ZeroDivisionError, OverflowError):
                x_next = (x_next + x_cur) / 2
                recuos += 1
        if f_next is None:
            motivo = "não foi possível retornar ao domínio (recuos esgotados)"
            break
        erro_rel = abs((x_next - x_cur) / x_next) * 100 if x_next != 0 else None
        tabela.append({"n": n, "x(n-1)": x_prev, "x(n)": x_cur, "x(n+1)": x_next,
                       "f(x(n+1))": f_next, "recuos": recuos, "erro_rel_%": erro_rel})
        raiz = x_next
        if erro_rel is not None and erro_rel < tol * 100:
            convergiu = True
            break
        x_prev, f_prev = x_cur, f_cur
        x_cur, f_cur = x_next, f_next

    if not convergiu and not motivo:
        motivo = "máximo de iterações atingido"
    return Resultado("secante amortecida", raiz, convergiu, len(tabela), colunas, tabela, motivo)
