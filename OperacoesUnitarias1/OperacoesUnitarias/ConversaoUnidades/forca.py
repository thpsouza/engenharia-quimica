from .massa import lbm_to_kg, kg_to_lbm

g = 9.80665


def n_to_dyna(x):
    return x * 1e5


def dyna_to_n(x):
    return x / 1e5


def lbf_to_n(x):
    return lbm_to_kg(x) * g


def n_to_lbf(x):
    return kg_to_lbm(x) / g
