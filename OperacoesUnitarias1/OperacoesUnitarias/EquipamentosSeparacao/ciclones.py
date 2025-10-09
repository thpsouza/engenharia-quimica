from math import pi, sqrt
from ..geral import isalambda, isafunction, isamethod, Funcao


def eficiencia_granulometrica(d:float|Funcao, d50:float) -> float:
    ## Defesa contra função lambda de entrada, para funcionar acoplado com outras funções    
    if isalambda(d) or isafunction(d) or isamethod(d):
        G = lambda x: (d(x)/d50)**2 / (1 + (d(x)/d50)**2)
    else:
        G = (d/d50)**2 / (1 + (d/d50)**2)
    return G


def calcular_d50(stk50:float, Dc:float, Q:float, ps:float, p:float, mu:float,
                 k1:float=None, Cv:float=None, n:float=None) -> float:
    d50_2 = stk50 * 9*pi*mu*Dc**3 / (2*(ps-p)*Q)
    if k1:
        d50_2 /= k1
    if Cv:
        if not n:
            raise ValueError("Se houver Cv, deve ser passado n também.\n")
        d50_2 /= (1-Cv)**n
    return sqrt(d50_2)


def calcular_Dc(stk50:float, d50:float, Q:float, ps:float, p:float, mu:float,
                 k1:float=None, Cv:float=None, n:float=None) -> float:
    Dc3 = 2*(ps - p)*Q*d50**2 / (9*pi*mu*stk50)
    if k1:
        Dc3 *= k1
    if Cv:
        if not n:
            raise ValueError("Se houver Cv, deve ser passado n também.\n")
        Dc3 *= (1-Cv)**n
    return Dc3**(1/3)


def Stk50(d50:float, Q:float, Dc:float, ps:float, p:float, mu:float,
          k1:float=None, Cv:float=None, n:float=None) -> float:
    stk50 = 2 * (ps - p)*Q*d50**2 / (9*pi*mu*Dc**3)
    if k1:
        stk50 *= k1
    if Cv:
        if not n:
            raise ValueError("Se houver Cv, deve ser passado n também.\n")
        stk50 *= (1-Cv)**n
    return stk50


def deltaP(Eu:float, Dc:float, Q:float, p:float) -> float:
    return 8*Eu*p*Q**2 / (pi**2 * Dc**4)


def potencia(dP:float, Qt:float, eficiencia=0.5):
    return dP * Qt / eficiencia
