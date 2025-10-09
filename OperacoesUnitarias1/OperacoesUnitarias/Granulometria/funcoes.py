### Granulometria

from numpy import asarray, ndarray, pi, sqrt
from . import GGS,Sigmoide,RRB,Distribuicao


def circularidade(area_projetada: float, perimetro: float) -> float:
    return sqrt(4 * pi * area_projetada / perimetro**2)


def esfericidade(V_particula: float, A_particula: float) -> float:
    r = (V_particula * 3 / (4 * pi))**(1/3)
    A_esfera = 4 * pi * r**2
    return A_esfera / A_particula


def diametro_medio_sauter(x: list, d: list | ndarray) -> float:
    x = asarray(x)
    d = asarray(d)
    return 1 / (x/d).sum()


def distribuicao_cumulativa(x:ndarray) -> ndarray:
    """Calcula a distribuição cumulativa de uma amostra, dado um array com as frações mássicas

    Args:
        x (ndarray(float)): Array de frações ponderais da amostra

    Returns:
        ndarray: Array da distribuicao cumulativa
    """    
    return asarray([x[i:].sum() for i in range(len(x))])


def melhor_modelo(y,d) -> Distribuicao:
    """Retorna o melhor modelo, baseado no critério R2

    Args:
        y (list(float)): Distribuição cumulativa menor que d
        d (list(float)): Diametros, em micra

    Returns:
        Distribuicao: O melhor modelo fittado.
    """
    melhor = None
    melhor_R2 = 0
    print(1)
    for modelo in [GGS(y,d),Sigmoide(y,d),RRB(y,d)]:
        modelo.fit()
        print(2)
        if modelo.R2 > melhor_R2:
            melhor_R2 = modelo.R2
            melhor = modelo
    return melhor