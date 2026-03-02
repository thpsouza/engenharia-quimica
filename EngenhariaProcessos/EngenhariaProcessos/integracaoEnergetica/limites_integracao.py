from EngenhariaProcessos.corrente import Corrente
from EngenhariaProcessos.integracaoEnergetica.visualizacao.tabela_cascata_termica import TabelaCascataTermica
from EngenhariaProcessos.integracaoEnergetica.intervalo_termico import IntervaloTermico
from EngenhariaProcessos.integracaoEnergetica.cascata_termica import (
    calcular_intervalos_cascata_termica,
    calcular_cascata_termica,
)


def consumo_maximo_utilidades(
    correntes: list[Corrente], cp_agua: float, dT_agua: float, dHvap_agua: float
):
    """Estima um limite superior para o consumo de utilidades (água e vapor).

    A função soma as cargas das correntes frias e quentes adotando a
    convenção interna de sinais e converte para vazões de utilidade com base
    em propriedades fornecidas.

    Parameters
    ----------
    correntes : list[Corrente]
        Lista de correntes do processo.
    cp_agua : float
        Capacidade calorífica efetiva usada para a água utilitária (kW/°C).
    dT_agua : float
        Elevação de temperatura disponível para a água de utilidades (°C).
    dHvap_agua : float
        Energia por massa de vapor utilizada para cálculo de vapor (kW por unidade).

    Returns
    -------
    tuple
        Retorna uma tupla ``(vazoes_massicas, Qs)`` onde ``vazoes_massicas`` é
        outra tupla com as vazões estimadas de (vapor, água) e ``Qs`` é a tupla
        com os valores brutos de energia (Q_vap, Q_agua).
    """
    Q_agua = 0
    Q_vap = 0
    for corrente in correntes:
        # Correntes quentes fornecem calor (Q ≤ 0)
        if corrente.Q <= 0:
            Q_agua -= corrente.Q
        # Correntes frias requerem calor (Q > 0)
        else:
            Q_vap -= corrente.Q
    return (-Q_vap / dHvap_agua, Q_agua / (cp_agua * dT_agua)), (Q_vap, Q_agua)


def consumo_minimo_utilidades(
    correntes: list[Corrente],
    cp_agua: float,
    dT_agua: float,
    dHvap_agua: float,
    intervalos: list[IntervaloTermico] | None = None,
    tabela: TabelaCascataTermica | None = None,
    dT_min: float = 10,
) -> tuple:
    """Calcula o consumo mínimo de utilidades utilizando a cascata térmica.

    Esta função encapsula a geração dos intervalos térmicos (quando não
    fornecidos), executa a cascata térmica e converte os resultados de energia
    em vazões de utilidades (vapor e água).

    Parameters
    ----------
    correntes : list[Corrente]
        Lista de correntes do processo.
    cp_agua : float
        Capacidade calorífica da água para cálculo da vazão de água utilitária.
    dT_agua : float
        Elevação de temperatura disponível para a água utilitária (°C).
    dHvap_agua : float
        Energia por massa de vapor usada para cálculo de vapor.
    intervalos : list[IntervaloTermico], optional
        Intervalos térmicos pré-calculados. Se None, serão gerados automaticamente.
    tabela : TabelaCascataTermica, optional
        Instância de tabela para preenchimento dos saldos por intervalo.
    dT_min : float, optional
        Delta T mínimo usado para construção dos intervalos (padrão: 10°C).

    Returns
    -------
    tuple
        ``(vazoes_massicas, Q_min, intervalos, tabela)`` onde:
        - ``vazoes_massicas``: tupla (vapor, água) com vazões calculadas;
        - ``Q_min``: tupla com os valores de energia (Q_vap, Q_agua);
        - ``intervalos``: lista de intervalos calculados/fornecidos;
        - ``tabela``: instância de ``TabelaCascataTermica`` preenchida.
    """
    if not intervalos:
        intervalos = calcular_intervalos_cascata_termica(correntes, dT_min)
    if not tabela:
        tabela = TabelaCascataTermica()

    Q_vap, Q_agua, tabela, intervalos = calcular_cascata_termica(
        correntes, intervalos, tabela, dT_min
    )

    vazoes_massicas = (-Q_vap / dHvap_agua, Q_agua / (cp_agua * dT_agua))
    Q_min = (Q_vap, Q_agua)
    return vazoes_massicas, Q_min, intervalos, tabela