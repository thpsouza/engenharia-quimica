from EngenhariaProcessos import Corrente, ListaCorrentes
from EngenhariaProcessos.integracaoEnergetica import (
    DiagramaCascataTermica,
    RPS, PD,
    calcular_cascata_termica,
)

def main():
    correntes = ListaCorrentes((
        Corrente(5, 60, 150),
        Corrente(7, 100, 220),
        Corrente(10, 180, 90),
        Corrente(2, 250, 140)
    ))
    
    Q_vap_necessario, Q_agua_necessario, tabela_cascata_termica, intervalos = calcular_cascata_termica(correntes)

    algoritmo_RPS = RPS(correntes, criterio='maior')
    integracoes, tabelas, utilidades = algoritmo_RPS()    
    
    # algoritmo_PD = PD(correntes)
    # integracoes, tabelas, utilidades = algoritmo_PD()
    
    print(f"Tabela de cascata térmica (kW):\n", tabela_cascata_termica, sep='')    
    print("Correntes integradas:\n", integracoes)
    print("Trocadores de calor:\n", utilidades)   
    DiagramaCascataTermica(correntes).plotar()

if __name__ == "__main__":
    main()