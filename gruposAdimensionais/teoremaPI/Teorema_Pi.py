import sympy as sp
import numpy as np
from Variaveis import *
from sympy import init_printing


class Pi():
    '''
    Classe customizada para criar grupos Pi.
    '''
    def __init__(self,n:int,expressao:str) -> None:
        self.n = n
        self.expressao = expressao
    def __repr__(self) -> str:
        PI = u'\u03A0'
        return f"{PI}{self.n} = {self.expressao}"


def achar_expoente(variavel:sp.Expr,dimensao:sp.Expr) -> int:
    '''
    Recebe uma variável em termo de dimensões primárias, e uma dimensão específica.
    Retorna o expoente da dimensão na variável.

    Ex: 
    >>> V = L/T
    >>> achar_expoente(V,L)
    1
    >>> achar_expoente(V,T)
    -1
    '''
    ## Contador para considerar erros desconhecidos
    # Caso o contador seja diferente de 1, a mesma dimensão foi considerada duas vezes
    # Provavelmente não será necessário.
    k = 0

    ## Se não houverem argumentos, a variável tem expoente 1 em uma dimensão apenas.
    argumentos = variavel.args
    if len(argumentos) == 0:
        ## Achar dimensão e definir expoente:
        expoente = [int(variavel == dimensao)]
        k+=1

    ## Considerar possibilidade variavel [=] 1/dimensao**n:
    elif all([str(dimensao) in str(argumentos[0]),isinstance(argumentos[1],sp.core.numbers.Integer)]):
        expoente = [argumentos[1]]
        k+=1

    ## Se houverem argumentos (mais de uma dimensão):
    else:
        for arg in argumentos:
            ## Se o argumento atual contiver a dimensão:
            ## Obtém a potência da dimensão -- Feito em lista para poder iterar numa linha apenas
            if str(dimensao) in str(arg):
                expoente = [j for j in arg.atoms() if j.is_number]           
                k+=1

                # Casos em que a dimensão tem potência 1
                if not expoente:
                    expoente = [1]

    ## Caso o contador seja 0, essa variável não tem tal dimensão
    if not k:
        expoente = [0]

    ## Levanta erros caso o contador seja maior que 1 (sobrescreveu expoente), ou se houver mais de um expoente na lista (não deve ser possível)
    if len(expoente)>1:
        raise Exception("Algum erro desconhecido ocorreu. (Mais de um expoente)")
    elif k>1:
        raise Exception("Algum erro desconhecido ocorreu. (Expoente sobrescrito)")
    
    ## Retorna o primeiro item da lista (expoente)
    return expoente[0]


def teorema_pi(variaveis:list,MLT:bool=True,dimensoes_primarias:list=None) -> list:
    '''
    Função para aplicar o Teorema Pi de Bunckingham

    Variáveis devem ser passadas com o auxílio da classe 'Variavel', em função das dimensões do problema, sejam elas 'MLT' ou não.
    # Observações: \n
    - O núcleo será escolhido a partir das m primeiras variáveis sempre.
    - A variável dependente das demais deve ser estar em último na lista.
    - Caso o parâmetro 'MLT' seja definido como False, devem ser passadas as dimensões primárias utilizadas, pelo parâmetro 'dimensoes_primarias'
    '''

    ## Definição das dimensões primárias
    if MLT:
        M,L,T = sp.symbols('M L T')
        dimensoes_primarias = M,L,T
    elif dimensoes_primarias is None:
        raise Exception("Erro. As dimensões primárias não foram definidas.")
    else:
        dimensoes_primarias = dimensoes_primarias

    ## Matriz das variáveis em termos das dimensões primárias
    matriz = sp.Matrix([[achar_expoente(v.dimensoes,d) for v in variaveis] for d in dimensoes_primarias])

    ## Núcleo da matriz
    nucleo_matriz = matriz.nullspace()

    ## Para fins de praticidade
    nucleo = variaveis[:len(dimensoes_primarias)]
    variaveis = np.asarray([v.simbolo for v in variaveis])

    ## Grupos Pi
    grupos_pi = []
    for i,j in enumerate(nucleo_matriz):
        expr =  (variaveis**np.array([k for k in j])).prod()
        grupos_pi.append(Pi(i+1,f"{expr}"))

    return [grupos_pi, matriz, nucleo, dimensoes_primarias]


def display(variaveis, pis, matriz, nucleo, dimensoes):
    init_printing()
    
    print(f"Dimensões primárias: {dimensoes}\n")
    
    print("Matriz:")
    sp.pprint(matriz)
    print()
    
    print("Variávies: \n\t%s\n" %"\n\t".join([f"{i.simbolo} - {i.descricao} - {i.dimensoes}" for i in variaveis]))
    print(f"Núcleo: {', '.join([str(i.simbolo) for i in nucleo])}\n")
    
    print("Grupamentos PI:")
    if pis:
        for pi in pis: 
            print(pi)


def main():
    ## Para criar variáveis:
    # Variavel('simbolo', 'dimensao', 'nome')
    
    ## O nucleo são os m primeiros itens da lista de varíaveis
    variaveis = [
        diametro,densidade,viscosidade,
        gravidade,tensao_superficial,velocidade,
        densidade_gas,viscosidade_gas
        ]
    
    grupos_pi, matriz, nucleo, dimensoes = teorema_pi(variaveis)
    display(variaveis, grupos_pi, matriz, nucleo, dimensoes)
    input()
 

if __name__ == '__main__':
    main()