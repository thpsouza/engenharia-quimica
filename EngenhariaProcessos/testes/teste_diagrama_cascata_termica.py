import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EngenhariaProcessos import Corrente, ListaCorrentes
from EngenhariaProcessos.integracaoEnergetica import DiagramaCascataTermica


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
    Corrente(7, 110, 240),
    Corrente(9, 160, 90),
    Corrente(11, 250, 140)
))

correntes5 = ListaCorrentes((        
    Corrente(8, 230, 150),
    Corrente(12, 130, 70),
    Corrente(5, 170, 200),
    Corrente(11, 80, 170)
))

DiagramaCascataTermica(correntes1).plotar()
DiagramaCascataTermica(correntes2).plotar()
DiagramaCascataTermica(correntes3).plotar()
DiagramaCascataTermica(correntes4).plotar()
DiagramaCascataTermica(correntes5).plotar()