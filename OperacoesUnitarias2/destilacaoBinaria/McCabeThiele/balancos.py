def caudais_simples(F:float, zF:float, xD:float, xB:float):
    D = (zF - xB)/(xD - xB) * F 
    B = F - D
    return D, B


def caudais_vapor_direto(F:float, zF:float, xD:float, xB:float, R:float, q:float):
    D = F * (zF - xB*q)/(xD + xB*R)
    B = q*F + R*D
    V = (R+1)*D + (q-1)*F
    return V, D, B


def caudais_vapor_direto_e_correntes_extras(F:list, zF:list, q:list, S:list, zS:list, s:list, xD:float, xB:float, R:float):
    aux1 = lambda x,y: x*y
    aux2 = lambda x,y,z: x*(z - y*xB) 
    D = (sum(map(aux2,F,q,zF)) - sum(map(aux2,S,s,zS)))/(R*xB + xD)
    B = sum(map(aux1,q,F)) - sum(map(aux1,s,S)) + R*D
    V = sum(S) - sum(F) + D + B
    return V, D, B


def caudais_entrada_e_saida_adicionais(F:list, zF:list, S:list, zS:list, xD:float, xB:float):
    aux = lambda x,y: x*y
    soma_entradas = sum(F)
    soma_saidas_extras = sum(S)
    D = (sum(map(aux,F,zF)) - sum(map(aux,S,zS)) - (soma_entradas - soma_saidas_extras)*xB) / (xD - xB)
    B = soma_entradas - soma_saidas_extras - D
    return D, B


if __name__ == "__main__":
    F = 60
    zF = 0.56
    xD = 0.94
    xB = 0.03
    F2 = 0#100
    zF2 = 0.4
    S = 0#20 
    zS = 0.74
    print(caudais_entrada_e_saida_adicionais([F,F2], [zF, zF2], [S], [zS], xD, xB))