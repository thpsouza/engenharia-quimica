from numpy import exp, log, polyfit, poly1d
import scipy.integrate as integrate

class Distribuicao:
    def __init__(self, y=None, x=None, linearizacao_y=lambda x: x, linearizacao_x=lambda x: x, linearizado=False, escala=1e-6, 
                 m=None, k=None, a=None):
        if (y is not None and x is not None):
            self.y = y
            self.x = x
            self.linearizacao_y = linearizacao_y
            self.linearizacao_x = linearizacao_x
            ## Variaveis a ser calculadas
            self.m, self.k, self.diametro_sauter = None, None, None
            ## Estados do modelo
            self.linearizado = linearizado
            self.fittado = False

        elif (m and k):
            self.m = m 
            self.k = k
            if a:
                self.a = a      
            self.fittado = True   
        else:
            raise ValueError("Devem ser passados os dados da distribuição, ou os coeficientes diretamente. \n")
            
        self.escala = escala
        self.escala_str = {1e-6:"µm", 1e-3:"mm", 1e0:"m"}[escala]

        ## Propriedades de cada modelo
        self.modelo = "Genérico"
        self.funcao = lambda i: i
        self.funcao_inversa = lambda j: j

        self.R2 = None
        self._coefs = None



    def _linearizar(self):
        if not self.linearizado:
            self.x = self.linearizacao_x(self.x)
            self.y = self.linearizacao_y(self.y)
            self.linearizado = True
        else:
            raise Exception('Modelo já foi linearizado.')

    def _calcular_R2(self):
        if self.fittado:
            SSR = ((self.y - self._polinomio(self.x)) ** 2).sum()
            SST = ((self.y - self.y.mean()) ** 2).sum()
            self.R2 = 1 - SSR / SST
        else:
            raise Exception('Modelo ainda não foi fitado.')

    def _calcular_coefs(self):
        if self.fittado:
            self.m = self._coefs[0]
            self.k = exp(-self._coefs[1] / self._coefs[0])
        else:
            raise Exception('Modelo ainda não foi fitado.')

    def _calcular_diametro_sauter(self):
        if self.fittado:
            #y = np.linspace(0, 1, 1000)[1:-1]
            #integral = np.trapz(1/self.funcao_inversa(y), y, dx=0.0001)
            integral = integrate.quad(lambda x: 1/self.funcao_inversa(x), 0, 1)[0]
            self.diametro_sauter = 1/integral
        else:
            raise Exception('Modelo ainda não foi fitado.')

    def fit(self):
        if not self.fittado:
            if not self.linearizado:
                self._linearizar()
            self._coefs = polyfit(self.x, self.y, 1)
            self._polinomio = poly1d(self._coefs)
            self.fittado = True
            self._calcular_R2()
            self._calcular_coefs()
            if self.modelo != "Genérico":
                self._calcular_diametro_sauter()
            return self
        else:
            raise Exception('Modelo já foi fitado.')

    def definir_coefs(self, k:float=None, m:float=None, a:float=None) -> None: 
        self.fittado = True
        if k:
            self.k = k
        if m:
            self.m = m
        if a:
            self.a = a

    def inversa(self, x):
        if self.fittado:
            return self.funcao_inversa(x)
        else:
            raise Exception('Modelo ainda não foi fitado.')

    def __str__(self):
        if self.fittado:
            try: 
                self.diametro_sauter
            except AttributeError: 
                self._calcular_diametro_sauter()
            return (f"Ajuste com modelo {self.modelo} (Escala: {self.escala_str}):\n" +
                    f"m: {self.m}\n" +
                    f"k: {self.k}\n" +
                    f"R²: {self.R2}\n" +
                    f"<d>: {self.diametro_sauter}\n"
                    )
        else:
            return "Ainda não foi fitado.\n"

    def __call__(self, x):
        if self.fittado:
            return self.funcao(x)
        else:
            raise Exception('Modelo ainda não foi fitado.')


class GGS(Distribuicao):
    def __init__(self, y=None, d=None, k=None, m=None, escala=1e-6):
        super().__init__(y=y, x=d, linearizacao_x=log, linearizacao_y=log, 
                         k=k, m=m, escala=escala)
        self.modelo = "GGS"
        self.funcao = lambda x: (x/(self.k*self.escala)) ** self.m
        self.funcao_inversa = lambda x: self.k*self.escala * x ** (1 / self.m)
        if self.fittado:
            self._calcular_diametro_sauter()


class Sigmoide(Distribuicao):
    def __init__(self, y=None, d=None, k=None, m=None, escala=1e-6):
        super().__init__(y, d, linearizacao_x=log, linearizacao_y=lambda x: log(1 / x - 1),
                         k=k, m=m, escala=escala)
        self.modelo = "Sigmoide"
        self.funcao = lambda x: 1 / (1 + ((self.k*self.escala)/x)**self.m)
        self.funcao_inversa = lambda x: self.k*self.escala / (1/x - 1)**(1/self.m)
        if self.fittado:
            self._calcular_diametro_sauter()

    def _calcular_coefs(self):
        self.m = -self._coefs[0]
        self.k = exp(self._coefs[1] / -self._coefs[0])


class RRB(Distribuicao):
    def __init__(self, y=None, d=None, k=None, m=None, escala=1e-6):
        super().__init__(y, d, linearizacao_x=log, linearizacao_y=lambda x: log(log(1 / (1 - x))), 
                         k=k, m=m, escala=escala)
        self.modelo = "RRB"
        self.funcao = lambda x: 1 - exp( -( (x/(self.k*self.escala))**self.m ) )
        self.funcao_inversa = lambda x: self.k*self.escala * log(1/(1-x))**(1/self.m)
        if self.fittado:
            self._calcular_diametro_sauter()


class Weibull(Distribuicao):
    def __init__(self, y=None, d=None, k=None, m=None, a:float=None, escala=1e-6):
        super().__init__(y, d, linearizacao_x=lambda x: log(x-a), linearizacao_y=lambda x: log(log(1 / (1 - x))), 
                         k=k, m=m, a=a, escala=escala)
        self.modelo = f"Weibull"
        self.funcao = lambda x: 1 - exp( -( ((x-a*self.escala)/(self.k*self.escala))**self.m ) )
        self.funcao_inversa = lambda x: self.k*self.escala * log(1/(1-x))**(1/self.m) + self.a*self.escala
        if self.fittado:
            self._calcular_diametro_sauter()
        
    def __str__(self):
        return super().__str__() + f"a: {self.a}\n"

