from __future__ import annotations

from typing import List

from .grid import Maze


def maze_to_hex_lines(maze: Maze) -> List[str]:
    """
    Convert maze.grid (values 0..15) into a list of uppercase hex strings.

    Each row in maze.grid becomes one string.
    Each cell becomes a single hex digit (0-9, A-F).
    """
    lines: List[str] = []

    for row in maze.grid:
        # Convert each cell (int 0..15) to a single uppercase hex digit
        line = "".join(format(cell, "X") for cell in row)
        lines.append(line)

    return lines
