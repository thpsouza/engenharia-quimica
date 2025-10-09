from math import sqrt, exp, log, pi
from ..geral import Funcao, isalambda, isafunction, isamethod


BRADLEY = 'Bradley'
RIETEMA = 'Rietema'
CBV_DEMCO = 'CBV-Demco'
TIPOS_PADRAO_HIDROCICLONE = [BRADLEY, RIETEMA, CBV_DEMCO]


## Equações gerais
def eficiencia_granulometrica_reduzida(d:float|Funcao, d50:float, n=3) -> float:
    ## Defesa contra função lambda de entrada, para funcionar acoplado com outras funções    
    if isalambda(d) or isafunction(d) or isamethod(d):
        G = lambda x: 1 - exp(-0.693 * (d(x)/d50)**n)
    else:
        G = 1 - exp(-0.693 * (d/d50)**n)
    return G


def reynolds(Q, Dc, p, mu):
    return 4 * p * Q / (pi * mu * Dc)


def calcular_d50(Stk50_Eu:float, Dc:float, Q:float, dP:float, 
                 ps:float, p:float, mu:float) -> float:
    return sqrt(Stk50_Eu * 36 * mu * p * Q / (pi * (ps-p) * dP * Dc))


def calcular_Cv_underflow(Et, Rf, Cv):
    return Et*Cv/(Rf*(1-Cv) + Et*Cv)

def calcular_Cv_overflow(Et, Q, Cv, Cv_underflow):
    return Cv*(1 - Et)/(1 - Cv/Cv_underflow * Et)

def calcular_vazao(hidrociclone, dP, Dc, p, mu, Cv=None):
    if hidrociclone not in TIPOS_PADRAO_HIDROCICLONE:
        raise ValueError("O hidrociclone não é de nenhuma família conhecida. Para um hidrociclone qualquer, use calcular_vazao_qualquer.")
    if hidrociclone is BRADLEY:
        Q = (Dc * dP**0.23 * mu**0.085 / (3.5 * p**0.31))**(1/0.54)
    elif hidrociclone is RIETEMA:
        if not Cv:
            raise ValueError("Para o hidrociclone do tipo Rietema, deve-se informar Cv. \n")
        Q = (Dc * dP**0.24 * mu**0.028 / (4 * p**0.27 * exp(-0.52 * Cv)))**(1/0.51)
    elif hidrociclone is CBV_DEMCO:
        Q = dP**0.5 * Dc**2 / (51.8 * p**0.5)
    else:
        raise NotImplementedError()
    return Q


## Equações para as famílias BRADLEY, RIETEMA E CBV-DEMCO 4H
def Eu(hidrociclone, Re, Cv):
    if hidrociclone not in TIPOS_PADRAO_HIDROCICLONE:
        raise ValueError("O hidrociclone não é de nenhuma família conhecida. Para um hidrociclone qualquer, use "
                         "Eu_qualquer.")
    k2, n3, n4 = {
        RIETEMA:(371.5, 0.12, -2.12),
        BRADLEY:(258, 0.37, -0),
        CBV_DEMCO:(3300, 0, 0)
    }[hidrociclone]
    return k2 * Re**n3 * exp(n4*Cv)


def razao_de_fluido(hidrociclone, Du, Dc, Eu):
    if hidrociclone not in TIPOS_PADRAO_HIDROCICLONE:
        raise ValueError("O hidrociclone não é de nenhuma família conhecida. Para um hidrociclone qualquer, use "
                         "razao_de_fluido_qualquer.")
    k3, n5, n6 = {
        RIETEMA:(1218, 4.75, -0.3),
        BRADLEY:(1.21e6, 2.63, -1.12),
        CBV_DEMCO:(0.127, 0.78, 0)
    }[hidrociclone]
    return k3 * (Du/Dc)**n5 * Eu**n6


def Stk50Eu(hidrociclone, Rf, Cv):
    if hidrociclone not in TIPOS_PADRAO_HIDROCICLONE:
        raise ValueError("O hidrociclone não é de nenhuma família conhecida. Para um hidrociclone qualquer, use "
                         "Stk50Eu_qualquer.")
    k1, n1, n2 = {
        RIETEMA:(0.0474, 0.74, 9),
        BRADLEY:(0.0550, 0.66, 12),
        CBV_DEMCO:(0.0088, 2.31, 15.5)
    }[hidrociclone]
    return k1 * log(1/Rf)**n1 * exp(n2*Cv)


## Equações para um hidrociclone qualquer
def Eu_qualquer(Dc, Di, Do, Du, L, l, Re, Cv):
    return 21.8 * Dc**0.57 * (Dc/Di)**2.61 * (Dc / (Do**2 + Du**2))**0.42 * (Dc / (L - l))**0.98 * Re**0.12 * exp(-0.51*Cv)


def razao_de_fluido_qualquer(Dc, Du, Do, Eu):
    return 1.18 * (Dc/Do)**5.97 * (Du/Dc)**3.10 * Eu**-0.54


def Stk50Eu_qualquer(Dc, Do, L, l, Rf, Cv):
    return 0.12 * (Dc/Do)**0.95 * (Dc / (L-l))**1.33 * (log(1/Rf))**0.79 * exp(12*Cv)
