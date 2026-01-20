import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import MultipleLocator
from Equilibrio.equilibrio import EquilibrioTermodinamico
from McCabeThiele.mccabe_thiele import McCabeThieleMethod
from McCabeThiele.mccabe_thiele_simples import McCabeThieleSimples
from McCabeThiele.mccabe_thiele_avancado import McCabeThieleAvancado
from scipy.interpolate import interp1d


def plotar_diagrama_equilibrio(axis, X, Y, especie_principal):
    axis.plot(X,Y,label="Curva de equilíbrio", color="tab:red")
    axis.plot(X,X,label="Reta auxiliar", color="black", alpha=0.5)
    axis.set_xlim((0,1))
    axis.set_ylim((0,1))
    axis.set_ylabel(f"y ({especie_principal})")
    axis.set_xlabel(f"x ({especie_principal})", loc='right')
    axis.xaxis.set_major_locator(MultipleLocator(0.1))
    axis.xaxis.set_minor_locator(MultipleLocator(0.02))
    axis.yaxis.set_major_locator(MultipleLocator(0.1))
    axis.yaxis.set_minor_locator(MultipleLocator(0.02))
    axis.grid(which='major', linestyle='-', linewidth=0.75, alpha=0.8)
    axis.grid(which='minor', linestyle=':', linewidth=0.75, alpha=0.8)
    axis.minorticks_on()
    axis.legend()
    

def atualizar_plot(x, fig, ax, McCabe, slider_zF, slider_q, slider_R):
    McCabe.limpar_listas()
    McCabe.atualizar_sliders(slider_zF.val, slider_R.val, slider_q.val)
    McCabe.update()
    McCabe.plotar_retas_operacao(ax)
    McCabe.montar_escada(ax)
    McCabe.plotar_detalhes(ax)
    # McCabe.imprimir_detalhes(salvar=False)
    fig.canvas.draw_idle()


def aplicar_metodo_mccabe_thiele(especies, F, zF, xD, xB, R, q, Eml=1.0, Emv=1.0, pressao=101325, 
                                 equilibrio=None, coluna:dict=None, dados_adicionais:tuple=None, opcoes:dict=None, pontos=100):  # type: ignore
    
    ## Opções de plot:
    if opcoes:
        plotar = opcoes["PLOTAR"]
        interativo = opcoes["INTERATIVO"]
        save = opcoes["SALVAR"]
    else:
        plotar = interativo = save = False

    ## Corpo do programa
    fig,ax = plt.subplots(figsize=(9,9))
    fig.suptitle(f"""Destilação binária {especies[0].capitalize()}/{especies[1].capitalize()} - McCabe-Thiele 
    ({pressao/101325:.1f} atm)""")
    
    # Curva de equilíbrio fornecida
    if equilibrio:
        X, Y, T = equilibrio 
    else:
        # Calcular equilibrio pelo módulo acoplado:
        Eq = EquilibrioTermodinamico()
        T0 = 323 # chute inicial
        X = np.linspace(0,1,pontos)
        *Y,T = Eq.calcular(especies, [X, 1-X], pressao, T0)
        Y = Y[0] # Só é necessária a curva da espécie de interesse
    
    # Interpolar os dados:
    y_de_x = interp1d(X, Y, kind='cubic', fill_value="extrapolate")  # type: ignore
    x_de_y = interp1d(Y, X, kind='cubic', fill_value="extrapolate")  # type: ignore
    T_de_x = interp1d(X, T, kind='cubic', fill_value="extrapolate") if len(T)>0 else None #type: ignore
    interpolacoes = [y_de_x, x_de_y, T_de_x]
    
    # Montar escada e obter estágios
    if plotar:
        # Plotar diagrama 
        X = np.linspace(0,1,pontos)
        plotar_diagrama_equilibrio(ax, X, y_de_x(X), especies[0])

        # Dados de entradas e saídas adicionais
        if any([Emv!=1.0, Eml!=1.0, any(coluna.values())]): # type: ignore
            
            F2, zF2, q2 = dados_adicionais[0] ## TODO: Melhorar toda essa estrutura...
            S, zS, s = dados_adicionais[1] #
            F = [F,F2] #
            zF = [zF, zF2] #
            q = [q, q2] #
            S = [S] #
            zS = [zS] #
            s = [s]  #
            
            val_q = q[0]
            val_zF = zF[0]
            Mc = McCabeThieleAvancado(xD, xB, R, F, zF, q, S, zS, s, Emv, Eml, interpolacoes, coluna) # type: ignore
        else:
            val_q = q
            val_zF = zF
            Mc = McCabeThieleSimples(zF, xD, xB, R, q, interpolacoes)
        
        # Plotar escada de McCabe
        Mc.plotar_retas_operacao(ax)
        Mc.title = "teste"
        Mc.montar_escada(ax) 
        Mc.plotar_detalhes(ax)
                
        # Sliders
        if interativo:
            plt.subplots_adjust(left=0.1, bottom=0.18)
            ax_zF = plt.axes([0.1, 0.09, 0.8, 0.02]) # type: ignore
            ax_R = plt.axes([0.1, 0.06, 0.8, 0.02]) # type: ignore
            ax_q = plt.axes([0.1, 0.03, 0.8, 0.02]) # type: ignore
            slider_zF = Slider(ax_zF, "$z_F$", xB+0.01, xD-0.01, valinit=val_zF, valstep=0.01)
            slider_R = Slider(ax_R, "$R$", 0, 10, valinit=R, valstep=0.2)
            slider_q = Slider(ax_q, "q", 0.1, 2.0, valinit=val_q, valstep=0.01)
            f = lambda x: atualizar_plot(x, fig, ax, Mc, slider_zF, slider_q, slider_R)
            slider_zF.on_changed(f)
            slider_R.on_changed(f)
            slider_q.on_changed(f)
            
        if save:
            plt.savefig(f"Graficos/McCabe-Thiele {especies[0].capitalize()}-{especies[1].capitalize()}.pdf")   
            
        plt.show()

    else:
        Mc = McCabeThieleMethod(zF, xD, xB, R, q, None, None, interpolacoes, None)
        Mc.calcular_caudais()
        Mc.update()
        Mc.calcular_Rmin()
        Mc.montar_escada() 
        
    Mc.imprimir_detalhes(salvar=True)