"""
generator.py — Maze generation (core).

Implements:
- MazeGenerator(...).generate() -> Maze

Generation strategy (v1):
- Start with all walls closed (ALL_WALLS)
- Use iterative DFS backtracker to carve passages (perfect maze)
- Keep wall coherence (opening between cells updates both sides)
- Borders are kept closed
"""

from __future__ import annotations

from typing import List, Optional, Set
import random

from .grid import (
    ALL_WALLS,
    Coord,
    Maze,
    N, E, S, W,
    in_bounds,
    neighbor,
    opposite,
    open_wall,
)


class MazeGenerator:
    """Generate a maze that matches the API contract."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit: Coord,
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self._rng = random.Random(seed)

        self._validate_init()

    def generate(self) -> Maze:
        """Generate and return a Maze instance."""
        grid = self._new_grid()

        # 1) Carve passages (perfect maze baseline)
        self._carve_dfs(grid, start=self.entry)

        # 2) If perfect=False, we could add loops later (optional for v1)
        # if not self.perfect:
        #     self._add_loops(grid)

        # 3) Defensive: ensure borders stay closed
        self._ensure_closed_borders(grid)

        return Maze(
            width=self.width,
            height=self.height,
            grid=grid,
            entry=self.entry,
            exit=self.exit,
            perfect=self.perfect,
            seed=self.seed,
        )

    # ======================
    # Internal helpers
    # ======================

    def _validate_init(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width/height must be > 0")

        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")

        if not in_bounds(self.width, self.height, self.entry):
            raise ValueError("entry out of bounds")

        if not in_bounds(self.width, self.height, self.exit):
            raise ValueError("exit out of bounds")

    def _new_grid(self) -> List[List[int]]:
        """Create a height x width grid initialized with all walls closed."""
        return [[ALL_WALLS for _ in range(self.width)]
                for _ in range(self.height)]

    def _ensure_closed_borders(self, grid: List[List[int]]) -> None:
        """Ensure outer borders are closed (bit=1)."""
        # Top and bottom rows
        for x in range(self.width):
            grid[0][x] |= N
            grid[self.height - 1][x] |= S

        # Left and right columns
        for y in range(self.height):
            grid[y][0] |= W
            grid[y][self.width - 1] |= E

    def _direction_between(self, a: Coord, b: Coord) -> int:
        """Return the direction from a to b, assuming they are adjacent."""
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay

        if dx == 1 and dy == 0:
            return E
        if dx == -1 and dy == 0:
            return W
        if dx == 0 and dy == 1:
            return S
        if dx == 0 and dy == -1:
            return N

        raise ValueError("Cells are not adjacent")

    def _open_between(self, grid: List[List[int]], a: Coord, b: Coord) -> None:
        """Open the wall between adjacent
        cells a and b (coherent on both sides)."""
        d = self._direction_between(a, b)

        ax, ay = a
        bx, by = b

        grid[ay][ax] = open_wall(grid[ay][ax], d)
        grid[by][bx] = open_wall(grid[by][bx], opposite(d))

    def _carve_dfs(self, grid: List[List[int]], start: Coord) -> None:
        """Iterative DFS backtracker to carve a perfect maze."""
        stack: List[Coord] = [start]
        visited: Set[Coord] = {start}

        directions = [N, E, S, W]

        while stack:
            cur = stack[-1]

            # Gather all unvisited neighbors
            candidates: List[Coord] = []
            for d in directions:
                nxt = neighbor(cur, d)
                if not in_bounds(self.width, self.height, nxt):
                    continue
                if nxt in visited:
                    continue
                candidates.append(nxt)

            # No candidates => backtrack
            if not candidates:
                stack.pop()
                continue

            # Choose one neighbor randomly and carve passage
            nxt = self._rng.choice(candidates)
            self._open_between(grid, cur, nxt)

            visited.add(nxt)
            stack.append(nxt)
