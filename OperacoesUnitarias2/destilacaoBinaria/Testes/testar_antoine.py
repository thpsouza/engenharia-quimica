import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from Equilibrio.PressaoSaturacao.substancias_antoine import *


def plot(especies, save=False, format='pdf'):
    t_min = float('inf')
    t_max = 0
    for i, especie in enumerate(especies):
        tmin = especie.tmin
        tmax = especie.tmax
        if tmin < t_min:
            t_min = tmin
        if tmax > t_max:
            t_max = tmax

        x = np.linspace(tmin, tmax)
        y = especie.calcular(x)
        plt.plot(x-273.15,y/100000,label=f"{i+1} - {especie.nome}")
    
    plt.title("Pressões de Saturação pela equação de Antoine")
    plt.xlim(t_min-273.15,t_max-273.15)
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Psat (bar)")
    plt.grid(which='both', linestyle='--', linewidth=0.75, alpha=0.8)
    plt.minorticks_on()
    plt.legend()
    if save:
        plt.savefig(f"./Graficos/Pressoes de Saturacao.{format}")
    plt.show()
    

def calcular(T, especies):
    if isinstance(T, (list,tuple,np.ndarray)):
        sol = np.zeros((len(especies), len(T)))
        for i, especie in enumerate(especies):
            for j, t in enumerate(T):
                    sol[i,j] = especie.calcular(t)
                    
    else:
        sol = np.zeros(len(especies))
        for i, especie in enumerate(especies):
            sol[i] = especie.calcular(T)
            
    return sol
    
    
def main():
    agua = AntoineAgua()
    alcool = AntoineEtanol()
    benzeno = AntoineBenzeno()  
    tolueno = AntoineTolueno()
    metanol = AntoineMetanol()
    p_xileno = AntoinePXILENO()  
    cloroformio = AntoineCloroformio()  
    acetona = AntoineAcetona()  
    especies = agua, alcool, benzeno, tolueno, metanol, p_xileno, cloroformio, acetona
    
    T = 450
    print(f"Psat(T = {T-273.15:.2f}°C):")
    for k, psat in enumerate(calcular(T, especies)):
        print(f" - {especies[k].nome}: {psat/100000:.4f} bar")
    
    plot(especies, True)
    
    
if __name__ == "__main__":
    main()