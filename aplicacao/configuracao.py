"""Catálogo dos métodos disponíveis na interface."""

METODOS = {
    "Linear": {
        "Bissecção": {
            "criterio": "Erro absoluto menor que a tolerância",
            "campos": [("equacao", "Equação f(x)", "50*x^1.5 + 30*x - 500"),
                       ("a", "Limite inferior a", "3"),
                       ("b", "Limite superior b", "5"),
                       ("tol", "Erro desejado (absoluto)", "0.01"),
                       ("max_iter", "Máximo de iterações", "100")],
        },
        "Newton-Raphson": {
            "criterio": "Quantidade de iterações especificada no problema",
            "campos": [("equacao", "Equação f(x)", "2*x^3 - 5*x^2 + 10*x - 490"),
                       ("derivada", "Derivada f'(x)", "6*x^2 - 10*x + 10"),
                       ("x0", "Aproximação inicial x₀", "2"),
                       ("max_iter", "Número de iterações", "4")],
        },
        "Secante": {
            "criterio": "Erro relativo percentual menor que a tolerância",
            "campos": [("equacao", "Equação f(x)", "-5000/x + 15*ln(x) - 0.01*x - ln(15)"),
                       ("x0", "Valor inicial x₀", "400"),
                       ("x1", "Valor inicial x₁", "500"),
                       ("tol_pct", "Tolerância relativa", "0.1"),
                       ("max_iter", "Máximo de iterações", "100")],
        },
    },
    "Não linear": {
        "Newton para sistema 2x2": {
            "criterio": "máx(|d₁|, |d₂|) menor que a tolerância",
            "variaveis": ("x1", "x2"),
            "equacoes": ("f1", "f2"),
            "iniciais": ("x1_0", "x2_0"),
            "campos": [("f1", "Equação f₁(x1,x2)", "x1^3 + 3*x2^2 - 21"),
                       ("f2", "Equação f₂(x1,x2)", "x1^2 + 2*x2 + 2"),
                       ("x1_0", "Valor inicial x1₀", "1.5"),
                       ("x2_0", "Valor inicial x2₀", "-2"),
                       ("tol", "Erro desejado para máx|d|", "0.01"),
                       ("max_iter", "Máximo de iterações", "100")],
        },
        "Newton para sistema 3x3": {
            "criterio": "máx(|dₓ|, |dᵧ|, |d_z|) menor que a tolerância",
            "variaveis": ("x", "y", "z"),
            "equacoes": ("f1", "f2", "f3"),
            "iniciais": ("x0", "y0", "z0"),
            "campos": [("f1", "Equação f₁(x,y,z)", "x^2 + y^2 + z^2 - 1"),
                       ("f2", "Equação f₂(x,y,z)", "2*x^2 + y^2 - 4*z"),
                       ("f3", "Equação f₃(x,y,z)", "3*x^2 - 4*y + z^2"),
                       ("x0", "Valor inicial x₀", "0.5"),
                       ("y0", "Valor inicial y₀", "0.5"),
                       ("z0", "Valor inicial z₀", "0.5"),
                       ("tol", "Erro desejado para máx|d|", "0.01"),
                       ("max_iter", "Máximo de iterações", "100")],
        },
    },
    "Interpolação": {
        "Lagrange": {
            "criterio": "Polinômio único que passa por todos os pontos informados",
            "campos": [("xs", "Valores de x (separados por ;)", "0,2; 0,4; 0,6; 0,8; 1,0"),
                       ("ys", "Valores de y (separados por ;)", "1,2214; 1,4918; 1,8221; 2,2255; 2,7183"),
                       ("x_interp", "Valor de x a interpolar", "0,23"),
                       ("valor_exato", "Valor exato (opcional)", "1,2586"),
                       ("max_derivada", "Máx. |f⁽ⁿ⁺¹⁾| (opcional)", "2,7183")],
        },
        "Newton - Diferenças Divididas": {
            "criterio": "Tabela triangular de diferenças divididas",
            "campos": [("xs", "Valores de x (separados por ;)", "0,1; 0,2; 0,4"),
                       ("ys", "Valores de y (separados por ;)", "2,9182; 2,6667; 2,4286"),
                       ("x_interp", "Valor de x a interpolar", "0,25"),
                       ("valor_exato", "Valor exato (opcional)", "2,6"),
                       ("max_derivada", "Máx. |f⁽ⁿ⁺¹⁾| (opcional)", "")],
        },
        "Gregory-Newton": {
            "criterio": "Diferenças progressivas em pontos igualmente espaçados",
            "campos": [("xs", "Valores de x (separados por ;)", "0,2; 0,4; 0,6; 0,8; 1,0"),
                       ("ys", "Valores de y (separados por ;)", "1,2214; 1,4918; 1,8221; 2,2255; 2,7183"),
                       ("x_interp", "Valor de x a interpolar", "0,23"),
                       ("valor_exato", "Valor exato (opcional)", "1,2586"),
                       ("max_derivada", "Máx. |f⁽ⁿ⁺¹⁾| (opcional)", "2,7183")],
        },
    },
    "Ajuste de curvas (MMQ)": {
        "Ajuste Linear": {
            "criterio": "Minimiza os quadrados dos resíduos de y = a₀ + a₁x",
            "campos": [("xs", "Valores de x (separados por ;)", "0; 1; 2; 3; 4"),
                       ("ys", "Valores de y (separados por ;)", "2,1; 4,9; 8,2; 10,8; 14,1"),
                       ("x_estimativa", "x para estimar y (opcional)", "2,5")],
        },
        "Ajuste Quadrático": {
            "criterio": "Minimiza os quadrados dos resíduos de y = a₀ + a₁x + a₂x²",
            "campos": [("xs", "Valores de x (separados por ;)", "0; 1; 2; 3; 4"),
                       ("ys", "Valores de y (separados por ;)", "1; 0; 1; 4; 9"),
                       ("x_estimativa", "x para estimar y (opcional)", "2,5")],
        },
        "Ajuste Exponencial": {
            "criterio": "Linearização de y = a·exp(bx), com valores de y positivos",
            "campos": [("xs", "Valores de x (separados por ;)", "0; 1; 2; 3; 4"),
                       ("ys", "Valores de y (separados por ;)", "2; 2,7; 3,6; 4,9; 6,6"),
                       ("x_estimativa", "x para estimar y (opcional)", "2,5")],
        },
    },
}

OPCOES_ERRO = {
    "tol": ("1", "0.1", "0.01", "0.001", "0.0001", "0.000001"),
    "tol_pct": ("1", "0.5", "0.1", "0.05", "0.01", "0.001"),
}
