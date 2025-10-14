import numpy as np
from scipy.optimize import root
from Equilibrio.CoeficienteAtividade.NRTL import ModeloNRTL
from Equilibrio.CoeficienteAtividade.parametros_interacao_binaria import ParametrosNRTL, ESPECIES_POSSIVEIS
from Equilibrio.PressaoSaturacao.substancias_antoine import *
# from Correcoes.poynting import PoyntingFactor

class EquilibrioTermodinamico:
    def __init__(self) -> None:
        self.called = False

    def coeficientes_atividade(self, especies, composicoes, temperatura):
        parametros = ParametrosNRTL().obter(especies)
        modelo = ModeloNRTL(parametros)
        coefs = modelo(composicoes, temperatura)
        return coefs

    def pressao_saturacao(self, especie, temperatura):
        match especie.upper():
            case "AGUA":
                modelo = AntoineAgua()
            case "ETANOL":
                modelo = AntoineEtanol()
            case "BENZENO":
                modelo = AntoineBenzeno()
            case "TOLUENO":
                modelo = AntoineTolueno()
            case "METANOL":
                modelo = AntoineMetanol()
            case "CLOROFORMIO":
                modelo = AntoineCloroformio()
            case "ACETONA":
                modelo = AntoineAcetona()
            case "P-XILENO":
                modelo = AntoinePXILENO()
            case _ :
                raise ValueError(f"Não é possível calcular a pressão de saturação da espécie '{especie}'. \n")
        return modelo(temperatura)

    def coeficiente_equilibrio(self, gamma, Psat, P, poynting=1, phi_sat=1, phi_v=1):
        return gamma * Psat * phi_sat * poynting / (P * phi_v)

    def _f(self, z, especies, X, pressao):
        assert self.called, "Esse método não deve ser utilizado de maneira independente.\n"
        T = z[0]
        Y = z[1:]
        equacoes = []
        gammas = self.coeficientes_atividade(especies, X, T)
        for i in range(len(X)):
            psat = self.pressao_saturacao(especies[i], T)
            K = self.coeficiente_equilibrio(gammas[i], psat, pressao)     
            equacoes.append(Y[i] - K*X[i])
        restricao = [np.sum(Y)-1]
        return equacoes+restricao
    
    def _calcular(self, especies, x, pressao, T0):
        T, *y = root(lambda z: self._f(z, especies, x, pressao), [T0, *x], tol=1e-6).x
        return T, *y

    def _calcular_multiplo(self, especies, X, pressao, T0):
        # Tratamento de T0
        if T0 is None:
            T0 = np.linspace(348,298,len(X)) #Chutes inicias quaisquer (25~75°C)
            T0_array = True
        else:
            T0_array = isinstance(T0, (list,tuple,np.ndarray))
        # Tratamento de X
        if not isinstance(X, np.ndarray):
            X = np.asarray(X).T
        # Cálculo para cada composição
        m = len(especies)   
        n = len(X)
        T = np.zeros(n)
        Y = np.zeros((m, n))
        for i in range(n):
            if T0_array:
                sol = self._calcular(especies, X[i], pressao, T0[i])
            else:
                sol = self._calcular(especies, X[i], pressao, T0)
            T[i] = sol[0]
            for j in range(m):
                Y[j, i] = sol[1:][j]
        return T, Y

    def calcular(self, especies, X, pressao, T0=None):
        self.called = True
        
        ## Defesa
        for especie in especies:
            if especie.upper() not in ESPECIES_POSSIVEIS:
                raise ValueError(f"Não é possível calcular o equilíbrio para a espécie '{especie}'. \n")
        
        ## Cálculo para múltiplas composições
        if isinstance(X[0], (list,tuple,np.ndarray)):
            T, Y = self._calcular_multiplo(especies, X, pressao, T0)
            
        ## Cálculo para uma única composição
        else:
            if T0 is None: 
                T0 = 323 #Chute inicial qualquer (50°C)
            T, *Y = self._calcular(especies, X, pressao, T0)
            
        self.called = False
        return *Y, T
    
    def __call__(self, especies, X, pressao, T0):
        return self.calcular(especies, X, pressao, T0)