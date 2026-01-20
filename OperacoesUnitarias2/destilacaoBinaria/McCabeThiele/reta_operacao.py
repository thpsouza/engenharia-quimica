class RetaOperacao:
    def __init__(self, a:float, b:float, nome:str) -> None:
        self.a = a
        self.b = b
        self.nome = nome
    
    def inversa(self, y) -> float:
        return (y - self.b)/self.a
    
    def __call__(self, x) -> float:
        return self.a * x + self.b
    
    def __repr__(self) -> str:
        return f"Reta de operação - {self.nome}"
    
    def __str__(self) -> str:
        return f"y = {self.a:.4f} * x + {self.b:.4f}"