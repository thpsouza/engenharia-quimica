"""Pacote principal do projeto EngenhariaProcessos.

Este pacote reúne módulos para análise de integração energética,
dimensionamento de trocadores de calor e utilitários auxiliares usados
no curso/projeto.

Estrutura (submódulos relevantes):
- ``dimensionamento``: Ferramentas para dimensionamento de trocadores de calor.
- ``integracaoEnergetica``: Análises de cascata térmica, limites de utilidades
  e algoritmos de síntese de redes de trocadores.

Exemplo rápido::

    from EngenhariaProcessos import Corrente
    from EngenhariaProcessos.integracaoEnergetica import consumo_minimo_utilidades

    c1 = Corrente(WCp=100, To=200, Td=100)
    c2 = Corrente(WCp=80, To=20, Td=120)
    vazoes, Q_min, intervalos, tabela = consumo_minimo_utilidades([c1, c2], 4.18, 10, 2256)

Itens exportados neste pacote:
    - ``Corrente``, ``ListaCorrentes``: classes básicas de representação de correntes.
"""

from . import (
    dimensionamento,
    integracaoEnergetica,
    # otimizacao
    )

from .corrente import Corrente, ListaCorrentes

__all__ = [
    "dimensionamento",
    "integracaoEnergetica",
    # "otimizacao",
    "Corrente",
    "ListaCorrentes",
]