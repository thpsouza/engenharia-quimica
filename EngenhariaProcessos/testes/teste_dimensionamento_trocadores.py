import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EngenhariaProcessos import Corrente
from EngenhariaProcessos.dimensionamento import TrocadorDeCalor


# Criar trocador de calor
U = 0.75 #kW/m²°C
corrente_quente = Corrente(2, 250, 140)
corrente_fria = Corrente(7, 100, 220)
tipo_dT = 'log'
trocador = TrocadorDeCalor(U, tipo_dT)
# Dimensionar
Qq, Qf, dT, area = trocador.dimensionar(
    *corrente_quente,
    *corrente_fria
)

print("\n" + "=" * 70)
print("EXEMPLO: DIMENSIONAMENTO DE TROCADOR DE CALOR")
print("=" * 70)

print("\nParâmetros de entrada:")
print(f"  Corrente quente: WCp = {corrente_quente.WCp} kW/°C, {corrente_quente.To}°C → {corrente_quente.Td}°C")
print(f"  Corrente fria: WCp = {corrente_fria.WCp} kW/°C, {corrente_fria.To}°C → {corrente_fria.Td}°C")
print(f"  Coeficiente U: {U} kW/(m²·°C)")
print(f"  Método ΔT: {'Logarítmica (LMTD)' if tipo_dT=='log' else 'Aritmética'}")

print("\n" + str(trocador))