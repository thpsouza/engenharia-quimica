import numpy as np
import os

class McCabeThieleMethod:
    def __init__(self, z_F, x_D, x_B, R, q, eq, eq_inverso) -> None:
        self.z_F = z_F
        self.x_D = x_D
        self.x_B = x_B
        self.R = R
        self.q = q
        self.eq = eq
        self.eq_inverso = eq_inverso
        self.plots = []
        self.annotations = []
        self._validar_inputs()
        print("Calculando...\n")
        self.update()
    
    
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
        
        
    def _verificar_pinch(self, tol=1e-3):
        self.pinch = False
        self.nao_fisico = False
        
        ## Intersecção
        if self.reta_operacao_retificacao(self.x_intercept) > self.eq(self.x_intercept):
            self.nao_fisico = True
            return #Returns para não precisa fazer as demais verificações
        elif np.isclose(self.reta_operacao_retificacao(self.x_intercept), self.eq(self.x_intercept)): 
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
            self.Vb = (self.z_F - self.x_B)/(self.x_D - self.z_F) * (self.R+1)
        
        else:
            # Alimentação
            self.a2 = self.q/(self.q-1)
            self.b2 = -self.z_F/(self.q-1)
            
            self.x_intercept = (self.b2 - self.b1) / (self.a1 + (-self.a2))
            self.Vb = -1/(1-(self.reta_operacao_alimentacao(self.x_intercept) - self.x_B)/(self.x_intercept - self.x_B))
        
        # Esgotamento
        self.a3 = (self.Vb+1)/self.Vb
        self.b3 = -self.x_B/self.Vb
    
        self._verificar_pinch()
        if self.pinch:
            self.title = rf"Zona de pinch para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
        elif self.nao_fisico:
            self.title = f"Zona fora do equilíbrio para R = {self.R:.2f}, q = {self.q:.2f}, $z_F$ = {self.z_F:.2f}"
    

    def reta_operacao_retificacao(self, x):
        return self.a1 * x  +  self.b1
    
    
    def reta_operacao_alimentacao(self, x):
        assert self.q!=1, "Esse método não funciona para para q = 1.\n"
        return self.a2 * x  +  self.b2
    
    
    def reta_operacao_esgotamento(self, x):
        return self.a3 * x  +  self.b3 
    
    
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
            
            
    def montar_escada(self, axis):
        if (self.pinch or self.nao_fisico):
            return
        
        ## Retificação
        xi_1 = self.x_D
        yi = self.reta_operacao_retificacao(xi_1)
        xi = self.eq_inverso(yi).item()
        contador = 1
        self.estagios = [[str(contador), xi, yi]]
        
        while xi > self.x_intercept:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_retificacao(xi)], color="tab:blue"))
            xi_1 = xi
            yi = self.reta_operacao_retificacao(xi_1)
            xi = self.eq_inverso(yi).item()
            contador+=1
            self.estagios.append([str(contador), xi, yi])
        self.n_alimentacao = contador
        
        ## Esgotamento
        while xi > self.x_B:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_esgotamento(xi)], color="tab:blue"))
            xi_1 = xi
            yi = self.reta_operacao_esgotamento(xi_1)
            xi = self.eq_inverso(yi).item()
            contador+=1
            self.estagios.append([str(contador), xi, yi])
            
        self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi, xi], [yi, xi], color="tab:blue"))
        self.title = f'Número total de estágios: {self.estagios[-1][0]}, Estágio ótimo para alimentação: {self.n_alimentacao}'
        
        
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
        
        # ##Caixa de texto bonita:
        # ax.text(0.6, 0.2, f'Número total de estágios: {self.estagios[-1][0]}\nEstágio ótimo para alimentação: {self.n_alimentacao}',
        #         fontsize=10, verticalalignment='top', 
        #         bbox=dict(boxstyle='round', facecolor='grey', alpha=0.5))
        

    def imprimir_detalhes(self):
        if not (self.pinch or self.nao_fisico):
            os.system('cls')
                                 
            ## Imprimir dados:
            print("Dados:")
            print(f"z_F = {self.z_F:.4f}")         
            print(f"R = {self.R:.4f}")         
            print(f"q = {self.q:.4f}")         
               
            ## Imprimir retas de operação
            # Retificação:
            print("\n- Reta de operação da região de retificação:")
            print(f" y = {self.a1:.4f} x  +  {self.b1:.4f}")
            print(f" y(x_D) = {self.x_D:.4f}")
            print(f" y(0) = {self.reta_operacao_retificacao(0):.4f}")
            
            # Alimentação:
            if self.q == 1:
                print(f"\n- Reta de operação da alimentação vertical em x = {self.z_F:.4f}.")
            else:                
                print("\n- Reta de operação da alimentação:")
                print(f" y = {self.a2:.4f} x  +  {self.b2:.4f}")
                print(f" y(z_F) = {self.x_D:.4f}")
                if self.q < 1:
                    print(f" y(0) = {self.reta_operacao_alimentacao(0):.4f}")
                else:
                    print(f" y(1) = {self.reta_operacao_alimentacao(1):.4f}")
            
            # Esgotamento:
            print("\n- Reta de operação da região de esgotamento:")
            print(f" y = {self.a3:.4f} x  +  {self.b3:.4f}")
            print(f" y(x_B) = {self.x_B:.4f}")
            print(f" y(1) = {self.reta_operacao_esgotamento(1):.4f}")
            
            
            ## Imprimir estágios
            string = "\nEstágio - (x, y)"
            for estagio, x, y in self.estagios:
                string += f"\n{estagio:<2} - ({x:.4f}, {y:.4f})"
            print(string)