# Implementação do Método Gráfico de McCabe-Thiele

**Autor:** Thiago Pacheco de Souza  
**Data:** 10/10/2025  
**Versão:** 1.1 

---

## Descrição

Este programa aplica o **método gráfico de McCabe-Thiele** para a resolução de um sistema de **destilação binária**, gerando o gráfico e indicando os estágios necessários.

O projeto é dividido em dois módulos principais:

1. **Cálculo do equilíbrio termodinâmico**  
2. **Implementação do método de McCabe-Thiele**
    
A **curva de equilíbrio** é calculada modelando a fase líquida pelo **coeficiente de atividade** (γ) e pela **pressão de saturação** de cada componente.  
Utiliza-se o modelo **NRTL** para γ e a **equação de Antoine** para Psat. 

As correções de Poynting e os coeficientes de fugacidade não foram implementados. Assim, a curva de equilíbrio termodinâmico gerada é precisa apenas para sistemas em baixas pressões.

### Espécies químicas atualmente suportadas:
- Água  
- Metanol  
- Etanol  
- Benzeno  
- Tolueno  
- p-Xileno  
- Acetona  
- Clorofórmio  

O módulo de aplicação do método é independente do módulo de equilíbrio, mas requer uma função de equilíbrio para esboçar os degraus. Para fins de performance, isso é feito interpolando
entre os pontos gerados pelo cálculo do equilíbrio. (Por padrão, são gerados 100 pontos.)
Futuramente, pretende-se implementar uma funcionalidade para inserção manual dos dados de equilíbrio, bem como uma opção de alterar a quantidade de pontos gerados pela calculadora implementada.

Além do módulo principal, há três scripts auxiliares para testar individualmente cada funcionalidade da geração de dados de equilíbrio, localizados na pasta 'Testes'.

---

## Como usar:

1. Execute o arquivo **main.py** diretamente para rodar a aplicação. (A importação da aplicação como um pacote externo ainda não é suportada.)
2. Os parâmetros de entrada podem ser ajustados nas variáveis globais dentro desse arquivo.
3. O modo interativo permite alterar dinamicamente os parâmetros do problema.  
   > Observação: esse modo pode ser um pouco lento.

---

# Dependências externas:

- `numpy`  
- `matplotlib`  
- `scipy`


## Limitações conhecidas:
- No modo interativo, é possível que atualizações muito rápidas crashem o programa.
- Por conta da interpolação dos dados equilíbrio, não há precisão total no desenho da escada de McCabe-Thiele, similarmente ao que ocorre na aplicação real deste método gráfico.
- O método não é aplicável após o ponto de azeótropo.


*Implementação didática do método de McCabe-Thiele para estudos de destilação binária.*
