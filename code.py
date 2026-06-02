class Atividade:
    def __init__(self, codigo: str, nome: str, inicio: float, fim: float, prioridade: int, participantes: int):
        self.codigo = codigo
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.prioridade = prioridade
        self.participantes = participantes

        def duracao(self) -> float:
            return self.fim - self.inicio
        
        def conflita_com(self, outra: "Atividade") -> bool:
            return self.inicio < outra.fim and outra.inicio < self.fim
        
        def __str__(self):
            h_ini = f"{int(self.inicio):02d}h{int((self.inicio % 1) * 60):02d}"
            h_fim = f"{int(self.fim):02d}h{int((self.fim % 1) * 60):02d}"
            return (f"[{self.codigo}] {self.nome:<30s} "
                    f"{h_ini}-{h_fim}  prio={self.prioridade}  part={self.participantes}")
        

#
# MERGE SORT
#

def merge_sort(lista: list[Atividade], chave: str = "fim") -> list[Atividade]:
    """
    Ordena uma lista de atividades usando Merge Sort.
    Complexidade: O(n log n)
    """

    if len(lista) <= 1:
        return lista[:]
    
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)
    return _merge(esquerda, direita, chave)

def _merge(esq: list[Atividade], dir: list[Atividade], chave: str) -> list[Atividade]:
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        val_e = getattr(esq[i], chave)
        val_d = getattr(dir[j], chave)
        if val_e <= val_d:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1

    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado

#
# ALGORITMO GULOSO
#  

