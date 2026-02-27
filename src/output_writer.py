from __future__ import annotations

from typing import List

from mazegen.grid import Maze, Coord
from mazegen.io_format import maze_to_hex_lines


def _coords_to_direction(a: Coord, b: Coord) -> str:
    """
    Convert two adjacent coordinates into a direction letter.
    """
    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay

    if dx == 1 and dy == 0:
        return "E"
    if dx == -1 and dy == 0:
        return "W"
    if dx == 0 and dy == 1:
        return "S"
    if dx == 0 and dy == -1:
        return "N"

    raise ValueError(f"Invalid step from {a} to {b}")


def path_to_directions(path: List[Coord]) -> str:
    """
    Convert a list of coordinates into a NESW direction string.
    """
    if len(path) < 2:
        return ""

    directions: List[str] = []

    for a, b in zip(path, path[1:]):
        directions.append(_coords_to_direction(a, b))

    return "".join(directions)


def write_output_file(path: str, maze: Maze, solution: List[Coord]) -> None:
    """
    Write the maze to a file in the required subject format.
    """
    hex_lines = maze_to_hex_lines(maze)
    direction_string = path_to_directions(solution)

    with open(path, "w", encoding="utf-8") as f:
        # Maze grid
        for line in hex_lines:
            f.write(line + "\n")

        # Empty line
        f.write("\n")

        # Entry
        f.write(f"{maze.entry[0]},{maze.entry[1]}\n")

        # Exit
        f.write(f"{maze.exit[0]},{maze.exit[1]}\n")

        # Path
        f.write(direction_string + "\n")
