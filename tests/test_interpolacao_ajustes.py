"""Testes dos conteúdos de interpolação polinomial e MMQ."""
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import aplicacao.calculos as calculos_aplicacao
from aplicacao.configuracao import METODOS
from core import (
    ajuste_exponencial,
    ajuste_linear,
    ajuste_quadratico,
    gregory_newton,
    lagrange,
    limite_superior_erro,
    newton_diferencas_divididas,
)


class TesteInterpolacao(unittest.TestCase):
    def setUp(self):
        self.xs = [0.1, 0.2, 0.4]
        self.ys = [2.9182, 2.6667, 2.4286]

    def test_lagrange_e_newton_produzem_mesmo_polinomio(self):
        lagrange_resultado = lagrange(self.xs, self.ys, 0.25)
        newton_resultado = newton_diferencas_divididas(self.xs, self.ys, 0.25)

        self.assertAlmostEqual(lagrange_resultado.valor, newton_resultado.valor)
        for x_i, y_i in zip(self.xs, self.ys):
            self.assertAlmostEqual(lagrange_resultado.avaliar(x_i), y_i)
            self.assertAlmostEqual(newton_resultado.avaliar(x_i), y_i)

    def test_gregory_newton_interpola_nos_uniformes(self):
        xs = [0.2, 0.4, 0.6, 0.8, 1.0]
        ys = [math.exp(x) for x in xs]
        resultado = gregory_newton(xs, ys, 0.23)

        self.assertAlmostEqual(resultado.valor, math.exp(0.23), places=4)
        self.assertIn("delta_1", resultado.tabela[0])

    def test_gregory_rejeita_nos_irregulares(self):
        with self.assertRaisesRegex(ValueError, "igualmente espaçados"):
            gregory_newton([0, 1, 3], [1, 2, 4], 2)

    def test_limite_superior_do_erro(self):
        limite = limite_superior_erro([0, 1, 2], 1.45, math.exp(-1))
        esperado = abs(1.45 * 0.45 * -0.55) * math.exp(-1) / math.factorial(3)
        self.assertAlmostEqual(limite, esperado)


class TesteAjustes(unittest.TestCase):
    def test_ajuste_linear(self):
        xs = [0, 1, 2, 3]
        resultado = ajuste_linear(xs, [2 + 3 * x for x in xs])
        self.assertAlmostEqual(resultado.coeficientes[0], 2)
        self.assertAlmostEqual(resultado.coeficientes[1], 3)
        self.assertAlmostEqual(resultado.r_quadrado, 1)

    def test_ajuste_quadratico(self):
        xs = [0, 1, 2, 3]
        resultado = ajuste_quadratico(xs, [1 - 2 * x + 0.5 * x ** 2 for x in xs])
        for calculado, esperado in zip(resultado.coeficientes, [1, -2, 0.5]):
            self.assertAlmostEqual(calculado, esperado)

    def test_ajuste_exponencial(self):
        xs = [0, 1, 2, 3]
        resultado = ajuste_exponencial(xs, [4 * math.exp(0.3 * x) for x in xs])
        self.assertAlmostEqual(resultado.coeficientes[0], 4)
        self.assertAlmostEqual(resultado.coeficientes[1], 0.3)

    def test_ajuste_exponencial_rejeita_y_nao_positivo(self):
        with self.assertRaisesRegex(ValueError, "positivos"):
            ajuste_exponencial([0, 1], [1, 0])


class TesteIntegracaoInterface(unittest.TestCase):
    def test_todos_os_metodos_da_unidade_2_geram_artefatos(self):
        categorias = ("Interpolação", "Ajuste de curvas (MMQ)")
        base_original = calculos_aplicacao.BASE_DIR
        with TemporaryDirectory() as temporario:
            calculos_aplicacao.BASE_DIR = Path(temporario)
            try:
                for categoria in categorias:
                    for metodo, configuracao in METODOS[categoria].items():
                        entradas = {chave: padrao
                                    for chave, _, padrao in configuracao["campos"]}
                        colunas, linhas, resumo, excel, grafico = (
                            calculos_aplicacao.calcular(categoria, metodo, entradas))
                        self.assertTrue(colunas, metodo)
                        self.assertTrue(linhas, metodo)
                        self.assertTrue(resumo, metodo)
                        self.assertTrue(excel.exists(), metodo)
                        self.assertTrue(grafico.exists(), metodo)
            finally:
                calculos_aplicacao.BASE_DIR = base_original


if __name__ == "__main__":
    unittest.main()
