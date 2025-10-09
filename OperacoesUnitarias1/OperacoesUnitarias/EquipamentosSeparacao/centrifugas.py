from math import pi, sqrt, log, tan
from ..geral import isalambda, isafunction, isamethod, Funcao


TUBULAR = 'tubular'
DISCO = 'disco'


def eficiencia_granulometrica(d:float|Funcao, d50:float, R1:float, R2:float) -> float:
    d100 = converter_d50_d100(d50, R1, R2)
    
    ## Defesa contra função lambda de entrada, para funcionar acoplado com outras funções    
    if isalambda(d) or isafunction(d) or isamethod(d):
        G = lambda x: (1/(1-(R1/R2)**2))*(1 - (0.5 + 0.5*(R1/R2)**2) ** ((d(x)/d50)**2)) if d(x) <= d100 else 1
    
    ## G é definida em partes:
    else:
        if d <= d100:
            G = (1/(1-(R1/R2)**2))*(1 - (0.5 + 0.5*(R1/R2)**2) ** ((d/d50)**2))
        else:
            G = 1.0
    return G


def calcular_d50(R1:float, R2:float, w:float, V:float, Q:float, ps:float, p:float, mu:float, 
                 k1:float=None, Cv:float=None, n:float=None) -> float:
    d50 = 9*mu*Q/((ps-p)*w**2*V) * log(2*R2**2/(R2**2 + R1**2))
    if k1:
        d50 /= k1
    if Cv:
        if not n:
            raise ValueError("Se houver Cv, deve ser passado n também.\n")
        d50 /= (1-Cv)**n
    return sqrt(d50)


def calcular_d100(R1:float, R2:float, w:float, V:float, Q:float, ps:float, p:float, mu:float, 
                 k1:float=None, Cv:float=None, n:float=None) -> float:
    d100 = 18*mu*Q/((ps-p)*w**2*V) * log(R2/R1)
    if k1:
        d100 /= k1
    if Cv:
        if not n:
            raise ValueError("Se houver Cv, deve ser passado n também.\n")
        d100 /= (1-Cv)**n
    return sqrt(d100)


def converter_d50_d100(d50, R1, R2):
    return d50 * sqrt(2*log(R2/R1)/log(2*R2**2 / (R2**2+R1**2)))


def sigma(centrifuga:str, R1:float, R2:float, L:float, w:float, g:float=9.81, n:int=None, theta:float=None) -> float:
    if centrifuga.lower() == TUBULAR:
        S = pi * (R2**2-R1**2)*L*w**2 / (g * log(2 / (1 + (R1/R2)**2)))
    elif centrifuga.lower() == DISCO:
        if not (n and theta):
            raise ValueError("Deve-se informar o número de discos e o ângulo. \n")
        S = 2*pi*n * (R2**3-R1**3)*w**2 / (3 * g * tan(theta))
    else:
        raise ValueError("A centrífuga deve ser ou tubular ou de disco. \n")
    return S


def calcular_w(centrifuga:str, sigma:float, R1:float, R2:float, L:float, g=9.81, n:int=None, theta:float=None) -> float:
    if centrifuga.lower() == TUBULAR:
        w = sqrt(sigma * g * log(2/(1 + (R1/R2)**2)) / (pi*L*(R2**2-R1**2)))
    elif centrifuga.lower() == DISCO:
        if not (n and theta):
            raise ValueError("Deve-se informar o número de discos e o ângulo. \n")
        w = sqrt(sigma * 3 * g * tan(theta) / (2 * pi * n * (R2**3 - R1**3)))
    else:
        raise ValueError("A centrífuga deve ser ou tubular ou de disco. \n")
    return w
