#!/usr/bin/env python
"""
Título: Implementação do método gráfico de McCabe-Thiele
Autor: Thiago Pacheco de Souza
Data: 2026-01-20
Versão: 2.0
Descrição:
    Este programa aplica o método gráfico de McCabe-Thiele para resoluçaõ de um sistema de destilação 
    binária, gerando o gráfico e indicando os estágios necessários.

    É dividido em dois módulos principais:
    1- Calculo do equilíbrio termodinâmico.
    2- Implementação do método de McCabe-Thiele.

    A curva de equilibrio é calculada modelando a fase líquida pelo coeficiente de atividade, γ, e 
    pela pressão de saturação de cada componente. Utiliza-se o modelo NRTL para γ, e a equação de 
    Antoine para Psat. As correção de Poynting e os coeficientes de fugacidade não foram implementados. 
    Logo, a curva de equilíbrio termodinâmico gerada só é precisa para sistemas em baixas pressões.

    De momento, as espécies químicas suportadas são:
    - Água
    - Metanol
    - Etanol
    - Benzeno
    - Tolueno
    - p-Xileno
    - Acetona
    - Cloroformio

    O módulo de aplicação do método é independente do módulo de equilíbrio, mas requer uma função de
    equilíbrio para esboçar os degraus. 
    
    É possível inserir manualmente os pontos X,Y,T do equilíbrio, que serão interpolados cubicamente 
    e plotados no diagrama.

    Além dos módulos principais, há 4 scripts para testar individual cada funcionalidade da geração
    de dados de equilíbrio e da aplicação do método.

Como usar:
    - Execute este script diretamente para rodar a aplicação.
    - Os parâmetros de entrada podem ser ajustados nas variáveis globais abaixo.
    - O modo interativo permite alterar os parâmetros de entrada do problema dinâmicamente. 

Dependências externas:
    - numpy
    - matplotlib
    - scipy
"""

## Instruções extras:
# 1 - Para R->inf, use um valor alto (R=10000, por exemplo). Nesse caso, deve-se desativar o modo interativo
# 2 - Se 'PLOTAR' for falso, os cálculos serão impressos no console apenas.
# 3 - O modo interativo pode deixar o programa um pouco lento, a depender da máquina.
# 4.1 - Para a inserção manual dos dados de equilíbrio, basta adicioná-los nos arrays X,Y,T.
# 4.2 - Quanto mais dados de equilíbrio forem inseridos, melhor será o ajuste da curva.
# 4.3 - As temperaturas precisam ser inseridas em Kelvin.
# 4.4 - Se deixados vazios, comentados ou deletados, o módulo de equilíbrio acoplado calculará a curva, 
# para espécies válidas.
# 5 - Os cálculos de equilíbrio podem apresentar desvios. Alguns dados coletados manualmente podem ser usados
# no lugar. ('from equilibrio.dados_manuais import equilibrio_...')


### Dados base do problema
pressao = 101325
especies = "acetona", "isopropanol"
F = 60
zF = 0.56
xD = 0.94
xB = 0.03
R = 2
q = 1
Eml = 1.0
Emv = 1.0

### Dados adicionais
## Alimentação extra na lateral da coluna
ALIMENTACAO_ADICIONAL = False
F2 = 100
zF2 = 0.4
q2 = 0.5

## Saída de produto na lateral da coluna
SAIDA_ADICIONAL = False
S = 20 # Vazão total
s = 1 # Porcentagem dessa corrente que é líquida
zS = 0.74

## Entrada de vapor direto na base da coluna:
ENTRADA_VAPOR_FUNDO = False

### Opções de plot
PLOTAR = True
INTERATIVO = True
SALVAR = False


### Dados de equilíbrio
# X = [0, 0.087, 0.249, 0.444, 0.568, 0.715, 0.844, 1]
# Y = [0, 0.223, 0.517, 0.727, 0.820, 0.900, 0.957, 1]
# T = [i+273.15 for i in [117, 110, 100, 90, 85, 80, 76, 72]]
from Equilibrio.dados_manuais import equilibrio_acetona_isopropanol
X,Y = equilibrio_acetona_isopropanol()



#######################################################################################################################


 
try:
    from logica import aplicar_metodo_mccabe_thiele
except ModuleNotFoundError as e:
    if any(('numpy' in e.msg, 'scipy' in e.msg, 'matplotlib' in e.msg)):
        print("Para rodar essa aplicação, é necessário ter instaladas as bibliotecas 'numpy', 'scipy' e 'matplotlib'.\
              \n\nIsso pode ser feito através do comando: 'pip install nome_do_modulo'. \n")
    else:
        print("Essa aplicação deve ser executada diretamente de sua pasta raiz. \n")
    input()
    
    
def main():
    ## Verificando a existência de dados de equilíbrio manuais
    if ("X" not in globals()) and ("Y" not in globals()):
        dados_equilibrio = None #Calculadora interna
    elif ("X" not in globals()) or ("Y" not in globals()):
        print("Para usar dados de equilíbrio inseridos manualmente, são necessários dados de X e Y. \n")
        input()
        exit()
    elif len(X) != len(Y): # type: ignore
        print("Foram inseridos X e Y de tamanhos diferentes. \n")
        input()
        exit()
    elif "T" in globals():
        if len(T) != len(X): # type: ignore
            print("Foram inseridos T, X e Y de tamanhos diferentes. \n")
            input()
            exit()
        else:
            dados_equilibrio = [X,Y,T]    # type: ignore
    else:
        dados_equilibrio = [X,Y,[]] # type: ignore
    
    ## Verificando inputs
    global Eml, Emv, S, zS, F2
    if Eml is None: # type: ignore
        Eml = 1.0
    if Emv is None: # type: ignore
        Emv = 1.0
    if S is None:
        S = 0
    if zS is None:
        zS = 0
    if F2 is None:
        F2 = 0

    ## Organizando inputs
    estrutura_coluna = {
        # "ALIMENTACAO_TOPO": ALIMENTACAO_TOPO,
        "ALIMENTACAO_ADICIONAL": ALIMENTACAO_ADICIONAL,
        "SAIDA_ADICIONAL": SAIDA_ADICIONAL,
        "VAPOR_DIRETO": ENTRADA_VAPOR_FUNDO        
    }
    dados_extra = [
        (F2, zF2, q2), (S, zS, s)
    ]
    
    opcoes_plot = {
        "PLOTAR": PLOTAR,
        "INTERATIVO": INTERATIVO,
        "SALVAR": SALVAR
        }
    
    aplicar_metodo_mccabe_thiele(especies, F, zF, xD, xB, R, q, Eml, Emv, pressao,  # type: ignore
                                 dados_equilibrio, estrutura_coluna, dados_extra, opcoes_plot,) # type: ignore

if __name__ == "__main__":
    main()