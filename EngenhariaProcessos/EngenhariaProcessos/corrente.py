class Corrente:
    """Representa uma corrente térmica de processo. Útil para análise de integração energética.

    A classe identifica automaticamente se a corrente é quente (Q ≤ 0, necessita resfriamento) ou 
    fria (Q > 0, necessita aquecimento).
    
    Attributes
    ----------
    WCp : float
        Capacidade térmica em fluxo (W·Cp) da corrente em kW/°C. Representa a quantidade
        de energia térmica por unidade de temperatura.
    To : float
        Temperatura inicial ou de origem da corrente em °C.
    Td : float
        Temperatura final ou de destino da corrente em °C.
    Q : float
        Carga térmica total da corrente em kW. Calculada como Q = WCp × (Td - To).
        Valor positivo indica corrente fria (necessita aquecimento).
        Valor nulo ou negativo indica corrente quente (disponível para resfriamento).
    quente : bool
        Flag de classificação da corrente. True se Q ≤ 0 (corrente quente),
        False se Q > 0 (corrente fria).
    unidades : dict
        Dicionário com as unidades utilizadas: {'calor': 'kW', 'temperatura': '°C'}.
        Permite customização das unidades de visualização.
    
    Examples
    --------
    Criar uma corrente fria (aquecimento necessário):
    
    >>> corrente_fria = Corrente(WCp=100, To=20, Td=80)
    >>> corrente_fria.Q
    6000.0
    >>> corrente_fria.quente
    False
    
    Criar uma corrente quente (resfriamento necessário):
    
    >>> corrente_quente = Corrente(WCp=150, To=200, Td=50)
    >>> corrente_quente.Q
    -22500.0
    >>> corrente_quente.quente
    True
    """
    def __init__(self, WCp: float, To: float, Td: float, unidades: dict = None) -> None:  # type: ignore
        """Inicializa uma nova corrente térmica com seus parâmetros.
        
        Calcula automaticamente a carga térmica total (Q) e classifica a corrente como
        quente ou fria com base no sinal da carga térmica usando a fórmula:
        Q = WCp × (Td - To)
        
        Parameters
        ----------
        WCp : float
            Capacidade térmica em fluxo da corrente em kW/°C.
            Deve ser um valor positivo.
        To : float
            Temperatura inicial ou de origem em °C.
        Td : float
            Temperatura final ou de destino em °C.
        unidades : dict, optional
            Dicionário com as unidades de 'calor' e 'temperatura'.
            Padrão: {'calor': 'kW', 'temperatura': '°C'}
            
        Notes
        -----
        - Se Q > 0: corrente fria (requer aquecimento) → quente = False
        - Se Q ≤ 0: corrente quente (disponível para resfriamento) → quente = True
        
        Warns
        -----
        - Se WCp for negativo, causará cálculos incorretos de carga térmica.
        """
        self.WCp = WCp
        self.To = To
        self.Td = Td
        self.Q = WCp * (Td - To)
        if self.Q < 0:
            self.quente = True
            self.tipo = 'Quente'
        elif self.Q > 0:
            self.quente = False
            self.tipo = 'Fria'
        else:
            self.quente = False
            self.tipo = 'Neutra'
            
        if unidades: 
            self.unidades = unidades
        else:
            self.unidades = {'calor':'kW', 'temperatura':'°C'}
        
    def calcular_carga_termica(self, T1: float = None, T2: float = None) -> float: # type: ignore
        """Calcula a carga térmica necessária para levar a corrente de T1 para T2.
        
        Utiliza a capacidade térmica em fluxo (WCp) para determinar a quantidade
        de energia térmica necessária para a mudança de temperatura especificada.
        
        Parameters
        ----------
        T1 : float, optional
            Temperatura inicial em °C. O padrão é a To da corrente.
        T2 : float, optional
            Temperatura final em °C. O padrão é a Td da corrente.
        
        Returns
        -------
        float
            Carga térmica (Q) em kW entre as temperaturas T1 e T2.
            Calculada como Q = WCp × (T2 - T1).
        
        Examples
        --------
        >>> corrente = Corrente(WCp=50, To=100, Td=150)
        >>> corrente.calcular_carga_termica(100, 150)
        2500.0
        >>> corrente.calcular_carga_termica(150, 100)
        -2500.0
        """
        if not T1:
            T1 = self.To
        if not T2:
            T2 = self.Td
        return self.WCp * (T2 - T1)
    
    def atualizar_corrente(self, WCp: float | None = None, To: float | None = None, Td: float | None = None) -> None:
        """Atualiza os parâmetros da corrente térmica.
        
        Permite modificar um ou mais parâmetros da corrente (WCp, To, Td)
        e recalcula automaticamente a carga térmica (Q) com base nos novos valores.
        
        Parameters
        ----------
        WCp : float, optional
            Novo valor de capacidade térmica em fluxo em kW/°C.
            Se None, o valor atual é mantido.
        To : float, optional
            Nova temperatura inicial em °C.
            Se None, o valor atual é mantido.
        Td : float, optional
            Nova temperatura final em °C.
            Se None, o valor atual é mantido.
        
        Examples
        --------
        >>> corrente = Corrente(WCp=100, To=20, Td=80)
        >>> corrente.Q
        6000.0
        >>> corrente.atualizar_corrente(To=30, Td=90)
        >>> corrente.Q
        6000.0
        """
        if WCp:
            self.WCp = WCp
        if To:
            self.To = To
        if Td:
            self.Td = Td
        self.Q = self.calcular_carga_termica(self.To, self.Td)
    
    def calcular_nova_temperatura(self, Q: float):
        if self.quente:
            self.atualizar_corrente(Td = self.To - Q/self.WCp)
        else:
            self.atualizar_corrente(Td = self.To + Q/self.WCp)
    
    def copy(self) -> "Corrente":
        """Cria uma cópia profunda (deep copy) da corrente atual.
        
        Retorna uma nova instância independente com os mesmos parâmetros
        térmicos e unidades da corrente original.
        
        Returns
        -------
        Corrente
            Uma nova instância de Corrente com os mesmos valores de WCp, To, Td e unidades.
        
        Examples
        --------
        >>> corrente_original = Corrente(WCp=100, To=20, Td=80)
        >>> corrente_copia = corrente_original.copy()
        >>> corrente_copia.WCp = 200
        >>> corrente_original.WCp, corrente_copia.WCp
        (100, 200)
        """
        c = Corrente(self.WCp, self.To, self.Td, self.unidades)
        c.quente = self.quente
        return c
    
    def __iter__(self):
        """Permite iterar sobre os atributos principais da corrente.
        
        Habilita desempacotamento direto dos parâmetros térmicos da corrente.
        
        Yields:
            float: WCp (capacidade térmica em fluxo)
            float: To (temperatura inicial)
            float: Td (temperatura final)
            
        Examples
        --------
            >>> corrente = Corrente(WCp=100, To=20, Td=80)
            >>> WCp, To, Td = corrente
            >>> WCp, To, Td
            (100, 20, 80)
        """
        yield self.WCp
        yield self.To
        yield self.Td
    
    def __contains__(self, item:tuple|list):
        """Verifica se a corrente está contida dentro de um intervalo de temperatura.
        
        Determina se a corrente térmica pode ser integrada dentro de um intervalo
        de temperatura, considerando sua classificação (quente ou fria).
        Útil para análises de pinch point e possibilidades de integração energética.
        
        Parameters
        ----------
        item : tuple or list
            Intervalo de temperatura [T_max, T_min] em °C a ser verificado.
            Deve conter exatamente 2 elementos numéricos com T_min < T_max.
            
        Returns
        -------
        bool
            True se a corrente está totalmente contida no intervalo, False caso contrário.
            - Correntes quentes (Q ≤ 0): To >= T_max AND Td <= T_min
            - Correntes frias (Q > 0): Td >= T_max AND To <= T_min
        
        Raises:
            TypeError: Se o argumento não for uma tupla ou lista.
            
        Examples
        --------
        Corrente quente entre 150°C e 50°C:
            >>> corrente = Corrente(WCp=100, To=150, Td=50)  # Corrente quente
            >>> (140, 60) in corrente  # Intervalo contido na corrente
            True
            >>> (150, 100) in corrente  # Intervalo contido na corrente
            True
            >>> (160, 40) in corrente  # Intervalo não contido na corrente
            False
            
        Corrente fria entre 30°C e 100°C:
            >>> corrente = Corrente(WCp=100, To=30, Td=100)  # Corrente fria
            >>> (100, 40) in corrente  # Intervalo contido na corrente
            True
            >>> (80, 50) in corrente  # Intervalo contido na corrente
            True
            >>> (100, 20) in corrente  # Intervalo não contido na corrente
            False
        """
        if isinstance(item, (tuple, list)):
            if self.quente:
                return (self.To >= item[0]) and (self.Td <= item[1])
            else:
                return (self.Td >= item[0]) and (self.To <= item[1])
        else:
            raise TypeError(f"O argumento deve ser uma tupla ou lista de tamanho 2, não {type(item).__name__}")
    
    def __repr__(self):
        """Retorna uma representação formatada da corrente.
        
        Fornece uma representação em string legível com todos os parâmetros
        principais da corrente e suas respectivas unidades.
        
        Returns
        -------
        str
            String formatada contendo:
            - Tipo de corrente: 'quente' ou 'fria'
            - WCp: Capacidade térmica em fluxo com unidade
            - To: Temperatura de origem com unidade
            - Td: Temperatura de destino com unidade
            - Q: Carga térmica com unidade
        
        Examples
        --------
        >>> corrente = Corrente(WCp=2, To=250, Td=140)
        >>> print(corrente)
            Corrente quente: WCp = 2, To = 250, Td = 140
        """    
        u_WCp = self.unidades['calor']+'/'+self.unidades['temperatura']
        u_T = self.unidades['temperatura']
        u_Q = self.unidades['calor']
        return f"Corrente {'quente' if self.quente else 'fria'}: " + \
            f"WCp = {self.WCp:.2f} {u_WCp}, To = {self.To:.2f} {u_T}, Td = {self.Td:.2f} {u_T}, Q = {self.Q:.2f} {u_Q}"


class ListaCorrentes(list):
    """Container especializado para gerenciar coleções de correntes térmicas.
    
    Herda de `list` e fornece funcionalidades adicionais específicas para trabalhar
    com múltiplas correntes de processo. Facilita operações em lote, cópia profunda
    e representação formatada de listas de correntes para análise de integração energética.
    
    Esta classe é ideal para manipular conjuntos de correntes quentes e frias em
    análises de pinch point e síntese de redes de trocadores de calor.
    
    Attributes
    ----------
    Herda todos os atributos e métodos de `list`.
    
    Examples
    --------
    Criar uma lista de correntes:
    
    >>> corrente1 = Corrente(WCp=100, To=20, Td=80)
    >>> corrente2 = Corrente(WCp=150, To=200, Td=50)
    >>> lista = ListaCorrentes([corrente1, corrente2])
    >>> len(lista)
    2
    
    Concatenar listas de correntes:
    
    >>> lista1 = ListaCorrentes([corrente1])
    >>> lista2 = ListaCorrentes([corrente2])
    >>> lista_combinada = lista1 + lista2
    >>> len(lista_combinada)
    2
    >>> type(lista_combinada)
    <class '__main__.ListaCorrentes'>
    """
    def __init__(self, *correntes):
        if len(correntes) == 1:
            correntes = correntes[0]
        super().__init__(correntes)
        for corrente in self:
            corrente.idx = self.index(corrente)
    
    def copy(self) -> "ListaCorrentes":
        """Cria uma cópia rasa da lista, sem criar novas instâncias das correntes na lista.
        
        Retorna uma nova instância de ListaCorrentes. Modificações nas cópias podem 
        afetar a lista original.
        
        Returns
        -------
        ListaCorrentes
            Nova instância da lista.
        
        Examples
        --------
        >>> original = ListaCorrentes([Corrente(100, 20, 80)])
        >>> copia = original.copy()
        >>> copia[0] = 1
        >>> original, copia
        ([Corrente(100, 20, 80)], [1])
        
        >>> copia = original.copy()
        >>> copia[0].WCp = 200
        >>> original[0].WCp, copia[0].WCp
        (200, 200)
        """
        return ListaCorrentes(self)
    
    def deepcopy(self) -> "ListaCorrentes":
        """Cria uma cópia profunda (deep copy) de todas as correntes na lista.
        
        Retorna uma nova instância de ListaCorrentes com cópias independentes
        de cada corrente, garantindo que modificações nas cópias não afetam
        a lista original.
        
        Returns
        -------
        ListaCorrentes
            Nova instância contendo cópias de todas as correntes.
        
        Examples
        --------
        >>> original = ListaCorrentes([Corrente(100, 20, 80)])
        >>> copia = original.deepcopy()
        >>> copia[0].WCp = 200
        >>> original[0].WCp, copia[0].WCp
        (100, 200)
        """
        return ListaCorrentes(map(lambda corrente: corrente.copy(), self)) # type: ignore
    
    def __repr__(self) -> str:
        """Retorna uma representação formatada de todas as correntes.
        
        Gera uma string com cada corrente em uma linha separada, facilitando
        a visualização e análise de múltiplas correntes simultaneamente.
        
        Returns
        -------
        str
            String com cada corrente formatada em uma linha separada.
        
        Examples
        --------
        >>> lista = ListaCorrentes([
        ...     Corrente(WCp=100, To=20, Td=80),
        ...     Corrente(WCp=150, To=200, Td=50)
        ... ])
        >>> print(lista)
        Corrente fria: WCp = 100.00 kW/°C, To = 20.00 °C, Td = 80.00 °C, Q = 6000.00 kW
        Corrente quente: WCp = 150.00 kW/°C, To = 200.00 °C, Td = 50.00 °C, Q = -22500.00 kW
        """
        return "\n".join(str(corrente) for corrente in self)
        
    def __add__(self, other: "ListaCorrentes") -> "ListaCorrentes": # type: ignore
        """Concatena duas listas de correntes, retornando uma nova ListaCorrentes.
        
        Permite usar o operador `+` para combinar duas listas de correntes,
        preservando o tipo ListaCorrentes no resultado (diferente de `list`
        que retornaria uma `list` comum).
        
        Parameters
        ----------
        other : ListaCorrentes or list
            Outra lista de correntes ou lista comum a ser concatenada.
        
        Returns
        -------
        ListaCorrentes
            Nova ListaCorrentes contendo todas as correntes das duas listas.
        
        Examples
        --------
        >>> lista1 = ListaCorrentes([Corrente(100, 20, 80)])
        >>> lista2 = ListaCorrentes([Corrente(150, 200, 50)])
        >>> lista_total = lista1 + lista2
        >>> len(lista_total)
        2
        >>> type(lista_total)
        <class '__main__.ListaCorrentes'>
        
        Notes
        -----
        O resultado sempre é uma ListaCorrentes, preservando funcionalidades
        especializadas mesmo ao concatenar com listas comuns.
        """
        return ListaCorrentes(list.__add__(self, other))