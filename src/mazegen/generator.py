"""
generator.py — Maze generation (core).

Implements:
- MazeGenerator(...).generate() -> Maze

Generation strategy:
- Start with all walls closed (ALL_WALLS)
- Try to place the "42" pattern as fully closed blocked cells (if possible)
- Use iterative DFS backtracker to carve passages (perfect maze baseline)
- Keep wall coherence (opening between cells updates both sides)
- If perfect=False, add extra openings ("loops") to create cycles
- Ensure borders stay closed
"""

from __future__ import annotations

import random
from typing import List, Optional, Set

from .grid import (
    ALL_WALLS,
    Coord,
    Maze,
    E,
    N,
    S,
    W,
    has_wall,
    in_bounds,
    neighbor,
    opposite,
    open_wall,
)
from .pattern42 import apply_blocked_cells, compute_42_cells


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

        # 0) Try to place the "42" pattern as fully closed blocked cells
        blocked, reason = compute_42_cells(
            self.width, self.height, self.entry, self.exit
        )
        blocked_set: Set[Coord] = blocked if blocked is not None else set()

        if blocked is not None:
            apply_blocked_cells(grid, blocked_set, self.width, self.height)

        # 1) Carve passages (perfect maze baseline), ignoring blocked cells
        self._carve_dfs(grid, start=self.entry, blocked=blocked_set)

        # 2) If perfect=False, add cycles by opening extra walls
        if not self.perfect:
            self._add_loops(grid, blocked_set)

        # 3) Ensure borders stay closed
        self._ensure_closed_borders(grid)

        return Maze(
            width=self.width,
            height=self.height,
            grid=grid,
            entry=self.entry,
            exit=self.exit,
            perfect=self.perfect,
            seed=self.seed,
            blocked=frozenset(blocked_set),
            pattern42_omitted=(blocked is None),
            pattern42_reason=reason,
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
        return [[ALL_WALLS for _ in range(
            self.width)] for _ in range(self.height)]

    def _ensure_closed_borders(self, grid: List[List[int]]) -> None:
        """Ensure outer borders are closed (bit=1)."""
        for x in range(self.width):
            grid[0][x] |= N
            grid[self.height - 1][x] |= S

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

    def _carve_dfs(
        self,
        grid: List[List[int]],
        start: Coord,
        blocked: Set[Coord],
    ) -> None:
        """Iterative DFS backtracker to carve
        a perfect maze (ignores blocked)."""
        if start in blocked:
            raise ValueError("entry is inside blocked cells (42 pattern)")

        stack: List[Coord] = [start]
        visited: Set[Coord] = set(blocked)  # treat blocked as already visited
        visited.add(start)

        directions = [N, E, S, W]

        while stack:
            cur = stack[-1]

            candidates: List[Coord] = []
            for d in directions:
                nxt = neighbor(cur, d)
                if not in_bounds(self.width, self.height, nxt):
                    continue
                if nxt in visited:
                    continue
                if nxt in blocked:
                    continue
                candidates.append(nxt)

            if not candidates:
                stack.pop()
                continue

            nxt = self._rng.choice(candidates)
            self._open_between(grid, cur, nxt)

            visited.add(nxt)
            stack.append(nxt)

    def _add_loops(self, grid: List[List[int]], blocked: Set[Coord]) -> None:
        """
        Add extra openings to create cycles when perfect=False.
        Keeps borders closed and ignores blocked cells.
        """
        # Simple heuristic for how many loops to add
        target = max(1, (self.width * self.height) // 30)
        attempts = target * 10  # prevent infinite loops
        directions = [N, E, S, W]

        while target > 0 and attempts > 0:
            attempts -= 1

            x = self._rng.randrange(self.width)
            y = self._rng.randrange(self.height)
            a: Coord = (x, y)

            if a in blocked:
                continue

            d = self._rng.choice(directions)
            b = neighbor(a, d)

            if not in_bounds(self.width, self.height, b):
                continue
            if b in blocked:
                continue

            # Avoid opening external borders
            if x == 0 and d == W:
                continue
            if x == self.width - 1 and d == E:
                continue
            if y == 0 and d == N:
                continue
            if y == self.height - 1 and d == S:
                continue

            ax, ay = a
            # Only open if currently closed
            # (so we actually create a new connection)
            if has_wall(grid[ay][ax], d):
                self._open_between(grid, a, b)
                target -= 1
