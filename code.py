import time


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

def algoritmo_guloso(atividades: list[Atividade]) -> tuple[list[Atividade], float]:
    """
    Seleciona atividades priorizando o término mais cedo.
    Retorna uma tupla com a lista de atividades selecionadas e a duração total. 
    """

    if not atividades:
        return [], 0.0
    
    # Ordenação
    atividades_ordenadas = merge_sort(atividades, chave="fim")

    # Seleção
    selecionadas = [atividades_ordenadas[0]]
    ultima_selecionada = atividades_ordenadas[0]

    # acumulador
    duracao_total = ultima_selecionada.duracao()

    # iteração gulosa
    for i in range(1, len(atividades_ordenadas)):
        atividade_atual = atividades_ordenadas[i]

        if atividade_atual.inicio >= ultima_selecionada.fim:
            selecionadas.append(atividade_atual)
            duracao_total += atividade_atual.duracao()
            ultima_selecionada = atividade_atual

        return selecionadas, duracao_total
    
#
# PROGRAMAÇÃO DINÂMICA 
#

def _peso(atividade: Atividade, metrica: str) -> int:
    """Retorna o peso da atividade baseado na métrica escolhida."""
    if metrica == "prioridade":
        return atividade.prioridade
    elif metrica == "participantes":
        return atividade.participantes
    else:
        return atividade.prioridade * atividade.participantes


def _ultimo_compativel(atividades_ordenadas: list[Atividade], idx: int) -> int:
    """
    Busca binária para encontrar o índice da última atividade que não conflita com a atividade no índice 'idx'.
    complexidade: O(log n)
    """

    lo, hi = 0, idx - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if atividades_ordenadas[mid].fim <= atividades_ordenadas[idx].inicio:
            # verifica se o próximo elemento também termina antes de idx começar
            # se sim, continua buscando à direita
            if atividades_ordenadas[mid+1].fim <= atividades_ordenadas[idx].inicio:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1

def programacao_dinamica(atividades: list[Atividade], metrica: str = "participantes") -> tuple[list[Atividade], int, float]:
    """
    algoritmo de programação dinâmica para seleção de atividades.
    Maxima o benefício total (soma dos pesos) sem gerar conflito de horários
    
    retorna:
    - lista de atividades selecionadas
    - benefício total: soma da métrica escolhida(ex: total de participantes)
    - tempo_ms: tempo gasto para execução do algoritmo em milissegundos
    """

    t0 = time.perf_counter()

    if not atividades:
        return [], 0, 0.0
    
    # Ordenação por mergesort
    atividades_ordenadas = merge_sort(atividades, chave="fim")
    n = len(atividades_ordenadas)
    pesos = [_peso(j, metrica) for j in atividades_ordenadas]

    # dp[i] armazenará o benefício máximo considerando as primeiras 'i' atividades.
    # O array tem tamanho n + 1 (1-based index) para facilitar a matemática.
    dp = [0] * (n + 1)

    #preenchimento da tabela dp
    for i in range(1, n + 1):
        lc = _ultimo_compativel(atividades_ordenadas, i - 1)

        # benefício incluindo a atividade atual
        incluir = pesos[i - 1] + (dp[lc + 1] if lc >= 0 else 0)

        # o valor na posição i será o máximo entre ignorar a atividade atual ou incluir
        dp[i] = max(dp[i - 1], incluir)

    # Reconstrução: descobrir quais atividades formaram o valor máximo
    selecionadas = []
    i = n
    while i >= 1:
        # Se dp[i] é igual a dp[i-1], significa que o valor máximo veio de ignorar a atividade atual
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            # Se for diferente, a atividade atual (i-1) faz parte da solução ótima
            selecionadas.append(atividades_ordenadas[i - 1])
            lc = _ultimo_compativel(atividades_ordenadas, i - 1)
            i = lc + 1 if lc >= 0 else 0

        # Invertemos a lista porque o rastreamento foi feito de trás para frente
        selecionadas.reverse()

        beneficio_total = dp[n]
        tempo_execucao_ms = (time.perf_counter() - t0) * 1000

        return selecionadas, beneficio_total, tempo_execucao_ms