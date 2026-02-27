from mazegen.generator import MazeGenerator
from mazegen.io_format import maze_to_hex_lines


def test_maze_to_hex_lines_dimensions():
    maze = MazeGenerator(4, 3, (0, 0), (3, 2), seed=42).generate()
    lines = maze_to_hex_lines(maze)

    print("\n[HEX OUTPUT - dimensions test]")
    for line in lines:
        print(line)

    assert len(lines) == maze.height
    assert all(len(line) == maze.width for line in lines)


def test_maze_to_hex_lines_are_valid_hex_characters():
    maze = MazeGenerator(6, 4, (0, 0), (5, 3), seed=123).generate()
    lines = maze_to_hex_lines(maze)

    print("\n[HEX OUTPUT - character validation test]")
    for line in lines:
        print(line)

    allowed = set("0123456789ABCDEF")

    for line in lines:
        assert set(line).issubset(allowed)


def test_hex_conversion_matches_decimal_values():
    maze = MazeGenerator(5, 5, (0, 0), (4, 4), seed=42).generate()
    lines = maze_to_hex_lines(maze)

    print("\n[HEX OUTPUT - exact match test]")
    for line in lines:
        print(line)

    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            expected_hex = format(cell, "X")
            assert lines[y][x] == expected_hex
