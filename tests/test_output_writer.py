from __future__ import annotations

from pathlib import Path

from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.validation import validate_maze
from output_writer import path_to_directions, write_output_file


def test_path_to_directions_basic():
    path = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    assert path_to_directions(path) == "ESWN"


def test_write_output_file_format(tmp_path: Path):
    maze = MazeGenerator(5, 5, (0, 0), (4, 4), seed=42).generate()
    validate_maze(maze)
    solution = solve(maze)

    out_file = tmp_path / "maze.txt"
    write_output_file(str(out_file), maze, solution)

    content = out_file.read_text(encoding="utf-8").splitlines()

    # Must have:
    # height lines of hex
    # 1 empty line
    # entry line
    # exit line
    # path line
    assert len(content) == maze.height + 1 + 3

    hex_lines = content[: maze.height]
    empty_line = content[maze.height]
    entry_line = content[maze.height + 1]
    exit_line = content[maze.height + 2]
    path_line = content[maze.height + 3]

    assert empty_line == ""

    # Each hex line should have width chars
    assert all(len(line) == maze.width for line in hex_lines)

    # Entry/Exit formatting
    assert entry_line == f"{maze.entry[0]},{maze.entry[1]}"
    assert exit_line == f"{maze.exit[0]},{maze.exit[1]}"

    # Path must be only NESW letters (can be empty if entry==exit)
    assert set(path_line).issubset(set("NESW"))
    assert path_line == path_to_directions(solution)
