from .volume import ft3_to_m3, m3_to_ft3
from .massa import lbm_to_kg, kg_to_lbm


def gpcm3_to_kgpm3(x):
    return x * 1e3


def kgpm3_to_gpcm3(x):
    return x * 1e-3


def lbmpft3_to_kgpm3(x):
    return 1/ft3_to_m3(1/lbm_to_kg(x))


def lbmpft3_to_gpcm3(x):
    return kgpm3_to_gpcm3(lbmpft3_to_kgpm3(x))
