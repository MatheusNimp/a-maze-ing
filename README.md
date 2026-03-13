*This project has been created as part of the 42 curriculum by Maamaral, Bfantine.*

## A-Maze-ing (Python)

## Description
This project generates and solves mazes based on a configuration file.

It supports:
- Deterministic generation via `SEED`
- Perfect mazes (single unique path) when `PERFECT=true`
- Non-perfect mazes (with cycles) when `PERFECT=false`
- A visible “42” pattern made of fully closed cells (omitted only when the maze is too small, with a console warning)
- Shortest-path solving (BFS)
- Export to the required hex-based output format
- Interactive ASCII visualization (regenerate / show-hide path / change wall colors)

---

## Instructions

### Requirements
- Python >= 3.10
- `make` (recommended)

### Install
```bash
make install
```
---
### Run
```bash
make run
```
Or directly:
```bash
python3 a_maze_ing.py config_default.txt
```
### Debug
```bash
make debug
```
### Lint
```bash
make lint
```
(Optional strict mode)
```bash
make lint-strict
```
### Build the reusable package (mazegen-*)
```bash
make build
ls dist
```
---
### Interactive ASCII controls

When running in ASCII mode:

- ``` r ``` regenerate a new maze

- ``` p ``` show/hide shortest path

- ``` c ``` change wall colors

- ``` w ``` write the output file again

- ``` h ``` help

- ``` q ```  quit

---
### Configuration file format

## Required keys

- ``` WIDTH ``` (int > 0)

- ``` HEIGHT ``` (int > 0)

- ``` ENTRY ``` (x,y within bounds)

- ``` EXIT ``` (x,y within bounds, different from ENTRY)

- ``` PERFECT ``` (true/false)

- ``` OUTPUT_FILE ``` (path)

## Optional keys

- ``` SEED ``` (int): reproducible generation

Example:
```bash
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=1,9
PERFECT=true
SEED=42
OUTPUT_FILE=maze_output.txt
```

Additional keys are ignored by the parser (future-proofing).

---
### Output file format

The output file is composed of:

1. ``` HEIGHT ``` lines of hexadecimal digits (each line has ```WIDTH ``` chars)

2. One empty line

3. ``` ENTRY ``` as x,y

4. ``` EXIT ``` as x,y

5. The shortest valid path as a string of ``` N/E/S/W ```

## Wall encoding (hex digit per cell)

Each cell is a 4-bit mask (1 = wall closed):

- bit 0: North (N)

- bit 1: East (E)

- bit 2: South (S)

- bit 3: West (W)

So each cell value is in ``` [0..15] ``` and is written as one hex digit ``` [0-9A-F] ``` .

---
### Algorithms

## Maze generation

Base generation uses an iterative DFS backtracker:

- Start with all walls closed

- Carve passages while maintaining wall coherence between adjacent cells

- This produces a spanning tree over all non-blocked cells (perfect maze baseline)

When ``` PERFECT=false ``` , cycles are added by opening a small number of extra walls:

- Only between in-bounds adjacent non-blocked cells

- External borders remain closed

Why DFS backtracker:

- Simple, fast, and produces a perfect maze by construction

- Easy to keep wall coherence (open both sides)

### Solving

We use BFS (Breadth-First Search) from ``` ENTRY ``` to ``` EXIT ``` :

- Guarantees the shortest path in number of steps

- Output path is converted from coordinates into ``` N/E/S/W ```

---
### The “42” pattern

The maze contains a visible “42” pattern, implemented as fully closed cells:

- These cells are stored in ``` maze.blocked ```

- The generator never carves passages into blocked cells

- The solver ignores blocked cells

- Validation allows blocked cells to be isolated, but requires full connectivity for all other cells

If the maze is too small to fit the pattern, the pattern is omitted and the program prints a warning in the console.

---
### Validation rules

Before solving/exporting, the maze is validated:

- Dimensions match the grid

- Cell values are in ``` [0..15] ```

- External borders are closed

- Neighbor wall coherence (E/W and N/S consistency)

- Full connectivity for all non-blocked cells (no isolated cells)

- No fully open 3x3 area (maximum corridor width is 2 cells)

---
### Reusable module: ``` mazegen ```

The reusable core package is in ``` src/mazegen/ ``` and contains:

- Grid representation and bitmask helpers

- Maze generation (with optional 42 pattern)

- Solving utilities

- Validation

## Install (from the built wheel)
```bash
python3 -m pip install dist/mazegen-*.whl
```
Minimal usage example
```bash
from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.validation import validate_maze

gen = MazeGenerator(width=15, height=15, entry=(0, 0), exit=(14, 14), perfect=True, seed=123)
maze = gen.generate()
validate_maze(maze)
path = solve(maze)

print(len(path), "steps")
```
---
### Resources

- Python dataclasses, random.Random, collections.deque (BFS)

- ANSI escape codes for terminal coloring

- 42 subject PDF specification (A-Maze-ing v2.0)

- https://www.geeksforgeeks.org/dsa/difference-between-bfs-and-dfs/

- https://youtu.be/pcKY4hjDrxk
---
### Use of AI tools

We used AI assistance for:

- Architecture review (module boundaries between CLI/core/renderer)

- Suggesting validation strategies (connectivity, 3x3-open detection)

- Reviewing output formatting requirements

- Proposing a Makefile workflow compatible with venv / PEP 668 environments
---
### Team & project management

## Roles

- Maamaral:
  1. Core generation integration (42 pattern hooks, regeneration loop)

  2. CLI orchestration and packaging workflow

- Bfantine:
  1. ASCII renderer implementation (colors + visualization details)
  
  2. Visual UX improvements and terminal interaction tweaks

## Planning

- Built a minimal end-to-end pipeline first (generate → validate → solve → export)

- Added interactive visualization features

- Added the 42 pattern as blocked cells without breaking connectivity/coherence

- Finalized tooling (lint/build) and documentation

















