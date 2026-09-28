"""Formatação textual dos resultados numéricos."""
import math

from .modelos import Resultado


def _fmt(valor, casas: int) -> str:
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return str(valor)
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, float):
        if math.isnan(valor):
            return "inválido"
        if math.isinf(valor):
            return "inf" if valor > 0 else "-inf"
        return f"{valor:.{casas}f}"
    return str(valor)


def imprimir_tabela(resultado: Resultado, casas: int = 5) -> None:
    """Imprime a tabela de iterações de um resultado com colunas alinhadas."""
    colunas = resultado.colunas
    larguras = {
        col: max([len(col)] + [len(_fmt(linha.get(col), casas))
                               for linha in resultado.tabela])
        for col in colunas
    }
    cabecalho = "  ".join(col.rjust(larguras[col]) for col in colunas)
    print(cabecalho)
    print("-" * len(cabecalho))
    for linha in resultado.tabela:
        print("  ".join(_fmt(linha.get(col), casas).rjust(larguras[col])
                        for col in colunas))
