import scipy.integrate as integrate
from ..geral import Funcao


def eficiencia_total(G, d50=None, G_reduzida=False, Rf=None):
    """Calcula a eficiência total de separação

    Args:
        G (Function): Eficiência granulométrica de separação
        d50 (float, optional): ...

    Returns:
        float: Eficiência total
    """
    if d50:
        Et = integrate.quad(lambda x: G(x,d50), 0, 1)[0]    
    else:
        Et = integrate.quad(lambda x: G(x), 0, 1)[0]
    if G_reduzida:
        if not Rf:
            raise ValueError("Se a eficiência granulométrica é reduzida, deve ser passado o Rf para corrigir o valor. \n")
        Et = Rf + Et*(1-Rf)
    return Et

def eficiencia_global(Et1:float=None, Et2:float=None, Gconj:Funcao=None) -> float:
    """Calcula a eficência global de 2 equipamentos em série

    Args:
        Et1 (float): Eficiência total do primeiro equipamento
        Et2 (float): Eficiência total do segundo equipamento
        Gconj (Funcao): Eficiência granulométrica do conjunto
        
    Returns:
        float: Eficiência global
    """
    if Gconj:
        Et = eficiencia_total(Gconj)
        #raise NotImplementedError()
    elif (Et1 and Et2):
        Et = Et1 + (1-Et1)*Et2
    else:
        raise ValueError("Devem ser passados Et1 e Et2, ou Gconj.\n")        
    return Et