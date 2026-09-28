# Laboratório de Métodos Numéricos

Aplicação educacional em Python para executar métodos numéricos, acompanhar as
etapas dos cálculos e gerar relatórios. A interface gráfica usa Tkinter e o
núcleo matemático também pode ser importado diretamente em outros programas.

## Funcionalidades

A aplicação está organizada em quatro categorias:

| Categoria | Métodos |
|---|---|
| Raízes de equações (`Linear`) | Bissecção, Newton-Raphson e secante amortecida |
| Sistemas (`Não linear`) | Newton para sistemas 2x2 e 3x3 |
| Interpolação | Lagrange, Newton por diferenças divididas e Gregory-Newton |
| Ajuste de curvas (`MMQ`) | Linear, quadrático e exponencial |

Cada execução apresenta uma tabela de cálculo, um resumo numérico e gera um
arquivo Excel e um gráfico PNG. Os exemplos preenchidos na interface podem ser
substituídos por outros dados.

## Requisitos

- Python 3.10 ou superior;
- Tkinter disponível na instalação do Python;
- dependências listadas em `requirements.txt`.

## Instalação e execução

No PowerShell, a partir da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python interface_metodos.py
```

Se o ambiente virtual já estiver configurado, execute apenas o último comando.

## Como usar a interface

1. Selecione o **Tipo do problema**.
2. Escolha o **Método**.
3. Revise ou substitua os dados preenchidos.
4. Clique em **Calcular e gerar arquivos**.
5. Consulte o resumo e a tabela ou use os botões para abrir o Excel e o gráfico.

Entradas inválidas são rejeitadas com uma mensagem explicando a correção
necessária. O máximo de iterações limita métodos iterativos e preserva os
resultados parciais quando a tolerância não é atingida.

### Equações

As equações devem representar expressões igualadas a zero. Use `x` nos métodos
de uma variável e os nomes exibidos nos campos para sistemas. A sintaxe aceita:

- `*` para multiplicação e `^` ou `**` para potência;
- constantes `e` e `pi`;
- `abs`, `acos`, `asin`, `atan`, `cos`, `cosh`, `exp`, `ln`, `log`, `log10`,
  `sin`, `sinh`, `sqrt`, `tan` e `tanh`.

Exemplo: `x^2 - 2`.

### Listas de pontos

Interpolação e MMQ recebem listas de valores de $x$ e $y$. Separe os itens com
ponto e vírgula. Ponto e vírgula decimal são aceitos:

```text
x: 0,2; 0,4; 0,6; 0,8; 1,0
y: 1,2214; 1,4918; 1,8221; 2,2255; 2,7183
```

As duas listas devem ter o mesmo tamanho. As abscissas da interpolação devem
ser distintas, e Gregory-Newton exige espaçamento uniforme entre elas.

### Campos opcionais

Na interpolação:

- `Valor exato` calcula $|f(x)-P_n(x)|$;
- `Máx. |f⁽ⁿ⁺¹⁾|` calcula o limite
  $|\prod_i(x-x_i)|M_{n+1}/(n+1)!$.

No MMQ, `x para estimar y` avalia o modelo ajustado e destaca o ponto no
gráfico. Esses campos podem ficar vazios.

## Resultados e arquivos

Os resultados são gravados em pastas criadas automaticamente:

| Categoria | Excel | Gráficos |
|---|---|---|
| Linear | `MetodosLineares/Excel` | `MetodosLineares/IMG/Graficos` |
| Não linear | `Metodo de newton/Excel` | `Metodo de newton/IMG/Graficos` |
| Interpolação | `Interpolacao/Excel` | `Interpolacao/IMG/Graficos` |
| MMQ | `AjusteCurvas/Excel` | `AjusteCurvas/IMG/Graficos` |

Os nomes incluem o método e a data/hora da execução. As planilhas contêm os
dados de entrada, o critério aplicado, o resumo e a mesma tabela apresentada na
interface.

As tabelas variam conforme o método:

- raízes: valores de cada iteração e erros;
- sistemas: variáveis, funções, passos e erro máximo;
- Lagrange: bases $L_i(x)$ e contribuições $y_iL_i(x)$;
- Newton e Gregory-Newton: tabelas de diferenças;
- MMQ: valores observados, estimados e resíduos.

## Observações numéricas

- Bissecção requer troca de sinal no intervalo inicial.
- Newton-Raphson pode parar se a derivada for nula.
- A secante amortecida recua quando uma tentativa sai do domínio da função.
- Interpolação com muitos pontos pode sofrer oscilações e perda de precisão.
- Gregory-Newton aceita somente pontos igualmente espaçados.
- O ajuste exponencial requer todos os valores de $y$ positivos.
- $R^2$ descreve a qualidade do ajuste, mas não garante que o modelo seja
  adequado ao fenômeno estudado.

## Uso como biblioteca

A API pública está disponível no pacote `core`:

```python
from core import lagrange, newton_diferencas_divididas

xs = [0.2, 0.4, 0.6, 0.8, 1.0]
ys = [1.2214, 1.4918, 1.8221, 2.2255, 2.7183]

por_lagrange = lagrange(xs, ys, 0.23)
por_newton = newton_diferencas_divididas(xs, ys, 0.23)

print(por_lagrange.valor)
print(por_newton.tabela)
```

Lagrange e Newton produzem o mesmo polinômio para o mesmo conjunto de pontos.
Os coeficientes retornados seguem a ordem $[a_0,a_1,\ldots,a_n]$, correspondente
a $P(x)=a_0+a_1x+\cdots+a_nx^n$.

## Arquitetura

```text
interface_metodos.py       Janela, eventos e apresentação Tkinter
aplicacao/
  configuracao.py          Catálogo de categorias, métodos e campos
  calculos.py              Validação, casos de uso e geração de arquivos
core/
  modelos.py               Tipos compartilhados
  raizes.py                Métodos de raízes
  sistemas.py              Newton para sistemas não lineares
  interpolacao.py          Interpoladores e análise de erro
  ajuste_curvas.py         Ajustes por mínimos quadrados
  expressoes.py            Compilação segura das equações
  graficos.py              Gráficos de funções de uma variável
  formatacao.py            Tabelas para uso em terminal
tests/
  test_interpolacao_ajustes.py
```

`core/metodos_numericos.py` permanece como fachada de compatibilidade para
imports antigos. Novos códigos devem importar diretamente de `core`.

## Testes

```powershell
python -m unittest discover -s tests -v
```

A suíte cobre os interpoladores, os três ajustes por MMQ, validações de domínio
e a geração de Excel e gráficos pelos fluxos de interpolação e ajuste de curvas.
