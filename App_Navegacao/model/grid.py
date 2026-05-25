"""
Módulo Grid: Estrutura de dados de grade central e sistema de terreno.

Este módulo define a grade 2D que representa o mapa de busca de caminho, incluindo:
- Constantes de tipo de célula (LIVRE, OBSTÁCULO, ARMADILHA, DIFÍCIL, INIMIGO)
- Custos de movimento para cada tipo de terreno
- Classe Grid para gerenciar estado da grade, consultar tipos de célula e redimensionar
- A grade serve como base para a classe Problem e é usada por
  algoritmos de busca e pela UI para renderização e edição

Tipos de célula permitem custos de movimento diferentes e perigos ambientais:
- LIVRE: Terreno aberto, passável com custo 1
- OBSTÁCULO: Barreira impassável, custo infinito (excluído de ações)
- ARMADILHA: Terreno perigoso, custo alto (5) para simular perigo
- DIFÍCIL: Terreno desafiador, custo moderado (3) para simular terreno acidentado
- INIMIGO: Personagem/NPC, custo 1 algoritmicamente mas letal durante animação
"""

# Constantes de tipo de célula — usadas em todo o sistema como IDs inteiros
FREE = 0          # Terreno aberto, passável
OBSTACLE = 1      # Barreira, impassável
TRAP = 2          # Área perigosa
DIFFICULT = 3     # Terreno áspero/desafiador
ENEMY = 4         # Personagem inimigo/NPC

# Nomes legíveis para cada tipo de célula (usado na UI)
CELL_NAMES = {
    FREE:     "Livre",
    OBSTACLE: "Obstáculo",
    TRAP:     "Armadilha",
    DIFFICULT:"Difícil",
    ENEMY:    "Inimigo",
}

# Custos de movimento para cada tipo de terreno
# Usado por algoritmos conscientes de custo (A*, Guloso) para encontrar caminhos ótimos
# OBSTÁCULO é impassável (custo infinito), então é excluído de ações válidas
# Células INIMIGO são transparentes para algoritmos de busca (custo 1) mas mortais
# durante execução da animação, permitindo ao sistema encontrar rotas de fuga quando
# nenhum caminho seguro existe
COSTS = {
    FREE:     1,
    TRAP:     5,
    DIFFICULT:3,
    OBSTACLE: float("inf"),
    ENEMY:    1,   # transparente ao algoritmo — letal na animação
}


class Grid:
    """Mapa de grade 2D com tipos de terreno e custos variáveis.

    Gerencia uma grade retangular de células, cada uma com um tipo (LIVRE, OBSTÁCULO, ARMADILHA,
    DIFÍCIL, INIMIGO). Fornece métodos para:
    - Consultar tipos de célula e custos de terreno
    - Validar posições da grade (verificações dentro dos limites)
    - Definir e obter células individuais
    - Redimensionar a grade com fixação e preservação de dados de célula existentes
    - Limpar todas as células de volta para terreno LIVRE

    A grade é a estrutura de dados central passada para a classe Problem para
    busca de caminho e é usada pela UI para renderização e edição.

    A indexação da grade usa a convenção (linha, coluna) onde linha=0 é topo, coluna=0 é esquerda.
    """

    def __init__(self, rows: int, cols: int):
        """Inicializa uma grade com dimensões dadas, todas as células LIVRE.

        Args:
            rows: Número de linhas da grade
            cols: Número de colunas da grade

        A grade começa com todas as células definidas como LIVRE (custo 1), criando um
        mapa vazio aberto pronto para adicionar obstáculos e terreno.
        """
        self.rows = rows
        self.cols = cols
        # Inicializa lista 2D com todas as células como terreno LIVRE
        self.cells = [[FREE] * cols for _ in range(rows)]

    def set_cell(self, row: int, col: int, cell_type: int) -> None:
        """Define uma célula específica para um tipo de terreno dado.

        Args:
            row: Índice de linha
            col: Índice de coluna
            cell_type: Um de LIVRE, OBSTÁCULO, ARMADILHA, DIFÍCIL, INIMIGO

        Usado por editores da UI e carregadores de mapa para pintar terreno na grade.
        Não valida limites — o chamador deve garantir que (linha, coluna) está dentro dos limites.
        """
        self.cells[row][col] = cell_type

    def get_cell(self, row: int, col: int) -> int:
        """Obtém o tipo de terreno de uma célula.

        Args:
            row: Índice de linha
            col: Índice de coluna

        Returns:
            Constante inteira (LIVRE, OBSTÁCULO, ARMADILHA, DIFÍCIL, INIMIGO)
        """
        return self.cells[row][col]

    def is_obstacle(self, row: int, col: int) -> bool:
        """Verifica se uma célula é um obstáculo impassável.

        Args:
            row: Índice de linha
            col: Índice de coluna

        Returns:
            True se o tipo de célula é OBSTÁCULO, False caso contrário

        Usado por Problem.actions() para excluir movimentos impossíveis de listas de
        ações válidas, garantindo que algoritmos apenas considerem vizinhos alcançáveis.
        """
        return self.cells[row][col] == OBSTACLE

    def cost(self, row: int, col: int) -> float:
        """Obtém o custo de movimento de uma célula.

        Args:
            row: Índice de linha
            col: Índice de coluna

        Returns:
            Valor de custo do dicionário COSTS (1, 3, 5 ou infinito)

        Usado por Problem.step_cost() para determinar o custo de se mover para
        uma célula. Permite que algoritmos conscientes de custo (A*, Guloso) prefiram
        caminhos mais baratos em vez de caminhos mais curtos. Células OBSTÁCULO retornam
        infinito, indicando que são impassáveis.
        """
        return COSTS[self.cells[row][col]]

    def in_bounds(self, row: int, col: int) -> bool:
        """Verifica se as coordenadas estão dentro dos limites da grade.

        Args:
            row: Índice de linha a verificar
            col: Índice de coluna a verificar

        Returns:
            True se 0 <= linha < linhas e 0 <= coluna < colunas, False caso contrário

        Usado por Problem.actions() para excluir movimentos que saem da grade,
        prevenindo acesso fora dos limites durante busca de caminho.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def resize(self, rows: int, cols: int) -> None:
        """Redimensiona a grade para novas dimensões, preservando células existentes.

        Args:
            rows: Novo número de linhas (será fixado para 3-100)
            cols: Novo número de colunas (será fixado para 3-100)

        Comportamento:
        - Fixa dimensões para intervalo [3, 100] para prevenir grades muito pequenas/grandes
        - Cria nova grade com novas dimensões, inicializada para LIVRE
        - Copia dados de célula existentes da grade antiga, usando sobreposição canto superior esquerdo
        - Se diminuindo, células em excesso são descartadas
        - Se aumentando, novas células são inicializadas para LIVRE

        Usado pela UI para permitir redimensionamento de grade em tempo de execução (ex., painel de controle).
        A fixação garante que grades permaneçam interativas e renderizáveis.
        """
        # Fixa para intervalo válido para manter usabilidade e desempenho
        rows = max(3, min(100, rows))
        cols = max(3, min(100, cols))

        # Cria nova grade com todo o terreno LIVRE
        new_cells = [[FREE] * cols for _ in range(rows)]

        # Copia células existentes da grade antiga (dentro dos limites do novo tamanho)
        # Isso preserva o mapa ao redimensionar, apenas perdendo o excesso se reduzindo
        for r in range(min(rows, self.rows)):
            for c in range(min(cols, self.cols)):
                new_cells[r][c] = self.cells[r][c]

        # Atualiza grade com novas dimensões e dados de célula
        self.rows = rows
        self.cols = cols
        self.cells = new_cells

    def clear(self) -> None:
        """Limpa todas as células de volta para terreno LIVRE (redefine o mapa).

        Inicializa uma nova grade com todas as células como LIVRE, redefinindo efetivamente
        o mapa para estado em branco. Usado pela ação "limpar" da UI para redefinir a grade
        sem alterar dimensões.
        """
        self.cells = [[FREE] * self.cols for _ in range(self.rows)]
