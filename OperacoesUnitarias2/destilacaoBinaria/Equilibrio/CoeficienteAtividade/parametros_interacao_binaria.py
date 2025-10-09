import numpy as np

ESPECIES_POSSIVEIS = {
    "METANOL":0,
    "ETANOL":1,
    "BENZENO":2,
    "P-XILENO":3,
    "TOLUENO":4,
    "CLOROFORMIO":5,
    "AGUA":6,
    "ACETONA":7
}

A = [
    [  0.000,  4.712,   -1.709,    0.678,    0.000,  0.000,    -0.693,   0.000], # Metanol
    [ -2.313,  0.000,    0.569,    4.075,    1.146,  0.000,    -0.801,  -1.079], # Etanol
    [ 11.580, -0.916,    0.000,    0.000, -  2.885,  0.000,    45.191,   0.422], # Benzeno
    [ -3.259, -5.639,    0.000,    0.000,    0.000,  0.000,     2.773,   0.000], # p-Xileno
    [  0.000, -1.722,    2.191,    0.000,    0.000,  0.000,  -247.879,  -1.285], # Tolueno
    [  0.000,  0.000,    0.000,    0.000,    0.000,  0.000,    -7.352,   0.538], # Clorofórmio
    [  2.732,  3.458,  140.087,  162.477,  627.053,  8.844,     0.000,   0.054], # Água
    [  0.000, -0.347,   -0.102,    0.000,    1.203,  0.965,     6.398,   0.000]  # Acetona
]

B = [
    [    0.0, -1162.3,   892.2,   295.5,   371.1,   -71.9,   173.0,   114.1],
    [  483.8,     0.0,   -54.8, -1202.4,  -113.5,  -148.9,   246.2,   479.1],
    [-3282.6,   882.0,     0.0,   122.7,  1124.0,  -375.4,   591.4,  -239.9],
    [ 1677.6,  2504.2,  -136.5,     0.0,    75.9,   -17.7,   296.7,   173.6],
    [  446.9,   992.7,  -863.7,   -91.1,     0.0,   -57.0, 14759.8,   630.1],
    [  690.1,   690.3,   313.0,  -120.2,   -25.2,     0.0,  3240.7,  -106.4],
    [ -617.3,  -586.1, -5954.3, -6046.0,-27269.4, -1140.1,     0.0,   420.0],
    [  101.9,   206.6,   306.1,    83.2,  -400.5,  -590.0, -1809.0,     0.0] 
]

C = [
    [0.0, 0.3, 0.4, 0.5, 0.3, 0.3, 0.3, 0.3], 
    [0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], 
    [0.0, 0.0, 0.0, 0.0, 0.3, 0.5, 0.2, 0.3], 
    [0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.2, 0.3], 
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3], 
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.3],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3], 
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

class ParametrosInteracaoBinaria:
    def __init__(self, especies_possiveis, tabelas) -> None:
        self.especies_possiveis = especies_possiveis
        self.tabelas = tabelas
        self.called = False
        self.assert_msg = "Esse método não deve ser usado independentemente. " + \
        "Para obter os parâmetros, use o método 'obter()'. \n"
    
    def _reduzir_tabelas(self):
        assert self.called, self.assert_msg
        n = len(self.especies)
        self.tabelas_reduzidas = np.zeros_like(self.tabelas)[:, :n, :n]
        for k, tabela in enumerate(self.tabelas):
            for i in range(n):
                for j in range(n):
                    self.tabelas_reduzidas[k,i,j] = tabela[self.especies_possiveis[self.especies[i]], 
                                                           self.especies_possiveis[self.especies[j]]]
                    
    def _espelhar_C(self):
        assert self.called, self.assert_msg
        self.tabelas_reduzidas[2]+=self.tabelas_reduzidas[2].T
    
    def obter(self, especies):
        self.called = True
        self.especies = [especie.upper() for especie in especies]
        self._reduzir_tabelas()
        self._espelhar_C()
        return self.tabelas_reduzidas
    
    
class ParametrosNRTL(ParametrosInteracaoBinaria):
    def __init__(self) -> None:
        super().__init__(ESPECIES_POSSIVEIS, np.asarray([A,B,C]))
        
        

def main():
    especies = "METANOL","ETANOL","BENZENO","AGUA","ACETONA"
    a,b,c = ParametrosNRTL().obter(especies)
    print(a)
    print(b)
    print(c)

if __name__ == "__main__":
    main()