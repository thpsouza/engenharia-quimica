import numpy as np

class McCabeThieleMethod:
    def __init__(self, z_F, x_D, x_B, R, q) -> None:
        self.z_F = z_F
        self.x_D = x_D
        self.x_B = x_B
        self.R = R
        self.q = q
        self.update()
        self.plots = []
        self.annotations = []
    
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
            # axis.axvline(x=self.z_F, ymin=self.z_F, ymax=self.reta_operacao_retificacao(self.z_F),
            #              color="black", linestyle=':', label="Reta de alimentação")
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
            
    def montar_escada(self, axis, x):
        ## Retificação
        xi_1 = self.x_D
        yi = self.reta_operacao_retificacao(xi_1)
        xi = x(yi).item()
        contador = 1
        self.estagios = [[str(contador), xi, yi]]
        
        while xi > self.x_intercept:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_retificacao(xi)], color="tab:blue"))
            xi_1 = xi
            yi = self.reta_operacao_retificacao(xi_1)
            xi = x(yi).item()
            contador+=1
            self.estagios.append([str(contador), xi, yi])
        self.n_alimentacao = contador
        
        ## Esgotamento
        while xi > self.x_B:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_esgotamento(xi)], color="tab:blue"))
            xi_1 = xi
            yi = self.reta_operacao_esgotamento(xi_1)
            xi = x(yi).item()
            contador+=1
            self.estagios.append([str(contador), xi, yi])
            
        self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi, xi], [yi, xi], color="tab:blue"))
        
    def plotar_detalhes(self, ax):
        for s, x, y in self.estagios:
            self.annotations.append(ax.annotate(s, xy=(x, y), xytext=(0,5), textcoords='offset points', ha='center', fontweight='bold'))
        ax.set_title(f'Número total de estágios: {self.estagios[-1][0]}, Estágio ótimo para alimentação: {self.n_alimentacao}')
        # ax.text(0.6, 0.2, f'Número total de estágios: {self.estagios[-1][0]}\nEstágio ótimo para alimentação: {self.n_alimentacao}',
        #         fontsize=10, verticalalignment='top', 
        #         bbox=dict(boxstyle='round', facecolor='grey', alpha=0.5))
        
    def obter_estagios(self):
        return self.estagios