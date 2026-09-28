"""Compilação segura de expressões matemáticas informadas pelo usuário."""
from __future__ import annotations

import ast
import math

FUNCOES_PERMITIDAS = {
    "abs": abs, "acos": math.acos, "asin": math.asin, "atan": math.atan,
    "cos": math.cos, "cosh": math.cosh, "exp": math.exp, "ln": math.log,
    "log": math.log, "log10": math.log10, "sin": math.sin,
    "sinh": math.sinh, "sqrt": math.sqrt, "tan": math.tan,
    "tanh": math.tanh,
}
CONSTANTES_PERMITIDAS = {"e": math.e, "pi": math.pi}
OPERADORES_PERMITIDOS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
                         ast.UAdd, ast.USub)


def compilar_expressao(texto: str, variaveis: tuple[str, ...]):
    """Converte uma expressão matemática validada em uma função chamável."""
    expressao = texto.strip().replace("^", "**")
    if not expressao:
        raise ValueError("A equação não pode ficar vazia.")
    try:
        arvore = ast.parse(expressao, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Equação inválida: {exc.msg}.") from exc

    nomes = set(variaveis) | set(FUNCOES_PERMITIDAS) | set(CONSTANTES_PERMITIDAS)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Name) and no.id not in nomes:
            raise ValueError(f"Nome não permitido na equação: {no.id}.")
        if isinstance(no, ast.Call):
            if not isinstance(no.func, ast.Name) or no.func.id not in FUNCOES_PERMITIDAS:
                raise ValueError("Use somente as funções matemáticas indicadas.")
            if no.keywords:
                raise ValueError("Argumentos nomeados não são permitidos.")
        elif isinstance(no, (ast.operator, ast.unaryop)):
            if not isinstance(no, OPERADORES_PERMITIDOS):
                raise ValueError("A equação contém um operador não permitido.")
        elif not isinstance(no, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call,
                                 ast.Name, ast.Load, ast.Constant)):
            raise ValueError("A equação contém uma construção não permitida.")
        if isinstance(no, ast.Constant) and not isinstance(no.value, (int, float)):
            raise ValueError("A equação aceita apenas constantes numéricas.")

    codigo = compile(arvore, "<equação>", "eval")

    def funcao(*valores):
        contexto = dict(FUNCOES_PERMITIDAS)
        contexto.update(CONSTANTES_PERMITIDAS)
        contexto.update(zip(variaveis, valores))
        resultado = float(eval(codigo, {"__builtins__": {}}, contexto))
        if not math.isfinite(resultado):
            raise ValueError("A equação produziu um valor não finito.")
        return resultado

    return funcao
