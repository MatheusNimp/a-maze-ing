from __future__ import annotations
from typing import List, Optional, Tuple
from mazegen.grid import Maze, has_wall, E, S

Coord = Tuple[int, int]

ANSI_COLORS = {
    "RESET": "\033[0m",
    "WALL": "\033[37m",
    "PATH": "\033[92m",
    "ENTRY": "\033[94m",
    "EXIT": "\033[91m",
    "PATTERN42": "\033[93m"
}

# Rendering constants
_CELL = "   "
_WALL_H = "---"
_WALL_V = "|"
_CORNER = "+"
_ENTRY = " E "
_EXIT = " X "
_PATH = " . "


def render_ascii(
    maze: Maze,
    solution: Optional[List[Coord]] = None,
) -> str:
    """Render a maze as ASCII art.

    Args:
        maze:     The maze to be rendered.
        solution: List of (x, y) coordinates representing the solution path.
                  If None, no path is displayed.

    Returns:
        A string with the maze ready to print.
    """
    # Convert solution list to a set for O(1) lookups
    sol_set = set(solution) if solution else set()

    # Start with the top border
    lines: List[str] = [_top_border(maze.width)]

    # Add a cell row and a bottom border row for each maze row
    for y in range(maze.height):
        lines.append(_row_cells(maze, y, sol_set))
        lines.append(_row_bottom(maze, y))

    # Join all rows into a single string separated by newlines
    return "\n".join(lines)


# ── helpers ──────────────────────────────────────────────────────────────────
def paint(text: str, color_name: str) -> str:
    color_code = ANSI_COLORS.get(color_name, ANSI_COLORS["RESET"])
    # Apply a color to a text
    return f"{color_code}{text}{ANSI_COLORS['RESET']}"


def _top_border(width: int) -> str:
    # Builds the top edge: +---+---+---+
    return _CORNER + (_WALL_H + _CORNER) * width


def _cell_content(coord: Coord, maze: Maze, sol_set: set) -> str:
    if coord == maze.entry:
        return f"{ANSI_COLORS['ENTRY']}{_ENTRY}{ANSI_COLORS['RESET']}"
    if coord == maze.exit:
        return f"{ANSI_COLORS['EXIT']}{_EXIT}{ANSI_COLORS['RESET']}"

    if coord in sol_set:
        return f"{ANSI_COLORS['PATH']}{_PATH}{ANSI_COLORS['RESET']}"

    if coord in maze.blocked:
        return f"{ANSI_COLORS['PATTERN42']} 42{ANSI_COLORS['RESET']}"

    return _CELL


def _row_cells(maze: Maze, y: int, sol_set: set) -> str:
    # Builds a row of cells with their east walls: | E | . |   |
    row = paint(_WALL_V, "WALL")
    for x in range(maze.width):
        content = _cell_content((x, y), maze, sol_set)
        # Use a wall character if east wall exists, otherwise open space
        east_wall = (
            paint(_WALL_V, "WALL")
            if has_wall(maze.grid[y][x], E)
            else "   "
        )
        row += content + east_wall
    return row


def _row_bottom(maze: Maze, y: int) -> str:
    # Builds the bottom border of a row: +---+   +---+
    row = paint(_CORNER, "WALL")
    for x in range(maze.width):
        # Use a wall segment if south wall exists, otherwise open space
        south = (
            paint(_WALL_H, "WALL")
            if has_wall(maze.grid[y][x], S)
            else "   "
        )
        row += south + _CORNER
    return row