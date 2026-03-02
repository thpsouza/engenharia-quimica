from math import log
from EngenhariaProcessos.corrente import Corrente


class TrocadorDeCalor:
    """Classe base para definir e dimensionar um trocador de calor.
    
    Implementa o dimensionamento de trocadores de calor a partir de parâmetros de entrada
    (temperaturas e capacidades térmicas das correntes) e do coeficiente global de troca térmica (U).
    
    A classe calcula automaticamente a carga térmica, a diferença média de temperatura e a área
    necessária para o trocador, suportando dois métodos de cálculo de média de temperatura:
    logarítmica (mais precisa) ou aritmética (simplificada).
    
    Attributes:
        U (float): Coeficiente global de troca térmica em kW/(m²·°C). Propriedade do trocador que
                  determina sua eficiência térmica.
        tipo_dT (str): Tipo de média de temperatura utilizada no cálculo. Pode ser:
                      - 'log': Média logarítmica (LMTD - recomendado para correntes em contracorrente)
                      - 'arit': Média aritmética (aproximação simplificada)
        called (bool): Flag interno para controle de execução dos métodos privados.
        Qq (float): Carga térmica da corrente quente em kW (calculado após dimensionar).
        Qf (float): Carga térmica da corrente fria em kW (calculado após dimensionar).
        Q (float): Menor valor entre |Qq| e Qf, representando o calor efetivamente transferido em kW.
        dT (float): Diferença média de temperatura em °C (calculada após dimensionar).
        area (float): Área necessária do trocador em m² (calculada após dimensionar).
    
    Examples:
        >>> # Criar um trocador com coeficiente U = 0.75 kW/(m²·°C) usando LMTD
        >>> trocador = TrocadorDeCalor(U=0.75, tipo_dT='log')
        >>> Qq, Qf, dT, area = trocador.dimensionar(
        ...     WCpq=2, Teq=250, Tsq=140,    # Corrente quente: 2 kW/°C, 250°C -> 140°C
        ...     WCpf=7, Tef=100, Tsf=220     # Corrente fria: 7 kW/°C, 100°C -> 220°C
        ... )
        >>> print(f"Carga: {Qq:.1f} kW, Área: {area:.2f} m²")
        Carga: 220.0 kW, Área: 38.39 m²
    """
    def __init__(self, U:float, tipo_dT:str='log') -> None:
        """Inicializa um novo trocador de calor com seus parâmetros principais.
        
        Args:
            U (float): Coeficiente global de troca térmica em kW/(m²·°C). Deve ser um valor positivo.
                      Valores típicos variam conforme o tipo de fluidos e configuração:
                      - Gás-gás: 0.01-0.1
                      - Gás-líquido: 0.1-1.0
                      - Líquido-líquido: 0.5-5.0
            tipo_dT (str, optional): Método de cálculo da diferença média de temperatura. 
                                     Padrão: 'log'. Valores aceitos:
                                     - 'log': Média logarítmica (LMTD), mais precisa
                                     - 'arit': Média aritmética, simplificada
        
        Raises:
            ValueError: Se tipo_dT não for 'log' ou 'arit'.
        
        Note:
            A inicialização apenas configura os parâmetros. O dimensionamento real (cálculo de área)
            ocorre quando o método dimensionar() é chamado.
        """
        self.U = U
        if tipo_dT not in ('log', 'arit'):
            raise ValueError("A variável tipo_dT só pode ser 'log' ou 'arit'. \n")
        self.tipo_dT = tipo_dT
        self.called = False
        self.dimensionado = False
    
    def _calcular_carga_termica(self, dT_min:float):
        """Calcula as cargas térmicas das correntes quente e fria, e a carga efetiva transferida.
        
        Método privado que calcula as cargas térmicas baseado nas capacidades e diferenças de temperatura.
        A carga efetiva (Q) é o menor valor entre as cargas das duas correntes, representando o máximo
        calor que pode ser transferido no trocador.
        
        Args:
            WCpq (float): Capacidade térmica em fluxo da corrente quente em kW/°C.
            WCpf (float): Capacidade térmica em fluxo da corrente fria em kW/°C.
            Teq (float): Temperatura de entrada da corrente quente em °C.
            Tsq (float): Temperatura de saída da corrente quente em °C.
            Tef (float): Temperatura de entrada da corrente fria em °C.
            Tsf (float): Temperatura de saída da corrente fria em °C.
        
        Attributes set:
            Qq (float): Carga térmica da corrente quente = WCpq * (Tsq - Teq)
            Qf (float): Carga térmica da corrente fria = WCpf * (Tsf - Tef)
            Q (float): Menor valor entre |Qq| e Qf (calor efetivamente transferido)
        
        Note:
            Este método não pode ser usado independentemente; deve ser chamado apenas via dimensionar().
        """
        assert self.called, "Esse método não pode ser usado independentemente."
        # Limitar troca
        if (self.trocada_quente.To - self.trocada_fria.Td < dT_min):
            self.trocada_fria.atualizar_corrente(Td = self.trocada_quente.To - dT_min)
        if (self.trocada_quente.Td - self.trocada_fria.To < dT_min):
            self.trocada_quente.atualizar_corrente(Td = self.trocada_fria.To + dT_min)
        # Calcular troca
        self.Qq = self.trocada_quente.Q
        self.Qf = self.trocada_fria.Q
        self.Q = min(abs(self.Qq), self.Qf)
        self.trocada_quente.calcular_nova_temperatura(self.Q)
        self.trocada_fria.calcular_nova_temperatura(self.Q)

    def _calcular_dT(self):
        """Calcula a diferença média de temperatura entre as correntes.
        
        Método privado que calcula a diferença média de temperatura usando o método especificado
        na inicialização (logarítmica ou aritmética). A diferença média é fundamental para o
        dimensionamento do trocador pela equação Q = U·A·ΔT.
        
        Para correntes em contracorrente (configuração assumida), são calculados:
        - delta1 = Teq - Tsf (diferença de temperatura em uma extremidade)
        - delta2 = Tsq - Tef (diferença de temperatura na outra extremidade)
        
        Args:
            Teq (float): Temperatura de entrada da corrente quente em °C.
            Tsq (float): Temperatura de saída da corrente quente em °C.
            Tef (float): Temperatura de entrada da corrente fria em °C.
            Tsf (float): Temperatura de saída da corrente fria em °C.
        
        Attributes set:
            dT (float): Diferença média de temperatura em °C, calculada como:
                       - Se tipo_dT='log': (delta1 - delta2) / ln(delta1/delta2) [LMTD]
                       - Se tipo_dT='arit': (delta1 + delta2) / 2 [média aritmética]
        
        Note:
            Este método não pode ser usado independentemente; deve ser chamado apenas via dimensionar().
            Para LMTD válida, delta1 e delta2 devem ter valores diferentes.
        """
        assert self.called, "Esse método não pode ser usado independentemente."
        delta1 = abs(self.trocada_quente.To - self.trocada_fria.Td)
        delta2 = abs(self.trocada_quente.Td - self.trocada_fria.To)
        match self.tipo_dT:
            case 'log':
                self.dT:float = (delta1 - delta2) / log(delta1/delta2)
            case 'arit':
                self.dT:float = (delta1 + delta2) / 2 
   
    def _calcular_area(self):
        """Calcula a área necessária do trocador de calor.
        
        Método privado que dimensiona a área do trocador usando a equação fundamental de transferência
        de calor: Q = U·A·ΔT, isolando A = Q / (U·ΔT).
        
        A área calculada representa a superfície de troca térmica necessária para transferir a quantidade
        de calor especificada sob as condições de operação definidas.
        
        Attributes set:
            area (float): Área do trocador em m², calculada como Q / (U * dT)
        
        Note:
            Este método não pode ser usado independentemente; deve ser chamado apenas via dimensionar().
            Requer que Q, U e dT já tenham sido calculados.
        """
        assert self.called, "Esse método não pode ser usado independentemente."
        self.area = self.Q / (self.U * self.dT)
   
    def dimensionar(self, WCpq, Teq, Tsq, WCpf, Tef, Tsf, dT_min:float=10) -> tuple[float, ...]:
        """Dimensiona o trocador de calor calculando todas as grandezas necessárias.
        
        Método principal que coordena o dimensionamento completo do trocador, executando em sequência:
        1. Cálculo das cargas térmicas das correntes
        2. Cálculo da diferença média de temperatura
        3. Cálculo da área necessária
        
        Args:
            WCpq (float): Capacidade térmica em fluxo da corrente quente em kW/°C.
            Teq (float): Temperatura de entrada da corrente quente em °C.
            Tsq (float): Temperatura de saída da corrente quente em °C.
            WCpf (float): Capacidade térmica em fluxo da corrente fria em kW/°C.
            Tef (float): Temperatura de entrada da corrente fria em °C.
            Tsf (float): Temperatura de saída da corrente fria em °C.
        
        Returns:
            tuple: Uma tupla contendo:
                - Qq (float): Carga térmica da corrente quente em kW
                - Qf (float): Carga térmica da corrente fria em kW
                - dT (float): Diferença média de temperatura em °C
                - area (float): Área necessária do trocador em m²
        
        Examples:
            >>> trocador = TrocadorDeCalor(U=0.75, tipo_dT='log')
            >>> Qq, Qf, dT, area = trocador.dimensionar(
            ...     WCpq=2, Teq=250, Tsq=140,
            ...     WCpf=7, Tef=100, Tsf=220
            ... )
            >>> print(f"Qq={Qq:.1f} kW, Qf={Qf:.1f} kW, dT={dT:.2f}°C, Área={area:.2f} m²")
        """
        self.called = True
        self.trocada_quente = Corrente(WCpq, Teq, Tsq)
        self.trocada_fria = Corrente(WCpf, Tef, Tsf)
        self._calcular_carga_termica(dT_min)
        self._calcular_dT()
        self._calcular_area()
        self.called = False
        self.dimensionado = True
        return self.Qq, self.Qf, self.dT, self.area

    def atualizar_correntes(self, corrente_quente:Corrente, corrente_fria:Corrente, inplace:bool=False) -> tuple[Corrente, Corrente]:
        assert self.dimensionado, "Esse método só pode ser usado após o dimensionamento completo do trocador. \n"
        if not inplace:
            corrente_quente = corrente_quente.copy()
            corrente_fria = corrente_fria.copy()
        corrente_quente.atualizar_corrente(To = self.trocada_quente.Td)
        corrente_fria.atualizar_corrente(To = self.trocada_fria.Td)
        return corrente_quente, corrente_fria
        
    def __repr__(self) -> str:
        """Retorna uma representação formatada dos resultados do dimensionamento.
        
        Produz uma string legível com os principais resultados do dimensionamento, incluindo
        cargas térmicas das correntes, diferença média de temperatura e área necessária.
        
        Returns:
            str: String formatada contendo:
                - Q: Carga térmica efetivamente transferida em kW
                - Potencial quente: Carga térmica da corrente quente (Qq)
                - Potencial fria: Carga térmica da corrente fria (Qf)
                - ΔT: Diferença média de temperatura (com indicação do método)
                - Área: Superfície de troca térmica em m²
        
        Examples:
            >>> trocador = TrocadorDeCalor(U=0.75, tipo_dT='log')
            >>> trocador.dimensionar(2, 250, 140, 7, 100, 220)
            (220.0, 840.0, 61.61, 38.39)
            >>> print(trocador)  # Exibe resultado formatado
            Trocador dimensionado:
             Q = 220.000 kW (Potencial quente: 220.000 kW, Potencial fria: 840.000 kW)
             ΔT_log = 61.61 °C
             Área = 38.39 m²
        """    
        return "Trocador dimensionado:\n" + \
            f"  |Q| = {self.Q:.3f} kW (Potencial quente: {self.Qq:.3f} kW, Potencial fria: {self.Qf:.3f} kW)\n" + \
            f"  ΔT_{self.tipo_dT} = {self.dT:.2f} °C\n" + \
            f"  Área = {self.area:.2f} m²\n" + \
            f"  {self.trocada_quente}\n" + \
            f"  {self.trocada_fria}"
    

class Aquecedor(TrocadorDeCalor):
    def __init__(self, T_vap:float, U: float, tipo_dT: str = 'log') -> None:
        super().__init__(U, tipo_dT)
        self.T_vap = T_vap
    
    def dimensionar(self, WCpf, Tef, Tsf) -> tuple[float, ...]: # pyright: ignore[reportIncompatibleMethodOverride]
        self.called = True
        self.trocada_quente = Corrente(0, self.T_vap, self.T_vap)
        self.trocada_fria = Corrente(WCpf, Tef, Tsf)
        self.Qq = self.Qf = self.Q = self.trocada_fria.Q
        self._calcular_dT()
        self._calcular_area()
        self.called = False
        self.dimensionado = True
        return self.Q, self.dT, self.area
    
    def atualizar_corrente(self, corrente_fria:Corrente, inplace:bool=False) -> Corrente:
        assert self.dimensionado, "Esse método só pode ser usado após o dimensionamento completo do trocador. \n"
        if not inplace:
            corrente_fria = corrente_fria.copy()
        corrente_fria.atualizar_corrente(To = self.trocada_fria.Td)
        return corrente_fria
        
class Resfriador(TrocadorDeCalor):
    def __init__(self, Tin_agua:float, Tout_agua:float, U: float, tipo_dT: str = 'log') -> None:
        super().__init__(U, tipo_dT)
        self.Tin_agua = Tin_agua
        self.Tout_agua = Tout_agua
    
    def dimensionar(self, WCpq, Teq, Tsq) -> tuple[float, ...]: # pyright: ignore[reportIncompatibleMethodOverride]
        self.called = True
        self.trocada_quente = Corrente(WCpq, Teq, Tsq)
        self.trocada_fria = Corrente(0, self.Tin_agua, self.Tout_agua)
        self.Qq = self.Qf = self.Q = abs(self.trocada_quente.Q)
        self._calcular_dT()
        self._calcular_area()
        self.called = False
        self.dimensionado = True
        return self.Q, self.dT, self.area
        
    def atualizar_corrente(self, corrente_quente:Corrente, inplace:bool=False) -> Corrente:
        assert self.dimensionado, "Esse método só pode ser usado após o dimensionamento completo do trocador. \n"
        if not inplace:
            corrente_quente = corrente_quente.copy()
        corrente_quente.atualizar_corrente(To = self.trocada_quente.Td)
        return corrente_quente