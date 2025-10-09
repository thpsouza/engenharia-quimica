import numpy as np

class ModeloNRTL:
    def __init__(self, parametros_interacao:np.ndarray=None, Tau:np.ndarray=None, G:np.ndarray=None) -> None: # type: ignore
        if (parametros_interacao is None) and (Tau is None and G is None):
            raise ValueError("Devem ser passados os parâmetros de interação binária, ou então G e Tau diretamente. \n")
        self.parametros = parametros_interacao
        self.Tau = Tau
        self.G = G
        self.called = False
        self.assert_msg = "Esse método não deve ser usado independentemente. " + \
        "Para calcular os coeficientes de atividade, chame a instância da classe, ou use o método 'calcular()'. \n"
        
    def _calcular_parametros_ij(self, i, j, T):
        assert self.called, self.assert_msg
        tau = self.parametros[0,i,j] + self.parametros[1,i,j] / T
        G = np.exp(-self.parametros[2,i,j] * tau)
        return tau, G
    
    def _obter_parametros_ij(self, i, j, T):
        assert self.called, self.assert_msg
        return self.Tau[i,j], self.G[i,j]
        
    def _nrtl(self, T):
        assert self.called, self.assert_msg
        ## Se já forem passados Tau e G ao invés de a,b,c, muda o método de obtenção dos parâmetros
        if ((self.Tau is not None) and (self.G is not None)):
            metodo = self._obter_parametros_ij
        else:
            metodo = self._calcular_parametros_ij
        ## Cálculo dos coeficientes de atividade para cada espécies:
        self.coeficientes_atividade = np.zeros_like(self.composicoes)
        for i in range(self.num_especies):
            # Parte 1
            num = 0
            den = 0
            for k in range(self.num_especies):
                tau, G = metodo(k, i, T)
                num += tau * G * self.composicoes[k]
                den += G * self.composicoes[k]
            parte1 = num/den
            # Parte 2
            parte2 = 0
            for j in range(self.num_especies):
                tau_ij, G_ij = metodo(i, j, T)
                num = 0
                den = 0
                for k in range(self.num_especies):
                    tau, G = metodo(k, j, T)
                    num += tau * G * self.composicoes[k]
                    den += G * self.composicoes[k]
                parte2 += self.composicoes[j] * G_ij / den * (tau_ij - num/den)
            # Juntando
            self.coeficientes_atividade[i] = np.exp(parte1+parte2)

    def calcular_parametros(self, T):
        assert (self.parametros is not None), "Esse método só pode ser usado se foram passados os parâmetros aij, bij e cij.\n"
        tau = self.parametros[0] + self.parametros[1] / T
        G = np.exp(-self.parametros[2] * tau)
        return tau, G

    def calcular(self, composicoes, temperatura):
        if not isinstance(composicoes, np.ndarray):
            self.composicoes = np.asarray(composicoes)
        else:
            self.composicoes = composicoes
        self.num_especies = len(composicoes)
        self.called = True
        self._nrtl(temperatura)
        self.called = False
        return self.coeficientes_atividade

    def __call__(self, composicoes, temperatura):
        return self.calcular(composicoes, temperatura)