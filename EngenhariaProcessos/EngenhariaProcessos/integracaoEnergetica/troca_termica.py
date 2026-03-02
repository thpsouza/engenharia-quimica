from EngenhariaProcessos.corrente import Corrente


class TrocaTermica:
    """Representa uma troca de calor entre dois pares de correntes.

    Attributes:
        id (int): Identificador único da troca no processo de síntese.
        corrente_quente (Corrente): Corrente que fornece calor.
        corrente_fria (Corrente): Corrente que recebe calor.
        n_quente (int): Índice da corrente quente na lista de entrada.
        n_fria (int): Índice da corrente fria na lista de entrada.
    """

    def __init__(self, id:int, corrente_quente:Corrente, corrente_fria:Corrente, id_quente:int, id_fria:int):
        self.id = id
        self.corrente_quente = corrente_quente
        self.corrente_fria = corrente_fria
        self.n_quente = id_quente
        self.n_fria = id_fria
        
    def __iter__(self):
        yield self.corrente_quente
        yield self.corrente_fria

    def __repr__(self):
        return f"{self.id}: 'Quente{self.n_quente} x Fria{self.n_fria}'"