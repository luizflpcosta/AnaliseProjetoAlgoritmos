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

# ==========================================
# GERAÇÃO DE TESTES E MÓDULOS DO SISTEMA
# ==========================================

def gerar_testes():
    """Gera os 3 conjuntos de testes obrigatórios do projeto."""
    
    # Teste 1 - Pequeno (5 a 8 atividades)
    teste1 = [
        Atividade("A1", "Reunião de Alinhamento", 8.0, 9.5, 3, 10),
        Atividade("A2", "Treinamento de Vendas", 9.0, 11.0, 2, 25),
        Atividade("A3", "Palestra de Inovação", 10.0, 12.0, 5, 50),
        Atividade("A4", "Workshop de Python", 11.5, 13.5, 4, 30),
        Atividade("A5", "Apresentação de Resultados", 13.0, 14.5, 5, 15),
        Atividade("A6", "Dinâmica de Grupo", 14.0, 16.0, 2, 20),
    ]

    # Teste 2 - Médio (10 a 20 atividades)
    teste2 = teste1 + [
        Atividade("A7", "Reunião de Marketing", 8.5, 10.5, 4, 12),
        Atividade("A8", "Treinamento de Liderança", 10.5, 12.5, 3, 18),
        Atividade("A9", "Palestra sobre IA", 13.5, 15.0, 5, 60),
        Atividade("A10", "Feedback Individual", 15.5, 16.5, 1, 2),
        Atividade("A11", "Planejamento Estratégico", 16.0, 18.0, 5, 8),
        Atividade("A12", "Workshop de Design", 9.5, 11.5, 3, 22),
    ]

    # Teste 3 - Maior (Mais de 30 atividades) - Gerado dinamicamente para facilitar
    import random
    teste3 = []
    for i in range(1, 35):
        inicio = round(random.uniform(8.0, 16.0), 1)
        duracao = round(random.uniform(1.0, 3.0), 1)
        teste3.append(Atividade(
            f"B{i}", 
            f"Atividade Extra {i}", 
            inicio, 
            inicio + duracao, 
            random.randint(1, 5), 
            random.randint(5, 100)
        ))

    return teste1, teste2, teste3


def buscar_atividade(atividades: list[Atividade], termo: str):
    """Realiza a busca de atividades por código ou nome."""
    resultados = [a for a in atividades if termo.lower() in a.codigo.lower() or termo.lower() in a.nome.lower()]
    if resultados:
        print(f"\n--- Resultados da Busca para '{termo}' ---")
        for a in resultados:
            print(a)
    else:
        print("\nNenhuma atividade encontrada.")


def comparar_solucoes(atividades: list[Atividade], nome_teste: str):
    """
    Executa ambos os algoritmos e compara o desempenho e os resultados obtidos.
    """
    print(f"\n{'='*50}")
    print(f" COMPARAÇÃO DE DESEMPENHO: {nome_teste.upper()} ({len(atividades)} atividades)")
    print(f"{'='*50}")

    # --- Execução Gulosa ---
    t0_guloso = time.perf_counter()
    sel_guloso, dur_guloso = algoritmo_guloso(atividades)
    tempo_guloso_ms = (time.perf_counter() - t0_guloso) * 1000
    
    # --- Execução Programação Dinâmica ---
    sel_dp, ben_dp, tempo_dp_ms = programacao_dinamica(atividades, metrica="participantes")

    print("\n[ ALGORITMO GULOSO (Foco em mais atividades) ]")
    print(f"Atividades Selecionadas : {len(sel_guloso)}")
    print(f"Tempo de Execução       : {tempo_guloso_ms:.4f} ms")
    print("Grade de Horários:")
    for a in sel_guloso: print(f"  -> {a}")

    print("\n[ PROGRAMAÇÃO DINÂMICA (Foco em Participantes) ]")
    print(f"Atividades Selecionadas : {len(sel_dp)}")
    print(f"Participantes Atingidos : {ben_dp}")
    print(f"Tempo de Execução       : {tempo_dp_ms:.4f} ms")
    print("Grade de Horários:")
    for a in sel_dp: print(f"  -> {a}")


def menu_principal():
    """Interface principal para demonstração do sistema."""
    t1, t2, t3 = gerar_testes()
    
    while True:
        print("\n" + "="*40)
        print(" SISTEMA DE AGENDAMENTO DE ATIVIDADES")
        print("="*40)
        print("1. Organizar e visualizar atividades (Merge Sort)")
        print("2. Buscar atividade específica")
        print("3. Executar e comparar Teste 1 (Pequeno)")
        print("4. Executar e comparar Teste 2 (Médio)")
        print("5. Executar e comparar Teste 3 (Maior)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\nAtividades do Teste 2 ordenadas por Início:")
            ordenadas = merge_sort(t2, chave="inicio")
            for a in ordenadas: print(a)
            
        elif opcao == "2":
            termo = input("Digite o código ou nome da atividade: ")
            buscar_atividade(t2, termo) # Usando o dataset médio como base de busca
            
        elif opcao == "3":
            comparar_solucoes(t1, "Teste 1 - Pequeno")
            
        elif opcao == "4":
            comparar_solucoes(t2, "Teste 2 - Médio")
            
        elif opcao == "5":
            comparar_solucoes(t3, "Teste 3 - Maior")
            
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()