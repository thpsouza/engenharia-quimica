### Dinâmica da Partícula

from math import log10


# Correlações de Coelho e Massarani
def k1(esfericidade: float) -> float:
    return 0.843 * log10(esfericidade / 0.065)


def k2(esfericidade: float) -> float:
    return 5.31 - 4.88 * esfericidade


def CdRep2(d: float, ps: float, p: float, mu: float, g: float = 9.81) -> float:
    return 4 * (ps - p) * p * g * d ** 3 / (3 * mu ** 2)


def Cd_Rep(vt: float, ps: float, p: float, mu: float, g: float = 9.81)  -> float:
    return 4 * (ps - p) * g * mu / (3 * p ** 2 * vt ** 3)


def Cd(Rep: float, k1: float, k2: float) -> float:
    return ((24 / k1 * Rep) ** 0.85 + k2 ** 0.85) ** 1.18


def Rep_cdrep2(cdrep2: float, k1: float, k2: float) -> float:
    return ((24 / (k1 * cdrep2)) ** 1.2 + (k2 / cdrep2) ** 0.6) ** -0.83


def Rep_cd_rep(cd_rep: float, k1: float, k2: float) -> float:
    return ((24 / (k1 * cd_rep)) ** 0.65 + (k2 / cd_rep) ** 1.3) ** 0.77


def Rep(k1, k2, cd_rep=None, cdrep2=None):
    if cdrep2:
        rep = Rep_cdrep2(cdrep2, k1, k2)
    elif cd_rep:
        rep = Rep_cd_rep(cd_rep, k1, k2)
    else:
        raise ValueError("Deve ser passado Cd/Rep ou CdRep²!\n")
    return rep