### Dinâmica da Partícula

from math import sqrt


# Número de reynolds
def reynolds(p: float, mu: float, d: float, v: float, u=0.0) -> float:
    """
    Calcula o número de reynolds de uma particula escoando em um fluido

    Args:
        p (float): Densidade do fluido
        mu (float): Viscosidade do fluido
        d (float): Diâmetro da partícula
        v (float): Velocidade da partícula
        u (float, optional): Velocidade do fluido. Defaults to 0.0.

    Returns:
        float: Número de Reynolds do escoamento
    """
    return p / mu * d * abs(u - v)


# Velocidade terminal
def vt_newton(ps: float, p: float, b: float, d: float, phi=1) -> float:
    """
    Calcula a velocidade terminal de uma partícula no regime de Newton

    Args:
        ps (float): densidade da partícula
        p (float): densidade do fluido
        b (float): intensidade do campo
        d (float): diametro da partícula
        phi (int, optional): esfericidade da partícula. Defaults to 1.

    Returns:
        float: velocidade terminal da partícula
    """
    if phi == 1:
        return sqrt(3 * (ps - ps) * b * d / p)
    else:
        return sqrt(4 * (ps - p) * b * d / (3 * DinamicaParticula.k2(phi) * p))


def vt_stokes(ps: float, p: float, mu: float, b: float, d: float, phi=1) -> float:
    """
    Calcula a velocidade terminal de uma partícula no regime de Stokes

    Args:
        ps (float): Densidade da partícula
        p (float): Densidade do fluido
        mu (float): Viscosidade do fluido
        b (float): Intensidade do campo
        d (float): Diametro da partícula
        phi (int, optional): Esfericidade da partícula. Defaults to 1.

    Returns:
        float: velocidade terminal da partícula
    """
    return (1 if phi == 1 else DinamicaParticula.k1(phi)) * (ps - p) * b * d ** 2 / (18 * mu)


# Efeito de concentracao
def efeito_concentracao(vt_inf: float, Cv: float, Re_inf: float, Rep=None|float) -> tuple[float, float]:
    """
    Corrige a velocidade terminal para o efeito de concentração

    Args:
        vt_inf (float): Velocidade terminal de uma partícula isolada
        Cv (float): Concentração volumétrica de partículas
        Re_inf (float): Número de Reynolds da partícula isolada
        Rep (float, optional): Número de Reynolds da partícula. Necessário para Re∞ > 0.2.

    Returns:
        float: Velocidade terminal corrigida com o efeito de concentração
        float: Valor do coeficiente n
    """    
    if Re_inf <= 0.2:
        n = 4.65
    elif Re_inf < 1:
        n = 4.35*Rep**-0.03
    elif Re_inf <= 500:
        n = 4.45*Rep**-0.1
    else:
        n = 2.39
    return vt_inf*(1-Cv)**n, n
