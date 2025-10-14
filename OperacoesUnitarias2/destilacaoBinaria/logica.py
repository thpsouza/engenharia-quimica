import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import MultipleLocator
from Equilibrio.equilibrio import EquilibrioTermodinamico
from McCabeThiele.mccabe_thiele import McCabeThieleMethod
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
    for plot in McCabe.plots:
        plot[0].remove()
    for annotation in McCabe.annotations:
        annotation.remove()
    McCabe.plots = []
    McCabe.annotations = []
    McCabe.z_F = slider_zF.val
    McCabe.R = slider_R.val
    McCabe.q = slider_q.val
    McCabe.update()
    McCabe.plotar_retas_operacao(ax)
    McCabe.montar_escada(ax)
    McCabe.plotar_detalhes(ax)
    McCabe.imprimir_detalhes()
    fig.canvas.draw_idle()


def aplicar_metodo_mccabe_thiele(especies, zF, xD, xB, R, q, Eml=1.0, Emv=1.0, pressao=101325, equilibrio=None, 
                                 plotar=True, interativo=False, save=False, pontos=100):
    fig,ax = plt.subplots(figsize=(9,9))
    fig.suptitle(f"""Destilação binária {especies[0].capitalize()}/{especies[1].capitalize()} - McCabe-Thiele 
    ({pressao/101325:.1f} atm)""")
    
    if equilibrio:
        X, Y, T = equilibrio 
        Y = [Y]
    else:
        # Calcular equilibrio:
        Eq = EquilibrioTermodinamico()
        T0 = 323 # chute inicial
        X = np.linspace(0,1,pontos)
        *Y,T = Eq.calcular(especies, [X, 1-X], pressao, T0)
    
    # Interpolar os dados:
    y_de_x = interp1d(X, Y[0], kind='cubic', fill_value="extrapolate")  # type: ignore
    x_de_y = interp1d(Y[0], X, kind='cubic', fill_value="extrapolate")  # type: ignore
    if len(T)>0:
        T_de_x = interp1d(X, T, kind='cubic', fill_value="extrapolate") #type: ignore
    else:
        T_de_x = None
    
    # Plotar diagrama 
    X = np.linspace(0,1,pontos)
    plotar_diagrama_equilibrio(ax, X, y_de_x(X), especies[0])
    
    # Montar escada e obter estágios
    ## Futuramente, a ideia é avaliar se faz sentido, em termos de performance, separar o cálculo dos estágios do plot em si.
    Mc = McCabeThieleMethod(zF, xD, xB, R, q, Emv, Eml, y_de_x, x_de_y, T_de_x)
    Mc.plotar_retas_operacao(ax)
    Mc.montar_escada(ax) 
    Mc.plotar_detalhes(ax)
    Mc.imprimir_detalhes()
    
    if plotar:
        # Sliders
        if interativo:
            plt.subplots_adjust(left=0.1, bottom=0.18)
            ax_zF = plt.axes([0.1, 0.09, 0.8, 0.02]) # type: ignore
            ax_R = plt.axes([0.1, 0.06, 0.8, 0.02]) # type: ignore
            ax_q = plt.axes([0.1, 0.03, 0.8, 0.02]) # type: ignore
            slider_zF = Slider(ax_zF, "$z_F$", xB+0.01, xD-0.01, valinit=zF, valstep=0.01)
            slider_R = Slider(ax_R, "$R$", 0, 100, valinit=R, valstep=0.2)
            slider_q = Slider(ax_q, "q", 0.1, 2.0, valinit=q, valstep=0.01)
            f = lambda x: atualizar_plot(x, fig, ax, Mc, slider_zF, slider_q, slider_R)
            slider_zF.on_changed(f)
            slider_R.on_changed(f)
            slider_q.on_changed(f)
            
        if save:
            plt.savefig(f"Graficos/McCabe-Thiele {especies[0].capitalize()}-{especies[1].capitalize()}.pdf")   
            
        plt.show()
        