from .forca import lbf_to_n, n_to_lbf
from .comprimento import ft_to_m, m_to_ft


def watt_to_hp(x):
    return m_to_ft(n_to_lbf(x)) / 550


def hp_to_watt(x):
    return ft_to_m(lbf_to_n(x)) * 550
