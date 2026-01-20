import numpy as np
import os
from McCabeThiele.balancos import caudais_simples

class McCabeThieleMethod:
    def __init__(self, z_F, x_D, x_B, R, q, Emv, Eml, equilibrio, coluna, tolerancia_numerica=1e-3):
        self.z_F = z_F
        self.q = q
        self.x_D = x_D
        self.x_B = x_B
        self.R = R
        self.ef_vap = Emv
        self.ef_liq = Eml
        self.eq = equilibrio[0]
        self.eq_inverso = equilibrio[1]
        self.T = equilibrio[2]
        self.coluna = coluna
        self.tol = tolerancia_numerica
    
        self.n_alimentacao = 0
        self.estagios = []
        self.temperaturas = []
        self.plots = []
        self.annotations = []
        self._validar_inputs()

    
    def _verificar_azeotropo(self, N=10000):
        self.x_azeotropo = None
        for i in range(1,N):
            if self.eq(i/N) <= i/N:
                self.x_azeotropo = i/N
                break

    
    def _validar_inputs(self):
        if self.x_B >= self.x_D:
            print(f"Parâmetros de entrada inválidos: x_B ({self.x_B}) deve ser menor que x_D ({self.x_D})\n")
            input()
            exit()
            
        self._verificar_azeotropo()
        if self.x_azeotropo:
            # xD deve estar abaixo do azeótropo
            if (self.x_D >= self.x_azeotropo):
                print(f"Parâmetros de entrada inválidos: Azeótropo em x = {self.x_azeotropo:.4f}.",\
                f"\nAmbos x_B ({self.x_B}) e x_D ({self.x_D}) precisam estar na mesma região do equilíbrio para que a separação seja possível.\n")
                input()
                exit()
            
        
    def _verificar_pinch(self):
        self.pinch = False
        self.nao_fisico = False
        
        ## Intersecção
        if self.y_intercept > self.eq_x_intercept:
            self.nao_fisico = True
            return #Returns para não precisa fazer as demais verificações
        elif np.isclose(self.y_intercept, self.eq_x_intercept, atol=self.tol): 
            self.pinch = True 
            return 
        
        ## Retificação
        x = np.linspace(self.x_intercept, self.x_D, 1000)
        d = self.eq(x) - self.reta_operacao_retificacao(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < self.tol:
            self.pinch = True
            return
        
        ## Esgotamento
        x = np.linspace(self.x_B, self.x_intercept, 1000)
        d = self.eq(x) - self.reta_operacao_esgotamento(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < self.tol:
            self.pinch = True
    

    def reta_operacao_retificacao(self, x):
        return self.a1 * x  +  self.b1
    
    
    def reta_operacao_retificacao_inversa(self, y):
        return (y - self.b1)/self.a1
    
    
    def reta_operacao_alimentacao(self, x):
        assert self.q!=1, "Esse método não funciona para para q = 1.\n"
        return self.a2 * x  +  self.b2
    
    
    def reta_operacao_esgotamento(self, x):
        return self.a3 * x  +  self.b3 
    
    
    def reta_operacao_esgotamento_inversa(self, y):
        return (y - self.b3)/self.a3
    
    
    def calcular_caudais(self):
        self.D, self.B = caudais_simples(1, self.z_F, self.x_D, self.x_B)
    
    
    def atualizar_sliders(self, zF, R, q):
        self.z_F = zF
        self.R = R
        self.q = q
    
    
    def limpar_listas(self):
        for plot in self.plots:
            plot[0].remove()
        for annotation in self.annotations:
            annotation.remove()
        self.plots.clear()
        self.annotations.clear()
        self.estagios.clear()
        self.temperaturas.clear()
    
    
    def update(self):
        # Retificação
        self.a1 = self.R/(self.R+1)
        self.b1 = self.x_D/(self.R+1)
        
        if self.q == 1:            
            self.x_intercept = self.z_F
            self.y_intercept = self.reta_operacao_retificacao(self.x_intercept)
        
        else:
            # Alimentação
            self.a2 = self.q/(self.q-1)
            self.b2 = -self.z_F/(self.q-1)
            self.x_intercept = (self.b2 - self.b1) / (self.a1 + (-self.a2))
            self.y_intercept = self.reta_operacao_alimentacao(self.x_intercept)
                
        # Esgotamento
        self.Vb = 1/((self.y_intercept - self.x_B)/(self.x_intercept - self.x_B) - 1)
        self.a3 = (self.Vb+1)/self.Vb
        self.b3 = -self.x_B/self.Vb

        self.eq_x_intercept = self.eq(self.x_intercept)
        self._verificar_pinch()
        if self.pinch:
            self.title = rf"Zona de pinch para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
        elif self.nao_fisico:
            self.title = f"Zona fora do equilíbrio para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
            
        ## Não recalcula Rmin e caudais a cada atualização nos sliders pois deixa muito lento.
        self.R_min = None
        
                
    def calcular_Rmin(self, tol=1e-4):
        R = np.linspace(0, 5, 10000)
        if self.q == 1:
            x_intercept = self.z_F
            for r in R:
                f = lambda x: r/(r+1) * x + self.x_D/(r+1)
                y_intercept = f(x_intercept)
                if np.isclose(f(x_intercept), self.eq(x_intercept), atol=tol):
                    self.R_min = r
                    self.x_Rmin = x_intercept
                    self.y_Rmin = y_intercept
        else:
            for r in R:
                a = r/(r+1)
                b = self.x_D/(r+1)
                f = lambda x: a * x + b
                x_intercept = (self.b2 - b) / (a + (-self.a2))
                y_intercept = f(x_intercept)
                if np.isclose(y_intercept, self.eq(x_intercept), atol=tol):
                    self.R_min = r
                    self.x_Rmin = x_intercept
                    self.y_Rmin = y_intercept
                    break
        

    def montar_escada(self): ## Apenas para imprimir no console
        if (self.pinch or self.nao_fisico):
            return
        
        ## Retificação
        contador = 1
        xi_1 = self.x_D
        yi = self.reta_operacao_retificacao(xi_1)
        xi = self.eq_inverso(yi).item()
        self.estagios = [[str(contador), xi, yi]]
        if self.T:
            self.temperaturas = [self.T(xi)]
            
        while xi > self.x_intercept:
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_retificacao(xi_1)
            xi = self.eq_inverso(yi).item()
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.n_alimentacao = contador
        
        ## Esgotamento
        while xi > self.x_B:
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_esgotamento(xi_1)
            xi = self.eq_inverso(yi).item()
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))


    def _informacoes_reta_retificacao(self):
        ## A reta de operação nunca cruzará x=0 abaixo do y=0.
        return [
            "\n- Reta de operação da região de retificação:",
            f" y = {self.a1:.4f} x  +  {self.b1:.4f},  α = {np.rad2deg(np.arctan(self.a1)):.2f}°",
            f" y(x_D) = {self.x_D:.4f}",
            f" y(0) = {self.reta_operacao_retificacao(0):.4f}"
            ]


    def _informacoes_reta_esgotamento(self):
        ret = [
            "\n- Reta de operação da região de esgotamento:",
            f" y = {self.a3:.4f} x  +  {self.b3:.4f},  α = {np.rad2deg(np.arctan(self.a3)):.2f}°",
            f" y(x_B) = {self.x_B:.4f}" #1o Ponto de referência da reta de esgotamento
        ]
        # Obtenção do 2o ponto de referência da reta de esgotamento
        for i in range(0, 11):
            x = i/10
            if x <= self.x_intercept:
                continue
            y = self.reta_operacao_esgotamento(x) 
            if y <= 1:
                ret.append(f" y({x:.4f}) = {y:.4f}")
                break
        return ret
    
    
    def _informacoes_reta_alimentacao(self, q, zF):
        if q == 1:
            ret = [f"\n- Reta de operação da alimentação vertical em x = {zF:.4f}."]
        else:       
            ret = [         
                "\n- Reta de operação da alimentação:",
                f" y = {self.a2:.4f} x  +  {self.b2:.4f},  α = {np.rad2deg(np.arctan(self.a2)):.2f}°",
                f" y(z_F) = {zF:.4f}" #1o Ponto de referência da reta da alimentação
                ]
            # Obtenção do segundo ponto de referência da reta de operação da alimentação:
            if q < 1:
                for i in range(0, 11)[::-1]:
                    x = i/10
                    if x >= zF: 
                        continue
                    y = self.reta_operacao_alimentacao(x) 
                    if y <= 1:
                        ret.append(f" y({x:.4f}) = {y:.4f}")
                        break
                else:
                    ret.append(f" y({zF-0.04:.4f}) = {self.reta_operacao_alimentacao(zF-0.04):.4f}")
            else:
                for i in range(0, 11):
                    x = i/10
                    if x <= zF: 
                        continue
                    y = self.reta_operacao_alimentacao(x) 
                    if y <= 1:
                        ret.append(f" y({x:.4f}) = {y:.4f}")
                        break
                else:
                    ret.append(f" y({zF+0.04:.4f}) = {self.reta_operacao_alimentacao(zF+0.04):.4f}")
        return ret
    
    
    def _informacoes_caudais(self):
        return ["\n - Caudais:", f" D/F = {self.D:.4f}", f" B/F = {self.B:.4f}"]


    def imprimir_detalhes(self, imprimir:bool=True, salvar:bool=False):
        ## Adicionar na lista as informações, uma a uma
        informacoes_para_impressao = []

        ## Dados de entrada:
        informacoes_para_impressao.append("Dados:")
        informacoes_para_impressao.append(f"x_D = {self.x_D:.4f}")         
        informacoes_para_impressao.append(f"x_B = {self.x_B:.4f}")         
        informacoes_para_impressao.append(f"R = {self.R:.4f}")         
        informacoes_para_impressao.append(f"z_F = {self.z_F:.4f}")         
        informacoes_para_impressao.append(f"q = {self.q:.4f}")  

        ## Caudais:
        informacoes_para_impressao.extend(self._informacoes_caudais())

        ## Retas de operação
        informacoes_para_impressao.extend(self._informacoes_reta_retificacao())
        informacoes_para_impressao.extend(self._informacoes_reta_esgotamento())
        informacoes_para_impressao.extend(self._informacoes_reta_alimentacao(self.q, self.z_F))
    
        ## Intersecção:
        informacoes_para_impressao.append(f"\nIntersecção das retas: ({self.x_intercept:.4f}, {self.y_intercept:.4f})")
            
        ## Rmin:
        if self.R_min:
            informacoes_para_impressao.append(f"\nRmin = {self.R_min:.4f}, (x,y) = ({self.x_Rmin:.4f}, {self.y_Rmin:.4f})") 
        
        ## Estágios
        if self.nao_fisico:
            informacoes_para_impressao.append("\nSistema fora do equilíbrio líquido-vapor. \n") 
        elif self.pinch:
            informacoes_para_impressao.append("\nRegião de pinch existente. Impossível destilar nas condições estabelecidas. \n")
        else:
            if self.T:
                string = "\nEstágios: i - (xi, yi) - T"
                for (estagio, x, y), T in zip(self.estagios, self.temperaturas):
                    string += f"\n{estagio:<2} - ({x:.4f}, {y:.4f}) - {T-273.15:.2f}°C"
            else: 
                string = "\nEstágios: i - (xi, yi)"
                for estagio, x, y in self.estagios:
                    string += f"\n{estagio:<2} - ({x:.4f}, {y:.4f})"
            informacoes_para_impressao.append(string)
            informacoes_para_impressao.append(f"Estágio ótimo para alimentação: {self.n_alimentacao}")
        
        ## Imprimir e salvar em um arquivo de texto
        texto = "\n".join(informacoes_para_impressao)
        if imprimir:
            print(texto)
        if salvar:
            with open("resultados.txt", "w+", encoding='utf-16') as f:
                f.write(texto)