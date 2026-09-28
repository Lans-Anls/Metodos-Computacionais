"""Métodos numéricos para sistemas de equações não lineares."""
from __future__ import annotations

import math

import numpy as np


def newton_sistema(funcoes, chute, max_iter: int, tol: float):
    """Resolve um sistema não linear com Jacobiana por diferenças centrais."""
    ponto = np.array(chute, dtype=float)
    dimensao = len(ponto)
    if len(funcoes) != dimensao:
        raise ValueError("O número de equações deve ser igual ao número de variáveis.")
    linhas = []
    for k in range(max_iter):
        valores = np.array([funcao(*ponto) for funcao in funcoes], dtype=float)
        jacobiana = np.empty((dimensao, dimensao), dtype=float)
        for coluna in range(dimensao):
            passo_h = math.sqrt(np.finfo(float).eps) * max(1.0, abs(ponto[coluna]))
            frente, tras = ponto.copy(), ponto.copy()
            frente[coluna] += passo_h
            tras[coluna] -= passo_h
            jacobiana[:, coluna] = (
                np.array([funcao(*frente) for funcao in funcoes])
                - np.array([funcao(*tras) for funcao in funcoes])
            ) / (2 * passo_h)
        passo = np.linalg.solve(jacobiana, valores)
        erro = float(np.max(np.abs(passo)))
        linhas.append((k, ponto.copy(), valores, erro, passo.copy()))
        ponto -= passo
        if erro < tol:
            break
    return linhas, ponto
