import numpy as np

class Antoine:
    def __init__(self, coeficientes:list, tmin: float, tmax: float, limite_superior: bool) -> None:
        """Psat em bar, coeficientes ajustados em log10
        """
        self.coeficientes = coeficientes
        self.tmin = tmin
        self.tmax = tmax
        self.limite_superior = limite_superior
        self.called = False
        self.assert_msg = "Esse método não deve ser usado independentemente. " + \
        "Para calcular a pressão de saturação, chame a instância da classe, ou use o método 'calcular()'. \n"
        
    def _obter_coeficientes(self, T):
        assert self.called, self.assert_msg
        # if T < self.tmin or T > self.tmax:
        #     raise ValueError(f"Temperatura ({T}K) fora do intervalo possível para 1 atm.")
        if self.limite_superior:
            for limite, coefs in self.coeficientes:
                if T <= limite:
                    break
        else:
            for limite, coefs in self.coeficientes:
                if T >= limite:
                    break
                
        return coefs # type: ignore
            
    def _calcular(self, T):
        self.called = True        
        if isinstance(T, (list, tuple, np.ndarray)):
            A = np.zeros_like(T)
            B = np.zeros_like(T)
            C = np.zeros_like(T)
            for i, t in enumerate(T):
                A[i], B[i], C[i] = self._obter_coeficientes(t)
        else:
            A,B,C = self._obter_coeficientes(T)
        self.called = False
        return A - B/(C+T)

    def calcular(self, T):
        return 10**self._calcular(T) * 100000

    def __call__(self, T):
        return self.calcular(T)