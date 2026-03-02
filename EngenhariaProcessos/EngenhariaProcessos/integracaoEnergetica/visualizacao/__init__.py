"""Subpacote de visualização de análises de integração energética.

Fornece classes para gerar visualizações gráficas de (1) diagramas de cascata
térmica mostrando os degraus de correntes quentes e frias, e (2) redes de
trocadores de calor com suas interconexões.

Exporta publicamente as principais ferramentas de plotagem:
    - ``DiagramaCascataTermica``
    - ``RedeTrocadoresCalor``
    - ``TabelaCascataTermica``
"""

from .tabela_cascata_termica import TabelaCascataTermica
try:
    from .diagrama_cascata_termica import DiagramaCascataTermica
    from .rede_trocadores import RedeTrocadoresCalor
except Exception:
    # Importação falhou (ex.: matplotlib não instalado). Disponibilizamos
    # nomes compatíveis, mas deixamos os objetos como None para evitar
    # falhas ao importar o pacote principal em ambientes sem dependências.
    DiagramaCascataTermica = None
    RedeTrocadoresCalor = None

__all__ = ["DiagramaCascataTermica", "RedeTrocadoresCalor", "TabelaCascataTermica"]
