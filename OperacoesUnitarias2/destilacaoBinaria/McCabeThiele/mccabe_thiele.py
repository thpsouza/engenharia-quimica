import numpy as np
import os

class McCabeThieleMethod:
    def __init__(self, z_F, x_D, x_B, R, q, Emv, Eml, eq, eq_inverso, T) -> None:
        self.z_F = z_F
        self.x_D = x_D
        self.x_B = x_B
        self.R = R
        self.q = q
        self.ef_vap = Emv
        self.ef_liq = Eml
        self.eq = eq
        self.eq_inverso = eq_inverso
        self.T = T
        self.plots = []
        self.annotations = []
        self._validar_inputs()
        print("Calculando...\n")
        self.update()
        self._calcular_Rmin()
    
    
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
    
    
    def plotar_retas_operacao(self, axis):
        n = 50
        ## Alimentação:
        if self.q == 1:
            self.plots.append(axis.plot([self.z_F, self.z_F], [self.z_F, self.reta_operacao_retificacao(self.z_F)], 
                                        color="black", linestyle=':', label="Reta de alimentação"))
        else:
            X = np.linspace(self.z_F, self.x_intercept, n)
            self.plots.append(axis.plot(X, self.reta_operacao_alimentacao(X), 
                                        color="black", linestyle=':', label="Reta de alimentação"))
        ## Retificação:
        X = np.linspace(self.x_D, self.x_intercept, n)
        self.plots.append(axis.plot(X, self.reta_operacao_retificacao(X), 
                                    color="black", linestyle='--', label="Reta de retificação"))
        ## Esgotamento:
        X = np.linspace(self.x_B, self.x_intercept, n)
        self.plots.append(axis.plot(X, self.reta_operacao_esgotamento(X), 
                                    color="black", linestyle='--', label="Reta de esgotamento"))
    
    
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
                    
    
    def _calcular_Rmin(self, tol=1e-4):
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
        
        
    def _verificar_pinch(self, tol=1e-3):
        self.pinch = False
        self.nao_fisico = False
        
        ## Intersecção
        if self.y_intercept > self.eq_x_intercept:
            self.nao_fisico = True
            return #Returns para não precisa fazer as demais verificações
        elif np.isclose(self.y_intercept, self.eq_x_intercept, atol=tol): 
            self.pinch = True 
            return 
        
        ## Retificação
        x = np.linspace(self.x_intercept, self.x_D, 1000)
        d = self.eq(x) - self.reta_operacao_retificacao(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < tol:
            self.pinch = True
            return
        
        ## Esgotamento
        x = np.linspace(self.x_B, self.x_intercept, 1000)
        d = self.eq(x) - self.reta_operacao_esgotamento(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < tol:
            self.pinch = True
    
    
    def update(self):
        # Retificação
        self.a1 = self.R/(self.R+1)
        self.b1 = self.x_D/(self.R+1)
        
        if self.q == 1:            
            self.x_intercept = self.z_F
            self.y_intercept = self.reta_operacao_retificacao(self.x_intercept)
            self.Vb = (self.z_F - self.x_B)/(self.x_D - self.z_F) * (self.R+1)
        
        else:
            # Alimentação
            self.a2 = self.q/(self.q-1)
            self.b2 = -self.z_F/(self.q-1)
            
            self.x_intercept = (self.b2 - self.b1) / (self.a1 + (-self.a2))
            self.y_intercept = self.reta_operacao_alimentacao(self.x_intercept)
            self.Vb = -1/(1-(self.y_intercept - self.x_B)/(self.x_intercept - self.x_B))
        
        # Esgotamento
        self.a3 = (self.Vb+1)/self.Vb
        self.b3 = -self.x_B/self.Vb
    
        self.eq_x_intercept = self.eq(self.x_intercept)
        self._verificar_pinch()
        if self.pinch:
            self.title = rf"Zona de pinch para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
        elif self.nao_fisico:
            self.title = f"Zona fora do equilíbrio para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
            
        ## Não recalcula Rmin a cada atualização nos sliders pois deixa muito lento.
        self.R_min = None
           
         
    def _escada_do_fundo(self, axis):        
        ## Refervedor total:
        contador = 1
        yi_1 = self.x_B
        xi = self.reta_operacao_esgotamento_inversa(yi_1)
        yi = self.eq(xi)
        self.estagios = [[str(contador), xi, yi]]
        if self.T:
            self.temperaturas = [self.T(xi)]

        ## Esgotamento
        while yi < self.y_intercept:
            self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, self.reta_operacao_esgotamento_inversa(yi)], [yi, yi], color="tab:blue"))
            contador+=1
            yi_1 = yi
            xi = self.reta_operacao_esgotamento_inversa(yi_1)
            yi_id = self.eq(xi)
            yi = yi_1 + self.ef_vap*(yi_id - yi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.n_alimentacao = contador
        
        ## Retificacao
        while yi < self.x_D:
            self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, self.reta_operacao_retificacao_inversa(yi)], [yi, yi], color="tab:blue"))
            contador+=1
            yi_1 = yi
            xi = self.reta_operacao_retificacao_inversa(yi_1)
            yi_id = self.eq(xi)
            yi = yi_1 + self.ef_vap*(yi_id - yi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi, yi], [yi, yi], color="tab:blue"))
        
        ## Contar a partir do topo
        n = len(self.estagios)
        self.n_alimentacao = n - self.n_alimentacao + 1
        for estagio in self.estagios:
            estagio[0] = str(n - int(estagio[0]) + 1)
        self.estagios.reverse()
          
          
    def _escada_do_topo(self, axis):
        ## Retificação
        contador = 1
        xi_1 = self.x_D
        yi = self.reta_operacao_retificacao(xi_1)
        xi_id = self.eq_inverso(yi).item()
        xi = xi_1 + self.ef_liq*(xi_id - xi_1)
        self.estagios = [[str(contador), xi, yi]]
        if self.T:
            self.temperaturas = [self.T(xi)]
        
        while xi > self.x_intercept:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_retificacao(xi)], color="tab:blue"))
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_retificacao(xi_1)
            xi_id = self.eq_inverso(yi).item()
            xi = xi_1 + self.ef_liq*(xi_id - xi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.n_alimentacao = contador
        
        ## Esgotamento
        while xi > self.x_B:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_esgotamento(xi)], color="tab:blue"))
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_esgotamento(xi_1)
            xi_id = self.eq_inverso(yi).item()
            xi = xi_1 + self.ef_liq*(xi_id - xi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
                
        # Refervedor total:
        self.plots.append(axis.plot([xi_1, xi_id], [yi, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi_id, xi_id], [yi, xi_id], color="tab:blue"))
        self.estagios[-1] = [str(contador), xi_id, yi]
                    

    def montar_escada(self, axis): 
        s = rf"($x_D$ = {self.x_D}, $x_B$ = {self.x_B}, $z_F$ = {self.z_F}, $R$ = {self.R}, $q$ = {self.q}"
        if (self.pinch or self.nao_fisico):
            return
        if (self.ef_vap is not None) and (self.ef_vap != 1.0):
            self._escada_do_fundo(axis)
            s += r", $E_{MV}$" + f" = {self.ef_vap})"
        else:
            if self.ef_liq is None:
                self.ef_liq = 1.0
                s += ")"
            else:
                s += r", $E_{ML}$" + f" = {self.ef_liq})"
            self._escada_do_topo(axis)
        self.title = f"Número total de estágios: {self.estagios[-1][0]}, Estágio ótimo para alimentação: {self.n_alimentacao}\n" + s 
        
        
    def plotar_detalhes(self, ax, n_max=20):
        if not (self.pinch or self.nao_fisico):
            ## Evita numerar estágios demais
            if len(self.estagios) >= n_max:
                for s, x, y in self.estagios[:5]:
                    self.annotations.append(ax.annotate(s, xy=(x, y), xytext=(0,5), textcoords='offset points', ha='center', fontweight='bold'))
                for s, x, y in self.estagios[-5:]:
                    self.annotations.append(ax.annotate(s, xy=(x, y), xytext=(0,5), textcoords='offset points', ha='center', fontweight='bold'))
            else:
                for s, x, y in self.estagios:
                    self.annotations.append(ax.annotate(s, xy=(x, y), xytext=(0,5), textcoords='offset points', ha='center', fontweight='bold'))
                    
        ax.set_title(self.title)
        

    def _imprimir_reta_retificacao(self):
        ## A reta de operação nunca cruzará x=0 abaixo do y=0.
        print("\n- Reta de operação da região de retificação:")
        print(f" y = {self.a1:.4f} x  +  {self.b1:.4f},  α = {np.rad2deg(np.arctan(self.a1)):.2f}°")
        print(f" y(x_D) = {self.x_D:.4f}")
        print(f" y(0) = {self.reta_operacao_retificacao(0):.4f}")


    def _imprimir_reta_alimentacao(self):
        if self.q == 1:
            print(f"\n- Reta de operação da alimentação vertical em x = {self.z_F:.4f}.")
        else:                
            print("\n- Reta de operação da alimentação:")
            print(f" y = {self.a2:.4f} x  +  {self.b2:.4f},  α = {np.rad2deg(np.arctan(self.a2)):.2f}°")
            print(f" y(z_F) = {self.z_F:.4f}")
            # Obtenção do segundo ponto da reta de operação:
            if self.q < 1:
                for i in range(0, 11)[::-1]:
                    x = i/10
                    if x >= self.z_F: 
                        continue
                    y = self.reta_operacao_alimentacao(x) 
                    if y <= 1:
                        print(f" y({x:.4f}) = {y:.4f}")
                        break
                else:
                    print(f" y({self.z_F-0.04:.4f}) = {self.reta_operacao_alimentacao(self.z_F-0.04):.4f}")
            else:
                for i in range(0, 11):
                    x = i/10
                    if x <= self.z_F: 
                        continue
                    y = self.reta_operacao_alimentacao(x) 
                    if y <= 1:
                        print(f" y({x:.4f}) = {y:.4f}")
                        break
                else:
                    print(f" y({self.z_F+0.04:.4f}) = {self.reta_operacao_alimentacao(self.z_F+0.04):.4f}")
            

    def _imprimir_reta_esgotamento(self):
        print("\n- Reta de operação da região de esgotamento:")
        print(f" y = {self.a3:.4f} x  +  {self.b3:.4f},  α = {np.rad2deg(np.arctan(self.a3)):.2f}°")
        print(f" y(x_B) = {self.x_B:.4f}")
        for i in range(0, 11):
            x = i/10
            if x <= self.x_intercept: 
                continue
            y = self.reta_operacao_esgotamento(x) 
            if y <= 1:
                print(f" y({x:.4f}) = {y:.4f}")
                break


    def imprimir_detalhes(self):
        os.system('cls')
        
        ## Imprimir dados:
        print("Dados:")
        print(f"x_D = {self.x_D:.4f}")         
        print(f"x_B = {self.x_B:.4f}")         
        print(f"z_F = {self.z_F:.4f}")         
        print(f"R = {self.R:.4f}")         
        print(f"q = {self.q:.4f}")  

        ## Imprimir retas de operação
        self._imprimir_reta_retificacao()
        self._imprimir_reta_alimentacao()
        self._imprimir_reta_esgotamento()
    
        ## Intersecção:
        print(f"\nIntersecção das retas: ({self.x_intercept:.4f}, {self.y_intercept:.4f})")
        
        ## Imprimir Rmin:
        if self.R_min:
            print(f"\nRmin = {self.R_min:.4f}, (x,y) = ({self.x_Rmin:.4f}, {self.y_Rmin:.4f})")
            
        if self.nao_fisico:
            print("\nSistema fora do equilíbrio líquido-vapor. \n") 
        elif self.pinch:
            print("\nRegião de pinch existente. Impossível destilar nas condições estabelecidas. \n")
        else:
            ## Imprimir estágios
            if self.T:
                string = "\nEstágios: i - (xi, yi) - T"
                for (estagio, x, y), T in zip(self.estagios, self.temperaturas):
                    string += f"\n{estagio:<2} - ({x:.4f}, {y:.4f}) - {T-273.15:.2f}°C"
            else: 
                string = "\nEstágios: i - (xi, yi)"
                for estagio, x, y in self.estagios:
                    string += f"\n{estagio:<2} - ({x:.4f}, {y:.4f})"
            print(string)
            print(f"Estágio ótimo para alimentação: {self.n_alimentacao}")
