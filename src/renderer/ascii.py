from __future__ import annotations
from typing import List, Optional, Tuple
from mazegen.grid import Maze, has_wall, E, S

Coord = Tuple[int, int]

# Cores dinâmicas para as paredes
ANSI_COLORS = {
    "WHITE": "\033[37m",
    "CYAN": "\033[36m",
    "MAGENTA": "\033[35m",
    "YELLOW": "\033[33m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
}

# Cores fixas para elementos específicos
COLOR_ENTRY = "\033[92m"      # Verde
COLOR_EXIT = "\033[91m"       # Vermelho
COLOR_PATH = "\033[94m"       # Azul
COLOR_P42 = "\033[93m"        # Amarelo Brilhante
RESET = "\033[0m"

# Símbolos de renderização
_CELL = "   "
_WALL_H = "---"
_WALL_V = "|"
_CORNER = "+"


def render_ascii(
    maze: Maze,
    solution: Optional[List[Coord]] = None,
    wall_color: str = ANSI_COLORS["WHITE"]
) -> str:
    """Renderiza o labirinto respeitando o alinhamento e cores."""
    sol_set = set(solution) if solution else set()
    lines: List[str] = [_top_border(maze.width, wall_color)]

    for y in range(maze.height):
        lines.append(_row_cells(maze, y, sol_set, wall_color))
        lines.append(_row_bottom(maze, y, wall_color))

    return "\n".join(lines)


def _top_border(width: int, color: str) -> str:
    """Cria a borda superior do labirinto."""
    segment = f"{color}{_WALL_H}{_CORNER}{RESET}"
    return f"{color}{_CORNER}{RESET}{segment * width}"


def _cell_content(coord: Coord, maze: Maze, sol_set: set[Coord]) -> str:
    """Retorna o conteúdo interno de uma célula com cores fixas."""
    if coord == maze.entry:
        return f"{COLOR_ENTRY} E {RESET}"
    if coord == maze.exit:
        return f"{COLOR_EXIT} X {RESET}"
    if coord in sol_set:
        return f"{COLOR_PATH} . {RESET}"
    if coord in maze.blocked:
        return f"{COLOR_P42} 42{RESET}"
    return _CELL


def _row_cells(maze: Maze, y: int, sol_set: set[Coord], color: str) -> str:
    """Renderiza uma linha de células e suas paredes verticais."""
    row = f"{color}{_WALL_V}{RESET}"
    for x in range(maze.width):
        content = _cell_content((x, y), maze, sol_set)
        # Parede Leste (E)
        if has_wall(maze.grid[y][x], E):
            east_wall = f"{color}{_WALL_V}{RESET}"
        else:
            east_wall = " "
        row += f"{content}{east_wall}"
    return row


def _row_bottom(maze: Maze, y: int, color: str) -> str:
    """Renderiza a borda inferior de cada célula da linha."""
    row = f"{color}{_CORNER}{RESET}"
    for x in range(maze.width):
        # Parede Sul (S)
        if has_wall(maze.grid[y][x], S):
            south = f"{color}{_WALL_H}{RESET}"
        else:
            south = "   "
        row += f"{south}{color}{_CORNER}{RESET}"
    return row
