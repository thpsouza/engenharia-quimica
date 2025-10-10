#!/usr/bin/env python
"""
Título: Implementação do método gráfico de McCabe-Thiele
Autor: Thiago Pacheco de Souza
Data: 2025-10-10
Versão: 1.2
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
    equilíbrio para esboçar os degraus. Futuramente, pretende-se implementar uma funcionalidade de 
    inserção manual dos dados de equilíbrio.

    Além dos módulos principais, há 3 scripts para testar individual cada funcionalidade da geração
    de dados de equilíbrio.

Como usar:
    - Execute este script diretamente para rodar a aplicação.
    - Os parâmetros de entrada podem ser ajustados nas variáveis globais abaixo.
    - O modo interativo permite alterar os parâmetros de entrada do problema dinâmicamente. 
    (Pode ser um pouco lento.)

Dependências externas:
    - numpy
    - matplotlib
    - scipy
"""

pressao = 101325
especies = "etanol", "agua"
zF = 0.5
xD = 0.8
xB = 0.05
R = 7/3 # Para R->inf, use um valor alto (R=10000, por exemplo). Nesse caso, o ideal é desativar o modo interativo
q = 1
INTERATIVO = True #Pode deixar um pouco lento...
SALVAR = False


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
    aplicar_metodo_mccabe_thiele(especies, zF, xD, xB, R, q, pressao, INTERATIVO, SALVAR)


if __name__ == "__main__":
    main()