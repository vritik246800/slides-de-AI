"""
Ícones desenhados vetorialmente renderizados com Pygame (sem emoji, sem ficheiros de imagem externos).

Este módulo fornece um conjunto de pequenos ícones vetoriais usados em toda a interface:
  - Operações de ficheiro: guardar, carregar, apagar
  - Edição: apagar (X)
  - Ações: ajuda, executar (triângulo de reprodução), animar (quadros de filme), limpar_caminho
  - Marcadores: início (bandeira), objetivo (alvo)

Cada ícone é desenhado como forma vetorial escalável com:
  - Posição superior-esquerda (x, y)
  - Cor (tupla RGB)
  - Tamanho (largura = altura, padrão 11px)

Ícones são desenhados com contornos (traços 1px) para visibilidade em tamanhos pequenos.
Todos os ícones estão centrados dentro seu quadrado delimitador.
"""
from __future__ import annotations
import math
import pygame


def draw(surf: pygame.Surface, name: str, x: int, y: int,
         color: tuple, size: int = 11) -> None:
    """Desenhar ícone vetorial por nome para a superfície.

    Parâmetros:
      - surf: superfície Pygame para desenhar
      - name: identificador do ícone (por ex, 'save', 'open', 'run', 'help')
      - x, y: posição em pixels superior-esquerda do quadrado delimitador do ícone
      - color: tupla RGB (por ex, (209, 255, 0) para lima)
      - size: largura/altura em pixels (padrão 11); dimensiona o ícone inteiro

    Ícones disponíveis:
      save, open, trash, erase, help, file, run, animate, clear_path, start, goal

    Se nome não for reconhecido, nada é desenhado.
    """
    w = h = size
    fns = {
        "save":       _save,
        "open":       _open,
        "trash":      _trash,
        "erase":      _erase,
        "help":       _help,
        "file":       _file,
        "run":        _run,
        "animate":    _animate,
        "clear_path": _clear_path,
        "start":      _flag,
        "goal":       _target,
    }
    fn = fns.get(name)
    if fn:
        fn(surf, x, y, w, h, color)


# ── Desenhadores de ícone individual ──────────────────────────────────────────
# Cada função desenha um tipo de ícone. Todas recebem (surf, x, y, w, h, color).
# Ícones são desenhados como contornos (traços) para clareza em tamanhos pequenos.

def _save(surf, x, y, w, h, c):
    """Desenhar ícone de disco flexível (guardar).

    Mostra quadrado com retângulo preenchido menor (área de rótulo) no topo
    e área de armazenamento no meio.
    """
    pygame.draw.rect(surf, c, (x, y, w, h), 1)
    fold = max(2, w // 3)
    pygame.draw.rect(surf, c, (x + 1, y + 1, w - fold - 1, h // 3))
    pygame.draw.rect(surf, c, (x + 2, y + h // 2 + 1, w - 4, h // 3), 1)


def _open(surf, x, y, w, h, c):
    """Desenhar ícone de pasta (carregar).

    Mostra contorno de pasta com aba no topo-esquerda (como aba de ficheiro).
    """
    tab_w = w // 2
    tab_h = max(2, h // 4)
    body_y = y + tab_h
    body_h = h - tab_h
    pygame.draw.rect(surf, c, (x, body_y, w, body_h), 1)
    pygame.draw.polygon(surf, c, [
        (x, body_y), (x + tab_w, body_y),
        (x + tab_w, y), (x, y),
    ], 0)


def _trash(surf, x, y, w, h, c):
    """Desenhar ícone de cesto de lixo (apagar).

    Mostra lata de lixo com tampa no topo, corpo abaixo e linha divisória no centro.
    """
    lid_y = y + 2
    pygame.draw.line(surf, c, (x, lid_y), (x + w, lid_y), 1)
    mx = x + w // 2
    pygame.draw.line(surf, c, (mx - 2, y), (mx + 2, y), 1)
    body_y = lid_y + 2
    pygame.draw.rect(surf, c, (x + 1, body_y, w - 2, h - body_y + y), 1)
    pygame.draw.line(surf, c, (mx, body_y + 2), (mx, y + h - 2), 1)


def _erase(surf, x, y, w, h, c):
    """Desenhar ícone X em negrito (fechar/apagar).

    Duas linhas diagonais cruzando para formar forma X.
    """
    pygame.draw.line(surf, c, (x + 1, y + 1), (x + w - 2, y + h - 2), 2)
    pygame.draw.line(surf, c, (x + w - 2, y + 1), (x + 1, y + h - 2), 2)


def _help(surf, x, y, w, h, c):
    """Desenhar ícone de ponto de interrogação (ajuda).

    Contorno de círculo com forma '?' dentro: arco para parte superior, linha para haste,
    e ponto para base.
    """
    r = min(w, h) // 2 - 1
    cx = x + w // 2
    cy = y + h // 2
    pygame.draw.circle(surf, c, (cx, cy), r, 1)
    # arco do '?'
    arc_rect = pygame.Rect(cx - 2, cy - r + 2, 5, 4)
    pygame.draw.arc(surf, c, arc_rect, 0, math.pi, 1)
    pygame.draw.line(surf, c, (cx, cy - r + 6), (cx, cy + 1), 1)
    pygame.draw.circle(surf, c, (cx, cy + 3), 1, 0)


def _file(surf, x, y, w, h, c):
    """Desenhar ícone de documento (ficheiro).

    Retângulo com canto dobrado no topo-direito e linhas de texto no corpo.
    """
    fold = max(2, w // 3)
    pts = [
        (x, y), (x + w - fold, y),
        (x + w, y + fold), (x + w, y + h),
        (x, y + h),
    ]
    pygame.draw.polygon(surf, c, pts, 1)
    pygame.draw.line(surf, c, (x + w - fold, y), (x + w - fold, y + fold), 1)
    pygame.draw.line(surf, c, (x + w - fold, y + fold), (x + w, y + fold), 1)
    mid = y + h // 2
    pygame.draw.line(surf, c, (x + 2, mid), (x + w - fold - 1, mid), 1)
    pygame.draw.line(surf, c, (x + 2, mid + 3), (x + w - fold - 1, mid + 3), 1)


def _run(surf, x, y, w, h, c):
    """Desenhar ícone de reprodução (executar).

    Triângulo preenchido apontando para a direita (forma de botão de reprodução).
    """
    pygame.draw.polygon(surf, c, [
        (x + 1, y + 1),
        (x + 1, y + h - 2),
        (x + w - 1, y + h // 2),
    ])


def _animate(surf, x, y, w, h, c):
    """Desenhar ícone de quadros de filme (animar).

    Três retângulos lado-a-lado, representando quadros de vídeo ou cronograma de animação.
    """
    fw = max(2, (w - 4) // 3)
    for i in range(3):
        fx = x + i * (fw + 2)
        pygame.draw.rect(surf, c, (fx, y + 2, fw, h - 4), 1)


def _clear_path(surf, x, y, w, h, c):
    """Desenhar ícone de linha tracejada com X (limpar caminho).

    Linha tracejada horizontal com X na extremidade direita (representando remoção de caminho).
    """
    my = y + h // 2
    for i in range(0, w - 5, 3):
        pygame.draw.line(surf, c, (x + i, my), (x + i + 1, my), 1)
    ex = x + w - 4
    pygame.draw.line(surf, c, (ex, my - 2), (ex + 3, my + 2), 1)
    pygame.draw.line(surf, c, (ex + 3, my - 2), (ex, my + 2), 1)


def _flag(surf, x, y, w, h, c):
    """Desenhar ícone de bandeira (marcador de início).

    Poste vertical com bandeira triangular no topo (indicador de ponto inicial).
    """
    pygame.draw.line(surf, c, (x + 1, y), (x + 1, y + h - 1), 1)
    pygame.draw.polygon(surf, c, [
        (x + 1, y), (x + w - 1, y + 3), (x + 1, y + 6),
    ])


def _target(surf, x, y, w, h, c):
    """Desenhar ícone de alvo (marcador de objetivo).

    Círculos concêntricos: anel externo, anel interno e ponto central.
    Representa alvo de tiro ao arco ou marcador de objetivo.
    """
    cx = x + w // 2
    cy = y + h // 2
    r_outer = min(w, h) // 2 - 1
    pygame.draw.circle(surf, c, (cx, cy), r_outer, 1)
    if r_outer > 3:
        pygame.draw.circle(surf, c, (cx, cy), r_outer - 3, 1)
    pygame.draw.circle(surf, c, (cx, cy), 1, 0)
