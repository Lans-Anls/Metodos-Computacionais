"""Tipos compartilhados pelos métodos numéricos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

Funcao = Callable[[float], float]


@dataclass
class Resultado:
    """Saída padronizada de qualquer método numérico."""

    metodo: str
    raiz: Optional[float]
    convergiu: bool
    iteracoes: int
    colunas: list[str]
    tabela: list[dict]
    motivo: str = ""
