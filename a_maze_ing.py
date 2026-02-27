from __future__ import annotations

import sys

from config_parser import parse_config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.validation import validate_maze
from output_writer import write_output_file


def main(argv: list[str]) -> int:
    # Usage: python a_maze_ing.py [config_path]
    config_path = argv[1] if len(argv) >= 2 else "config_default.txt"

    cfg = parse_config(config_path)

    gen = MazeGenerator(
        cfg.width,
        cfg.height,
        cfg.entry,
        cfg.exit,
        perfect=cfg.perfect,
        seed=cfg.seed,
    )
    maze = gen.generate()

    validate_maze(maze)
    solution = solve(maze)

    write_output_file(cfg.output, maze, solution)

    print(f"OK: wrote output to {cfg.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))