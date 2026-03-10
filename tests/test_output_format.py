# tests/test_output_format.py
from __future__ import annotations

from pathlib import Path
import re

from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from output_writer import write_output_file


HEX_ROW_RE = re.compile(r"^[0-9A-F]+$")
PATH_RE = re.compile(r"^[NESW]*$")


def test_output_file_format(tmp_path: Path) -> None:
    out = tmp_path / "maze.txt"

    width = 10
    height = 8

    gen = MazeGenerator(
        width=width,
        height=height,
        entry=(0, 0),
        exit=(width - 1, height - 1),
        perfect=True,
        seed=42,
    )
    maze = gen.generate()
    path = solve(maze)

    write_output_file(str(out), maze, path)

    lines = out.read_text(encoding="utf-8").splitlines()

    # Expect: HEIGHT rows + blank line + 3 lines (entry, exit, path)
    assert len(lines) == height + 1 + 3

    grid_lines = lines[:height]
    blank = lines[height]
    entry_line = lines[height + 1]
    exit_line = lines[height + 2]
    path_line = lines[height + 3]

    # Grid lines must be width chars of hex each
    for row in grid_lines:
        assert len(row) == width
        assert HEX_ROW_RE.match(row) is not None

    # Blank line
    assert blank == ""

    # Entry/exit coords in "x,y"
    assert entry_line == f"{maze.entry[0]},{maze.entry[1]}"
    assert exit_line == f"{maze.exit[0]},{maze.exit[1]}"

    # Path is only N/E/S/W letters
    assert PATH_RE.match(path_line) is not None
