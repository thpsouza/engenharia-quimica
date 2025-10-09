import matplotlib.pyplot as plt


class Funcao:
    """
    Classe para representar uma função de uma variável e uma constante desconhecida
    """
    def __init__(self, funcao_lambda, cte):
        self.f = funcao_lambda
        self.cte = cte
        
    def __call__(self, x):
        return self.f(x, self.cte)


def isamethod(v):
    class CLASS:
        def f(self): ...
    return isinstance(v, type(CLASS().f))


def isafunction(v):
    def FUNCTION(): ...
    return isinstance(v, type(FUNCTION))


def isalambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


def metodo_secante(f:Funcao, x0:float, x1:float, valor_referencia:float=None, tolerancia:float=10e-4, max_iteracoes=100):
    ''' 
    Função para aplicar o método das secantes
    '''
    for contador in range(1, max_iteracoes+1):
        # Regra da secante
        x2 = x1 - f(x1) / ((f(x1) - f(x0))/(x1 - x0))
        
        # Avaliar função no valor e comparar com valor de referência
        if valor_referencia:
            erro = f(x2) - valor_referencia
        # Se não houver valor de referência, calcula o erro relativo da solução
        else:
            erro = (x2 - x1)/x1
        
        # Condição de parada
        if abs(erro) <= tolerancia: 
            break
            
        # Atualizar valores
        x0 = x1
        x1 = x2
        
    return x2, erro, contador
    
    
def quadratura_gaussiana(f:Funcao, a:float, b:float):
    '''
    Essa função aplica a quadratura gaussiana de 3 pontos em uma função f, no intervalo [a,b]
    '''
    ## Lazy import
    from math import sqrt
    ## Coeficientes
    m = (b-a)/2
    c = (b+a)/2
    ## Pontos
    x1 = -m*sqrt(0.6) + c
    x2 = c
    x3 = m*sqrt(0.6) + c
    ## Integral:
    I = m * (5/9*f(x1) + 8/9*f(x2) + 5/9*f(x3))
    return I


def interpolacao_linear(x, x1, x2, y1, y2):
    """
    Interpola o valor de y(x) dado intervalo [y1(x1), y2(x2)], tal que x1 <= x <= x2
    """
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


def metodo_de_ferrari(a: float, b: float, c: float):
    """
    Essa função soluciona um polinômio do tipo ax^4 + bx + c = 0
    """
    delta0 = 12 * a * c
    delta1 = 27 * a * b ** 2
    q = b / a
    Q = ((delta1 + (delta1 ** 2 - delta0 ** 2) ** (1 / 2)) / 2) ** (1 / 3)
    S = (1 / (3 * a) * (Q + delta0 / Q)) ** (1 / 2) / 2
    x1 = -S + (-4 * S ** 2 + q / S) ** (1 / 2) / 2
    x2 = -S - (-4 * S ** 2 + q / S) ** (1 / 2) / 2
    x3 = S + (-4 * S ** 2 - q / S) ** (1 / 2) / 2
    x4 = S - (-4 * S ** 2 - q / S) ** (1 / 2) / 2
    return {'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4}


def plotar(X: list, Y: list, **kwargs):
    """
    Plota vários k gráficos com n funções em cada.

    Parâmetros
    ----------
        X: list/tuple(list, ...)
            Lista(s) de pontos do eixo x.
            SE mais de uma lista for passada, gera k subplots em uma mesma figura, sendo k = len(X).

        Y: list/tuple(list, ...)/tuple(list[list, ...], ...)
            Lista(s) de pontos do eixo y.
            SE mais de uma lista for passada, gera k subplots em uma mesma figura, sendo k = len(X).
            SE os elementos da lista forem outra tupla, plota "n" funções em cada subplot.

        n: int
            Número de funções plotadas em cada subplot.

    kwargs:
    ----------
        label{i}_{j}: str
            Legenda da função j do gráfico i

        title{i}: str
            Título do gráfico i

        xlabel{i}: str
            Label do eixo x do gráfico i

        ylabel{i}: str
            Label do eixo y do gráfico i

        size: tuple(int, int)
            Tamanho da figura total

    EX:
    ----------
    >>> X = [float, ...]
    >>> Y1 = [(f1(x), f2(x)), ...]
    >>> Y2 = [(g1(x), g2(x)), ...]
    >>> plotar(X=X, Y=[Y1,Y2], xtitle1='Titulo1', xtitle2='Titulo2')
    --> Gera 2 subplots na mesma figura, com 2 funções em cada subplot.

    """
    ## Y: <class 'list'> ---> len = k
    ## Y[0]: <class 'list'>
    ## Y[0][0]: <class 'tuple'> ---> len = n
    ## Y[0][0][0]: <class 'numpy.float64'>

    ## Lazy import
    from numpy import ndarray

    ## Defesa de Y
    if isinstance(Y[0], (list, tuple, ndarray)):
        if isinstance(Y[0][0], (list, tuple, ndarray)):
            ## Contagem de subplots:
            k = len(Y)
            ## Contagem de funções por subplot
            n = len(Y[0][0])
        else:
            Y = [Y]
            k = 1
            n = 1
    else:
        k = 1
        n = 1

    ## Defesa de X
    if not isinstance(X[0], (list, tuple, ndarray)):
        X = [X for i in range(k)]

    ## Inicia a figura 
    if "size" in kwargs:
        size = kwargs[f"size"]
    else:
        size = (10, 8)
    fig = plt.figure(figsize=size)
    axs = fig.subplots(k)
    plt.subplots_adjust(hspace=0.5)

    ## Defesa dos axs
    if k == 1:
        axs = [axs]

    for i in range(k):
        ## Plota as funções no subplot
        if isinstance(Y[i], (list, tuple, ndarray)):
            Y_i = list(zip(*Y[i]))
        else:
            #Y_i = list(Y[i])
            Y_i = [Y]
        for j in range(n):
            if f"label{i + 1}_{j + 1}" in kwargs:
                #print(Y_i)
                axs[i].plot(X[i], Y_i[j], label=kwargs[f"label{i + 1}_{j + 1}"])
            else:
                axs[i].plot(X[i], Y_i[j])
            if f"title{i + 1}" in kwargs:
                axs[i].set_title(kwargs[f"title{i + 1}"], fontsize=16, loc='center')
            if f"xlabel{i + 1}" in kwargs:
                axs[i].set_xlabel(kwargs[f"xlabel{i + 1}"], fontsize=13)
            if f"ylabel{i + 1}" in kwargs:
                axs[i].set_ylabel(kwargs[f"ylabel{i + 1}"], fontsize=13)
        axs[i].legend()
        axs[i].grid()

    plt.show()

