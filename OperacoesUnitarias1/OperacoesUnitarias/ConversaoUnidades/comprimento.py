## Sistema métrico
import time


def cm_to_m(x):
    return x * 0.01


def m_to_cm(x):
    return x * 100


## Sistema inglês
def in_to_ft(x):
    return x / 12


def ft_to_in(x):
    return x * 12


# Conversões entre sistemas
def cm_to_in(x):
    return x / 2.54


def cm_to_ft(x):
    return x / (2.54 * 12)


def m_to_in(x):
    return x * 100 / 2.54


def m_to_ft(x):
    return x * 100 / (12 * 2.54)


def in_to_cm(x):
    return x * 2.54


def in_to_m(x):
    return x * 0.0254


def ft_to_cm(x):
    return x * 30.48


def ft_to_m(x):
    return x * 0.3048
