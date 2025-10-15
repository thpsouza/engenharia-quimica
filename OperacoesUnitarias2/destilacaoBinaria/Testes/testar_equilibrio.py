import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from Equilibrio.equilibrio import EquilibrioTermodinamico
from Equilibrio.dados_manuais import equilibrio_etanol_agua, equilibrio_cloroformio_benzeno


def calcular_curvas_de_equilibrio(modelo, especies, X, pressao, T0=None):    
    if T0 is None:
        T0 = np.linspace(350,300,len(X))
    Y = np.zeros_like(X)
    T = np.zeros_like(X)
    for i, x in enumerate(X):
        sol = modelo.calcular(especies, [x, 1-x], pressao, T0[i])
        T[i] = sol[-1]
        Y[i] = sol[:-1][0]
    return Y, T


def _plotar_diagrama_equilibrio(axis, X, Y, especie_principal):
    axis.plot(X,Y,label="Curva de equilíbrio calculada")
    axis.plot(X,X,label="Reta auxiliar",color="tab:grey")
    axis.set_xlim((0,1))
    axis.set_ylim((0,1))
    axis.set_ylabel(f"y ({especie_principal})")
    axis.set_xlabel(f"x ({especie_principal})")
    axis.grid(which='both', linestyle='--', linewidth=0.75, alpha=0.8)
    axis.minorticks_on()
    axis.legend()


def _plotar_diagrama_TXY(axis, T, X, Y, especie_principal):
    axis.plot(X,T-273,label="Curva de bolha")
    axis.plot(Y,T-273,label="Curva de orvalho")
    axis.set_xlim((0,1))
    axis.set_ylabel("T (°C)")
    axis.set_xlabel(f"x/y ({especie_principal})", loc='right')
    axis.grid(which='both', linestyle='--', linewidth=0.75, alpha=0.8)
    axis.minorticks_on()
    axis.legend()


def plotar(T, X, Y, especies, pressao, save=False, format='pdf'):
    fig, axs = plt.subplots(1,2,figsize=(12, 6),subplot_kw=dict(box_aspect=1))
    match especies:
        case ["etanol", "agua"]:
            XY = equilibrio_etanol_agua()
        case ["cloroformio", "benzeno"]:
            XY = equilibrio_cloroformio_benzeno()
        case _:
            XY = None
    if XY:
        axs[0].scatter(*XY, label="Dados manuais", alpha=0.6, marker=".")
    _plotar_diagrama_equilibrio(axs[0], X, Y, especies[0])
    _plotar_diagrama_TXY(axs[1], T, X, Y, especies[0])
    fig.suptitle(f"{especies[0]}/{especies[1]}\n({pressao/101325:.0f} atm)")
    if save:
        fig.savefig(f"./Graficos/Diagramas {especies[0]}-{especies[1]}.{format}")
    plt.show()


def main():
    # Dados
    pressao = 101325
    especies = "etanol", "agua" #letras minusculas
    equilibrio = EquilibrioTermodinamico()
    
    # Calculo individual
    x = 0.895
    y1, y2, temp = equilibrio.calcular(especies, (x, 1-x), pressao, 373)
    print(f"x = {x:.4f}, y = {y1:.4f}, T = {temp-273.15:.4f} °C")
    
    # Plot
    X = np.linspace(0,1,100)
    Y, T = calcular_curvas_de_equilibrio(equilibrio, especies, X, pressao)
    plotar(T, X, Y, especies, pressao, save=True)    
    

if __name__ == "__main__":
    main()
    