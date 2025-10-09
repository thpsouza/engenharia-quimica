from math import pi

def velocidade_fluido(vazao, diametro_base, cilindrico=True, area=None):
    """Calcula a velocidade do fluido em um elutriador, dada sua vazão, área da base e geometria

    Args:
        vazao (float): Vazão da corrente de fluido
        diametro_base (float): Diâmetro da base do elutriador, supondo cilindrico
        cilindrico (bool, optional): Geometria cilindrica do elutriador. Defaults to True.
        area (float, optional): Área transversal do elutriador. Defaults to None.

    Raises:
        ValueError: Se a geometria não for cilindrica, deve-se passar a área

    Returns:
        float: Velocidade do fluido
    """
    if cilindrico:
        area = area = pi * diametro_base ** 2 / 4
    else:
        if area is None:
            raise ValueError("Se a geometria não é cilindrica, a área da seção transversal deve ser informada.\n")
    return vazao/area
