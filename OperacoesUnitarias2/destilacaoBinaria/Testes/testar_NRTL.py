import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from Equilibrio.CoeficienteAtividade.parametros_interacao_binaria import ParametrosNRTL
from Equilibrio.CoeficienteAtividade.NRTL import ModeloNRTL


def plotar(X, Y, T, especies, save=False, format='pdf'):
    for i, especie in enumerate(especies):
        plt.plot(X,Y[i],label=fr"$\gamma_{{{especie}}}$")
    plt.title(f"Coeficientes de atividade de {especies[0]} e {especies[1]} a T={T-273.15:.2f}°C")
    plt.xlim(0,1)
    plt.xlabel(f"x/y ({especies[0]})")
    plt.ylabel(r"$\gamma$")
    plt.grid(which='both', linestyle='--', linewidth=0.75, alpha=0.8)
    plt.minorticks_on()
    plt.legend()
    if save:
        plt.savefig(f"./Graficos/Coefs Atividade {especies[0]}-{especies[1]}.{format}")
    plt.show()


def main():
    especies = "Etanol", "Agua"
    composicoes = 0.895, 1-0.895
    temperatura = 79 + 273.15
    
    parametros = ParametrosNRTL()  
    modelo = ModeloNRTL(parametros.obter(especies))
    gammas = modelo.calcular(composicoes, temperatura)
    print(f"γ1 = {gammas[0]}, γ2 = {gammas[1]}")
    
    a,b,c = parametros.obter(especies)
    tau, G = modelo.calcular_parametros(temperatura)
    print("a:")
    print(a)
    print("b:")
    print(b)
    print("c:")
    print(c)
    print("τ:")
    print(tau)
    print("G:")
    print(G)
    
    # modelo = ModeloNRTL(Tau=np.asarray([[0.,-0.10186611],[1.79365242,0]]), G=np.asarray([[1.,1.03103158],[0.58385902,1]]))
    # print(modelo.calcular(composicoes, temperatura))
    
    # Plot
    T = 355
    X = np.linspace(0,1,100)
    Y1 = []
    Y2 = []
    for x in X:
        gammas = modelo.calcular((x,1-x), T)
        Y1.append(gammas[0])
        Y2.append(gammas[1])
    plotar(X, [Y1,Y2], T, especies, save=True)    
    
    
    
    
if __name__ == "__main__":
    main()