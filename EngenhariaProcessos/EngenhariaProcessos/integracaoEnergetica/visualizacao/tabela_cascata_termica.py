class TabelaCascataTermica(list):
    """Tabela formatada de saldos da cascata térmica.

    Herda de ``list`` e fornece formatação visual para exibir intervalos,
    resíduos, ofertas, demandas e saldos de forma legível.

    Attributes:
        headers (list): Lista de nomes das colunas.
        larguras (list): Largura de cada coluna para alinhamento.
        str_header (str): String formatada do cabeçalho.
    """

    def __init__(self):
        # Cabeçalho alinhado à direita
        self.headers = ["Intervalo", "Residuo", "Oferta", "Demanda", "Saldo"]
        self.larguras = list(map(len, self.headers))
        self.str_header = " " + "  ".join(f"{h:>{w}}" for h, w in zip(self.headers, self.larguras)) + "\n"
        # self.str_header += "\n " + "-"*(2*len(self.headers)+sum(self.larguras))         
    
    def __repr__(self) -> str:
        # Linhas alinhadas à direita
        self.linhas = []
        for sublista in self:
            linha = " " + "  ".join(f"{v:>{w}.2f}" if isinstance(v, float) else f"{v:>{w}}" for v, w in zip(sublista, self.larguras))
            self.linhas.append(linha)
        # Centralizar cada linha em relação ao comprimento total
        # largura_total = sum(larguras) + (len(larguras) - 1)  # espaços
        # linhas_centralizadas = [l.center(largura_total) for l in linhas]
        return self.str_header + "\n".join(self.linhas)