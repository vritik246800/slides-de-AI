"""
Painel de controle da barra lateral para o visualizador de busca de caminhos.

Este módulo:
  - Fornece interface para selecionar modos de edição de grade (início, objetivo, obstáculo, etc.)
  - Permite seleção de algoritmo (BFS, Guloso, A*)
  - Mostra controles de dimensão de grade (redimensionar com botões +/-)
  - Renderiza botões de ação (Executar, Executar Todos, Animar, Limpar Caminho, Limpar Tudo)
  - Exibe tabela de métricas comparando resultados de algoritmo
  - Mostra legenda de cores explicando todos tipos de célula e marcadores

O painel é desenhado como barra lateral vertical no lado direito da janela.
Todo o texto está em português. As cores seguem a paleta AIOX dark-cockpit.
Botões destacam quando ativos (texto lima em fundo escuro).
"""
from __future__ import annotations
import pygame

# ── Paleta AIOX Dark Cockpit ─────────────────────────────────────────────────
NEAR_BLACK   = (  5,   5,   5)   # #050505 canvas
SURFACE      = ( 17,  17,  19)   # #111113 surface-panel
SURFACE_CARD = ( 15,  15,  17)   # #0F0F11 surface-dark
SURFACE_ELEV = ( 21,  21,  24)   # #151518 surface-hover
LIME         = (209, 255,   0)   # #D1FF00 acento primário
CREAM        = (244, 244, 232)   # #F4F4E8 texto primeiro plano
FG_META      = (156, 156, 156)   # #9C9C9C texto mudo
FLARE        = (237,  70,   9)   # #ED4609 destrutivo
BLUE_INFO    = (  0, 153, 255)   # #0099FF informativo
SUCCESS      = ( 34, 197,  94)   # #22C55E sucesso
GOLD         = (251, 191,  36)   # #FBBF24 aviso ouro
HAIRLINE     = ( 40,  40,  42)   # hairline borda (rgba 156,156,156 .15 aprox)

PANEL_BG = SURFACE_CARD
DARK     = CREAM
GRAY     = FG_META
WHITE    = CREAM

C_BLUE   = BLUE_INFO
C_PURPLE = SURFACE_ELEV
C_GREEN  = SUCCESS
C_RED    = FLARE
C_ORANGE = GOLD
C_TEAL   = BLUE_INFO

# ── Tabela de métricas ─────────────────────────────────────────────────────────
_TBL_HDR_BG  = NEAR_BLACK
_TBL_HDR_FG  = LIME
_TBL_ROW_BG  = [SURFACE, SURFACE_ELEV]
_TBL_FG      = CREAM
_TBL_BEST    = LIME
_TBL_NONE    = FG_META
_TBL_LINE    = HAIRLINE

# col: (cabeçalho, proporção da largura, alinhamento E/D)
_TCOLS = [
    ("Algoritmo",  0.19, "E"),
    ("Custo",      0.13, "D"),
    ("Nos",        0.12, "D"),
    ("Passos",     0.13, "D"),
    ("Tempo(ms)",  0.15, "D"),
    ("Viagem(s)",  0.28, "D"),
]

# ── Legenda ────────────────────────────────────────────────────────────────────
LEGEND = [
    (( 17,  17,  19), "Livre (c=1)"),
    (( 61,  61,  61), "Obstáculo"),
    (( 40,  40,  42), "Difícil (c=3)"),
    ((237,  70,   9), "Armadilha (c=5)"),
    ((251, 191,  36), "Inimigo"),
    ((209, 255,   0), "Início (S)"),
    ((  0, 153, 255), "Objetivo (G)"),
    ((209, 255,   0), "Caminho"),
    (( 65,  77,  14), "Explorado"),
    ((237,  70,   9), "Morto"),
]
_LEG_PER_ROW = 3

MODES = [
    ("Inicio (S)",  "start"),
    ("Objetivo (G)","goal"),
    ("Obstaculo",   "obstacle"),
    ("Dificil",     "difficult"),
    ("Armadilha",   "trap"),
    ("Inimigo",     "enemy"),
    ("Apagar",      "erase"),
]

ALGOS = ["BFS", "Greedy", "A*"]

_MAX_ROWS = 100
_MAX_COLS = 100
_MIN_DIM  = 3


class _Btn:
    """Simples widget de botão com rótulo de texto e estado ativo.

    Atributos:
      - rect: pygame.Rect para posição e tamanho
      - label: texto de exibição
      - bg, fg: cores de fundo e primeiro plano (usadas quando inativo)
      - value: string identificadora (retornada ao aplicativo ao clicar; padrão é rótulo)
      - active: True se este botão está selecionado (exclusivo de grupo)

    Quando active=True, botão exibe fundo lima com texto preto.
    Quando active=False, botão usa cores bg/fg especificadas.
    """

    def __init__(self, rect, label, bg, fg=CREAM, value=None):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.bg     = bg
        self.fg     = fg
        self.value  = value if value is not None else label
        self.active = False

    def draw(self, surf, font):
        """Renderizar botão para superfície com estilo ativo/inativo."""
        if self.active:
            bg, fg = LIME, NEAR_BLACK
        else:
            bg, fg = self.bg, self.fg
        pygame.draw.rect(surf, bg, self.rect)
        pygame.draw.rect(surf, HAIRLINE, self.rect, width=1)
        if font:
            txt = font.render(self.label, True, fg)
            surf.blit(txt, txt.get_rect(center=self.rect.center))

    def hit(self, pos):
        """Verificar se posição de rato está dentro retângulo do botão."""
        return self.rect.collidepoint(pos)


class ControlsPanel:
    """Barra lateral direita contendo todos controles de edição de grade e algoritmo.

    Seções (topo para fundo):
      1. MODO DE EDICAO: 7 botões (2 colunas) para seleção de tipo de célula
      2. ALGORITMO: 3 botões para seleção BFS, Guloso, A*
      3. TAMANHO (máx 100x100): botões +/- para linhas e colunas
      4. ACOES: 5 botões de ação (Executar, Executar Todos, Animar, Limpar Caminho, Limpar Tudo)
      5. METRICAS: Tabela compacta comparando resultados de algoritmo
      6. LEGENDA: Chave de cores explicando todos tipos de célula e marcadores

    Grupos de botões são mutuamente exclusivos (ativar um desativa outros no grupo).
    Tabela de métricas exibe melhores valores destacados em lima ao comparar 2+ algoritmos.
    Legenda é ancorada no fundo do painel e desliza com redimensionamento.

    Estado:
      - _mode_btns, _algo_btns: grupos de botões exclusivos
      - _action_btns: botões não-exclusivos (cada um mapeado para string de ação)
      - _metric_rows: lista de dicionários de Metrics.to_rows()
      - _rows, _cols: mudanças de dimensão de grade pendentes (aplicadas via ação redimensionar)
    """

    def __init__(self, x: int, y: int, w: int, h: int,
                 initial_rows: int = 15, initial_cols: int = 18):
        self.rect  = pygame.Rect(x, y, w, h)
        self._x    = x
        self._y    = y
        self._w    = w
        self._h    = h

        self._rows = initial_rows
        self._cols = initial_cols

        self._metric_rows: list = []

        self._mode_btns:   list[_Btn]             = []
        self._algo_btns:   list[_Btn]             = []
        self._action_btns: list[tuple[_Btn, str]] = []
        self._resize_btns: list[tuple[_Btn, str]] = []

        self._font_title: pygame.font.Font | None = None
        self._font_btn:   pygame.font.Font | None = None
        self._font_small: pygame.font.Font | None = None

        self._build()

    # ── Público ────────────────────────────────────────────────────────────────

    def init_fonts(self):
        """Inicializar fontes para títulos de seção, botões e tabela de métricas."""
        self._font_title = pygame.font.SysFont("Menlo, Courier New, monospace", 11, bold=True)
        self._font_btn   = pygame.font.SysFont("Menlo, Courier New, monospace", 11)
        self._font_small = pygame.font.SysFont("Menlo, Courier New, monospace", 10)

    @property
    def mode(self) -> str:
        """Retornar modo de edição atualmente selecionado (por ex, 'start', 'obstacle', 'erase')."""
        for b in self._mode_btns:
            if b.active:
                return b.value
        return "obstacle"

    @property
    def algorithm(self) -> str:
        """Retornar algoritmo atualmente selecionado (BFS, Guloso ou A*)."""
        for b in self._algo_btns:
            if b.active:
                return b.value
        return "A*"

    @property
    def pending_rows(self) -> int:
        """Retornar contagem de linhas pendentes (modificada por botões +/-, aplicada via ação redimensionar)."""
        return self._rows

    @property
    def pending_cols(self) -> int:
        """Retornar contagem de colunas pendentes (modificada por botões +/-, aplicada via ação redimensionar)."""
        return self._cols

    def set_grid_size(self, rows: int, cols: int):
        """Atualizar dimensões de grade exibidas (chamado após grade redimensionar)."""
        self._rows = rows
        self._cols = cols

    def update_geometry(self, x: int, y: int, w: int, h: int):
        """Reposicionar e redimensionar painel (chamado quando divisor é arrastado).

        Reconstrói todos layouts de botão com base em novas dimensões.
        """
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self.rect = pygame.Rect(x, y, w, h)
        self._mode_btns   = []
        self._algo_btns   = []
        self._action_btns = []
        self._resize_btns = []
        self._build()

    def set_metrics(self, rows: list):
        """Atualizar tabela de métricas com resultados de comparação de Metrics.to_rows()."""
        self._metric_rows = rows if rows else []

    def handle_click(self, pos) -> str | None:
        """Processar clique de rato em botões do painel.

        Retorna string de ação se botão de ação clicado (por ex, 'run', 'animate').
        Retorna 'resize' se botão redimensionar clicado.
        Retorna None se botão modo/algoritmo clicado (muda apenas estado, nenhuma ação).
        """
        for b in self._mode_btns:
            if b.hit(pos):
                for bb in self._mode_btns:
                    bb.active = False
                b.active = True
                return None

        for b in self._algo_btns:
            if b.hit(pos):
                for bb in self._algo_btns:
                    bb.active = False
                b.active = True
                return None

        # Botões redimensionar (+/- para linhas e colunas)
        for b, action in self._resize_btns:
            if b.hit(pos):
                if action == "rows_minus":
                    self._rows = max(_MIN_DIM, self._rows - 1)
                elif action == "rows_plus":
                    self._rows = min(_MAX_ROWS, self._rows + 1)
                elif action == "cols_minus":
                    self._cols = max(_MIN_DIM, self._cols - 1)
                elif action == "cols_plus":
                    self._cols = min(_MAX_COLS, self._cols + 1)
                return "resize"

        # Botões de ação (Executar, Executar Todos, Animar, Limpar Caminho, Limpar Tudo)
        for b, action in self._action_btns:
            if b.hit(pos):
                return action

        return None

    def draw(self, surf):
        """Renderizar painel de controle inteiro para superfície.

        Desenha fundo, todas seções (modo, algoritmo, redimensionar, ações, métricas),
        e legenda no fundo. Legenda é ancorada no fundo do painel e escala com redimensionamento.
        """
        pygame.draw.rect(surf, PANEL_BG, self.rect)
        pygame.draw.rect(surf, HAIRLINE, self.rect, width=1)

        self._draw_section(surf, "MODO DE EDICAO", self._mode_section_y)
        for b in self._mode_btns:
            b.draw(surf, self._font_btn)

        self._draw_sep(surf, self._algo_sep_y)
        self._draw_section(surf, "ALGORITMO", self._algo_section_y)
        for b in self._algo_btns:
            b.draw(surf, self._font_btn)

        self._draw_sep(surf, self._resize_sep_y)
        self._draw_section(surf, "TAMANHO  (max 100x100)", self._resize_section_y)
        self._draw_resize_controls(surf)

        self._draw_sep(surf, self._action_sep_y)
        self._draw_section(surf, "ACOES", self._action_section_y)
        for b, _ in self._action_btns:
            b.draw(surf, self._font_btn)

        self._draw_sep(surf, self._metrics_sep_y)
        self._draw_section(surf, "METRICAS", self._metrics_section_y)
        tbl_y = self._metrics_section_y + 18
        tbl_x = self._x + 6
        tbl_w = self._w - 12
        self._draw_metrics_table(surf, tbl_x, tbl_y, tbl_w)

        # Legend anchored at bottom of panel
        leg_rows = (len(LEGEND) + _LEG_PER_ROW - 1) // _LEG_PER_ROW
        leg_h    = leg_rows * 17 + 20   # rows × row_h + title
        leg_y    = self.rect.bottom - leg_h - 6
        self._draw_sep(surf, leg_y - 6)
        self._draw_section(surf, "LEGENDA", leg_y)
        self._draw_legend(surf, leg_y + 18)

    # ── Construção interna ────────────────────────────────────────────────────

    def _build(self):
        """Construir todos botões e calcular posições de disposição com base em tamanho de painel.

        Chamado na inicialização e após atualização de geometria (redimensionamento de janela/divisor).
        Calcula posições de botão, tamanhos e coordenadas y para cada seção.
        """
        x, w = self._x + 6, self._w - 12
        y = self._y + 6

        # Mode section
        self._mode_section_y = y
        y += 18
        bw = (w - 4) // 2
        for i, (label, value) in enumerate(MODES):
            bx = x + (i % 2) * (bw + 4)
            by = y + (i // 2) * 28
            b  = _Btn((bx, by, bw, 24), label, SURFACE, CREAM, value=value)
            if value == "obstacle":
                b.active = True
            self._mode_btns.append(b)
        y += ((len(MODES) + 1) // 2) * 28 + 4

        # Algo section
        self._algo_sep_y = y
        y += 10
        self._algo_section_y = y
        y += 18
        aw = (w - 2 * 4) // 3
        for i, algo in enumerate(ALGOS):
            bx = x + i * (aw + 4)
            b  = _Btn((bx, y, aw, 24), algo, SURFACE, CREAM, value=algo)
            if algo == "A*":
                b.active = True
            self._algo_btns.append(b)
        y += 28 + 4

        # Resize section
        self._resize_sep_y = y
        y += 10
        self._resize_section_y = y
        y += 18

        half_w = (w - 4) // 2
        bsz    = 26

        btn_rows_minus = _Btn((x,                y, bsz, 24), "-", FLARE,   CREAM, value="rows_minus")
        btn_rows_plus  = _Btn((x + half_w - bsz, y, bsz, 24), "+", SUCCESS, NEAR_BLACK, value="rows_plus")
        cx2 = x + half_w + 4
        btn_cols_minus = _Btn((cx2,                    y, bsz, 24), "-", FLARE,   CREAM, value="cols_minus")
        btn_cols_plus  = _Btn((cx2 + half_w - bsz,     y, bsz, 24), "+", SUCCESS, NEAR_BLACK, value="cols_plus")

        self._resize_btns   = [
            (btn_rows_minus, "rows_minus"),
            (btn_rows_plus,  "rows_plus"),
            (btn_cols_minus, "cols_minus"),
            (btn_cols_plus,  "cols_plus"),
        ]
        self._resize_lx     = x
        self._resize_cx     = cx2
        self._resize_half_w = half_w
        self._resize_bsz    = bsz
        self._resize_btns_y = y
        y += 28 + 4

        # Action section
        self._action_sep_y = y
        y += 10
        self._action_section_y = y
        y += 18
        actions = [
            ("Executar",       "run",        LIME,         NEAR_BLACK),
            ("Executar Todos", "run_all",    SURFACE_ELEV, CREAM),
            ("Animar Caminho", "animate",    BLUE_INFO,    NEAR_BLACK),
            ("Limpar Caminho", "clear_path", SURFACE,      CREAM),
            ("Limpar Tudo",    "clear_all",  FLARE,        CREAM),
        ]
        for label, key, bg, fg in actions:
            b = _Btn((x, y, w, 26), label, bg, fg)
            self._action_btns.append((b, key))
            y += 30

        # Metrics section
        self._metrics_sep_y    = y
        y += 10
        self._metrics_section_y = y

    # ── Ajudantes de desenho ───────────────────────────────────────────────────

    def _draw_resize_controls(self, surf):
        """Desenhar controles de dimensão de grade (botões +/- e rótulos de tamanho atual)."""
        for b, _ in self._resize_btns:
            b.draw(surf, self._font_btn)
        if not self._font_btn:
            return
        bsz = self._resize_bsz
        by  = self._resize_btns_y
        rows_t = self._font_btn.render(f"Lin: {self._rows:3d}", True, CREAM)
        surf.blit(rows_t, (self._resize_lx + bsz + 4, by + 5))
        cols_t = self._font_btn.render(f"Col: {self._cols:3d}", True, CREAM)
        surf.blit(cols_t, (self._resize_cx + bsz + 4, by + 5))

    def _draw_metrics_table(self, surf, x: int, y: int, w: int):
        """Desenhar tabela de comparação compacta de resultados de algoritmo.

        Estrutura da tabela:
          - Linha de cabeçalho: Algoritmo | Custo | Nos | Passos | Tempo(ms) | Viagem(s)
          - Linhas de dados: uma por algoritmo (BFS, Guloso, A*)
          - Melhores valores destacados em lima ao comparar 2+ algoritmos
          - Cores de linha alternadas para legibilidade
          - Linhas de grade separam linhas e colunas
        """
        rows = self._metric_rows
        font = self._font_small
        if not font:
            return

        if not rows:
            t = font.render("Sem resultados.", True, GRAY)
            surf.blit(t, (x + 4, y + 4))
            return

        # Larguras de coluna a partir de proporções
        cw = [int(w * p) for _, p, _ in _TCOLS]
        cw[-1] = w - sum(cw[:-1])
        cx = [x + sum(cw[:i]) for i in range(len(cw))]

        hdr_h = 20
        row_h = 18

        # Detecção de melhor valor (apenas destacar ao comparar ≥2 algos)
        valid = [r for r in rows if r["found"]]
        bests: dict = {}
        highlight = len(rows) > 1 and len(valid) > 1
        if highlight and valid:
            bests["cost"]          = min(r["cost"]          for r in valid)
            bests["expanded"]      = min(r["expanded"]       for r in valid)
            bests["steps"]         = min(r["steps"]          for r in valid)
            bests["time_ms"]       = min(r["time_ms"]        for r in valid)
            ts = [r["travel_time_s"] for r in valid if r.get("travel_time_s") is not None]
            bests["travel_time_s"] = min(ts) if ts else None

        def _cell(text, ci, ry, rh, align, fg):
            t = font.render(text, True, fg)
            if align == "E":
                surf.blit(t, (cx[ci] + 3, ry + (rh - t.get_height()) // 2))
            else:
                surf.blit(t, t.get_rect(right=cx[ci] + cw[ci] - 3,
                                        centery=ry + rh // 2))

        # Linha de cabeçalho
        pygame.draw.rect(surf, _TBL_HDR_BG, (x, y, w, hdr_h))
        for i, (hdr, _, align) in enumerate(_TCOLS):
            _cell(hdr, i, y, hdr_h, align, _TBL_HDR_FG)

        # Linhas de dados
        for ri, row in enumerate(rows):
            ry = y + hdr_h + ri * row_h
            pygame.draw.rect(surf, _TBL_ROW_BG[ri % 2], (x, ry, w, row_h))

            _cell(row["algo"], 0, ry, row_h, "E", _TBL_FG)

            if row["found"]:
                cost_str  = str(int(row["cost"])) if row["cost"] == int(row["cost"]) else f"{row['cost']:.1f}"
                steps_str = str(row["steps"])
                exp_str   = str(row["expanded"])
                time_str  = f"{row['time_ms']:.2f}"
                ts = row.get("travel_time_s")
                anim_str  = f"{ts:.1f}" if ts is not None else "---"

                pairs = [
                    (1, "cost",          cost_str),
                    (2, "expanded",      exp_str),
                    (3, "steps",         steps_str),
                    (4, "time_ms",       time_str),
                    (5, "travel_time_s", anim_str),
                ]
                for ci, key, text in pairs:
                    bv = bests.get(key)
                    rv = row.get(key)
                    is_best = (highlight and bv is not None and rv is not None
                               and abs(rv - bv) < 1e-9)
                    _cell(text, ci, ry, row_h, "D", _TBL_BEST if is_best else _TBL_FG)
            else:
                for ci in range(1, 6):
                    _cell("---", ci, ry, row_h, "D", _TBL_NONE)

        # Linhas de grade
        total_h = hdr_h + len(rows) * row_h
        # horizontal
        for ri in range(len(rows) + 1):
            ly = y + hdr_h + ri * row_h
            pygame.draw.line(surf, _TBL_LINE, (x, ly), (x + w, ly))
        # vertical (pular separador primeira coluna para legibilidade)
        for i in range(1, len(_TCOLS)):
            vx = cx[i]
            pygame.draw.line(surf, _TBL_LINE, (vx, y), (vx, y + total_h))
        # borda
        pygame.draw.rect(surf, _TBL_LINE, (x, y, w, total_h), width=1)

    def _draw_section(self, surf, title, ty):
        """Desenhar texto de cabeçalho de seção (por ex, 'MODO DE EDICAO', 'ALGORITMO')."""
        if self._font_title:
            t = self._font_title.render(title, True, FG_META)
            surf.blit(t, (self._x + 6, ty))

    def _draw_sep(self, surf, sy):
        """Desenhar linha separadora horizontal entre seções."""
        pygame.draw.line(surf, HAIRLINE,
                         (self._x + 4, sy + 4),
                         (self._x + self._w - 4, sy + 4))

    def _draw_legend(self, surf, start_y: int):
        """Desenhar legenda de cores (3 colunas) explicando todos tipos de célula e marcadores.

        Cada entrada de legenda é um pequeno quadrado colorido com rótulo.
        Legenda é ancorada no fundo do painel e escala com largura do painel.
        """
        total_w  = self._w - 12
        cell_w   = total_w // _LEG_PER_ROW
        x        = self._x + 6
        for i, (color, label) in enumerate(LEGEND):
            col = i % _LEG_PER_ROW
            row = i // _LEG_PER_ROW
            lx  = x + col * cell_w
            ly  = start_y + row * 17
            pygame.draw.rect(surf, color,   (lx, ly + 2, 11, 11))
            pygame.draw.rect(surf, FG_META, (lx, ly + 2, 11, 11), width=1)
            if self._font_small:
                txt = self._font_small.render(label, True, CREAM)
                surf.blit(txt, (lx + 14, ly + 1))
