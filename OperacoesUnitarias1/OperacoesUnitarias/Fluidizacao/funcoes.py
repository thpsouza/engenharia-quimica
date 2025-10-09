
def deltaP_distribuidor(deltaP_leito):
    if 0.1*deltaP_leito >= 3550:
        return 0.1*deltaP_leito
    return 3550


def potencia_fluidizacao_liquido(Wb, Q, p, g=9.81, eficiencia=0.5):
    raise NotImplementedError()


def potencia_fluidizacao_gas(P1, P2, Q2, cp, cv, eficiencia=0.5):
    raise NotImplementedError()
