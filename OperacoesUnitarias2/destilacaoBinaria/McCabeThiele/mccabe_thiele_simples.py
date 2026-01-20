import numpy as np
from McCabeThiele.mccabe_thiele import McCabeThieleMethod


class McCabeThieleSimples(McCabeThieleMethod):
    def __init__(self, z_F, x_D, x_B, R, q, equilibrio) -> None:
        super().__init__(z_F, x_D, x_B, R, q, None, None, equilibrio, None)
        print("Calculando...\n")
        self.calcular_caudais()
        self.update()
        self.calcular_Rmin()
           
                    
    def montar_escada(self, axis): # type: ignore
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
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_retificacao(xi)], color="tab:blue"))
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
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_esgotamento(xi)], color="tab:blue"))
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_esgotamento(xi_1)
            xi = self.eq_inverso(yi).item()
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi, xi], [yi, xi], color="tab:blue"))
        
        s = rf"($x_D$ = {self.x_D:.3f}, $x_B$ = {self.x_B:.3f}, $z_F$ = {self.z_F:.3f}, $R$ = {self.R:.3f}, $q$ = {self.q:.3f})"
        self.title = f"Número total de estágios: {self.estagios[-1][0]}, Estágio ótimo para alimentação: {self.n_alimentacao}\n" + s 
        
        
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
