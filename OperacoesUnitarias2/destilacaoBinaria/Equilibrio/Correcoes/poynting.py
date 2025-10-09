class PoyntingFactor:
    def __init__(self) -> None:
        raise NotImplementedError("Não é possível usar a correção de Poynting por enquanto. \n")
        
    def calcular(self):
        return 1
        
    def __call__(self):
        return self.calcular()