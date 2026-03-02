from EngenhariaProcessos.corrente import Corrente, ListaCorrentes
from EngenhariaProcessos.integracaoEnergetica.troca_termica import TrocaTermica
from typing import Callable


class AlgoritmoBase:
    """Base para algoritmos de síntese de redes de trocadores de calor.

    Esta classe implementa a lógica comum a diferentes estratégias de matching
    entre correntes quentes e frias, com cálculo automático de temperaturas
    e verificação de viabilidade termodinâmica.

    Attributes:
        dT_min (float): Diferença mínima de temperatura permitida entre pares
            de correntes (°C).
        correntes_quentes (ListaCorrentes): Cópia das correntes quentes do
            processo.
        correntes_frias (ListaCorrentes): Cópia das correntes frias do
            processo.
        integracoes (list): Lista de trocas de calor realizadas
            (objetos TrocaTermica).
        tabelas (list): Histórico de estados do sistema a cada iteração.
        utilidades (list): Cargas de utilidades (resfriamento/aquecimento)
            necessárias."""
    def __init__(self, correntes:ListaCorrentes, criterios_selecao:tuple[Callable,Callable], dT_min:float=10) -> None:
        self.dT_min = dT_min
        self.integracoes = []
        self.tabelas = []
        self.utilidades = []
        self.contador_trocas = 0
        self.criterio_quente = criterios_selecao[0]
        self.criterio_fria = criterios_selecao[1]
        ## Separar correntes em frias e quentes, criando novas instâncias de 'Corrente' ao fazê-lo:
        self.correntes_quentes = ListaCorrentes(
            map(lambda corrente: corrente.copy(), filter(lambda corrente: corrente.quente==True, correntes))) # type: ignore
        self.correntes_frias = ListaCorrentes(
            map(lambda corrente: corrente.copy(), filter(lambda corrente: corrente.quente==False, correntes))) # type: ignore
        self.correntes = self.correntes_frias + self.correntes_quentes
        self.trocas_por_corrente = {corrente:[] for corrente in self.correntes}
    
    def verificar_trocas_viaveis(self) -> None:
        ## Filtrar correntes já esgotadas:
        self.quentes_validas = list(filter(lambda corrente: corrente.Q!=0, self.correntes_quentes))
        self.frias_validas = list(filter(lambda corrente: corrente.Q!=0, self.correntes_frias))
        ## Verificar trocas viáveis:
        if self.quentes_validas and self.frias_validas: 
            self.trocas_viaveis = max(self.quentes_validas, key=lambda x: x.To).To > min(self.frias_validas, key=lambda x: x.To).To
        else:
            self.trocas_viaveis = False
        
    def inserir_aquecedor(self, num_troca, corrente, num_corrente):
        ...

    def selecionar_correntes(self) -> tuple[tuple[Corrente, int], ...]: ## GENERALIZAR MÉTODO
        correntes_quentes_possiveis = self.quentes_validas.copy() #shallow copy
        while len(correntes_quentes_possiveis) > 0:
            CQ = self.criterio_quente(correntes_quentes_possiveis)
            
            ## Verifica se é físicamente possível realizar a troca, e se ela já não foi feita:
            correntes_frias_possiveis = []
            for corrente in self.frias_validas:
                if (corrente.To < CQ.To) and (corrente not in self.trocas_por_corrente[CQ]):
                    correntes_frias_possiveis.append(corrente)
                    
            ## Se não houver como trocar mais com essa corrente quente, passa para a próxima:
            if len(correntes_frias_possiveis) == 0:
                correntes_quentes_possiveis.remove(CQ)
                continue
            
            ## Se for possível, seleciona a FTO e salva essa troca QTOxFTO
            else:
                CF = self.criterio_fria(correntes_frias_possiveis)
                self.trocas_por_corrente[CQ].append(CF)
                break
        else:
            return (0,0),(0,0) # type: ignore
    
        return (CQ, self.correntes_quentes.index(CQ)+1), (CF, self.correntes_frias.index(CF)+1)
    
    def atualizar_temperaturas(self, CQ, CF, TEQ, TSQ, TEF, TSF) -> None:
        ...
    
    def aplicar_algoritmo(self) -> tuple[ list[TrocaTermica], list[tuple[int, ListaCorrentes]], list[tuple[str, int, int]] ]:
        self.contador_trocas = 0
        self.tabelas.append((self.contador_trocas, self.correntes.deepcopy()))
        # print(0, self.correntes, sep="\n")
        while self.trocas_viaveis:       
            aquecedor = False
            (CQ, nQ), (CF, nF) = self.selecionar_correntes()
            if CQ == 0:
                break
            ## Fixa temperaturas de entrada quente e fria, e define como metas provisórias as temperaturas de
            ## saída quente e fria.
            TEQ, TEF, TSQ, TSF = CQ.To, CF.To, CQ.Td, CF.Td
            ## Corrigir temperaturas de saída se necessário, para respeitar o dT_minimo:
            if TEQ - TSF < self.dT_min:
                TSF = TEQ - self.dT_min
                aquecedor = True
                # self.inserir_aquecedor(self.contador_trocas, TSF, CF.Td)
            if TSQ - TEF < self.dT_min:
                TSQ = TEF + self.dT_min
            ## Cálculo de carga térmica disponível para troca:
            self.oferta = abs(CQ.calcular_carga_termica(TEQ, TSQ))
            self.demanda = abs(CF.calcular_carga_termica(TEF, TSF))
            ## Atualizando correntes com os valores recalculados
            self.atualizar_temperaturas(CQ, CF, TEQ, TSQ, TEF, TSF)            
            ## Salvando iteração atual:
            self.contador_trocas+=1
            if aquecedor:
                self.inserir_aquecedor(self.contador_trocas, CF, nF)
            self.tabelas.append((self.contador_trocas, self.correntes.deepcopy()))
            self.integracoes.append(TrocaTermica(self.contador_trocas, CQ, CF, nQ, nF))
            ## Verificar validade da próxima iteração
            self.verificar_trocas_viaveis()
            # print(contador, self.correntes, sep="\n")
            
        ## Trocadores necessários
        for corrente in self.frias_validas:
            nF = self.correntes_frias.index(corrente)
            self.utilidades.append((f"Aquecimento necessário ({corrente.tipo}{nF+1})", corrente.To, corrente.Td))
        for corrente in self.quentes_validas:
            nQ = self.correntes_quentes.index(corrente)
            self.utilidades.append((f"Resfriamento necessário ({corrente.tipo}{nQ+1})", corrente.To, corrente.Td))
        
        return self.integracoes, self.tabelas, self.utilidades

    def __call__(self) -> tuple[ list[TrocaTermica], list[tuple[int, ListaCorrentes]], list[tuple[str, int, int]] ]:
        self.verificar_trocas_viaveis()
        if not self.trocas_viaveis:
            return [], [(0, self.correntes)], []# type: ignore
        return self.aplicar_algoritmo()


class RPS(AlgoritmoBase):
    def __init__(self, correntes: ListaCorrentes, criterio: str = 'maior', dT_min: float = 10) -> None:
        if criterio == 'maior': #QMTO x FMTO
            funcao_selecao = lambda y: max(y, key=lambda x: x.To)
        elif criterio == 'menor': #QmTO x FmTO
            funcao_selecao = lambda y: min(y, key=lambda x: x.To)
        else: 
            raise ValueError("O critério de escolha de correntes deve ser 'maior' ou 'menor'.\n")
        super().__init__(correntes, (funcao_selecao, funcao_selecao), dT_min)

    def atualizar_temperaturas(self, CQ, CF, TEQ, TSQ, TEF, TSF):
        if self.oferta <= self.demanda:
            nova_TSQ = TSQ
            nova_TSF = TEF + self.oferta/CF.WCp
        else:
            nova_TSF = TSF
            nova_TSQ = TEQ - self.demanda/CQ.WCp
        CF.atualizar_corrente(To=nova_TSF)
        CQ.atualizar_corrente(To=nova_TSQ)


class PD(AlgoritmoBase):
    def __init__(self, correntes: ListaCorrentes, dT_min: float = 10) -> None:
        super().__init__(correntes, (lambda y: max(y, key=lambda x: x.To), lambda y: max(y, key=lambda x: x.Td)), dT_min)
        
    def inserir_aquecedor(self, num_troca, corrente, num_corrente):
        self.integracoes.append((num_troca, f"Aquecedor em {corrente.tipo}{num_corrente}"))
    
    def atualizar_temperaturas(self, CQ, CF, TEQ, TSQ, TEF, TSF):
        if self.oferta <= self.demanda:
            nova_TSQ = TSQ
            nova_TEF = TSF - self.oferta/CF.WCp
            if nova_TEF > TSQ:
                nova_TSQ = (CQ.WCp*TEQ - CF.WCp*(TSF + self.dT_min))/(CQ.WCp - CF.WCp)
                nova_TEF = nova_TSQ - self.dT_min
        else:
            nova_TEF = TEF
            nova_TSQ = TEQ - self.demanda/CQ.WCp
        CF.atualizar_corrente(Td=nova_TEF)
        CQ.atualizar_corrente(To=nova_TSQ)
        

class Pinch(AlgoritmoBase):
    ...