from __future__ import annotations

from pathlib import Path

from mazegen.generator import MazeGenerator
from mazegen.validation import validate_maze
from mazegen.solver import solve
from mazegen.io_format import maze_to_hex_lines
from output_writer import write_output_file, path_to_directions


def test_integration_end_to_end(tmp_path: Path):
    print("\n" + "=" * 80)
    print("[INTEGRATION] Start end-to-end pipeline test")
    print("=" * 80)

    # ---------------------------------------------------------------------
    print("\n[1/6] Generate maze (MazeGenerator)")
    gen = MazeGenerator(10, 10, (0, 0), (9, 9), seed=42)
    maze = gen.generate()
    print(f"Generated maze: width={maze.width}, height={maze.height},"
          f" entry={maze.entry}, exit={maze.exit}, seed={maze.seed}")

    # ---------------------------------------------------------------------
    print("\n[2/6] Validate maze structure (validate_maze)")
    validate_maze(maze)
    print("Validation OK")

    # ---------------------------------------------------------------------
    print("\n[3/6] Solve maze shortest path (solve)")
    solution = solve(maze)
    print(f"Solution length: {len(solution)}")
    print(f"Solution endpoints: start={solution[0]} end={solution[-1]}")
    assert solution[0] == maze.entry
    assert solution[-1] == maze.exit

    # ---------------------------------------------------------------------
    print("\n[4/6] Convert maze to hex lines (maze_to_hex_lines)")
    hex_lines = maze_to_hex_lines(maze)
    print(f"Hex lines: {len(hex_lines)} lines, "
          f"each should have {maze.width} chars")
    print("Sample (first 3 lines):")
    for line in hex_lines[:3]:
        print(line)

    assert len(hex_lines) == maze.height
    assert all(len(line) == maze.width for line in hex_lines)

    # ---------------------------------------------------------------------
    print("\n[5/6] Write output file (write_output_file)")
    out_file = tmp_path / "maze_output.txt"
    write_output_file(str(out_file), maze, solution)
    print(f"Wrote file: {out_file}")

    # ---------------------------------------------------------------------
    print("\n[6/6] Read and verify file format")
    content = out_file.read_text(encoding="utf-8").splitlines()
    print(f"Total lines in file (splitlines): {len(content)}")

    # Expected structure:
    # - maze.height lines of hex
    # - 1 empty line
    # - entry
    # - exit
    # - path NESW
    expected_total_lines = maze.height + 1 + 3
    print(f"Expected total lines: {expected_total_lines}")
    assert len(content) == expected_total_lines

    file_hex = content[: maze.height]
    empty_line = content[maze.height]
    entry_line = content[maze.height + 1]
    exit_line = content[maze.height + 2]
    path_line = content[maze.height + 3]

    print("\n-- Parsed footer --")
    print(f"empty_line: {repr(empty_line)}")
    print(f"entry_line: {entry_line}")
    print(f"exit_line: {exit_line}")
    print(f"path_line (first 60 chars): {path_line[:60]}")

    assert empty_line == ""
    assert file_hex == hex_lines
    assert entry_line == f"{maze.entry[0]},{maze.entry[1]}"
    assert exit_line == f"{maze.exit[0]},{maze.exit[1]}"
    assert set(path_line).issubset(set("NESW"))
    assert path_line == path_to_directions(solution)

    print("\n[INTEGRATION] OK End-to-end pipeline test PASSED")
