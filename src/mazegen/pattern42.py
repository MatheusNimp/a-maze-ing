from __future__ import annotations

from typing import Optional, Set, Tuple

from .grid import (
    ALL_WALLS,
    Coord,
    E,
    N,
    S,
    W,
    close_wall,
    in_bounds,
    neighbor,
    opposite,
)


def compute_42_cells(
    width: int,
    height: int,
    entry: Coord,
    exit: Coord,
) -> Tuple[Optional[Set[Coord]], Optional[str]]:
    """
    Compute the set of cells that should
    be fully closed to draw a visible "42".

    Returns:
        (blocked_cells, reason)
        - blocked_cells is None if the pattern can't be placed.
        - reason contains a human-readable explanation when omitted.
    """
    pat_w, pat_h = 7, 5
    if width < pat_w or height < pat_h:
        return None, "maze too small for 42 pattern"

    ox = (width - pat_w) // 2
    oy = (height - pat_h) // 2

    rel: Set[Coord] = set()

    # --- "4" in a 3x5 block (x=0..2, y=0..4) ---
    # left vertical upper part (x=0, y=0..2)
    for y in range(3):
        rel.add((0, y))
    # middle horizontal (y=2, x=0..2)
    for x in range(3):
        rel.add((x, 2))
    # right vertical full (x=2, y=0..4)
    for y in range(5):
        rel.add((2, y))

    # --- "2" in a 3x5 block (x=4..6, y=0..4), column 3 is spacing ---
    # top horizontal
    for x in range(4, 7):
        rel.add((x, 0))
    # upper right vertical
    for y in range(3):
        rel.add((6, y))
    # middle horizontal
    for x in range(4, 7):
        rel.add((x, 2))
    # lower left vertical
    for y in range(2, 5):
        rel.add((4, y))
    # bottom horizontal
    for x in range(4, 7):
        rel.add((x, 4))

    blocked: Set[Coord] = set()
    for (rx, ry) in rel:
        c = (ox + rx, oy + ry)
        if c == entry or c == exit:
            return None, "42 pattern overlaps entry/exit"
        blocked.add(c)

    return blocked, None


def apply_blocked_cells(
    grid: list[list[int]],
    blocked: Set[Coord],
    width: int,
    height: int,
) -> None:
    """
    Force blocked cells to be fully closed AND keep neighbor coherence.
    """
    # 1) blocked cells fully closed
    for (x, y) in blocked:
        grid[y][x] = ALL_WALLS

    # 2) for each neighbor of a blocked cell (that is NOT blocked),
    #    ensure its wall towards the blocked cell is closed.
    dirs = [N, E, S, W]
    for a in blocked:
        for d in dirs:
            b = neighbor(a, d)
            if not in_bounds(width, height, b):
                continue
            if b in blocked:
                continue
            bx, by = b
            grid[by][bx] = close_wall(grid[by][bx], opposite(d))
