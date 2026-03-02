class IntervaloTermico:
    """Representa um intervalo de temperatura em análises térmicas.

    Mantém as temperaturas sempre ordenadas (Ti > Tf) para facilitar
    comparações e operações de cascata térmica. Suporta igualdade,
    comparabilidade e hash para uso em estruturas como sets.

    Attributes:
        Ti (float): Temperatura superior (maior) em °C.
        Tf (float): Temperatura inferior (menor) em °C.
    """

    def __init__(self, Ti, Tf) -> None:
        # Sempre ordenado da maior T para a menor:
        if Ti > Tf:
            self.Ti = Ti
            self.Tf = Tf
        else:
            self.Ti = Tf
            self.Tf = Ti
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, IntervaloTermico):
            return NotImplemented
        comparacao_direta = (self.Ti == other.Ti) and (self.Tf == other.Tf)
        comparacao_reversa = (self.Ti == other.Tf) and (self.Tf == other.Ti)
        return comparacao_direta or comparacao_reversa
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, IntervaloTermico):
            return NotImplemented
        return self.Ti < other.Ti
    
    def __gt__(self, other):
        if not isinstance(other, IntervaloTermico):
            return NotImplemented
        return self.Ti > other.Ti # Compara sempre em relação à maior temperatura (Ti)
    
    def __hash__(self) -> int:
        return hash((self.Ti, self.Tf))
    
    def __repr__(self) -> str:
        return f"({self.Ti}, {self.Tf})"