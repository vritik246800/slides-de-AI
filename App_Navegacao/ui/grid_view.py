"""
Renderização e interação de grade para o visualizador de busca de caminhos.

Este módulo:
  - Renderiza células de grade 2D com cores baseadas no tipo de célula
  - Exibe células início (S), objetivo (G), caminho e exploradas
  - Manipula cliques de rato e edição com arrasto para pintar
  - Suporta tamanho dinâmico de célula (baseado em área disponível e dimensões de grade)
  - Anima revelação de célula (células exploradas e de caminho aparecem incrementalmente)
  - Mostra marcador de morte (X) quando personagem bate em inimigo durante animação

Esquema de cores segue paleta AIOX dark-cockpit. Tipos de célula: LIVRE, OBSTÁCULO,
DIFÍCIL, ARMADILHA, INIMIGO. Cores especiais para marcadores (S=início, G=objetivo),
visualizações caminho/explorado e estado de morte.
"""
from __future__ import annotations
import pygame
from model.grid import FREE, OBSTACLE, TRAP, DIFFICULT, ENEMY

# Área fixa disponível para a grade (pixels)
GRID_AREA_W = 560
GRID_AREA_H = 580

CELL = 32        # tamanho máximo de célula (exportado para compatibilidade)
_CELL_MIN = 4

# Paleta AIOX dark cockpit
_BASE = {
    FREE:     ( 17,  17,  19),   # surface-panel #111113
    OBSTACLE: ( 61,  61,  61),   # charcoal #3D3D3D
    TRAP:     (237,  70,   9),   # flare #ED4609
    DIFFICULT:( 40,  40,  42),   # surface elevada
    ENEMY:    (251, 191,  36),   # aviso ouro #FBBF24
}
C_START    = (209, 255,   0)   # lima #D1FF00
C_GOAL     = (  0, 153, 255)   # azul #0099FF
C_PATH     = (209, 255,   0)   # lima #D1FF00
C_EXPLORED = ( 65,  77,  14)   # tonalidade lima-25 em surface
C_DEAD     = (237,  70,   9)   # flare #ED4609
C_GRID_LINE= ( 35,  35,  37)   # borda hairline
C_TEXT     = (  5,   5,   5)   # quase preto #050505


class GridView:
    """Renderiza a grade 2D e gerencia estado de visualização de célula de grade.

    Responsabilidades:
      - Renderizar células de grade com cores apropriadas (terreno, início, objetivo, caminho, explorado)
      - Manipular entrada de rato (clique/arrasto para selecionar células)
      - Gerenciar visualização de resultado (conjuntos de caminho e explorado)
      - Animar revelações de célula (via acúmulo de reveal_anim())
      - Rastrear posição morta (quando personagem bate em inimigo)
      - Calcular tamanho dinâmico de célula com base em área disponível e dimensões de grade

    Estado:
      - grid: referência ao modelo Grid (somente leitura)
      - start, goal: tupla (r, c) ou None para marcadores início/objetivo
      - _path_set, _explored: conjuntos de células (r, c) para visualização de resultado final
      - _anim_shown: dicionário de (r, c) -> "exp"|"path" para animação de revelação incremental
      - _dead_pos: (r, c) onde personagem morreu (marcado com X)
      - cell: tamanho atual de célula em pixels (calculado a partir de área e dimensões de grade)

    Origem (ox, oy) é a posição em pixels superior-esquerda da grade.
    """

    def __init__(self, grid, origin_x: int, origin_y: int, on_click=None):
        self.grid     = grid
        self.ox       = origin_x
        self.oy       = origin_y
        self.on_click = on_click

        self.start: tuple | None = None
        self.goal:  tuple | None = None

        self._path_set:   set  = set()
        self._path_list:  list = []
        self._explored:   set  = set()
        self._anim_shown: dict = {}   # pos -> "exp" | "path"  (buffer de quadro de animação)
        self._dead_pos:   tuple | None = None

        self._font: pygame.font.Font | None = None
        self._area_w = GRID_AREA_W
        self._area_h = GRID_AREA_H
        self.cell = self._compute_cell()

    # ── Público ────────────────────────────────────────────────────────────────

    def init_font(self):
        """Inicializar fonte usada para renderizar rótulos de célula (S, G, E, X)."""
        self._font = pygame.font.SysFont("Menlo, Courier New, monospace", 10, bold=True)

    def update_area(self, w: int, h: int):
        """Atualizar área disponível (pixels) para a grade.

        Chamado quando janela é redimensionada ou divisor é arrastado.
        Garante tamanho mínimo de 100x100 pixels.
        """
        self._area_w = max(100, w)
        self._area_h = max(100, h)

    def update_cell_size(self):
        """Recalcular tamanho de célula com base em área atual e dimensões de grade.

        Chamado após área ser atualizada. Tamanho de célula é limitado entre _CELL_MIN e CELL.
        """
        self.cell = self._compute_cell()

    def set_result(self, path, explored):
        """Exibir resultado de algoritmo: destacar caminho e células exploradas.

        Chamado após algoritmo se completar. Limpa estado de animação (_anim_shown)
        e marcador de morte para que resultado seja totalmente visível sem animação.
        """
        self._path_list  = list(path)     if path     else []
        self._path_set   = set(self._path_list)
        self._explored   = set(explored)  if explored else set()
        self._anim_shown = {}
        self._dead_pos   = None

    def clear_result(self):
        """Limpar toda visualização de resultado (caminho, explorado, animação, morte)."""
        self._path_list  = []
        self._path_set   = set()
        self._explored   = set()
        self._anim_shown = {}
        self._dead_pos   = None

    def reveal_anim(self, pos: tuple, kind: str):
        """Acumular uma revelação de célula durante reprodução de animação.

        Chamado uma vez por célula durante animação. Kind é "exp" (explorado) ou "path".
        Células são desenhadas com base no estado _anim_shown, permitindo revelação incremental.
        """
        self._anim_shown[pos] = kind

    def mark_dead(self, pos: tuple):
        """Marcar posição onde personagem morreu (bateu em inimigo).

        Define _dead_pos, que faz essa célula renderizar com rótulo X e cor de morte.
        """
        self._dead_pos = pos

    def draw(self, surf):
        """Renderizar toda a grade para a superfície Pygame.

        Itera através de todas as células e desenha cada uma com estado atual
        (cor de terreno, sobreposição, animação, marcador, etc.).
        """
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                self._draw_cell(surf, r, c)

    def draw_cell(self, surf, r: int, c: int):
        """Renderizar uma única célula. Invólucro público para _draw_cell()."""
        self._draw_cell(surf, r, c)

    def handle_event(self, event) -> tuple | None:
        """Processar eventos de rato (clique ou arrasto-pintura na grade).

        Retorna tupla (r, c) se célula foi clicada/arrastada, None caso contrário.
        Suporta clique-esquerdo e arrasto-pintura-esquerdo.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.cell_at(event.pos)
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            return self.cell_at(event.pos)
        return None

    # ── Interno ───────────────────────────────────────────────────────────────

    def _compute_cell(self) -> int:
        """Calcular tamanho de célula em pixels com base em área disponível.

        Tamanho da célula = max(célula_mín, min(célula_máx, área_l/colunas, área_a/linhas))
        Isto garante que células dimensionem para caber em espaço disponível enquanto respeitam min/máx.
        """
        return max(_CELL_MIN, min(CELL,
                                  self._area_w // self.grid.cols,
                                  self._area_h // self.grid.rows))

    def cell_at(self, pos) -> tuple | None:
        """Converter posição do rato para grade (linha, coluna) se dentro dos limites.

        Retorna tupla (r, c) ou None se clique estiver fora da área de grade.
        """
        mx, my = pos
        c = (mx - self.ox) // self.cell
        r = (my - self.oy) // self.cell
        if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
            return (r, c)
        return None

    def _draw_cell(self, surf, r: int, c: int):
        """Renderizar uma única célula com todas sobreposições e rótulos.

        Prioridade (maior para menor):
          1. Marcador morto (X) se esta é posição de morte
          2. Marcadores início/objetivo (S/G) com cores especiais
          3. Células animadas (revelação de caminho ou explorado durante animação)
          4. Resultado final (caminho ou explorado após animação terminar)
          5. Cor de terreno base (LIVRE, OBSTÁCULO, DIFÍCIL, ARMADILHA, INIMIGO)

        Rótulos (S, G, E, X) apenas renderizam se célula for >=10px.
        Linhas de grade são desenhadas como bordas 1px ao redor de cada célula.
        """
        sz  = self.cell
        x   = self.ox + c * sz
        y   = self.oy + r * sz
        pos = (r, c)

        # Determinar cor da célula (prioridade: morto > início/objetivo > caminho/explorado/anim > terreno)
        if pos == self._dead_pos:
            color = C_DEAD
        elif pos == self.start:
            color = C_START
        elif pos == self.goal:
            color = C_GOAL
        elif pos in self._path_set:
            color = C_PATH
        elif pos in self._explored:
            color = C_EXPLORED
        elif pos in self._anim_shown:
            color = C_PATH if self._anim_shown[pos] == "path" else C_EXPLORED
        else:
            color = _BASE.get(self.grid.get_cell(r, c), (255, 255, 255))

        # Desenhar retângulo de célula e borda
        pygame.draw.rect(surf, color, (x, y, sz, sz))
        pygame.draw.rect(surf, C_GRID_LINE, (x, y, sz, sz), width=1)

        # Desenhar rótulo de célula se célula for grande o suficiente (>=10px)
        if sz >= 10 and self._font:
            cx, cy = x + sz // 2, y + sz // 2
            if pos == self._dead_pos:
                # Personagem morreu aqui
                t = self._font.render("X", True, C_TEXT)
                surf.blit(t, t.get_rect(center=(cx, cy)))
            elif pos == self.start:
                # Marcador início
                t = self._font.render("S", True, C_TEXT)
                surf.blit(t, t.get_rect(center=(cx, cy)))
            elif pos == self.goal:
                # Marcador objetivo
                t = self._font.render("G", True, C_TEXT)
                surf.blit(t, t.get_rect(center=(cx, cy)))
            elif self.grid.get_cell(r, c) == ENEMY and pos not in self._anim_shown and pos not in self._path_set:
                # Rótulo inimigo (apenas se não for parte de animação ou caminho)
                t = self._font.render("E", True, C_TEXT)
                surf.blit(t, t.get_rect(center=(cx, cy)))
