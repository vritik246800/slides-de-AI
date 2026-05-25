"""
Orquestrador da janela principal Pygame para o visualizador de busca de caminhos IA.

Este módulo:
  - Inicializa e gerencia a janela Pygame (redimensionável, padrão 1060x730)
  - Orquestra GridView (renderização de grade), ControlsPanel (controles UI) e execução de algoritmos
  - Implementa o loop de eventos principal com alvo de 60 FPS
  - Gerencia animação de células exploradas e travessia de caminho (com atrasos baseados em terreno)
  - Manipula I/O de ficheiros (salvar/carregar mapas como JSON)
  - Renderiza abas: "Grelha" (editor de grade) e "Análise" (comparação de métricas)
  - Implementa divisor com arrasto para redimensionar entre grade e painel de controles
  - Mostra barra de menu (Ficheiro, Ajuda), menus suspensos, menus contextuais e sobreposição de ajuda
  - Executa algoritmos (BFS, Guloso, A*) com resolução de dois passos (evitar inimigos primeiro, depois forçar)

Esquema de cores segue paleta AIOX dark-cockpit (fundos escuros, acento lima, texto creme).
Todo o texto voltado para o utilizador está em português.
"""
from __future__ import annotations
import sys
import os
import json
import subprocess
import pygame

from model.grid    import Grid, FREE, OBSTACLE, TRAP, DIFFICULT, ENEMY, CELL_NAMES
from model.state   import State
from model.problem import Problem
from algorithms.bfs    import bfs
from algorithms.greedy import greedy
from algorithms.astar  import astar
from metrics.tracker   import Metrics
from ui.grid_view import GridView, GRID_AREA_W, GRID_AREA_H, C_PATH, C_EXPLORED, C_START, C_GOAL
from ui.controls  import ControlsPanel
from ui           import icons

# ── Disposição ────────────────────────────────────────────────────────────────
WIN_W, WIN_H   = 1060, 730
ROWS,  COLS    = 15, 18
GRID_X         = 10
MENU_BAR_H     = 22
HEADER_H       = 53           # barra de menu + linha de título

TAB_BAR_H      = 26           # faixa de abas abaixo do cabeçalho
TAB_BAR_Y      = HEADER_H     # = 53
GRID_Y         = TAB_BAR_Y + TAB_BAR_H + 2   # = 81

PANEL_X = GRID_X + GRID_AREA_W + 15
PANEL_Y = GRID_Y - 5
PANEL_W = WIN_W - PANEL_X - 8
PANEL_H = WIN_H - PANEL_Y - 8

# ── Paleta AIOX Dark Cockpit ─────────────────────────────────────────────────
BG        = (  5,   5,   5)   # #050505 canvas
HEADER_BG = ( 15,  15,  17)   # #0F0F11 surface-dark
HEADER_FG = (244, 244, 232)   # #F4F4E8 creme
MSG_OK    = ( 34, 197,  94)   # #22C55E sucesso
MSG_ERR   = (237,  70,   9)   # #ED4609 flare
MSG_INFO  = (156, 156, 156)   # #9C9C9C fg-meta

# Menu / suspenso
MENU_ACTIVE  = ( 28,  28,  30)   # surface-overlay
DROP_BG      = ( 17,  17,  19)   # surface-panel
DROP_FG      = (244, 244, 232)   # creme
DROP_HOVER   = ( 28,  28,  30)   # surface-overlay
DROP_BORDER  = ( 40,  40,  42)   # hairline
DROP_W       = 220
DROP_ITEM_H  = 26
DROP_SEP_H   = 8
MENU_ITEM_W  = 80

# Menu contextual
CTX_W        = 220
CTX_ITEM_H   = 26
CTX_SEP_H    = 8
CTX_HDR_FG   = (156, 156, 156)   # fg-meta

# Largura da coluna de ícones dentro dos menus
MENU_ICON_SZ  = 11
MENU_ICON_COL = 18   # px reservado para ícone + espaço antes do rótulo

# Sobreposição de ajuda
HELP_W        = 640
HELP_H        = 480
HELP_BG       = ( 15,  15,  17)
HELP_BORDER   = ( 40,  40,  42)
HELP_HDR_FG   = (209, 255,   0)   # acento lima
HELP_FG       = (244, 244, 232)
HELP_META     = (156, 156, 156)
HELP_SEC_FG   = (209, 255,   0)
HELP_CLOSE_BG = ( 40,  40,  42)

# Barra de abas
TAB_ACTIVE_BG   = ( 21,  21,  24)
TAB_INACTIVE_BG = ( 10,  10,  12)
TAB_ACTIVE_FG   = (209, 255,   0)
TAB_INACTIVE_FG = (156, 156, 156)
TAB_BORDER      = ( 40,  40,  42)

# Aba Análise — cores do gráfico por algoritmo
_ALGO_COLORS = {
    "BFS":    (  0, 153, 255),
    "Greedy": (251, 191,  36),
    "A*":     (209, 255,   0),
}

# (rótulo da coluna, chave métrica, é_exibição_float)
_CHART_DEFS = [
    ("Custo Total",          "cost",          False),
    ("Nos Expandidos",       "expanded",      False),
    ("Passos do Caminho",    "steps",         False),
    ("Tempo Computacao(ms)", "time_ms",       True),
    ("Tempo de Viagem(s)",   "travel_time_s", True),
]


def _file_dialog(mode: str) -> str:
    """Abre diálogo de ficheiro num subprocess para evitar conflito pygame/tkinter no macOS."""
    script = (
        "import tkinter as tk\n"
        "from tkinter import filedialog\n"
        "root = tk.Tk(); root.withdraw()\n"
    )
    if mode == "save":
        script += (
            "p = filedialog.asksaveasfilename("
            "title='Guardar Mapa', defaultextension='.json',"
            "filetypes=[('JSON','*.json'),('Todos','*.*')])\n"
        )
    else:
        script += (
            "p = filedialog.askopenfilename("
            "title='Carregar Mapa',"
            "filetypes=[('JSON','*.json'),('Todos','*.*')])\n"
        )
    script += "print(p or ''); root.destroy()\n"
    result = subprocess.run([sys.executable, "-c", script],
                            capture_output=True, text=True)
    return result.stdout.strip()


ALGO_MAP = {"BFS": bfs, "Greedy": greedy, "A*": astar}
EDIT_TO_CELL = {
    "obstacle": OBSTACLE,
    "difficult": DIFFICULT,
    "trap":     TRAP,
    "enemy":    ENEMY,
    "erase":    FREE,
}

_PATH_DELAY = {
    FREE:      100,
    DIFFICULT: 350,
    TRAP:      700,
}
_PATH_DELAY_DEFAULT = 100
_EXP_DELAY_MS       = 16
_ANIM_TARGET_FRAMES = 60

# Menu Ficheiro: (nome_ícone, rótulo, ação) ou None = separador
_FILE_MENU = [
    ("save",  "Guardar Mapa   Ctrl+S", "save_map"),
    ("open",  "Carregar Mapa  Ctrl+O", "load_map"),
    None,
    ("trash", "Limpar Tudo",           "clear_all"),
]

# Conteúdo do guia de utilização: (tipo, texto)
# tipo: "title" | "section" | "row" | "sep"
_HELP_CONTENT = [
    ("title",   "GUIA DE UTILIZACAO"),
    ("sep",     ""),
    ("section", "EDICAO DA GRELHA"),
    ("row",     "Seleciona um modo no painel lateral e clica nas celulas"),
    ("row",     "Clica e arrasta para editar multiplas celulas"),
    ("row",     "Botao direito do rato → menu de contexto"),
    ("sep",     ""),
    ("section", "TIPOS DE CELULAS"),
    ("row",     "Livre (c=1)      Custo normal de movimento"),
    ("row",     "Obstaculo        Intransponivel; excluido dos algoritmos"),
    ("row",     "Dificil (c=3)    Terreno pesado; custo elevado"),
    ("row",     "Armadilha (c=5)  Custo muito elevado na animacao"),
    ("row",     "Inimigo          Passavel pelos algoritmos; mata na animacao"),
    ("sep",     ""),
    ("section", "ALGORITMOS"),
    ("row",     "BFS     Largura primeiro; otimo em numero de passos"),
    ("row",     "Greedy  Heuristica h(n); rapido mas nao otimo em custo"),
    ("row",     "A*      f=g+h; otimo em custo (heuristica admissivel)"),
    ("sep",     ""),
    ("section", "ACOES"),
    ("row",     "Executar        Corre o algoritmo selecionado"),
    ("row",     "Executar Todos  Compara BFS, Greedy e A* na tabela"),
    ("row",     "Animar Caminho  Mostra a animacao passo a passo"),
    ("row",     "Limpar Caminho  Remove o resultado sem alterar a grelha"),
    ("row",     "Limpar Tudo     Repoe a grelha ao estado inicial"),
    ("sep",     ""),
    ("section", "ATALHOS DE TECLADO"),
    ("row",     "Ctrl+S   Guardar mapa em ficheiro JSON"),
    ("row",     "Ctrl+O   Carregar mapa de ficheiro JSON"),
    ("row",     "Esc      Fechar menus / Sair da aplicacao"),
]


class App:
    """Janela de aplicação principal e loop de eventos.

    Responsabilidades:
      - Configuração e redimensionamento de janela (pygame.RESIZABLE)
      - Manipulação de eventos (teclado, rato, redimensionamento de janela)
      - Execução de algoritmos e gestão de resultados
      - Reprodução de animação (exploração célula por célula e travessia de caminho)
      - Persistência de ficheiros (salvar/carregar)
      - Renderização de todos os elementos da interface (grade, controles, menus, ajuda)
      - Comutação de abas entre editor de grade e vista de análise

    Gestão de estado:
      - self._grid: instância Grid (modelo do mundo)
      - self._view: GridView (renderiza grade e resultados)
      - self._ctrl: ControlsPanel (interface da barra lateral)
      - self._metrics: rastreador Metrics (registra resultados)
      - self._last_result: dicionário de resultado de algoritmo mais recente
      - self._anim_*: estado de animação (passos, índice, tamanho de lote, cronometragem)
      - self._menu_open, self._ctx, self._help_open: estado de sobreposição
      - self._divider_x: posição do separador grade/painel arrastável
    """

    def __init__(self):
        pygame.init()
        self._win_w = WIN_W
        self._win_h = WIN_H
        self._screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
        pygame.display.set_caption("Navegação 2D com IA — BFS / Greedy / A*")

        self._clock   = pygame.time.Clock()
        self._grid    = Grid(ROWS, COLS)
        self._metrics = Metrics()

        self._view = GridView(self._grid, GRID_X, GRID_Y)
        self._view.init_font()

        self._ctrl = ControlsPanel(PANEL_X, PANEL_Y, PANEL_W, PANEL_H,
                                   initial_rows=ROWS, initial_cols=COLS)
        self._ctrl.init_fonts()

        # Estado da aba
        self._active_tab:      int  = 0   # 0 = Grelha, 1 = Análise
        self._tab_rects:       list = []
        self._analysis_scroll: int  = 0
        self._last_metric_rows: list = []

        self._font_header     = pygame.font.SysFont("Arial", 14, bold=True)
        self._font_msg        = pygame.font.SysFont("Menlo, Courier New, monospace", 11)
        self._font_menu       = pygame.font.SysFont("Menlo, Courier New, monospace", 11)
        self._font_drop       = pygame.font.SysFont("Menlo, Courier New, monospace", 11)
        self._font_help_title = pygame.font.SysFont("Arial", 15, bold=True)
        self._font_help_sec   = pygame.font.SysFont("Menlo, Courier New, monospace", 11, bold=True)
        self._font_help_body  = pygame.font.SysFont("Menlo, Courier New, monospace", 11)
        self._font_analysis   = pygame.font.SysFont("Menlo, Courier New, monospace", 10)
        self._font_analysis_h = pygame.font.SysFont("Menlo, Courier New, monospace", 11, bold=True)

        self._last_result: dict | None = None
        self._msg       = "Clica nas celulas para editar. S = inicio, G = objetivo."
        self._msg_color = MSG_INFO

        # Estado de animação
        self._anim_steps:     list = []
        self._anim_idx:       int  = 0
        self._anim_batch:     int  = 1
        self._animating:      bool = False
        self._anim_next_time: int  = 0

        # Estado da barra de menu
        self._menu_open: str | None = None   # "ficheiro" ou None
        self._drop_rects: list      = []     # [(Rect, ação), ...]
        self._ficheiro_rect = pygame.Rect(0,            0, MENU_ITEM_W, MENU_BAR_H)
        self._ajuda_rect    = pygame.Rect(MENU_ITEM_W,  0, MENU_ITEM_W, MENU_BAR_H)

        # Estado do menu contextual
        self._ctx: dict | None = None        # veja _open_ctx()

        # Estado da sobreposição de ajuda
        self._help_open: bool              = False
        self._help_close_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        # Divisor arrastável entre grade e painel de controles
        self._divider_x:      int  = PANEL_X   # borda esquerda do painel
        self._drag_div:       bool = False
        self._drag_div_off:   int  = 0          # deslocamento do rato no início do arrasto
        self._div_hover:      bool = False

    # ── Loop principal ────────────────────────────────────────────────────────

    def run(self):
        """Loop de eventos principal — executa a ~60 FPS até sair.

        Ordem de processamento de eventos:
          1. QUIT, VIDEORESIZE → sair ou refazer disposição
          2. MOUSEWHEEL → deslocar aba Análise se ativa
          3. KEYDOWN → verificar Ctrl+S/O (salvar/carregar), Esc (menu/ajuda/sair), caso contrário enviar
          4. Outros eventos → enviar para manipuladores

        Cada iteração:
          - Processar todos os eventos enfileirados
          - Animar (\_tick_anim processa um lote de células reveladas)
          - Redesenho completo da janela
          - Limitar a 60 FPS
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._win_w = max(800, event.w)
                    self._win_h = max(600, event.h)
                    self._screen = pygame.display.set_mode(
                        (self._win_w, self._win_h), pygame.RESIZABLE)
                    self._relayout()
                elif event.type == pygame.MOUSEWHEEL:
                    if self._active_tab == 1:
                        self._analysis_scroll = max(
                            0, self._analysis_scroll - event.y * 24)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self._help_open:
                            self._help_open = False
                        elif self._menu_open or self._ctx:
                            self._close_menus()
                        else:
                            running = False
                    elif event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                        self._save_map()
                    elif event.mod & pygame.KMOD_CTRL and event.key == pygame.K_o:
                        self._load_map()
                    else:
                        self._handle_event(event)
                else:
                    self._handle_event(event)

            self._tick_anim()
            self._draw()
            self._clock.tick(60)

        pygame.quit()
        sys.exit()

    # ── Eventos ────────────────────────────────────────────────────────────────

    def _close_menus(self):
        """Fechar qualquer menu aberto, suspenso ou contextual."""
        self._menu_open = None
        self._ctx       = None

    def _handle_event(self, event):
        """Encaminhar eventos de rato/teclado para manipuladores apropriados.

        Hierarquia de prioridade (topo = maior prioridade):
          1. Sobreposição de ajuda (botão fechar)
          2. Menu contextual (menu de clique direito de célula)
          3. Cliques na barra de abas
          4. Barra de menu (botões Ficheiro, Ajuda)
          5. Itens do menu suspenso
          6. Divisor arrastável entre grade e painel
          7. Cliques de célula de grade (se active_tab == 0)
          8. Cliques de botão do painel de controles

        O evento é consumido após manipulação; manipuladores de menor prioridade não o veem.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # ── sobreposição de ajuda (maior prioridade) ──────────────────────
            if self._help_open:
                if event.button == 1 and self._help_close_rect.collidepoint(pos):
                    self._help_open = False
                return

            # ── menu contextual ───────────────────────────────────────────────
            if self._ctx:
                if event.button == 1:
                    for rect, action in self._ctx.get("rects", []):
                        if rect.collidepoint(pos):
                            # enviar ANTES de limpar ctx — erase_cell precisa ler self._ctx
                            if action:
                                self._dispatch(action)
                            self._ctx = None
                            return
                self._ctx = None
                return

            # ── barra de abas ─────────────────────────────────────────────────
            if TAB_BAR_Y <= pos[1] < TAB_BAR_Y + TAB_BAR_H and event.button == 1:
                for i, rect in enumerate(self._tab_rects):
                    if rect.collidepoint(pos):
                        self._active_tab = i
                        self._analysis_scroll = 0
                        return
                return

            # ── barra de menu ─────────────────────────────────────────────────
            if pos[1] < MENU_BAR_H and event.button == 1:
                if self._ficheiro_rect.collidepoint(pos):
                    toggle = "ficheiro" if self._menu_open != "ficheiro" else None
                    self._menu_open = toggle
                    self._rebuild_drop_rects()
                elif self._ajuda_rect.collidepoint(pos):
                    self._menu_open = None
                    self._help_open = True
                else:
                    self._menu_open = None
                return

            # ── clique suspenso aberto ────────────────────────────────────────
            if self._menu_open and event.button == 1:
                for rect, action in self._drop_rects:
                    if rect.collidepoint(pos):
                        self._menu_open = None
                        if action:
                            self._dispatch(action)
                        return
                # clique fora do suspenso → fechá-lo, deixar evento passar
                self._menu_open = None

            if self._menu_open:
                self._menu_open = None

            # ── clique direito na grade → menu contextual ──────────────────────
            if event.button == 3:
                cell = self._view.cell_at(pos)
                if cell is not None:
                    self._open_ctx(pos, cell)
                    return

        # ── divisor arrastável ────────────────────────────────────────────────
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self._div_hover = self._divider_hit_rect().collidepoint(mx, my)
            if self._drag_div:
                new_x = mx + self._drag_div_off
                min_x = GRID_X + 200 + 15
                max_x = self._win_w - 300 - 8
                self._divider_x = max(min_x, min(max_x, new_x))
                self._relayout_divider()
                return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self._drag_div:
            self._drag_div = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._divider_hit_rect().collidepoint(event.pos):
                self._drag_div     = True
                self._drag_div_off = self._divider_x - event.pos[0]
                return

        # ── eventos normais de grade / painel ──────────────────────────────────
        if self._drag_div:
            return
        if self._active_tab == 0:
            cell = self._view.handle_event(event)
            if cell is not None:
                self._on_cell(cell[0], cell[1])
                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = self._ctrl.handle_click(event.pos)
            if action:
                self._dispatch(action)

    # ── Ajudantes suspensos ───────────────────────────────────────────────────

    def _rebuild_drop_rects(self):
        """Reconstruir retângulos de teste de colisão para itens suspensos no menu Ficheiro.

        Chamado quando o menu Ficheiro abre/fecha para calcular pares (Rect, ação)
        para cada item. Separadores (None) são ignorados.
        """
        if self._menu_open != "ficheiro":
            self._drop_rects = []
            return
        rects = []
        x = self._ficheiro_rect.x
        y = MENU_BAR_H
        for item in _FILE_MENU:
            if item is None:
                y += DROP_SEP_H
            else:
                _icon, _label, action = item
                rects.append((pygame.Rect(x, y, DROP_W, DROP_ITEM_H), action))
                y += DROP_ITEM_H
        self._drop_rects = rects

    # ── Menu contextual ──────────────────────────────────────────────────────

    def _open_ctx(self, pos, cell):
        """Abrir menu contextual de clique direito para célula de grade.

        Mostra:
          - Rótulo tipo célula (Livre, Obstáculo, etc.)
          - Opção Apagar Célula
          - Opções Guardar/Carregar Mapa

        O menu é limitado aos limites da janela (horizontal e vertical).
        Retângulos de teste de colisão são armazenados em self._ctx para manipulação de cliques.
        """
        mx, my = pos
        if mx + CTX_W > self._win_w:
            mx = self._win_w - CTX_W - 4

        ct    = self._grid.get_cell(cell[0], cell[1])
        # formato: (nome_ícone | None, rótulo, ação | None, é_cabeçalho)
        items = [
            (None,    f"Celula: {CELL_NAMES.get(ct, '?')}", None,         True),
            None,
            ("erase", "Apagar Celula",  "erase_cell",  False),
            None,
            ("save",  "Guardar Mapa",   "save_map",    False),
            ("open",  "Carregar Mapa",  "load_map",    False),
        ]

        rects = []
        cy = my
        for item in items:
            if item is None:
                cy += CTX_SEP_H
            else:
                _icon, label, action, _hdr = item
                rects.append((pygame.Rect(mx, cy, CTX_W, CTX_ITEM_H), action))
                cy += CTX_ITEM_H

        # limitar verticalmente
        total_h = cy - my
        if my + total_h > self._win_h:
            shift   = (my + total_h) - self._win_h + 4
            my     -= shift
            rects   = [(pygame.Rect(r.x, r.y - shift, r.w, r.h), a) for r, a in rects]

        self._ctx = {
            "x": mx, "y": my, "cell": cell,
            "items": items, "rects": rects,
        }

    # ── Ações de célula ───────────────────────────────────────────────────────

    def _on_cell(self, r: int, c: int):
        """Manipular edição de célula de grade (clique/arrasto no editor de grade).

        Dependendo do modo atual:
          - "start": definir marcador grid.start
          - "goal": definir marcador grid.goal
          - caso contrário (obstáculo, armadilha, difícil, inimigo, apagar): pintar célula com esse tipo

        Quando qualquer célula é pintada, limpar animação e resultados em cache.
        Isso garante que uma nova solução seja necessária antes de exibir caminhos obsoletos.
        """
        mode = self._ctrl.mode
        view = self._view
        if mode == "start":
            view.start = (r, c)
        elif mode == "goal":
            view.goal = (r, c)
        else:
            ct = EDIT_TO_CELL[mode]
            self._grid.set_cell(r, c, ct)
            if (r, c) == view.start:
                view.start = None
            if (r, c) == view.goal:
                view.goal  = None
        self._stop_anim()
        view.clear_result()
        self._last_result = None
        self._metrics.clear()
        self._ctrl.set_metrics([])

    def _dispatch(self, action: str):
        """Encaminhar string de ação para método manipulador.

        Ações válidas:
          - run, run_all → resolver com algoritmos atuais/todos
          - animate → reproduzir visualização célula por célula
          - clear_path, clear_all → remover resultados ou redefinir grade
          - resize → aplicar mudanças pendentes de dimensão de grade
          - save_map, load_map → I/O de ficheiro
          - erase_cell → limpar célula do menu contextual
          - open_help → mostrar sobreposição de ajuda
        """
        {
            "run":        self._run,
            "run_all":    self._run_all,
            "animate":    self._start_anim,
            "clear_path": self._clear_path,
            "clear_all":  self._clear_all,
            "resize":     self._resize,
            "save_map":   self._save_map,
            "load_map":   self._load_map,
            "erase_cell": self._erase_ctx_cell,
            "open_help":  self._open_help,
        }.get(action, lambda: None)()

    def _erase_ctx_cell(self):
        """Apagar (definir como LIVRE) a célula do menu contextual de clique direito."""
        if not self._ctx or "cell" not in self._ctx:
            return
        r, c = self._ctx["cell"]
        self._grid.set_cell(r, c, FREE)
        v = self._view
        if (r, c) == v.start:
            v.start = None
        if (r, c) == v.goal:
            v.goal  = None
        self._stop_anim()
        v.clear_result()
        self._last_result = None
        self._metrics.clear()
        self._ctrl.set_metrics([])

    def _open_help(self):
        """Mostrar sobreposição de ajuda."""
        self._help_open = True

    # ── Guardar / Carregar ────────────────────────────────────────────────────

    def _save_map(self):
        """Guardar mapa atual para ficheiro JSON (células, início, objetivo, dimensões).

        Gera diálogo de ficheiro tkinter em subprocess para evitar conflito pygame/tkinter no macOS.
        Mostra mensagem de sucesso/erro na barra de estado.
        """
        path = _file_dialog("save")
        if not path:
            return
        data = {
            "rows":  self._grid.rows,
            "cols":  self._grid.cols,
            "cells": [row[:] for row in self._grid.cells],
            "start": list(self._view.start) if self._view.start else None,
            "goal":  list(self._view.goal)  if self._view.goal  else None,
        }
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            self._set_msg(f"Mapa guardado: {os.path.basename(path)}", MSG_OK)
        except Exception as e:
            self._set_msg(f"Erro ao guardar: {e}", MSG_ERR)

    def _load_map(self):
        """Carregar mapa do ficheiro JSON, substituindo estado da grade.

        Lê dimensões, células, início e objetivo do ficheiro.
        Limpa animação e resultados. Redimensiona vista se dimensões mudaram.
        Mostra mensagem de sucesso/erro na barra de estado.
        """
        path = _file_dialog("open")
        if not path:
            return
        try:
            with open(path) as f:
                data = json.load(f)
            rows = int(data["rows"])
            cols = int(data["cols"])
            self._stop_anim()
            self._grid.resize(rows, cols)
            for r in range(rows):
                for c in range(cols):
                    self._grid.cells[r][c] = data["cells"][r][c]
            self._view.start = tuple(data["start"]) if data.get("start") else None
            self._view.goal  = tuple(data["goal"])  if data.get("goal")  else None
            self._view.update_cell_size()
            self._view.clear_result()
            self._last_result = None
            self._metrics.clear()
            self._ctrl.set_metrics([])
            self._ctrl.set_grid_size(rows, cols)
            self._set_msg(f"Mapa carregado: {os.path.basename(path)}", MSG_OK)
        except Exception as e:
            self._set_msg(f"Erro ao carregar: {e}", MSG_ERR)

    # ── Refazer disposição no redimensionamento ───────────────────────────────

    def _relayout(self):
        """Limitar posição do divisor e recalcular áreas painel/grade no redimensionamento de janela.

        Chamado por evento VIDEORESIZE para garantir que grade e painel permaneçam dentro dos limites
        e mantenham tamanhos mínimos.
        """
        # Clamp divider when window shrinks
        min_x = GRID_X + 200 + 15
        max_x = self._win_w - 300 - 8
        self._divider_x = max(min_x, min(max_x, self._divider_x))
        self._relayout_divider()

    def _relayout_divider(self):
        """Recalcular geometria de grade e painel com base na posição do divisor.

        Atualiza GridView.area e tamanho de célula, e posição/tamanho de ControlsPanel.
        Chamado durante arrasto ou redimensionamento de janela.
        """
        w, h = self._win_w, self._win_h
        panel_x = self._divider_x
        panel_y = PANEL_Y
        panel_w = max(200, w - panel_x - 8)
        panel_h = max(300, h - panel_y - 8)
        self._ctrl.update_geometry(panel_x, panel_y, panel_w, panel_h)
        grid_area_w = max(200, panel_x - GRID_X - 15)
        grid_area_h = max(200, h - GRID_Y - 40)
        self._view.update_area(grid_area_w, grid_area_h)
        self._view.update_cell_size()

    def _divider_hit_rect(self) -> pygame.Rect:
        """Retornar retângulo de teste de colisão para o divisor arrastável (linha vertical).

        Centrado em self._divider_x, 10px de largura, estende-se de GRID_Y até o fundo da janela.
        """
        cx = self._divider_x - 7   # center of the gap
        return pygame.Rect(cx - 5, GRID_Y, 10, self._win_h - GRID_Y)

    # ── Algoritmos ────────────────────────────────────────────────────────────

    def _compute_anim_time(self, path) -> float | None:
        """Calcular duração total de animação para travessia de caminho em segundos.

        Soma atrasos por célula do dicionário _PATH_DELAY com base no tipo de terreno.
        Usado para preencher result["travel_time_s"] para exibição de métricas.
        Retorna None se o caminho estiver vazio.
        """
        """Soma de atrasos de animação por célula para células de caminho → segundos."""
        if not path:
            return None
        total_ms = sum(
            _PATH_DELAY.get(self._grid.get_cell(r, c), _PATH_DELAY_DEFAULT)
            for r, c in path
        )
        return total_ms / 1000.0

    def _make_problem(self, avoid_enemies: bool = True) -> Problem | None:
        """Criar instância de Problema a partir do estado da grade atual e marcadores.

        Valida que início e objetivo estão definidos, depois constrói Problema com
        o sinalizador avoid_enemies especificado. Retorna None e mostra erro se marcadores faltarem.
        """
        v = self._view
        if v.start is None or v.goal is None:
            self._set_msg("Define o Inicio (S) e o Objetivo (G) primeiro.", MSG_ERR)
            return None
        sr, sc = v.start
        gr, gc = v.goal
        return Problem(self._grid, State(sr, sc), State(gr, gc), avoid_enemies=avoid_enemies)

    def _solve(self, fn) -> dict | None:
        """Resolvedor de dois passos: primeiro evitar inimigos, depois forçar se necessário.

        Passo 1: Chama fn(problema) com avoid_enemies=True.
        Se resultado não tiver caminho (caminho=None), Passo 2: Chama fn(problema) com avoid_enemies=False.

        Isto permite que animações prossigam mesmo quando nenhum caminho seguro existe; o personagem
        atingirá um inimigo durante reprodução e acionará o estado de morte "capturado".

        Retorna o dicionário de resultado final do algoritmo, ou None se a criação de problema falhar.
        """
        safe_prob = self._make_problem(avoid_enemies=True)
        if safe_prob is None:
            return None
        result = fn(safe_prob)
        if result["path"] is None:
            forced_prob = self._make_problem(avoid_enemies=False)
            result = fn(forced_prob)
        return result

    def _run(self):
        """Resolver usando o algoritmo atualmente selecionado (BFS, Guloso ou A*).

        Executa o algoritmo via _solve(), registra métricas, exibe caminho/explorado em vista,
        e inicia animação. Mostra resumo de resultado (custo, nós, tempo) na barra de estado.
        """
        if self._view.start is None or self._view.goal is None:
            self._set_msg("Define o Inicio (S) e o Objetivo (G) primeiro.", MSG_ERR)
            return
        name = self._ctrl.algorithm
        self._set_msg(f"A executar {name}...", MSG_INFO)
        self._draw()

        result = self._solve(ALGO_MAP[name])
        if result is None:
            return
        result["travel_time_s"] = self._compute_anim_time(result["path"])
        self._last_result = result
        self._metrics.clear()
        self._metrics.record(name, result)
        self._view.set_result(result["path"], result["explored"])
        self._last_metric_rows = self._metrics.to_rows()
        self._ctrl.set_metrics(self._last_metric_rows)

        if result["path"]:
            self._set_msg(
                f"{name}: custo={result['cost']}  nos={result['expanded']}  "
                f"tempo={result['time']*1000:.2f}ms", MSG_OK)
            self._start_anim()
        else:
            self._set_msg(f"{name}: sem solucao encontrada.", MSG_ERR)

    def _run_all(self):
        """Resolver com os três algoritmos (BFS, Guloso, A*) e comparar métricas.

        Executa cada algoritmo, registra todos os resultados em self._metrics, e exibe último caminho
        com todas as métricas na tabela e gráficos da aba Análise.
        """
        if self._view.start is None or self._view.goal is None:
            self._set_msg("Define o Inicio (S) e o Objetivo (G) primeiro.", MSG_ERR)
            return
        self._set_msg("A executar todos os algoritmos...", MSG_INFO)
        self._draw()

        self._metrics.clear()
        last = None
        for name, fn in ALGO_MAP.items():
            r = self._solve(fn)
            if r is None:
                return
            r["travel_time_s"] = self._compute_anim_time(r["path"])
            self._metrics.record(name, r)
            last = r

        self._last_result = last
        self._view.set_result(last["path"], last["explored"])
        self._last_metric_rows = self._metrics.to_rows()
        self._ctrl.set_metrics(self._last_metric_rows)

        if last and last["path"]:
            self._set_msg("Comparacao completa — a animar.", MSG_OK)
            self._start_anim()
        else:
            self._set_msg("Comparacao completa. Ver metricas.", MSG_OK)

    # ── Redimensionar ────────────────────────────────────────────────────────

    def _resize(self):
        """Aplicar mudanças de dimensão de grade pendentes do painel de controles.

        Redimensiona grade, limpa início/objetivo se fora dos limites, limpa animação e resultados,
        e atualiza tamanho de célula de vista. Mostra novas dimensões na barra de estado.
        """
        rows = self._ctrl.pending_rows
        cols = self._ctrl.pending_cols
        self._stop_anim()
        self._grid.resize(rows, cols)
        v = self._view
        if v.start and not self._grid.in_bounds(*v.start):
            v.start = None
        if v.goal and not self._grid.in_bounds(*v.goal):
            v.goal = None
        v.clear_result()
        self._view.update_cell_size()
        self._last_result = None
        self._metrics.clear()
        self._ctrl.set_metrics([])
        self._set_msg(
            f"Matriz: {rows}x{cols}  (celula={self._view.cell}px)", MSG_INFO)

    # ── Animação ───────────────────────────────────────────────────────────────

    def _start_anim(self):
        """Inicializar reprodução de animação de células exploradas e caminho.

        Combina células exploradas (lote rápido) seguidas por células de caminho (dependente de terreno).
        Calcula tamanho de lote ideal para atingir ~60 frames de animação.
        Limpa estado de animação anterior e marca vista como animando.
        """
        if not self._last_result or not self._last_result["path"]:
            self._set_msg("Executa um algoritmo primeiro.", MSG_ERR)
            return
        self._stop_anim()
        self._view.clear_result()

        path     = self._last_result["path"]
        explored = self._last_result["explored"]
        path_set = set(path)

        self._anim_steps = (
            [(pos, "exp")  for pos in explored if pos not in path_set]
            + [(pos, "path") for pos in path]
        )
        n = len(self._anim_steps)
        self._anim_batch = max(1, n // _ANIM_TARGET_FRAMES)
        self._anim_idx   = 0
        self._animating  = True
        self._set_msg("A animar...", MSG_INFO)

    def _tick_anim(self):
        """Processar um quadro de animação (múltiplas células por lote).

        Cronometragem:
          - Células exploradas: revelação em lote com atraso de 16ms (animação rápida de múltiplas células)
          - Células de caminho: revelação individual com atraso dependente de terreno

        Caso especial: células INIMIGAS param animação e marcam personagem morto.
        Quando animação se completa, finaliza vista e mostra mensagem de conclusão.
        """
        if not self._animating:
            return

        now = pygame.time.get_ticks()
        if now < self._anim_next_time:
            return

        if self._anim_idx >= len(self._anim_steps):
            self._animating = False
            self._view.set_result(
                self._last_result["path"],
                self._last_result["explored"],
            )
            self._set_msg("Animacao concluida.", MSG_OK)
            return

        pos, kind = self._anim_steps[self._anim_idx]

        if kind == "exp":
            for _ in range(self._anim_batch):
                if self._anim_idx >= len(self._anim_steps):
                    break
                p, k = self._anim_steps[self._anim_idx]
                if k != "exp":
                    break
                self._view.reveal_anim(p, k)
                self._anim_idx += 1
            self._anim_next_time = now + _EXP_DELAY_MS
        else:
            cell_type = self._grid.get_cell(pos[0], pos[1])
            if cell_type == ENEMY:
                self._animating = False
                self._view.mark_dead(pos)
                self._set_msg("Personagem capturado pelo inimigo!", MSG_ERR)
                return
            self._view.reveal_anim(pos, kind)
            self._anim_idx += 1
            delay = _PATH_DELAY.get(cell_type, _PATH_DELAY_DEFAULT)
            self._anim_next_time = now + delay

    def _stop_anim(self):
        """Parar toda animação e redefinir variáveis de estado de animação."""
        self._animating      = False
        self._anim_steps     = []
        self._anim_idx       = 0
        self._anim_next_time = 0

    # ── Limpar ────────────────────────────────────────────────────────────────

    def _clear_path(self):
        """Remover visualização de caminho/explorado sem alterar células de grade ou início/objetivo."""
        self._stop_anim()
        self._view.clear_result()
        self._last_result = None
        self._set_msg("Caminho limpo.", MSG_INFO)

    def _clear_all(self):
        """Redefinir grade inteira para estado inicial (tudo LIVRE, sem marcadores, sem resultados)."""
        self._stop_anim()
        self._grid.clear()
        self._view.start = None
        self._view.goal  = None
        self._view.clear_result()
        self._last_result = None
        self._metrics.clear()
        self._ctrl.set_metrics([])
        self._set_msg("Mapa limpo.", MSG_INFO)

    # ── Desenhar ───────────────────────────────────────────────────────────────

    def _draw(self):
        """Redesenho de tela inteira (chamado a cada quadro a 60 FPS).

        Desenha:
          1. Preenchimento de fundo
          2. Barra de cabeçalho (barra de menu + título)
          3. Barra de abas (Grelha | Análise)
          4. Conteúdo da aba ativa:
             - Aba 0: Grade + controles + mensagem
             - Aba 1: Tabela de métricas + gráficos
          5. Divisor arrastável
          6. Camadas de sobreposição (em ordem de prioridade):
             - Menu suspenso
             - Menu contextual
             - Sobreposição de ajuda (maior)

        Usa pygame.display.flip() para trocar buffers.
        """
        w, h = self._win_w, self._win_h
        self._screen.fill(BG)

        # Full header background
        pygame.draw.rect(self._screen, HEADER_BG, (0, 0, w, HEADER_H))

        # Menu bar (top slice of header)
        self._draw_menu_bar()

        # Title (below menu bar, inside remaining header)
        title_y = MENU_BAR_H + (HEADER_H - MENU_BAR_H) // 2
        title = self._font_header.render(
            "Navegacao de Personagem em Grelha 2D  |  BFS · Greedy · A*",
            True, HEADER_FG)
        self._screen.blit(title, title.get_rect(midleft=(10, title_y)))

        # Tab bar
        self._draw_tab_bar()

        if self._active_tab == 0:
            # ── Aba Grade ──────────────────────────────────────────────────────
            self._view.draw(self._screen)
            gw = self._grid.cols * self._view.cell
            gh = self._grid.rows * self._view.cell
            pygame.draw.rect(self._screen, (40, 40, 42),
                             (GRID_X - 1, GRID_Y - 1, gw + 2, gh + 2), width=1)
            msg = self._font_msg.render(self._msg, True, self._msg_color)
            self._screen.blit(msg, (GRID_X, GRID_Y + gh + 8))
        else:
            # ── Aba Análise ────────────────────────────────────────────────────
            self._draw_analysis_tab()

        self._ctrl.draw(self._screen)

        # Pega do divisor
        div_cx = self._divider_x - 7
        if self._drag_div:
            line_col = (200, 200, 205)
            dot_col  = (220, 220, 225)
        elif self._div_hover:
            line_col = (120, 120, 128)
            dot_col  = (160, 160, 168)
        else:
            line_col = (55, 55, 60)
            dot_col  = (80, 80, 88)
        pygame.draw.line(self._screen, line_col, (div_cx, GRID_Y), (div_cx, h - 8))
        mid_y = (GRID_Y + h) // 2
        for dy in (-12, -4, 4, 12):
            pygame.draw.circle(self._screen, dot_col, (div_cx, mid_y + dy), 2)

        # Sobreposição de suspenso
        if self._menu_open:
            self._draw_dropdown()

        # Sobreposição de menu contextual
        if self._ctx:
            self._draw_ctx_menu()

        # Sobreposição de ajuda (camada mais alta)
        if self._help_open:
            self._draw_help_overlay()

        pygame.display.flip()

    def _draw_menu_bar(self):
        """Desenhar barra de menu (botões Ficheiro, Ajuda com ícones e rótulos)."""
        pygame.draw.line(self._screen, MENU_ACTIVE,
                         (0, MENU_BAR_H), (self._win_w, MENU_BAR_H))

        # Botão Ficheiro
        if self._menu_open == "ficheiro":
            pygame.draw.rect(self._screen, MENU_ACTIVE, self._ficheiro_rect)
        r = self._ficheiro_rect
        icon_x = r.x + 6
        icon_y = r.y + (MENU_BAR_H - MENU_ICON_SZ) // 2
        icons.draw(self._screen, "file", icon_x, icon_y, HEADER_FG, MENU_ICON_SZ)
        txt = self._font_menu.render("Ficheiro", True, HEADER_FG)
        self._screen.blit(txt, (icon_x + MENU_ICON_SZ + 4,
                                r.y + (MENU_BAR_H - txt.get_height()) // 2))

        # Botão Ajuda
        if self._help_open:
            pygame.draw.rect(self._screen, MENU_ACTIVE, self._ajuda_rect)
        r2 = self._ajuda_rect
        icon_x2 = r2.x + 6
        icon_y2 = r2.y + (MENU_BAR_H - MENU_ICON_SZ) // 2
        icons.draw(self._screen, "help", icon_x2, icon_y2, HEADER_FG, MENU_ICON_SZ)
        txt2 = self._font_menu.render("Ajuda", True, HEADER_FG)
        self._screen.blit(txt2, (icon_x2 + MENU_ICON_SZ + 4,
                                 r2.y + (MENU_BAR_H - txt2.get_height()) // 2))

    def _draw_dropdown(self):
        """Desenhar menu suspenso Ficheiro com ícones, rótulos e separadores.

        Destaca item sob rato. Usa retângulos pré-computados de _rebuild_drop_rects().
        """
        x = self._ficheiro_rect.x
        y = MENU_BAR_H
        mx, my = pygame.mouse.get_pos()

        total_h = sum(DROP_ITEM_H if it else DROP_SEP_H for it in _FILE_MENU)

        pygame.draw.rect(self._screen, (0, 0, 0),
                         (x + 4, y + 4, DROP_W, total_h))
        pygame.draw.rect(self._screen, DROP_BG, (x, y, DROP_W, total_h))
        pygame.draw.rect(self._screen, DROP_BORDER,
                         (x, y, DROP_W, total_h), width=1)

        cy = y
        ri = 0
        for item in _FILE_MENU:
            if item is None:
                mid = cy + DROP_SEP_H // 2
                pygame.draw.line(self._screen, DROP_BORDER,
                                 (x + 8, mid), (x + DROP_W - 8, mid))
                cy += DROP_SEP_H
            else:
                icon_name, label, _ = item
                rect = self._drop_rects[ri][0]
                if rect.collidepoint(mx, my):
                    pygame.draw.rect(self._screen, DROP_HOVER, rect)
                icon_y = cy + (DROP_ITEM_H - MENU_ICON_SZ) // 2
                icons.draw(self._screen, icon_name, x + 6, icon_y,
                           DROP_FG, MENU_ICON_SZ)
                txt = self._font_drop.render(label, True, DROP_FG)
                self._screen.blit(txt, (x + 6 + MENU_ICON_COL,
                                        cy + (DROP_ITEM_H - txt.get_height()) // 2))
                cy += DROP_ITEM_H
                ri += 1

    def _draw_ctx_menu(self):
        """Desenhar menu contextual de clique direito com rótulo de célula, apagar e opções de guardar/carregar.

        Destaca itens sob rato. Ajusta posição vertical se ultrapassar janela.
        """
        ctx   = self._ctx
        items = ctx["items"]
        mx    = ctx["x"]
        my    = ctx["y"]
        mouse = pygame.mouse.get_pos()

        total_h = sum(CTX_ITEM_H if it else CTX_SEP_H for it in items)

        pygame.draw.rect(self._screen, (0, 0, 0),
                         (mx + 4, my + 4, CTX_W, total_h))
        pygame.draw.rect(self._screen, DROP_BG, (mx, my, CTX_W, total_h))
        pygame.draw.rect(self._screen, DROP_BORDER,
                         (mx, my, CTX_W, total_h), width=1)

        cy = my
        ri = 0
        for item in items:
            if item is None:
                mid = cy + CTX_SEP_H // 2
                pygame.draw.line(self._screen, DROP_BORDER,
                                 (mx + 8, mid), (mx + CTX_W - 8, mid))
                cy += CTX_SEP_H
            else:
                icon_name, label, _action, is_header = item
                rect = ctx["rects"][ri][0]
                if not is_header and rect.collidepoint(mouse):
                    pygame.draw.rect(self._screen, DROP_HOVER, rect)
                fg = CTX_HDR_FG if is_header else DROP_FG
                if icon_name and not is_header:
                    icon_y = cy + (CTX_ITEM_H - MENU_ICON_SZ) // 2
                    icons.draw(self._screen, icon_name, mx + 6, icon_y, fg, MENU_ICON_SZ)
                    text_x = mx + 6 + MENU_ICON_COL
                else:
                    text_x = mx + 12
                txt = self._font_drop.render(label, True, fg)
                self._screen.blit(txt, (text_x, cy + (CTX_ITEM_H - txt.get_height()) // 2))
                cy += CTX_ITEM_H
                ri += 1

    def _draw_help_overlay(self):
        """Desenhar sobreposição de ajuda centrada com título, seções de conteúdo, botão fechar.

        Conteúdo inclui:
          - Cabeçalhos de seção e divisores
          - Guia de edição (modos, tipos de célula)
          - Explicações de algoritmo
          - Descrições de ação
          - Atalhos de teclado

        Inclui sobreposição de escurecimento semitransparente e efeito de sombra no painel.
        """
        w, h = self._win_w, self._win_h
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 170))
        self._screen.blit(dim, (0, 0))

        ox = (w - HELP_W) // 2
        oy = (h - HELP_H) // 2

        # Sombra
        pygame.draw.rect(self._screen, (0, 0, 0),
                         (ox + 6, oy + 6, HELP_W, HELP_H))
        # Painel
        pygame.draw.rect(self._screen, HELP_BG, (ox, oy, HELP_W, HELP_H))
        pygame.draw.rect(self._screen, HELP_BORDER, (ox, oy, HELP_W, HELP_H), width=1)

        # Barra de cabeçalho
        hdr_h = 32
        pygame.draw.rect(self._screen, HELP_BORDER, (ox, oy, HELP_W, hdr_h))

        # Ícone de cabeçalho + título
        icons.draw(self._screen, "help", ox + 10,
                   oy + (hdr_h - MENU_ICON_SZ) // 2, HELP_HDR_FG, MENU_ICON_SZ)
        if self._font_help_title:
            t = self._font_help_title.render("GUIA DE UTILIZACAO", True, HELP_HDR_FG)
            self._screen.blit(t, (ox + 10 + MENU_ICON_SZ + 6,
                                  oy + (hdr_h - t.get_height()) // 2))

        # Botão Fechar [X]
        close_sz = 20
        close_x  = ox + HELP_W - close_sz - 6
        close_y  = oy + (hdr_h - close_sz) // 2
        self._help_close_rect = pygame.Rect(close_x, close_y, close_sz, close_sz)
        mouse = pygame.mouse.get_pos()
        btn_bg = (60, 60, 62) if self._help_close_rect.collidepoint(mouse) else HELP_CLOSE_BG
        pygame.draw.rect(self._screen, btn_bg, self._help_close_rect)
        pygame.draw.rect(self._screen, HELP_BORDER, self._help_close_rect, width=1)
        icons.draw(self._screen, "erase", close_x + 4, close_y + 4,
                   HELP_FG, close_sz - 8)

        # Conteúdo
        pad_x   = ox + 18
        content_y = oy + hdr_h + 12
        max_y   = oy + HELP_H - 40
        cy      = content_y

        for kind, text in _HELP_CONTENT:
            if cy > max_y:
                break
            if kind == "sep":
                cy += 6
                pygame.draw.line(self._screen, HELP_BORDER,
                                 (pad_x, cy), (ox + HELP_W - 18, cy))
                cy += 6
            elif kind == "section":
                if self._font_help_sec:
                    t = self._font_help_sec.render(text, True, HELP_SEC_FG)
                    self._screen.blit(t, (pad_x, cy))
                    cy += t.get_height() + 4
            elif kind == "row":
                if self._font_help_body:
                    t = self._font_help_body.render(text, True, HELP_FG)
                    self._screen.blit(t, (pad_x + 12, cy))
                    cy += t.get_height() + 3

        # Botão Fechar no fundo
        btn_w, btn_h = 100, 26
        btn_x = ox + (HELP_W - btn_w) // 2
        btn_y = oy + HELP_H - btn_h - 10
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_hover = btn_rect.collidepoint(mouse)
        pygame.draw.rect(self._screen, (50, 50, 52) if btn_hover else HELP_CLOSE_BG, btn_rect)
        pygame.draw.rect(self._screen, HELP_BORDER, btn_rect, width=1)
        if self._font_help_body:
            lbl = self._font_help_body.render("Fechar", True, HELP_FG)
            self._screen.blit(lbl, lbl.get_rect(center=btn_rect.center))
        # Fazer botão inferior também fechar
        if btn_rect.collidepoint(mouse):
            self._help_close_rect = btn_rect

    def _draw_tab_bar(self):
        """Desenhar faixa de abas (Grelha | Análise) com aba ativa destacada.

        Aba ativa mostra cor de acento lima e sublinhado. Armazena retângulos de teste de colisão para manipulação de cliques.
        """
        tab_w = 90
        tab_gap = 2
        self._tab_rects = []
        for i, label in enumerate(("Grelha", "Analise")):
            rect = pygame.Rect(
                GRID_X + i * (tab_w + tab_gap), TAB_BAR_Y, tab_w, TAB_BAR_H)
            self._tab_rects.append(rect)
            active = self._active_tab == i
            pygame.draw.rect(self._screen,
                             TAB_ACTIVE_BG if active else TAB_INACTIVE_BG, rect)
            pygame.draw.rect(self._screen, TAB_BORDER, rect, width=1)
            if active:
                pygame.draw.line(self._screen, TAB_ACTIVE_FG,
                                 (rect.x, rect.y), (rect.right - 1, rect.y), 2)
            fg = TAB_ACTIVE_FG if active else TAB_INACTIVE_FG
            t = self._font_menu.render(label, True, fg)
            self._screen.blit(t, t.get_rect(center=rect.center))

    # ── Aba Análise ───────────────────────────────────────────────────────────

    def _draw_analysis_tab(self):
        """Desenhar aba Análise: tabela de métricas seguida por gráficos de barra horizontal.

        Mostra comparação de BFS, Guloso e A* em 5 métricas:
          - Custo Total (custo do caminho)
          - Nos Expandidos (nós explorados)
          - Passos do Caminho (comprimento do caminho)
          - Tempo Computacao (tempo do algoritmo)
          - Tempo de Viagem (duração da animação)

        Implementa deslocamento (roda do rato) e polegar da barra de deslocamento. Melhores valores destacados em lima.
        """
        ax = GRID_X
        ay = GRID_Y
        aw = self._ctrl.rect.x - ax - 12
        ah = self._win_h - ay - 8

        # Fundo
        pygame.draw.rect(self._screen, (15, 15, 17), (ax, ay, aw, ah))
        pygame.draw.rect(self._screen, (40, 40, 42), (ax, ay, aw, ah), width=1)

        # Recorte para área de análise
        clip = pygame.Rect(ax, ay, aw - 8, ah)
        self._screen.set_clip(clip)

        scroll = self._analysis_scroll
        cy = ay + 10 - scroll

        rows = self._last_metric_rows

        # ── Seção tabela de métricas ──────────────────────────────────────────
        cy = self._analysis_section(ax + 8, cy, aw - 16, "METRICAS")
        cy = self._analysis_table(ax + 8, cy, aw - 16, rows)
        cy += 10

        # ── Seção gráficos ────────────────────────────────────────────────────
        cy = self._analysis_section(ax + 8, cy, aw - 16, "GRAFICOS")
        for title, key, is_float in _CHART_DEFS:
            cy = self._analysis_chart(ax + 8, cy, aw - 16, title, key, rows, is_float)

        # Calcular limite de deslocamento
        content_h = (cy + scroll) - ay + 20
        max_scroll = max(0, content_h - ah)
        self._analysis_scroll = min(self._analysis_scroll, max_scroll)

        self._screen.set_clip(None)

        # Barra de deslocamento
        if max_scroll > 0:
            sb_x = ax + aw - 6
            thumb_h = max(20, int(ah * ah / content_h))
            thumb_y = ay + int(scroll * (ah - thumb_h) / max_scroll)
            pygame.draw.rect(self._screen, (30, 30, 32), (sb_x, ay, 5, ah))
            pygame.draw.rect(self._screen, (90, 90, 94), (sb_x, thumb_y, 5, thumb_h))

    def _analysis_section(self, x, y, w, title) -> int:
        """Desenhar cabeçalho de seção (título + separador hairline) e retornar nova posição y.

        Usado para títulos de seção "METRICAS" e "GRAFICOS" na aba Análise.
        """
        pygame.draw.line(self._screen, (40, 40, 42), (x, y + 8), (x + w, y + 8))
        t = self._font_analysis_h.render(title, True, (156, 156, 156))
        self._screen.blit(t, (x, y + 12))
        return y + 28

    def _analysis_table(self, x, y, w, rows) -> int:
        """Desenhar tabela de resultados do algoritmo com 6 colunas e retornar nova posição y.

        Colunas: Algoritmo | Custo | Nos | Passos | Tempo(ms) | Viagem(s)
        - Linha de cabeçalho em fundo escuro
        - Linhas de dados com cor de fundo alternada
        - Melhores valores (por coluna, ao comparar 2+ algoritmos) destacados em lima
        - "---" mostrado para algoritmos que não encontraram caminho

        Quando ≥2 algoritmos executam, destaca o melhor (mínimo) valor em cada coluna.
        """
        font = self._font_analysis
        if not font:
            return y

        col_defs = [
            ("Algoritmo",  0.19, "L"),
            ("Custo",      0.13, "R"),
            ("Nos",        0.12, "R"),
            ("Passos",     0.13, "R"),
            ("Tempo(ms)",  0.15, "R"),
            ("Viagem(s)",  0.28, "R"),
        ]
        cw = [int(w * p) for _, p, _ in col_defs]
        cw[-1] = w - sum(cw[:-1])
        cx = [x + sum(cw[:i]) for i in range(len(cw))]

        hdr_h, row_h = 18, 16
        LIME   = (209, 255,   0)
        CREAM  = (244, 244, 232)
        META   = (156, 156, 156)
        HDR_BG = (  5,   5,   5)
        ROW_BG = [(17, 17, 19), (21, 21, 24)]

        def cell(text, ci, ry, rh, align, fg):
            t = font.render(text, True, fg)
            if align == "L":
                self._screen.blit(t, (cx[ci] + 3, ry + (rh - t.get_height()) // 2))
            else:
                self._screen.blit(t, t.get_rect(
                    right=cx[ci] + cw[ci] - 3, centery=ry + rh // 2))

        # Cabeçalho
        pygame.draw.rect(self._screen, HDR_BG, (x, y, w, hdr_h))
        for i, (hdr, _, align) in enumerate(col_defs):
            cell(hdr, i, y, hdr_h, align, LIME)

        if not rows:
            pygame.draw.rect(self._screen, ROW_BG[0], (x, y + hdr_h, w, row_h))
            t = font.render("Sem resultados.", True, META)
            self._screen.blit(t, (x + 4, y + hdr_h + 2))
            return y + hdr_h + row_h

        valid = [r for r in rows if r["found"]]
        highlight = len(rows) > 1 and len(valid) > 1
        bests: dict = {}
        if highlight and valid:
            bests["cost"]     = min(r["cost"]     for r in valid)
            bests["expanded"] = min(r["expanded"]  for r in valid)
            bests["steps"]    = min(r["steps"]     for r in valid)
            bests["time_ms"]  = min(r["time_ms"]   for r in valid)
            ts = [r["travel_time_s"] for r in valid if r.get("travel_time_s") is not None]
            bests["travel_time_s"] = min(ts) if ts else None

        for ri, row in enumerate(rows):
            ry = y + hdr_h + ri * row_h
            pygame.draw.rect(self._screen, ROW_BG[ri % 2], (x, ry, w, row_h))
            cell(row["algo"], 0, ry, row_h, "L", CREAM)
            if row["found"]:
                ts = row.get("travel_time_s")
                vals = [
                    (1, "cost",          str(int(row["cost"])) if row["cost"] == int(row["cost"]) else f"{row['cost']:.1f}"),
                    (2, "expanded",      str(row["expanded"])),
                    (3, "steps",         str(row["steps"])),
                    (4, "time_ms",       f"{row['time_ms']:.2f}"),
                    (5, "travel_time_s", f"{ts:.1f}" if ts is not None else "---"),
                ]
                for ci, key, text in vals:
                    bv = bests.get(key)
                    rv = row.get(key)
                    is_best = highlight and bv is not None and rv is not None and abs(rv - bv) < 1e-9
                    cell(text, ci, ry, row_h, "R", LIME if is_best else CREAM)
            else:
                for ci in range(1, 6):
                    cell("---", ci, ry, row_h, "R", META)

        total_h = hdr_h + len(rows) * row_h
        pygame.draw.rect(self._screen, (40, 40, 42), (x, y, w, total_h), width=1)
        return y + total_h

    def _analysis_chart(self, x, y, w, title, key, rows, is_float) -> int:
        """Desenhar gráfico de barra horizontal para uma métrica e retornar nova posição y.

        Mostra uma linha por algoritmo:
          - Nome do algoritmo (esquerda)
          - Barra preenchida proporcional ao valor (centro)
          - Texto de valor (direita, com estrela ★ se melhor)

        Largura da barra é proporcional a valor / valor_máx. Melhor valor é destacado
        com estrela e cor lima ao comparar 2+ algoritmos.
        """
        font = self._font_analysis
        LIME  = (209, 255,   0)
        CREAM = (244, 244, 232)
        META  = (156, 156, 156)
        TRACK = ( 25,  25,  28)
        BORD  = ( 40,  40,  42)

        # Título
        t = self._font_analysis_h.render(title, True, LIME)
        self._screen.blit(t, (x, y))
        y += 16

        valid = [r for r in rows if r.get(key) is not None and r["found"]]
        if not valid:
            t = font.render("Sem dados.", True, META)
            self._screen.blit(t, (x + 8, y))
            return y + 20

        max_val = max(r[key] for r in valid) or 1
        best_val = min(r[key] for r in valid)

        label_w = 52
        val_w   = 64
        bar_x   = x + label_w
        bar_max = w - label_w - val_w - 6
        bar_h   = 13
        gap     = 5

        for row in rows:
            color = _ALGO_COLORS.get(row["algo"], (200, 200, 200))
            val   = row.get(key)

            lt = font.render(row["algo"], True, CREAM)
            self._screen.blit(lt, (x, y + (bar_h - lt.get_height()) // 2))

            if val is not None and row["found"]:
                bw = max(1, int(bar_max * val / max_val))
                pygame.draw.rect(self._screen, TRACK, (bar_x, y, bar_max, bar_h))
                pygame.draw.rect(self._screen, color,  (bar_x, y, bw,     bar_h))
                pygame.draw.rect(self._screen, BORD,   (bar_x, y, bar_max, bar_h), width=1)
                is_best = len(valid) > 1 and abs(val - best_val) < 1e-9
                val_str = (f"{val:.2f}" if is_float else str(int(val)))
                if is_best and len(valid) > 1:
                    val_str = "★ " + val_str
                fg = LIME if (is_best and len(valid) > 1) else CREAM
                vt = font.render(val_str, True, fg)
                self._screen.blit(vt, (bar_x + bar_max + 4, y + (bar_h - vt.get_height()) // 2))
            else:
                pygame.draw.rect(self._screen, TRACK, (bar_x, y, bar_max, bar_h))
                nt = font.render("---", True, META)
                self._screen.blit(nt, (bar_x + 4, y + (bar_h - nt.get_height()) // 2))

            y += bar_h + gap

        return y + 8

    def _set_msg(self, text: str, color):
        """Atualizar mensagem de estado (mostrada abaixo da grade na aba Grelha).

        Cor deve ser MSG_OK (sucesso), MSG_ERR (erro) ou MSG_INFO (neutro).
        """
        self._msg       = text
        self._msg_color = color
