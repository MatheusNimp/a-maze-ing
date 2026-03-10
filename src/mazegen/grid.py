"""
grid.py — Core types and grid utilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, FrozenSet

# (x, y)
Coord = Tuple[int, int]

# Wall bit masks (1 = closed wall)
N: int = 1
E: int = 2
S: int = 4
W: int = 8

ALL_WALLS: int = N | E | S | W  # 15


@dataclass(frozen=True)
class Maze:
    """Public Maze container exchanged between core and app."""
    width: int
    height: int
    grid: List[List[int]]     # grid[y][x], values 0..15
    entry: Coord
    exit: Coord
    perfect: bool
    seed: Optional[int] = None

    # --- Pattern 42 support ---
    # Cells that must remain fully closed (used to draw "42").
    blocked: FrozenSet[Coord] = frozenset()

    # If the maze is too small (or conflicts with entry/exit),
    # the pattern may be omitted.
    # The CLI should print a warning when this happens.
    pattern42_omitted: bool = False
    pattern42_reason: Optional[str] = None


def in_bounds(width: int, height: int, coord: Coord) -> bool:
    """True if coord is inside bounds of a width x height grid."""
    x, y = coord
    return 0 <= x < width and 0 <= y < height


def neighbor(coord: Coord, direction: int) -> Coord:
    """Return neighbor coordinate in a direction (no bounds checking).

    direction must be one of N/E/S/W (1/2/4/8).
    """
    x, y = coord
    if direction == N:
        return (x, y - 1)
    if direction == E:
        return (x + 1, y)
    if direction == S:
        return (x, y + 1)
    if direction == W:
        return (x - 1, y)
    raise ValueError("Invalid direction (expected N/E/S/W).")


def opposite(direction: int) -> int:
    """Return opposite direction (N<->S, E<->W)."""
    if direction == N:
        return S
    if direction == S:
        return N
    if direction == E:
        return W
    if direction == W:
        return E
    raise ValueError("Invalid direction (expected N/E/S/W).")


def has_wall(cell: int, direction: int) -> bool:
    """True if the wall is CLOSED in this cell."""
    return (cell & direction) != 0


def open_wall(cell: int, direction: int) -> int:
    """Return new cell value with this wall OPEN (bit set to 0)."""
    return cell & ~direction


def close_wall(cell: int, direction: int) -> int:
    """Return new cell value with this wall CLOSED (bit set to 1)."""
    return cell | direction
