import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EngenhariaProcessos import Corrente, ListaCorrentes
from EngenhariaProcessos.integracaoEnergetica import TabelaCascataTermica
from EngenhariaProcessos.integracaoEnergetica import calcular_intervalos_cascata_termica, calcular_cascata_termica


cp_agua = 0.00116 #kWh/kg°C
dT_agua = 20 #°C
dHvap_agua = 0.48 #kWh/kg

correntes1 = ListaCorrentes((
    Corrente(5, 60, 150),
    Corrente(7, 100, 220),
    Corrente(10, 180, 90),
    Corrente(2, 250, 140)
))

correntes2 = ListaCorrentes((
    Corrente(4, 80, 140),
    Corrente(1.5, 150, 30),
    Corrente(2, 20, 135),
    Corrente(3, 170, 60)
))

correntes3 = ListaCorrentes((   
    Corrente(8, 200, 130),
    Corrente(2, 150, 70),
    Corrente(7, 140, 190),
    Corrente(4, 80, 160)
))

correntes4 = ListaCorrentes((
    Corrente(8, 60, 170),
    Corrente(9, 160, 90),
    Corrente(11, 250, 140),
    Corrente(7, 110, 240),
))

correntes5 = ListaCorrentes((        
    Corrente(8, 230, 150),
    Corrente(12, 130, 70),
    Corrente(5, 170, 200),
    Corrente(11, 80, 170)
))

intervalos = calcular_intervalos_cascata_termica(correntes1, dT_min=10)
tabela1 = TabelaCascataTermica()
_, _, tabela1, _ = calcular_cascata_termica(correntes1, intervalos, tabela1, dT_min=10)

_, _, tabela2, _ = calcular_cascata_termica(correntes2)
_, _, tabela3, _ = calcular_cascata_termica(correntes3)
_, _, tabela4, _ = calcular_cascata_termica(correntes4)
_, _, tabela5, _ = calcular_cascata_termica(correntes5)


print("\nTabela correntes 1:", tabela1, sep="\n")
print("\nTabela correntes 2:", tabela2, sep="\n")
print("\nTabela correntes 3:", tabela3, sep="\n")
print("\nTabela correntes 4:", tabela4, sep="\n")
print("\nTabela correntes 5:", tabela5, sep="\n")