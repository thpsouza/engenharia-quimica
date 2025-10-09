from math import sqrt
from ..geral import isalambda, isafunction, isamethod


def calcular_d50(G:float, d:float):
    return sqrt(d**2 * 0.5/G)
    


def eficiencia_granulometrica(d:float, d50:float=None, d100:float=None) -> float:
    """Calcula a eficiencia granulométrica de uma câmara de poeira

    Args:
        d (float): Diâmetro para calcular eficiência
        d50 (float): Diâmetro cuja eficiência granulométrica é 50%
        d100 (float, optional): Diâmetro cuja eficiência é 100%. Defaults to None.

    Returns:
        float: Eficiência granulométrica para d (G(d))
    """
    ## Defesa contra argumento faltando
    if not (d50 or d100):
        raise ValueError("Deve ser passado d50 ou d100. \n")
    
    ## Caso seja passado o argumento d50, deve-se converter para d100
    elif d50:
        d100 = d50*sqrt(2)
    
    ## Defesa contra função lambda de entrada, para funcionar acoplado com outras funções    
    if isalambda(d) or isafunction(d) or isamethod(d):
        G = lambda x: (d(x)/d100)**2 if d(x) <= d100 else 1
    
    ## G é definida em partes:
    else:
        if d <= d100:
            G = (d/d100)**2
        else:
            G = 1.0

    return G




def eficiencia_granulometrica_global(G1, G2):
    return G1 + (1-G1)*G2