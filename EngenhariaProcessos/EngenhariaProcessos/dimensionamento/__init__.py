"""Subpacote `dimensionamento`.

Contém ferramentas para dimensionamento de equipamentos térmicos, em
particular trocadores de calor. Fornece classes utilitárias para modelar
e calcular parâmetros de projeto como áreas, coeficientes e vazões.

Exporta principal classe:
    - ``TrocadorDeCalor``: classe base para dimensionamento de trocadores.
    - ``Aquecedor``, ``Resfriador``: conveniências/derivações específicas.
"""

from .trocador_de_calor import TrocadorDeCalor, Aquecedor, Resfriador

__all__ = ["TrocadorDeCalor", "Aquecedor", "Resfriador"]