from __future__ import annotations
from config_parser import parse_config, Config
from mazegen.generator import MazeGenerator
from mazegen.grid import Coord, Maze
from mazegen.solver import solve
from mazegen.validation import validate_maze
from output_writer import write_output_file
from renderer.ascii import ANSI_COLORS, render_ascii

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))


def _generate_and_solve(
        cfg: Config,) -> tuple[MazeGenerator, Maze, list[Coord]]:
    gen = MazeGenerator(
        cfg.width,
        cfg.height,
        cfg.entry,
        cfg.exit,
        perfect=cfg.perfect,
        seed=cfg.seed,
    )

    maze = gen.generate()

    if maze.pattern42_omitted and maze.pattern42_reason:
        print(f"Warning: {maze.pattern42_reason}. 42 pattern omitted.")

    validate_maze(maze)
    solution = solve(maze)
    write_output_file(cfg.output, maze, solution)

    return gen, maze, solution


def _print_help() -> None:
    print()
    print("Commands:")
    print("  r  regenerate maze")
    print("  p  show/hide shortest path")
    print("  c  change wall color")
    print("  w  write output file again")
    print("  h  help")
    print("  q  quit")
    print()


def main(argv: list[str]) -> int:
    config_path = argv[1] if len(argv) >= 2 else "config_default.txt"

    try:
        cfg = parse_config(config_path)

        gen, maze, solution = _generate_and_solve(cfg)

        show_path = False
        color_names = list(ANSI_COLORS.keys())
        color_index = 0

        _print_help()

        while True:
            current_color_name = color_names[color_index]
            wall_color = ANSI_COLORS[current_color_name]

            print()
            print(f"Output file: {cfg.output}")
            print(f"Wall color: {current_color_name}")
            print(f"Path visible: {'yes' if show_path else 'no'}")
            print()

            print(
                render_ascii(
                    maze,
                    solution if show_path else None,
                    wall_color=wall_color,
                )
            )

            cmd = input("\n[r/p/c/w/h/q] > ").strip().lower()

            if cmd == "q":
                print("Bye.")
                break

            if cmd == "h":
                _print_help()
                input("Press Enter to continue...")
                continue

            if cmd == "p":
                show_path = not show_path
                continue

            if cmd == "c":
                color_index = (color_index + 1) % len(color_names)
                continue

            if cmd == "w":
                write_output_file(cfg.output, maze, solution)
                print(f"OK: wrote output to {cfg.output}")
                continue

            if cmd == "r":
                maze = gen.generate()

                if maze.pattern42_omitted and maze.pattern42_reason:
                    print(
                        f"Warning: {maze.pattern42_reason}. "
                        "42 pattern omitted."
                    )

                validate_maze(maze)
                solution = solve(maze)
                write_output_file(cfg.output, maze, solution)
                print(f"OK: wrote output to {cfg.output}")
                continue

            print("Unknown command. Type 'h' for help.")

        return 0

    except FileNotFoundError:
        print(f"Error: config file not found: {config_path}")
        return 1
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
