from __future__ import annotations
from typing import List, Optional, Tuple
from mazegen.grid import Maze, has_wall, E, S

Coord = Tuple[int, int]

# Rendering constants
_CELL   = "   "
_WALL_H = "---"
_WALL_V = "|"
_CORNER = "+"
_ENTRY  = " E "
_EXIT   = " X "
_PATH   = " . "


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

def _top_border(width: int) -> str:
    # Builds the top edge: +---+---+---+
    return _CORNER + (_WALL_H + _CORNER) * width


def _cell_content(coord: Coord, maze: Maze, sol_set: set) -> str:
    # Returns the display content for a single cell
    if coord == maze.entry:
        return _ENTRY
    if coord == maze.exit:
        return _EXIT
    if coord in sol_set:
        return _PATH  # Cell is part of the solution path
    return _CELL      # Empty cell


def _row_cells(maze: Maze, y: int, sol_set: set) -> str:
    # Builds a row of cells with their east walls: | E | . |   |
    row = _WALL_V
    for x in range(maze.width):
        content = _cell_content((x, y), maze, sol_set)
        # Use a wall character if east wall exists, otherwise open space
        east_wall = _WALL_V if has_wall(maze.grid[y][x], E) else " "
        row += content + east_wall
    return row


def _row_bottom(maze: Maze, y: int) -> str:
    # Builds the bottom border of a row: +---+   +---+
    row = _CORNER
    for x in range(maze.width):
        # Use a wall segment if south wall exists, otherwise open space
        south = _WALL_H if has_wall(maze.grid[y][x], S) else _CELL
        row += south + _CORNER
    return row