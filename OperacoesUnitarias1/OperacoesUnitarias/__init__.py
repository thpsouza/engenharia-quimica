# ## Import externals
# import sys
# externals = []
# modules = {
#     "math":"from math import sqrt, log, log10, exp, tanh, pi, asin",
#     "matplotplib":"import matplotlib.pyplot as plt", 
#     "numpy":"import numpy as np", 
#     "sympy":"import sympy as sp", 
#     "scipy":"import scipy.integrate as integrate"
# }
# for module in modules:
#     if module not in sys.modules:
#         print(f"importing {module}\n")
#         externals.
#         exec(modules[module])


## Topicos OP1
from . import (
    Granulometria,
    DinamicaParticula,
    EquipamentosSeparacao,
    MeiosPorosos,
    Fluidizacao
    )
from .Granulometria import *
from .EquipamentosSeparacao import (
    camaras_de_poeira as CamaraPoeira,
    ciclones as Ciclone,
    elutriadores as Elutriador,
    hidrociclones as Hidrociclone,
    centrifugas as Centrifuga,
    sedimentadores as Sedimentador,
    eficiencia as EficienciaSeparacao
)

## Conversao de unidades
from . import ConversaoUnidades as conversao

## Gerais
from .geral import *
from .propriedades_materiais import *
