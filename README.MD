# Projeto Integrador - Sistema de Agendamento de Atividades

## 1. Descrição da Solução
Este projeto implementa um sistema de agendamento de atividades corporativas (treinamentos, palestras e reuniões) focado na resolução de conflitos de horário. O objetivo central do sistema é analisar uma lista de eventos com horários sobrepostos e selecionar o conjunto ideal de atividades que podem ser realizadas sem conflito. O sistema permite a organização das atividades, buscas por termos específicos e a análise comparativa de desempenho entre diferentes estratégias de resolução computacional.

## 2. Algoritmos Utilizados
O sistema foi desenvolvido em Python e faz uso de três abordagens algorítmicas principais:

* **Merge Sort:** Algoritmo de ordenação baseado na estratégia de "divisão e conquista", utilizado obrigatoriamente para organizar as atividades com base em seus horários de término ou início antes de passarem pela seleção. Possui complexidade $O(n \log n)$.
* **Algoritmo Guloso (Greedy):** Seleciona as atividades priorizando sempre aquela que termina mais cedo, garantindo que o recurso (sala/horário) seja liberado o mais rápido possível. Essa estratégia foca em maximizar a **quantidade** de atividades agendadas no dia.
* **Programação Dinâmica:** Técnica adicional que avalia o cenário global dividindo-o em subproblemas (neste caso, ignorar ou incluir uma atividade verificando o último evento compatível). Diferente da solução gulosa, a Programação Dinâmica busca maximizar o **benefício total** (peso), priorizando o preenchimento da agenda com as atividades que possuam o maior número de participantes.

## 3. Comparação entre as Abordagens Implementadas
Os algoritmos foram testados em três cenários com volumes diferentes de dados: Pequeno, Médio e Maior. 

| Cenário | Métrica | Algoritmo Guloso | Programação Dinâmica |
| :--- | :--- | :--- | :--- |
| **Teste 1 - Pequeno (6 ativ.)** | Atividades Selecionadas | 3 | 3 |
| | Benefício (Participantes) | N/A | 80 |
| | Tempo de Execução | 0.0440 ms | 0.0503 ms |
| **Teste 2 - Médio (12 ativ.)** | Atividades Selecionadas | 5 | 5 |
| | Benefício (Participantes) | N/A | 130 |
| | Tempo de Execução | 0.0608 ms | 0.0380 ms |
| **Teste 3 - Maior (34 ativ.)** | Atividades Selecionadas | 4 | 4 |
| | Benefício (Participantes) | N/A | 274 |
| | Tempo de Execução | 0.0837 ms | 0.1108 ms |

**Análise:** Ambos os algoritmos conseguiram agendar um número similar de eventos na maioria dos cenários (como visto no Teste 3, onde ambos selecionaram 4 atividades). A Programação Dinâmica apresentou um tempo de execução que pode ser ligeiramente superior ao Guloso (ex: 0.1108 ms vs 0.0837 ms no Teste 3), o que é esperado devido à etapa adicional de construção da tabela de memoização. Em contrapartida, a Programação Dinâmica provou-se altamente eficaz na sua proposta de maximizar o peso, conseguindo encontrar uma combinação de horários diferente que totalizou 274 participantes no cenário de estresse, cumprindo o objetivo de otimizar o benefício.

## 4. Exemplos de Entradas e Saídas
Abaixo estão exemplos reais do processamento do sistema para o **Teste 2 - Médio**.

**Entrada (Algumas das atividades disponíveis e desordenadas):**
* `[A1] Reunião de Alinhamento (08h00-09h30)`
* `[A4] Workshop de Python (11h30-13h30)`
* `[A9] Palestra sobre IA (13h30-15h00)`
* `[A10] Feedback Individual (15h30-16h30)`
* `[A11] Planejamento Estratégico (16h00-18h00)`
* `[A12] Workshop de Design (09h30-11h30)`

**Saída 1 - Algoritmo Guloso (Foco em mais atividades):**
Nesta execução, o algoritmo encontrou a seguinte grade priorizando o término mais cedo:
1. `-> [A1] Reunião de Alinhamento      08h00-09h30  prio=3  part=10`
2. `-> [A12] Workshop de Design         09h30-11h30  prio=3  part=22`
3. `-> [A4] Workshop de Python          11h30-13h30  prio=4  part=30`
4. `-> [A9] Palestra sobre IA           13h30-15h00  prio=5  part=60`
5. `-> [A10] Feedback Individual        15h30-16h30  prio=1  part=2`

**Saída 2 - Programação Dinâmica (Foco em Participantes):**
Nesta execução, o algoritmo também selecionou 5 atividades, mas trocou a última opção para maximizar o número de participantes (totalizando 130 pessoas):
1. `-> [A1] Reunião de Alinhamento      08h00-09h30  prio=3  part=10`
2. `-> [A12] Workshop de Design         09h30-11h30  prio=3  part=22`
3. `-> [A4] Workshop de Python          11h30-13h30  prio=4  part=30`
4. `-> [A9] Palestra sobre IA           13h30-15h00  prio=5  part=60`
5. `-> [A11] Planejamento Estratégico   16h00-18h00  prio=5  part=8`