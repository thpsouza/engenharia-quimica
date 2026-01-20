import sys
import os
from scipy.interpolate import interp1d
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Equilibrio.dados_manuais import equilibrio_etanol_agua
from McCabeThiele.mccabe_thiele import McCabeThieleMethod

def main():
    X, Y = equilibrio_etanol_agua()
    y_de_x = interp1d(X, Y, kind='cubic', fill_value="extrapolate")  # type: ignore
    x_de_y = interp1d(Y, X, kind='cubic', fill_value="extrapolate")  # type: ignore
    
    Mc = McCabeThieleMethod(0.32, 0.75, 0.02, 2, 1.25, None, None, [y_de_x, x_de_y, None], None)
    Mc.calcular_caudais()
    Mc.update()
    Mc.calcular_Rmin()
    Mc.montar_escada()
    Mc.imprimir_detalhes()

if __name__ == "__main__":
    main()
    