from __future__ import annotations

from .grid import Maze, N, E, S, W, has_wall


def validate_maze(maze: Maze) -> None:
    """
    Validate maze structural integrity.

    Raises ValueError if invalid.
    """
    _validate_dimensions(maze)
    _validate_cells_range(maze)
    _validate_borders_closed(maze)
    _validate_neighbor_coherence(maze)


def _validate_dimensions(maze: Maze) -> None:
    if maze.width <= 0 or maze.height <= 0:
        raise ValueError("Maze dimensions must be > 0")

    if len(maze.grid) != maze.height:
        raise ValueError("Grid height does not match maze.height")

    for y, row in enumerate(maze.grid):
        if len(row) != maze.width:
            raise ValueError(f"Grid width mismatch at row y={y}")


def _validate_cells_range(maze: Maze) -> None:
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            if not (0 <= cell <= 15):
                raise ValueError(
                    f"Cell out of range (0..15) at (x={x}, y={y}): {cell}")


def _validate_borders_closed(maze: Maze) -> None:
    g = maze.grid
    w = maze.width
    h = maze.height

    # Top row must have N closed
    for x in range(w):
        if not has_wall(g[0][x], N):
            raise ValueError(f"Top border open to North at (x={x}, y=0)")

    # Bottom row must have S closed
    for x in range(w):
        if not has_wall(g[h - 1][x], S):
            raise ValueError(
                f"Bottom border open to South at (x={x}, y={h-1})")

    # Left column must have W closed
    for y in range(h):
        if not has_wall(g[y][0], W):
            raise ValueError(f"Left border open to West at (x=0, y={y})")

    # Right column must have E closed
    for y in range(h):
        if not has_wall(g[y][w - 1], E):
            raise ValueError(f"Right border open to East at (x={w-1}, y={y})")


def _validate_neighbor_coherence(maze: Maze) -> None:
    g = maze.grid
    w = maze.width
    h = maze.height

    # Check E/W coherence
    for y in range(h):
        for x in range(w - 1):
            a = g[y][x]
            b = g[y][x + 1]

            a_e_closed = has_wall(a, E)
            b_w_closed = has_wall(b, W)

            if a_e_closed != b_w_closed:
                raise ValueError(
                    "Inconsistent E/W walls between "
                    f"(x={x}, y={y}) and (x={x+1}, y={y})"
                )

    # Check N/S coherence
    for y in range(h - 1):
        for x in range(w):
            a = g[y][x]
            b = g[y + 1][x]

            a_s_closed = has_wall(a, S)
            b_n_closed = has_wall(b, N)

            if a_s_closed != b_n_closed:
                raise ValueError(
                    "Inconsistent N/S walls between "
                    f"(x={x}, y={y}) and (x={x}, y={y+1})"
                )
