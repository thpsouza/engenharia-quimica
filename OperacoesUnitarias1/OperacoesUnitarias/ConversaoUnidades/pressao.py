from .forca import lbf_to_n, n_to_lbf
from .area import in2_to_m2, m2_to_in2


def dynapcm2_to_pa(x):
    return x * 0.1


def psi_to_pa(x):
    return 1/in2_to_m2(1/lbf_to_n(x))


def bar_to_pa(x):
    return x * 1e5


def atm_to_pa(x):
    return x * 101325


def mmHg_to_pa(x):
    return x * 101325 / 760


def cmHG_to_pa(x):
    return x * 10 * 101325 / 760


def cmH2O_to_pa(x):
    return x * 98.0665


def pa_to_dynapcm2(x):
    return x * 10


def pa_to_psi(x):
    return 1/m2_to_in2(1/n_to_lbf(x))


def pa_to_bar(x):
    return x * 1e-5


def pa_to_atm(x):
    return x / 101325
