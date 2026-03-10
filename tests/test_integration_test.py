# tests/test_integration.py
from __future__ import annotations

from pathlib import Path

from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.validation import validate_maze
from output_writer import write_output_file


def test_full_pipeline_creates_valid_output_file(tmp_path: Path) -> None:
    out = tmp_path / "maze_out.txt"

    print("\n[INTEGRATION] generate maze 15x15 seed=123 perfect=True")
    gen = MazeGenerator(
        width=15,
        height=15,
        entry=(0, 0),
        exit=(14, 14),
        perfect=True,
        seed=123,
    )
    maze = gen.generate()

    print("[INTEGRATION] check 42 presence")
    assert not maze.pattern42_omitted
    assert len(maze.blocked) > 0

    print("[INTEGRATION] validate_maze")
    validate_maze(maze)

    print("[INTEGRATION] solve shortest path")
    path = solve(maze)
    assert path[0] == maze.entry
    assert path[-1] == maze.exit
    print(f"[INTEGRATION] path length: {len(path)}")

    print("[INTEGRATION] write output file")
    write_output_file(str(out), maze, path)
    assert out.exists()
    assert out.stat().st_size > 0
    print(f"[INTEGRATION] output size: {out.stat().st_size} bytes")


def test_42_is_omitted_for_small_mazes() -> None:
    print("\n[INTEGRATION] generate SMALL maze 6x4 (42 should be omitted)")
    gen = MazeGenerator(
        width=6,
        height=4,
        entry=(0, 0),
        exit=(5, 3),
        perfect=True,
        seed=1,
    )
    maze = gen.generate()

    assert maze.pattern42_omitted
    assert maze.pattern42_reason is not None
    assert len(maze.blocked) == 0
    print(f"[INTEGRATION] omitted reason: {maze.pattern42_reason}")

    validate_maze(maze)
    path = solve(maze)
    assert path[0] == maze.entry
    assert path[-1] == maze.exit
    print(f"[INTEGRATION] path length: {len(path)}")
