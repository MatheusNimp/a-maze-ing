from mazegen import MazeGenerator, N, E, S, W


def test_generator_creates_grid_with_correct_dimensions():
    gen = MazeGenerator(4, 3, (0, 0), (3, 2), seed=42)
    maze = gen.generate()

    assert maze.width == 4
    assert maze.height == 3
    assert len(maze.grid) == 3
    assert len(maze.grid[0]) == 4


def test_generator_cells_are_not_all_closed():
    gen = MazeGenerator(4, 4, (0, 0), (3, 3), seed=42)
    maze = gen.generate()

    all_cells = [cell for row in maze.grid for cell in row]
    assert any(cell != 15 for cell in all_cells)


def test_borders_closed():
    gen = MazeGenerator(5, 5, (0, 0), (4, 4), seed=42)
    maze = gen.generate()
    g = maze.grid

    # top row: N closed
    assert all((g[0][x] & N) != 0 for x in range(maze.width))
    # bottom row: S closed
    assert all((g[maze.height-1][x] & S) != 0 for x in range(maze.width))
    # left col: W closed
    assert all((g[y][0] & W) != 0 for y in range(maze.height))
    # right col: E closed
    assert all((g[y][maze.width-1] & E) != 0 for y in range(maze.height))


def test_print_maze_for_visual_debug():
    gen = MazeGenerator(5, 5, (0, 0), (4, 4), seed=42)
    maze = gen.generate()

    print()
    for row in maze.grid:
        print(",".join(str(cell) for cell in row))
