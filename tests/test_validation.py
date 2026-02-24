import pytest

from mazegen.generator import MazeGenerator
from mazegen.validation import validate_maze
from mazegen.grid import N, E, S, W


def test_validate_ok_for_generated_maze():
    maze = MazeGenerator(8, 6, (0, 0), (7, 5), seed=42).generate()
    # Não deve levantar exceção
    validate_maze(maze)


def test_validate_rejects_cell_out_of_range():
    maze = MazeGenerator(4, 4, (0, 0), (3, 3), seed=42).generate()

    # quebra: coloca valor inválido (> 15)
    maze.grid[1][1] = 99  # type: ignore[misc]

    with pytest.raises(ValueError, match=r"Cell out of range"):
        validate_maze(maze)


def test_validate_rejects_inconsistent_ew_walls():
    maze = MazeGenerator(4, 4, (0, 0), (3, 3), seed=42).generate()

    # Forçar inconsistência entre (1,1) e (2,1):
    # diz que (1,1) tem E aberta (bit E = 0) e (2,1) tem W fechada (bit W = 1)
    # Para garantir: removemos E de A e adicionamos W em B
    y = 1
    x = 1

    maze.grid[y][x] &= ~E        # abre E em A
    maze.grid[y][x + 1] |= W     # fecha W em B  (inconsistente)

    with pytest.raises(ValueError, match=r"Inconsistent E/W walls"):
        validate_maze(maze)


def test_validate_rejects_inconsistent_ns_walls():
    maze = MazeGenerator(4, 4, (0, 0), (3, 3), seed=42).generate()

    # Forçar inconsistência entre (1,1) e (1,2):
    # diz que (1,1) tem S aberta (bit S = 0) e (1,2) tem N fechada (bit N = 1)
    y = 1
    x = 1

    maze.grid[y][x] &= ~S        # abre S em A
    maze.grid[y + 1][x] |= N     # fecha N em B (inconsistente)

    with pytest.raises(ValueError, match=r"Inconsistent N/S walls"):
        validate_maze(maze)