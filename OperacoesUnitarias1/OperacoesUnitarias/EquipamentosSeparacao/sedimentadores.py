def vazao_concentrado(Q, Cv, Cvu):
    return Q * Cv/Cvu


def area_minima(Q, tmin, z0):
    return Q * tmin / z0


def fatores_correcao_area(Dmin: float):
    # O fator f1 está contido no intervalo [1.10, 1.25]. Aqui, é escolhida a média
    f1 = 1.175
    # O fator f2 é calculo através do diâmetro mínimo:
    if Dmin <= 5:
        f2 = 1.5
    elif Dmin < 30:
        f2 = 1.56 - 0.012*Dmin
    else:
        f2 = 1.2
    return f1, f2


def correcao_area_minima(Amin, Dmin):
    f1, f2 = fatores_correcao_area(Dmin)
    return Amin * f1 * f2


def area_minima_lamelados(A_lamela, N, theta):
    # Lazy import
    from math import cos
    return 0.5 * N * A_lamela * cos(theta)


def HCD(tu, tc, Q, Amin, Cv, Cvu):
    return 4 * Q * (tu - tc) / (3 * Amin) * Cv/Cvu


def altura_minima(tu, tc, Q, Amin, Cv, Cvu):
    # HA e HB estão contidos, respectivamente, nos intervalos [0.45, 0.75] e [0.3, 0.6]. Aqui, serão escolhidos os
    # valores médios.
    HA = 0.6
    HB = 0.45
    return HCD(tu, tc, Q, Amin, Cv, Cvu) + HA + HB
