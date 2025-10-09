Título: Implementação do método gráfico de McCabe-Thiele
Autor: Thiago Pacheco de Souza
Data: 2025-10-08
Versão: 1.0
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

Limitações conhecidas:
    No modo interativo, é possível que atualizações muito rápidas crashem o programa.
    Além disso, deve-se evitar situações de 'pinch', pois também irá causar o travamento da aplicação.