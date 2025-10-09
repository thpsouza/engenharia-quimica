from Equilibrio.PressaoSaturacao.antoine import Antoine

   
class AntoineAgua(Antoine):
    def __init__(self) -> None:
        self.nome="Água"
        #limites superiores
        coeficientes = [
            [303.00, [5.40221, 1838.675, -31.737]],
            [333.00, [5.20389, 1733.926, -39.485]],
            [363.00, [5.07680, 1659.793, -45.854]],
            [373.15, [5.08354, 1663.125, -45.622]],
            # [573.00, [3.55959, 643.748, -198.043]]
        ]
        tmin = 273.15
        tmax = 573.00
        limite_superior = True
        super().__init__(coeficientes, tmin, tmax, limite_superior)

    # def calcular(self, T):
        # A, B, C = 18.3036, 3816.44, -46.13
        # return np.exp(A - B/(T+C)) * 133.322


class AntoineEtanol(Antoine):
    def __init__(self) -> None:
        self.nome="Etanol"
        #limites inferiores
        coeficientes = [
            # [366.63, [5.07680, 1659.793, -45.854]],
            [292.77, [5.24677, 1598.673, -46.424]],
            [273.15, [5.37229, 1670.409, -40.191]]
        ]
        tmin = 273.15
        tmax = 513.91
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)
    
    # def calcular(self, T):
        # A, B, C = 18.9119, 3803.98, -41.68
        # return np.exp(A - B/(T+C)) * 133.322
    

class AntoineBenzeno(Antoine):
    def __init__(self) -> None:
        self.nome="Benzeno"
        #limites inferiores
        coeficientes = [
            [287.70, [4.01814, 1203.835, -53.226]],
            [354.07, [4.72583, 1660.652,  -1.461]],
            [373.50, [(4.72583+4.60362)/2, (1660.652+1701.073)/2,  (-1.461+20.806)/2]],
            [421.56, [4.60362, 1701.073,  20.806]]
        ]
        tmin = 287.70
        tmax = 554.8
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)
    
    
class AntoineTolueno(Antoine):
    def __init__(self) -> None:
        self.nome="Tolueno"
        #limites inferiores
        coeficientes = [
            [273.00, [4.14157, 1377.578, -50.507]],
            # [273.13, [4.23679, 1426.448, -45.957]],
            # [303.00, [4.08245, 1346.382, -53.508]],
            [308.52, [4.07827, 1343.943, -53.773]],
            [384.66, [(4.07827+4.54436)/2, (1343.943+1738.123)/2,  (-53.773+0.394)/2]],
            [420.00, [4.54436, 1738.123, 0.394]]
        ]
        tmin = 273
        tmax = 580
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)
    

class AntoineMetanol(Antoine):
    def __init__(self) -> None:
        self.nome="Metanol"
        #limites inferiores
        coeficientes = [
            [288.10, [5.20409, 1581.341, -33.50]],
            [353.50, [5.15853, 1569.613, -34.846]]
        ]
        tmin = 288.1
        tmax = 512.63
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)   
    

class AntoinePXILENO(Antoine):
    def __init__(self) -> None:
        self.nome="p-Xileno"
        #limites inferiores
        coeficientes = [
            [286.43, [4.14553, 1474.403, -55.377]],
            [331.44, [4.11138, 1450.688, -58.16]],
            [420.00, [4.50944, 1788.91, -13.902]]
        ]
        tmin = 286.43
        tmax = 600
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)   


class AntoineCloroformio(Antoine):
    def __init__(self) -> None:
        self.nome="Clorofórmio"
        #limites inferiores
        coeficientes = [
            [215.0, [4.20772, 1233.129, -40.953]],
            [334.4, [4.56992, 1486.455, -8.612]]
        ]
        tmin = 215
        tmax = 527
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)   
        

class AntoineAcetona(Antoine):
    def __init__(self) -> None:
        self.nome="Acetona"
        #limites inferiores
        coeficientes = [
            [259.16, [4.42448, 1312.253, -32.445]]
        ]
        tmin = 259.16
        tmax = 507.60
        limite_superior = False
        super().__init__(coeficientes, tmin, tmax, limite_superior)   
