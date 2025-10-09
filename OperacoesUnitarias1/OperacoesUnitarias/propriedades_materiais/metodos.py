from ..geral import interpolacao_linear
from . import agua, ar

def p_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "p")


def kar_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "kar")


def ni_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "ni")


def cp_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "cp")


def Pr_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "Pr")

def mu_ar(T):
    """ T em Kelvin """
    return _propriedade_ar(T, "ni") * _propriedade_ar(T, "p")


def _propriedade_ar(T, propriedade):
    """ T em Kelvin, propriedades: p,kar,ni,cp,Pr"""
    if T % 100 > 50:
        T1 = T // 100 * 100 + 50
    elif T % 100 < 50:
        T1 = T // 100 * 100
    else:
        return eval(f"ar.{propriedade}{int(T)}")
    T2 = T1 + 50
    prop1 = eval(f"ar.{propriedade}{int(T1)}")
    prop2 = eval(f"ar.{propriedade}{int(T2)}")
    return interpolacao_linear(T, T1, T2, prop1, prop2)


def p_agua(T):
    """ T em Kelvin """
    return _propriedade_agua(T, "p")


def mu_agua(T):
    """ T em Kelvin """
    return _propriedade_agua(T, "mu")


def k_agua(T):
    """ T em Kelvin """
    return _propriedade_agua(T, "k")


def cp_agua(T):
    """ T em Kelvin """
    return _propriedade_agua(T, "cp")


def Pr_agua(T):
    """ T em Kelvin """
    return _propriedade_agua(T, "Pr")


def _propriedade_agua(T, propriedade):
    """ T em Kelvin, propriedades: p,mu,k,cp,Pr"""
    
    if 290 <= T <= 305:
        if 290 < T < 300:
            T1 = 290
            T2 = 300
        elif 300 < T < 305:
            T1 = 300
            T2 = 305
        else:
            return eval(f"agua.{propriedade}{int(T)}")
        prop1 = eval(f"agua.{propriedade}{int(T1)}")
        prop2 = eval(f"agua.{propriedade}{int(T2)}")
        return interpolacao_linear(T, T1, T2, prop1, prop2)
    else:
        raise NotImplementedError("Só há propriedades no intervalo 290K~305K.")