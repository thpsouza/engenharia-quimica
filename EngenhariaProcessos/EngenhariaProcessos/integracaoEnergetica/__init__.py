"""Subpacote `integracaoEnergetica` do projeto EngenhariaProcessos.

Contém ferramentas para análise de integração energética e síntese de
redes de trocadores de calor, incluindo:

- Representação de correntes de processo (classe `Corrente`).
- Construção da cascata térmica e cálculo de intervalos.
- Cálculo dos limites mínimos e máximos de utilidades (vapor/água).
- Algoritmos de síntese de trocadores (ex.: `RPS`, `PD`).
- Ferramentas de visualização (diagramas e tabelas).

Importante: este arquivo expõe as APIs mais usadas pelo usuário; mantê-las
no nível do pacote facilita imports como ``from EngenhariaProcessos.integracaoEnergetica import consumo_minimo_utilidades``.
"""

from .algoritmos_integracao import RPS, PD#, Pinch
from .cascata_termica import calcular_intervalos_cascata_termica, calcular_cascata_termica
from .intervalo_termico import IntervaloTermico
from .limites_integracao import consumo_maximo_utilidades, consumo_minimo_utilidades
from .troca_termica import TrocaTermica
from .visualizacao.tabela_cascata_termica import TabelaCascataTermica
try:
    from .visualizacao.diagrama_cascata_termica import DiagramaCascataTermica
except Exception:
    DiagramaCascataTermica = None

__all__ = [
    "RPS",
    "PD",
    # "Pinch",
    "calcular_intervalos_cascata_termica",
    "calcular_cascata_termica",
    "IntervaloTermico",
    "consumo_maximo_utilidades",
    "consumo_minimo_utilidades",
    "TrocaTermica",
    "TabelaCascataTermica",
    "DiagramaCascataTermica",
]