"""
Módulo Problem: Definição formal do problema para busca de caminho em grade.

Este módulo define a classe Problem, que encapsula a formulação do problema de busca
para busca de caminho em grade 2D. Implementa a interface clássica de definição de problema de IA:
- actions(state): retorna movimentos válidos de um state
- result(state, action): retorna o novo state após aplicar uma ação
- step_cost(state, action): retorna o custo dessa transição
- is_goal(state): verifica se um state é o objetivo

A classe Problem atua como intermediária entre a estrutura de dados Grid
e os algoritmos de busca (BFS, Guloso, A*). Ela impõe as regras de movimento válido:
- Não pode mover para obstáculos
- Não pode mover fora dos limites da grade
- Pode opcionalmente evitar células inimigo (resolução em duas passagens)

O movimento é restrito a movimentos 4-direcionais (cardinais): cima, baixo, esquerda, direita.
Movimento diagonal não é permitido.
"""

from model.state import State
from model.grid import Grid, ENEMY

# Ações de movimento 4-direcional como (delta_linha, delta_coluna)
# Usadas para explorar vizinhos em direções cardinais: cima, baixo, esquerda, direita
# Movimento diagonal NÃO está incluído neste sistema
ACTIONS = [
    (-1, 0),  # cima: diminui linha
    (1, 0),   # baixo: aumenta linha
    (0, -1),  # esquerda: diminui coluna
    (0, 1),   # direita: aumenta coluna
]


class Problem:
    """Definição formal do problema para busca de caminho em grade 2D.

    Encapsula a formulação completa do problema: a grade, state inicial,
    state de objetivo e as regras para ações válidas e custos de movimento.

    Implementa a interface clássica de problema de busca de IA com métodos que
    definem o espaço de estado do problema e dinâmica de transição:
    - actions(state): expande um state retornando todos os movimentos vizinhos válidos
    - result(state, action): calcula o state resultante após uma ação
    - step_cost(state, action): obtém o custo de mover para um vizinho
    - is_goal(state): testa se um state é o objetivo

    Características principais:
    - Impõe limites da grade e evitação de obstáculos
    - Suporta evitação opcional de inimigos (pode ser alternado para resolução em duas passagens)
    - Movimento restrito a 4 direções cardinais (cima, baixo, esquerda, direita)
    - Custos derivados de tipos de terreno da grade (LIVRE=1, ARMADILHA=5, DIFÍCIL=3)

    Usado por algoritmos de busca (BFS, Guloso, A*) para explorar o espaço de estado
    e encontrar caminhos do inicial ao objetivo.
    """

    def __init__(self, grid: Grid, initial: State, goal: State, avoid_enemies: bool = True):
        """Inicializa um problema de busca de caminho em uma grade dada.

        Args:
            grid: O objeto Grid contendo tipos de terreno e custos
            initial: O State inicial (posição)
            goal: O State objetivo a alcançar
            avoid_enemies: Se True, células INIMIGO são excluídas de ações válidas.
                           Se False, células INIMIGO são passáveis (custo 1) mas serão
                           letais durante animação. Padrão True para caminhos seguros.

        A flag avoid_enemies permite resolução em duas passagens:
        - Primeira passagem: resolve com avoid_enemies=True para encontrar rotas seguras
        - Segunda passagem (se primeira falhar): resolve com avoid_enemies=False para encontrar
          qualquer caminho, até através de inimigos (personagem "morrerá" durante animação)
        """
        self.grid = grid
        self.initial = initial
        self.goal = goal
        self.avoid_enemies = avoid_enemies

    def actions(self, state: State) -> list:
        """Retorna todos os movimentos de ação válidos de um state dado.

        Args:
            state: O State atual a expandir

        Returns:
            Lista de ações válidas como tuplas (delta_linha, delta_coluna)

        Expande um state verificando todas as 4 posições vizinhas cardinais e
        filtrando:
        - Movimentos fora dos limites da grade (verificados via in_bounds)
        - Movimentos para obstáculos (verificados via is_obstacle)
        - Movimentos para células inimigo (apenas se avoid_enemies=True)

        Usado por algoritmos de busca para explorar a fronteira. A lista retornada
        define os vizinhos que um state pode transicionar em um passo.

        Abordagem de iteração:
        1. Para cada direção de ação possível (cima, baixo, esquerda, direita)
        2. Calcula a posição vizinha (nl, nc)
        3. Verifica limites: pula se fora dos limites
        4. Verifica obstáculos: pula se terreno é impassável
        5. Verifica inimigos: pula se avoid_enemies e célula é INIMIGO
        6. Se todas as verificações passarem, adiciona ação à lista válida
        """
        valid = []
        for dr, dc in ACTIONS:
            # Calcula coordenadas do vizinho aplicando o deslocamento da ação
            nr, nc = state.row + dr, state.col + dc

            # Verificação de limite: pula se vizinho está fora da grade
            if not self.grid.in_bounds(nr, nc):
                continue

            # Verificação de obstáculo: pula se vizinho é uma barreira impassável
            if self.grid.is_obstacle(nr, nc):
                continue

            # Verificação de inimigo: pula se avoid_enemies é True e célula contém inimigo
            if self.avoid_enemies and self.grid.get_cell(nr, nc) == ENEMY:
                continue

            # Todas as verificações passaram, essa é uma ação válida
            valid.append((dr, dc))

        return valid

    def result(self, state: State, action: tuple) -> State:
        """Calcula o state resultante após aplicar uma ação.

        Args:
            state: O State atual
            action: Uma tupla de ação (delta_linha, delta_coluna) (deve ser válida)

        Returns:
            Novo State na posição após mover pelo deslocamento da ação

        Aplica uma ação a um state adicionando os deltas da ação à
        posição atual. Usado por algoritmos de busca para gerar sucessores.

        Nota: Este método NÃO valida a ação. O chamador é
        responsável por garantir que a ação é válida (i.e., veio de actions()).
        Aplicar uma ação inválida (ex., para um obstáculo) é um erro do chamador.
        """
        dr, dc = action
        return State(state.row + dr, state.col + dc)

    def step_cost(self, state: State, action: tuple) -> float:
        """Obtém o custo de executar uma ação de um state.

        Args:
            state: O State atual
            action: A ação a executar (delta_linha, delta_coluna)

        Returns:
            Custo (float) de mover para o state vizinho resultante

        Calcula o custo de terreno de mover para o state resultante. Usado por
        algoritmos conscientes de custo (A*, Guloso) para avaliar qualidade de caminho.

        O custo é determinado pelo dicionário COSTS em grid.py:
        - Terreno LIVRE: custo 1
        - Terreno ARMADILHA: custo 5 (perigoso)
        - Terreno DIFÍCIL: custo 3 (áspero)
        - OBSTÁCULO: custo infinito (impassável, excluído de ações)
        - INIMIGO: custo 1 (transparente algoritmicamente, mas letal em animação)

        Algoritmo:
        1. Chama result(state, action) para obter o state vizinho
        2. Consulta a grade pelo custo daquela célula vizinha
        3. Retorna o custo (custo do caminho acumulará esses)
        """
        new_state = self.result(state, action)
        return self.grid.cost(new_state.row, new_state.col)

    def is_goal(self, state: State) -> bool:
        """Verifica se um state é o state objetivo.

        Args:
            state: O State a testar

        Returns:
            True se state é igual ao objetivo, False caso contrário

        Usado por algoritmos de busca para detectar quando o objetivo foi alcançado.
        Este teste interrompe a busca e permite ao algoritmo extrair o
        caminho de solução (rastreamento reverso do atual ao inicial).

        A igualdade é verificada usando State.__eq__, que compara coordenadas
        (linha, coluna).
        """
        return state == self.goal
