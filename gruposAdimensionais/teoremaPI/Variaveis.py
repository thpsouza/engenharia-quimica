from sympy import Symbol,sympify

class Variavel():
    '''
    Classe customizada para variáveis na análise dimensional
    '''
    def __init__(self, simbolo:str, dimensoes:str, descricao:str="") -> None:
        self.simbolo = Symbol(simbolo)
        self.dimensoes = sympify(dimensoes)
        self.descricao = descricao
    def __mul__(self,other):
        if isinstance(other,Variavel):
            return self.simbolo*other.simbolo
        else:
            return self.simbolo*other
    __rmul__ = __mul__ 
    def __repr__(self) -> str:
        return f"{self.simbolo} [=] {self.dimensoes}"


#### "Dicionário" com algumas variáveis pré-prontas

## Propriedades fluido
densidade = Variavel('p','M/L**3',"Densidade do fluido")
viscosidade = Variavel('mu','M/L/T',"Viscosidade do fluido")
tensao_superficial = Variavel('σ','M/T**2',"Tensão superficial do fluido")
viscosidade_cinematica = Variavel('Ni','L**2/T',"Viscosidade cinemática do fluido")

## Propriedades gás
densidade_gas = Variavel('p_g','M/L**3',"Densidade do gás")
viscosidade_gas = Variavel('mu_g','M/L/T',"Viscosidade do gás")

## Propriedades de comprimento
comprimento = Variavel('x','L',"Comprimento")
altura = Variavel('h','L',"Altura")
raio = Variavel('r','L',"Raio")
diametro_maior = Variavel('D','L',"Diâmetro externo")
diametro = diametro_menor = Variavel('d','L',"Diâmetro (interno)")
comprimento_de_onda = Variavel('λ','L',"Comprimento de onda")
rugosidade = Variavel('E','L',"Rugosidade relativa")
perda_de_carga = Variavel('h_L','L',"Perda de carga")

## Tempo
tempo = Variavel('t','T',"Tempo")

## Velocidades
velocidade = Variavel('v','L/T',"Velocidade linear")
velocidade_som = Variavel('c','L/T',"Velocidade do som")
velocidade_angular = Variavel('w','1/T',"Velocidade angular")

## Demais
gravidade = Variavel('g','L/T**2',"Aceleração da gravidade")
potencia = Variavel('Pot','M*L**2/T**3',"Potência")
pressao = Variavel('P','M/L/T**2',"Pressão")




