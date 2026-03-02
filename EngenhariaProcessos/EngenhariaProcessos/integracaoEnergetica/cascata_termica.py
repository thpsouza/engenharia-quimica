from EngenhariaProcessos.corrente import Corrente
from EngenhariaProcessos.integracaoEnergetica.intervalo_termico import IntervaloTermico
from EngenhariaProcessos.integracaoEnergetica.visualizacao.tabela_cascata_termica import TabelaCascataTermica


def calcular_intervalos_cascata_termica(correntes: list, dT_min: float = 10, separado=False) -> list:
    """Constrói a grid de temperaturas para análise de integração energética.

    Esta função cria os intervalos de temperatura onde serão calculadas as cargas
    das correntes. Para cada corrente, são definidas temperaturas deslocadas de
    ±ΔT_min dependendo se a corrente é quente ou fria, respeitando o princípio
    de diferença mínima de temperatura.

    Parameters:
        correntes (list[Corrente]): Lista de objetos Corrente a serem analisadas.
        dT_min (float, optional): Diferença mínima de temperatura em °C.
            Padrão: 10. Tipicamente 5-30 dependendo da aplicação.
        separado (bool, optional): Se True, retorna listas separadas para
            correntes quentes e frias. Se False, retorna lista única ordenada
            de todos os intervalos. Padrão: False.

    Returns:
        list: Lista ordenada de objetos IntervaloTermico (em ordem decrescente
            de temperatura) ou tupla com duas listas se separado=True.

    Examples:
        >>> correntes = [
        ...     Corrente(WCp=5, To=60, Td=150),
        ...     Corrente(WCp=10, To=180, Td=90)
        ... ]
        >>> intervalos = calcular_intervalos_cascata_termica(correntes, dT_min=10)
        >>> print(f"Grid de intervalos: {intervalos}")
        Grid de intervalos: [(190, 180), (170, 160), ...]
    """
    if separado:
        T_quentes = []
        T_frias = []
        for corrente in correntes:
            if corrente.quente:
                T_quentes.extend([corrente.To, corrente.To-dT_min, corrente.Td, corrente.Td-dT_min])
            else:
                T_frias.extend([corrente.To, corrente.To+dT_min, corrente.Td, corrente.Td+dT_min])
        # T_quentes.sort(reverse=True)
        # T_frias.sort(reverse=True)
        return [T_quentes, T_frias]
    else:
        intervalos = []
        for corrente in correntes:
            c = (corrente.Q > 0) - (corrente.Q < 0)
            intervalos.append(IntervaloTermico(corrente.To, corrente.To+c*dT_min))
            intervalos.append(IntervaloTermico(corrente.Td, corrente.Td+c*dT_min))
        
        # Ordenar no tipo: [(170, 160), (150, 140), (145, 135), (90, 80), (60, 50), (30, 20)]
        #                   [170, 160,   150, 145,   140, 135,   90, 80,   60, 50,   30, 20]
        intervalos = list(set(intervalos))
        intervalos.sort(reverse=True)
        return intervalos
    

def _calcular_cargas_intervalo(correntes: list[Corrente], subintervalos: list[IntervaloTermico]) -> tuple:
    """Calcula oferta e demanda de calor dentro de um intervalo.

    Função auxiliar interna que verifica quais correntes operam dentro de um
    determinado intervalo de temperatura e calcula as respectivas cargas
    térmicas.

    Parameters:
        correntes (list[Corrente]): Lista de correntes do processo.
        subintervalos (list[IntervaloTermico]): Intervalo com dois elementos
            (superior e inferior).

    Returns:
        tuple: ``(oferta, demanda)`` do intervalo em kW, com convenção
            de sinais interna.
    """
    oferta = demanda = 0
    for corrente in correntes:
        if corrente.quente and ((subintervalos[0].Ti, subintervalos[1].Ti) in corrente):
            oferta -= corrente.calcular_carga_termica(subintervalos[0].Ti, subintervalos[1].Ti)
        elif ((subintervalos[0].Tf, subintervalos[1].Tf) in corrente):
            demanda -= corrente.calcular_carga_termica(subintervalos[0].Tf, subintervalos[1].Tf)
    return oferta, demanda

    
def calcular_cascata_termica(
    correntes: list[Corrente],
    intervalos: list[IntervaloTermico] | None = None,
    tabela: TabelaCascataTermica | None = None,
    dT_min: float = 10,
) -> tuple:
    """Executa o cálculo completo da cascata térmica.

    Calcula os saldos de energia acumulada por intervalo de temperatura,
    determinando os limites mínimos de vapor (utilidade quente) e água
    (utilidade fria) necessários para o processo.

    Parameters:
        correntes (list[Corrente]): Lista de correntes do processo.
        intervalos (list[IntervaloTermico], optional): Intervalos pré-calculados.
            Se None, serão gerados automaticamente.
        tabela (TabelaCascataTermica, optional): Instância de tabela para
            preenchimento. Se None, será criada uma nova.
        dT_min (float, optional): Delta T mínimo (°C). Padrão: 10.

    Returns:
        tuple: ``(Q_vap, Q_agua, tabela, intervalos)`` onde:
            - Q_vap (float): Calor de resfriamento mínimo necessário (kW).
            - Q_agua (float): Calor de aquecimento mínimo necessário (kW).
            - tabela (TabelaCascataTermica): Tabela com saldos por intervalo.
            - intervalos (list): Intervalos utilizados no cálculo.
    """
    
    if not tabela:
        tabela = TabelaCascataTermica()
    if not intervalos:
        intervalos = calcular_intervalos_cascata_termica(correntes, dT_min)

    # Calcular q nos intervalos
    Q_vap = 0
    saldo_acumulado = 0
    
    for i in range(0, len(intervalos)-1):
        saldo_anterior = saldo_acumulado # (resíduo)
        oferta, demanda = _calcular_cargas_intervalo(correntes, intervalos[i:i+2])
        saldo_acumulado += oferta - demanda 
        tabela.append([i+1, saldo_anterior, oferta, demanda, saldo_acumulado])
        
        # Verificar pinch:
        if saldo_acumulado < 0:
            Q_vap += saldo_acumulado
            saldo_acumulado = 0

    # No último intervalo, o calor remanescente precisa ser retirado com água de utilidades.
    Q_agua = saldo_acumulado
    
    return Q_vap, Q_agua, tabela, intervalos