import matplotlib.pyplot as plt
from EngenhariaProcessos.integracaoEnergetica.cascata_termica import calcular_intervalos_cascata_termica


class DiagramaCascataTermica:
    """Gera visualização de diagrama de cascata térmica.

    Constrói diagrama gráfico que mostra os degraus de temperatura das
    correntes quentes (vermelho) e frias (azul), facilitando a visualização
    de oportunidades de integração energética.
    """
    def __init__(self, correntes:list|None=None, dT_min:float=10) -> None:
        if not correntes:
            raise ValueError("Devem ser passadas as correntes para que se possa plotar o diagrama . \n")
        else:
            self.correntes = correntes
            self.dT_min = dT_min
            self.temperaturas_quentes, self.temperaturas_frias = calcular_intervalos_cascata_termica(correntes, dT_min, separado=True)
            self.temperaturas = self.temperaturas_quentes + self.temperaturas_frias

    def _plotar_bordas(self):
        self.T_min = min(self.temperaturas)
        self.T_max = max(self.temperaturas)
        self.ax.vlines(self.x_left, self.T_min, self.T_max, color='black', linewidth=2)
        self.ax.vlines(self.x_right, self.T_min, self.T_max, color='black', linewidth=2)
        self.ax.hlines(self.T_max, self.x_left, self.x_right, color='black', linewidth=2)
        self.ax.hlines(self.T_min, self.x_left, self.x_right, color='black', linewidth=2)

    def _plotar_degraus(self):
        ## Degraus alternados coloridos  
        # Degraus quentes
        i = 0
        while i < len(self.temperaturas_quentes):
            y_top = self.temperaturas_quentes[i]
            y_bottom = self.temperaturas_quentes[i+1]
            if y_bottom == y_top: 
                y_bottom -= self.dT_min
                i+=2
            self.ax.hlines(y_top, xmin=self.x_left, xmax=self.x_mid, color="tab:red", linewidth=1.5)
            self.ax.vlines(self.x_mid, ymin=y_bottom, ymax=y_top, color="tab:red", linewidth=1)
            self.ax.hlines(y_bottom, xmin=self.x_mid, xmax=self.x_right, color="tab:red", linewidth=1, linestyle='--')
            i+=2
        # Degraus frios
        j = 0
        while j < len(self.temperaturas_frias):
            y_bottom = self.temperaturas_frias[j]
            y_top = self.temperaturas_frias[j+1]
            if y_bottom == y_top: 
                y_bottom -= self.dT_min
                j+=2
            self.ax.hlines(y_top, xmin=self.x_left, xmax=self.x_mid, color="tab:blue", linewidth=1, linestyle='--')
            self.ax.vlines(self.x_mid, ymin=y_bottom, ymax=y_top, color="tab:blue", linewidth=1)
            self.ax.hlines(y_bottom, xmin=self.x_mid, xmax=self.x_right, color="tab:blue", linewidth=1.5)
            j+=2
        
    def _plotar_setas(self):
        ## Setas (correntes)
        n_quentes = 0
        n_frias = 0
        for corrente in self.correntes:
            if corrente.quente: n_quentes+=1
            else: n_frias+=1
        contador_quentes = 0
        contador_frias = 0
        dx_quentes = (self.x_mid - self.x_left)/(n_quentes+1)
        dx_frias = (self.x_right - self.x_mid)/(n_frias+1)
        for corrente in self.correntes:
            if corrente.quente:
                contador_quentes+=1
                self.ax.annotate("", 
                                 xy=(dx_quentes*contador_quentes, corrente.Td), 
                                 xytext=(dx_quentes*contador_quentes, corrente.To),
                                 arrowprops=dict(arrowstyle='->', lw=1, color='red'))
                self.ax.text(dx_quentes*contador_quentes-0.02, corrente.To+2, rf"$Q_{contador_quentes}$", color='red')
            else:   
                contador_frias+=1
                self.ax.annotate("", 
                                 xy=(dx_frias*contador_frias+self.x_mid, corrente.Td), 
                                 xytext=(dx_frias*contador_frias+self.x_mid, corrente.To),
                                 arrowprops=dict(arrowstyle='->', lw=1, color='blue'))
                self.ax.text(dx_frias*contador_frias-0.02+self.x_mid, corrente.To-5, rf"$F_{contador_frias}$", color='blue')
        
    def _plotar_ticks(self):
        ## Ticks temps quentes
        self.ax.set_ylim(self.T_min - self.dT_min, self.T_max + self.dT_min)
        self.ax.set_yticks(self.temperaturas)
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.set_xlim(-0.05, 1.05)
        self.ax.set_xticks([])
        for tl in self.ax.get_yticklabels():
            tl.set_color("tab:red")
            tl.set_fontsize(10)
        
        ## Ticks temps frias
        ax2 = self.ax.twinx()
        ax2.set_ylim(self.ax.get_ylim())
        ax2.set_yticks(self.temperaturas)
        for tl in ax2.get_yticklabels():
            tl.set_color("tab:blue")
            tl.set_fontsize(10)

    def plotar(self):
        fig, self.ax = plt.subplots(figsize=(6, 7))
        self.x_left, self.x_mid, self.x_right = 0.0, 0.5, 1.0
        self._plotar_bordas()
        self._plotar_degraus()
        self._plotar_setas()
        self._plotar_ticks()
        plt.title("Diagrama de Cascata Térmica")
        plt.tight_layout()
        plt.show()