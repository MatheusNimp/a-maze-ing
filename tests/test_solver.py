import pytest

from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.grid import in_bounds


def test_solver_returns_path_from_entry_to_exit():
    maze = MazeGenerator(10, 10, (0, 0), (9, 9), seed=42).generate()
    path = solve(maze)

    assert path[0] == maze.entry
    assert path[-1] == maze.exit
    assert len(path) >= 1


def test_solver_path_steps_are_adjacent_and_in_bounds():
    maze = MazeGenerator(12, 8, (0, 0), (11, 7), seed=123).generate()
    path = solve(maze)

    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        assert in_bounds(maze.width, maze.height, (x1, y1))
        assert in_bounds(maze.width, maze.height, (x2, y2))
        # Manhattan distance must be 1 (adjacent)
        assert abs(x1 - x2) + abs(y1 - y2) == 1


def test_solver_respects_walls():
    # For every move in the returned path, ensure there is no wall blocking it
    from mazegen.grid import N, E, S, W, has_wall

    maze = MazeGenerator(15, 10, (0, 0), (14, 9), seed=999).generate()
    path = solve(maze)
    g = maze.grid

    for a, b in zip(path, path[1:]):
        ax, ay = a
        bx, by = b
        cell = g[ay][ax]

        dx = bx - ax
        dy = by - ay

        if dx == 1 and dy == 0:      # E
            assert not has_wall(cell, E)
        elif dx == -1 and dy == 0:   # W
            assert not has_wall(cell, W)
        elif dx == 0 and dy == 1:    # S
            assert not has_wall(cell, S)
        elif dx == 0 and dy == -1:   # N
            assert not has_wall(cell, N)
        else:
            pytest.fail("Non-adjacent step in path")


def test_solver_raises_if_no_path():
    # Create a tiny maze and block the start completely (all walls closed)
    maze = MazeGenerator(2, 2, (0, 0), (1, 1), seed=42).generate()

    # Force start to be isolated: close all walls in start
    #  and also ensure neighbors are closed coherently.
    maze.grid[0][0] = 15  # all walls closed at start

    # Also close neighbor sides that would connect to it
    maze.grid[0][1] |= 8  # neighbor to the East: close W
    maze.grid[1][0] |= 1  # neighbor to the South: close N

    with pytest.raises(RuntimeError, match="No path"):
        solve(maze)
