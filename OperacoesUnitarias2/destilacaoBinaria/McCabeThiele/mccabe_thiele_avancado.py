import numpy as np
from McCabeThiele.mccabe_thiele import McCabeThieleMethod
from McCabeThiele.balancos import caudais_simples, caudais_vapor_direto, caudais_entrada_e_saida_adicionais, caudais_vapor_direto_e_correntes_extras
from McCabeThiele.reta_operacao import RetaOperacao

class McCabeThieleAvancado(McCabeThieleMethod):
    def __init__(self, x_D:float, x_B:float, R:float, F:list, z_F:list, q:list, S:list, z_S:list, s:list, Emv:float, Eml:float, equilibrio:list, coluna:dict) -> None:
        super().__init__(z_F, x_D, x_B, R, q, Emv, Eml, equilibrio, coluna)
        self.a = []
        self.b = []
        self.c = []
        self.retas_operacao = []
        self.retas_auxiliares = []    
        self.estagios_otimos = []
        self.x_intercepts = []
        self.y_intercepts = []
        self.F = F
        self.S = S
        self.s = s
        self.z_S = z_S
        
        # TODO: Generalizar para mais de uma entrada e mais de uma saída adicionais.
        self.m_entradas = 1
        self.n_saidas_adicionais = 0
        if coluna["ALIMENTACAO_ADICIONAL"]:
            self.m_entradas+=1  
        if coluna["SAIDA_ADICIONAL"]:
            self.n_saidas_adicionais+=1
        self.num_correntes_laterais = self.m_entradas + self.n_saidas_adicionais
        
        print("Calculando...\n")
        if (self.num_correntes_laterais) > 1:
            self.correntes_extras = True
            self.update()
        else:
            self.correntes_extras = False
            self.update()
            self.calcular_Rmin()
            
        
    def atualizar_sliders(self, zF, R, q):
        self.z_F[0] = zF
        self.R = R
        self.q[0] = q
    
    
    def limpar_listas(self):
        self.a.clear()
        self.b.clear()
        self.c.clear()
        self.retas_operacao.clear()
        self.retas_auxiliares.clear()
        self.estagios_otimos.clear()
        self.x_intercepts.clear()
        self.y_intercepts.clear()
        super().limpar_listas()
    
        
    def calcular_caudais(self):
        if self.coluna["VAPOR_DIRETO"]:
            if self.correntes_extras:
                self.V, self.D, self.B = caudais_vapor_direto_e_correntes_extras(
                    self.F, self.z_F, self.q, self.S, self.z_S, self.s, self.x_D, self.x_B, self.R
                    )
            else:
                self.V, self.D, self.B = caudais_vapor_direto(self.F[0], self.z_F[0], self.x_D, self.x_B, self.R, self.q[0])
        elif self.correntes_extras:
            self.D, self.B = caudais_entrada_e_saida_adicionais(
                self.F, self.z_F, self.S, self.z_S, self.x_D, self.x_B
            )
        else:
            ## Sempre que não houver correntes extras, self.z_F já será um float.
            self.D, self.B = caudais_simples(self.F[0], self.z_F[0], self.x_D, self.x_B)


    def _organizar_inputs(self):
        self.correntes = [(self.R, self.x_D, self.D)]
        for i in range(self.m_entradas):
            self.correntes.append((self.q[i], self.z_F[i], self.F[i]))
        for j in range(self.n_saidas_adicionais):
            self.correntes.append((self.s[j], self.z_S[j], -self.S[j]))
        self.correntes.sort(key=lambda x: x[1], reverse=True)


    def calcular_coeficientes(self):
        # i == 0
        self.a.append(self.R*self.D)
        self.b.append(self.x_D*self.D)
        self.c.append((self.R+1)*self.D)
        # i >= 1
        for i in range(1, self.num_correntes_laterais + 1):
            kj, zj, Vj = self.correntes[i]        
            self.a.append(self.a[i-1] + kj*Vj)
            self.b.append(self.b[i-1] - zj*Vj)
            self.c.append(self.c[i-1] + (kj-1)*Vj)
    
    
    def _verificar_pinch(self):
        # Retificação
        x = np.linspace(self.x_intercepts[0], self.x_D, 1000)
        d = self.eq(x) - self.reta_operacao_retificacao(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < self.tol:
            self.pinch = True
            return
        # Regiões intermediárias
        for i in range(1, self.num_correntes_laterais):
            x = np.linspace(self.x_intercepts[i-1], self.x_intercepts[i], 1000)
            d = self.eq(x) - self.retas_operacao[i](x)
            if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
                self.pinch = True
                return
            elif np.min(np.abs(d)) < self.tol:
                self.pinch = True
                return
        # Esgotamento
        x = np.linspace(self.x_B, self.x_intercepts[-1], 1000)
        d = self.eq(x) - self.reta_operacao_esgotamento(x)
        if len(np.where(np.diff(np.sign(d)) != 0)[0]) > 0:
            self.pinch = True
            return
        elif np.min(np.abs(d)) < self.tol:
            self.pinch = True
    

    def update(self):
        self.pinch = False
        self.nao_fisico = False
        self.calcular_caudais()
        self._organizar_inputs()
        self.calcular_coeficientes()
        
        ## Retas de operação e Interseções:
        # Retificação
        self.a1 = self.a[0]/self.c[0]
        self.b1 = self.b[0]/self.c[0]
        self.retas_operacao.append(RetaOperacao(self.a1, self.b1, "Retificação"))
        x_intercept = (self.b[0]/self.c[0] - self.b[1]/self.c[1]) / (self.a[1]/self.c[1] - self.a[0]/self.c[0])
        eq_intercept = self.eq(x_intercept)
        self.x_intercepts.append(x_intercept)
        self.y_intercepts.append(self.reta_operacao_retificacao(x_intercept))
        if self.y_intercepts[-1] > eq_intercept:
            self.nao_fisico = True
        elif np.isclose(self.y_intercepts[-1], eq_intercept, atol=self.tol): 
            self.pinch = True
            
        # Corpo da coluna
        for i in range(1, self.num_correntes_laterais):
            # Retas de operação das regiões intermediárias
            self.retas_operacao.append(RetaOperacao(self.a[i]/self.c[i], self.b[i]/self.c[i], f"Corpo {i}"))
            x_intercept = (self.b[i]/self.c[i] - self.b[i+1]/self.c[i+1]) / (self.a[i+1]/self.c[i+1] - self.a[i]/self.c[i])
            eq_intercept = self.eq(x_intercept)
            self.x_intercepts.append(x_intercept)
            self.y_intercepts.append(self.retas_operacao[i](x_intercept))
            if self.y_intercepts[i] > eq_intercept:
                self.nao_fisico = True
            elif np.isclose(self.y_intercepts[i], eq_intercept, atol=self.tol): 
                self.pinch = True
            # Retas auxiliares (alimentação extra e saídas laterais)
            kj, zj, _ = self.correntes[i]
            if kj == 1: #q==1 / s==1
                self.retas_auxiliares.append(None)
            else:
                self.retas_auxiliares.append(RetaOperacao(-kj/(1-kj), zj/(1-kj), f"Auxiliar {i}"))
        if not self.retas_auxiliares:
            # Se não houverem correntes extras de entrada ou saída, não haverão iterações no laço,  
            # e os segundos itens dos arrays correspondederão aos da reta auxiliar de alimentação.
            self.a2 = self.a[1]/self.c[1]
            self.b2 = self.b[1]/self.c[1]
        # Iteração extra necessária para a(s) reta(s) de operação auxiliar(es)
        kj, zj, _ = self.correntes[-1]
        if kj == 1: #q==1 / s==1
            self.retas_auxiliares.append(None)
        else:
            self.retas_auxiliares.append(RetaOperacao(-kj/(1-kj), zj/(1-kj), f"Auxiliar {len(self.correntes)-1}"))
            
        # Esgotamento
        self.x_intercept = self.x_intercepts[-1]
        self.y_intercept = self.y_intercepts[-1]
        if self.coluna["VAPOR_DIRETO"]:
            self.Vb = None #Não existe nesse caso
            self.a3 = self.y_intercept/(self.x_intercept - self.x_B)
            self.b3 = -self.a3*self.x_B
        else:
            self.Vb = 1/((self.y_intercept - self.x_B)/(self.x_intercept - self.x_B) - 1)
            self.a3 = (self.Vb+1)/self.Vb
            self.b3 = -self.x_B/self.Vb
        self.retas_operacao.append(RetaOperacao(self.a3, self.b3, f"Esgotamento"))

        ## Análise de pinch:
        # O trecho anterior verifica apenas as intersecções das retas para análise de pinch.
        # Para verificar em todos os pontos de todas as retas, utiliza-se o método abaixo:
        if not (self.pinch or self.nao_fisico):
            self._verificar_pinch()
        
        ## Não recalcula Rmin a cada atualização nos sliders pois deixa muito lento.
        self.R_min = None
        
        # print(self.retas_operacao)
        # for reta in self.retas_operacao:
        #     print(reta)


    def _escada_do_topo(self, axis):
        ## Retificação
        contador = 1
        xi_1 = self.x_D
        yi = self.reta_operacao_retificacao(xi_1)
        xi = xi_1 + self.ef_liq*(self.eq_inverso(yi).item() - xi_1)
        self.estagios = [[str(contador), xi, yi]]
        if self.T:
            self.temperaturas = [self.T(xi)]
        
        while xi > self.x_intercepts[0]:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_retificacao(xi)], color="tab:blue"))
            contador+=1
            xi_1 = xi
            yi = self.reta_operacao_retificacao(xi_1)
            xi = xi_1 + self.ef_liq*(self.eq_inverso(yi).item() - xi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.estagios_otimos.append(contador)
        
        ## Corpo coluna
        for i in range(1, self.num_correntes_laterais):    
            while xi > self.x_intercepts[i]:
                self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
                self.plots.append(axis.plot([xi, xi], [yi, self.retas_operacao[i](xi)], color="tab:blue"))
                contador+=1
                xi_1 = xi
                yi = self.retas_operacao[i](xi_1)
                xi = xi_1 + self.ef_liq*(self.eq_inverso(yi).item() - xi_1)
                self.estagios.append([str(contador), xi, yi])
                if self.T:
                    self.temperaturas.append(self.T(xi))
            self.estagios_otimos.append(contador)
        
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

        if self.coluna["VAPOR_DIRETO"]:
            self.plots.append(axis.plot([xi_1, xi], [yi, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, xi], [yi, self.reta_operacao_esgotamento(xi)], color="tab:blue"))
        else:
        # Refervedor:
            self.plots.append(axis.plot([xi_1, xi_id], [yi, yi], color="tab:blue")) # type: ignore
            self.plots.append(axis.plot([xi_id, xi_id], [yi, xi_id], color="tab:blue")) # type: ignore
            self.estagios[-1] = [str(contador), xi_id, yi] # type: ignore
                    
                    
    def _escada_do_fundo(self, axis):       
        ## Último andar (100% eficiente se houver refervedor):
        contador = 1
        yi_1 = self.reta_operacao_esgotamento(self.x_B)
        xi = self.reta_operacao_esgotamento_inversa(yi_1)
        yi = self.eq(xi)
        if self.coluna ["VAPOR_DIRETO"]:
            ## Se não houver refervedor, aplica a eficiência como para qualquer outro estágio
            yi = yi_1 + self.ef_vap*(yi - yi_1)        
        self.estagios = [[str(contador), xi, yi]]
        if self.T:
            self.temperaturas = [self.T(xi)]

        ## Esgotamento
        while yi < self.y_intercepts[-1]:
            self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, self.reta_operacao_esgotamento_inversa(yi)], [yi, yi], color="tab:blue"))
            contador+=1
            yi_1 = yi
            xi = self.reta_operacao_esgotamento_inversa(yi_1)
            yi = yi_1 + self.ef_vap*(self.eq(xi) - yi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.estagios_otimos.append(contador)

        # Corpo da coluna:
        for i in range(self.num_correntes_laterais-1, 0, -1):
            while yi < self.y_intercepts[i-1]:
                self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
                self.plots.append(axis.plot([xi, self.retas_operacao[i].inversa(yi)], [yi, yi], color="tab:blue"))
                contador+=1
                yi_1 = yi
                xi = self.retas_operacao[i].inversa(yi_1)
                yi = yi_1 + self.ef_vap*(self.eq(xi) - yi_1)
                self.estagios.append([str(contador), xi, yi])
                if self.T:
                    self.temperaturas.append(self.T(xi))
            self.estagios_otimos.append(contador)

        ## Retificacao
        while yi < self.x_D:
            self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
            self.plots.append(axis.plot([xi, self.reta_operacao_retificacao_inversa(yi)], [yi, yi], color="tab:blue"))
            contador+=1
            yi_1 = yi
            xi = self.reta_operacao_retificacao_inversa(yi_1)
            yi = yi_1 + self.ef_vap*(self.eq(xi) - yi_1)
            self.estagios.append([str(contador), xi, yi])
            if self.T:
                self.temperaturas.append(self.T(xi))
        self.plots.append(axis.plot([xi, xi], [yi_1, yi], color="tab:blue"))
        self.plots.append(axis.plot([xi, yi], [yi, yi], color="tab:blue"))
        
        ## Numerar a partir do topo
        n = len(self.estagios)
        for estagio in self.estagios:
            estagio[0] = str(n - int(estagio[0]) + 1)
        self.estagios.reverse()
        # Contar estágio ótimo a partir do topo
        for k, estagio_otimo in enumerate(self.estagios_otimos):
            self.estagios_otimos[k] = estagio_otimo*-1 + n+1
        
        
    def montar_escada(self, axis): # type: ignore
        string_titulo = rf"($x_D$ = {self.x_D:.3f}, $x_B$ = {self.x_B:.3f}, $z_F$ = {self.z_F[0]:.3f}, $R$ = {self.R:.3f}, $q$ = {self.q[0]:.3f}"
        if self.pinch:
            self.title = rf"Zona de pinch para R = {self.R:.2f}, q = {self.q[0]:.2f}, $z_F$ = {self.z_F[0]:.2f}"
            return
        if self.nao_fisico:
            self.title = f"Zona fora do equilíbrio para R = {self.R:.2f}, q = {self.q[0]:.2f}, $z_F$ = {self.z_F[0]:.2f}"
            return
        if (self.ef_vap is not None) and (self.ef_vap != 1.0):
            self._escada_do_fundo(axis)
            string_titulo += r", $E_{MV}$" + f" = {self.ef_vap})"
        else:
            if self.ef_liq is None:
                self.ef_liq = 1.0
                string_titulo += ")"
            else:
                string_titulo += r", $E_{ML}$" + f" = {self.ef_liq})"
            self._escada_do_topo(axis)
        self.title = f"Número total de estágios: {self.estagios[-1][0]}\n" + string_titulo 
    
    
    def _informacoes_caudais(self):
        if self.coluna["VAPOR_DIRETO"]:
            ret = [
                "\n - Caudais:",
                f" V/F = {self.V:.4f}",
                f" D/F = {self.D:.4f}",
                f" B/F = {self.B:.4f}"
            ]
        elif self.coluna["ALIMENTACAO_ADICIONAL"] or self.coluna["SAIDA_ADICIONAL"]:
            ret = [
                "\n - Caudais:",
                f" D = {self.D:.4f}",
                f" B = {self.B:.4f}"
            ]
        else:   
            ret = super()._informacoes_caudais()
        return ret
    
    
    def _informacoes_retas_intermediarias(self):
        ret = []
        for i, reta in enumerate(self.retas_operacao[1:-1]):
            ret.extend(
                [f"\n- Reta de operação intermediária {i+1}:",
                    f" y = {reta.a:.4f} x  +  {reta.b:.4f},  α = {np.rad2deg(np.arctan(reta.a)):.2f}°",
                    f" y({self.x_intercepts[i]:.4f}) = {self.y_intercepts[i]:.4f}",
                    f" y({self.x_intercepts[i+1]:.4f}) = {self.y_intercepts[i+1]:.4f}"]
                )
        return ret
    
    
    def _informacoes_retas_auxiliares(self):
        if not self.correntes_extras:
            return self._informacoes_reta_alimentacao(self.q[0], self.z_F[0])
        else:
            ret = []
            for i, reta in enumerate(self.retas_auxiliares):
                if reta is None:
                    ret.extend(
                        [f"\n- Reta auxiliar {i+1} vertical em x = {self.x_intercepts[i]:.4f}."]
                    )
                else:
                    ret.extend(
                        [f"\n- Reta auxiliar {i+1}:",
                            f" y = {reta.a:.4f} x  +  {reta.b:.4f},  α = {np.rad2deg(np.arctan(reta.a)):.2f}°",
                            f" y({self.correntes[i+1][1]:.4f}) = {self.correntes[i+1][1]:.4f}",
                            f" y({self.x_intercepts[i]:.4f}) = {self.y_intercepts[i]:.4f}"]
                        )
            return ret


    def imprimir_detalhes(self, imprimir:bool=True, salvar:bool=False):
        informacoes_para_impressao = []

        ## Dados de entrada:
        informacoes_para_impressao.append("Dados:")
        informacoes_para_impressao.append(f"x_D = {self.x_D:.4f}")         
        informacoes_para_impressao.append(f"x_B = {self.x_B:.4f}")         
        informacoes_para_impressao.append(f"R = {self.R:.4f}")         
        informacoes_para_impressao.append(f"z_F = {', '.join(str(self.z_F[i]) for i in range(self.m_entradas))}")         
        informacoes_para_impressao.append(f"q = {', '.join(str(self.q[i]) for i in range(self.m_entradas))}")   
        if self.coluna["SAIDA_ADICIONAL"]:              
            informacoes_para_impressao.append(f"z_S = {', '.join(str(self.z_S[i]) for i in range(self.n_saidas_adicionais))}")         
            informacoes_para_impressao.append(f"s = {', '.join(str(self.s[i]) for i in range(self.n_saidas_adicionais))}")                 
        
        ## Caudais:
        informacoes_para_impressao.extend(self._informacoes_caudais())

        ## Retas de operação
        informacoes_para_impressao.extend(self._informacoes_reta_retificacao())
        if self.correntes_extras:
            informacoes_para_impressao.extend(self._informacoes_retas_intermediarias())
        informacoes_para_impressao.extend(self._informacoes_reta_esgotamento())
        
        ## Retas auxliares
        informacoes_para_impressao.extend(self._informacoes_retas_auxiliares())
    
        ## Intersecção:
        if self.correntes_extras:
            informacoes_para_impressao.append(f"\nIntersecção das retas de alimentação e saídas extras:")
            for k, (x,y) in enumerate(zip(self.x_intercepts, self.y_intercepts)):
                informacoes_para_impressao.append(f" {k} - ({x:.4f}, {y:.4f})")
        else:
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
            informacoes_para_impressao.append(f"Estágio(s) ótimo(s) para a(s) corrente(s) lateral(is): {', '.join(str(i) for i in self.estagios_otimos)}")
        
        ## Imprimir e salvar em um arquivo de texto
        texto = "\n".join(informacoes_para_impressao)
        if imprimir:
            print(texto)
        if salvar:
            with open("resultados.txt", "w+", encoding='utf-16') as f:
                f.write(texto)  

    
    def plotar_retas_operacao(self, axis):
        n = 50
        # Retificação
        X = np.linspace(self.x_D, self.x_intercepts[0], n)
        self.plots.append(axis.plot(X, self.reta_operacao_retificacao(X), 
                                    color="black", linestyle='--', label="Reta de retificação"))
        # Meio da coluna
        for i in range(1, self.num_correntes_laterais):
            X = np.linspace(self.x_intercepts[i-1], self.x_intercepts[i], n)
            self.plots.append(axis.plot(X, self.retas_operacao[i](X),
                                        color="black", linestyle='--'))
        # Esgotamento
        X = np.linspace(self.x_B, self.x_intercepts[-1], n)
        self.plots.append(axis.plot(X, self.reta_operacao_esgotamento(X), 
                                    color="black", linestyle='--', label="Reta de esgotamento"))
        
        # Retas auxiliares de alimentações e saídas laterais:
        for i in range(self.num_correntes_laterais):
            kj, zj, _ = self.correntes[i+1]
            if kj == 1: # q/s == 1
                self.plots.append(axis.plot([zj, zj], [zj, self.y_intercepts[i]], 
                                color="black", linestyle=':'))
            else:
                X = np.linspace(zj, self.x_intercepts[i], n)
                self.plots.append(axis.plot(X, self.retas_auxiliares[i](X), 
                                            color="black", linestyle=':'))
       
       
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
