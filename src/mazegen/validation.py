from __future__ import annotations

from collections import deque
from typing import Deque, Set

from .grid import Maze, Coord, N, E, S, W, has_wall, in_bounds, neighbor


def validate_maze(maze: Maze) -> None:
    """
    Validate maze structural integrity.

    Raises ValueError if invalid.
    """
    _validate_dimensions(maze)
    _validate_cells_range(maze)
    _validate_entry_exit(maze)
    _validate_borders_closed(maze)
    _validate_neighbor_coherence(maze)
    _validate_connectivity_except_blocked(maze)
    _validate_no_open_3x3(maze)


def _validate_dimensions(maze: Maze) -> None:
    if maze.width <= 0 or maze.height <= 0:
        raise ValueError("Maze dimensions must be > 0")

    if len(maze.grid) != maze.height:
        raise ValueError("Grid height does not match maze.height")

    for y, row in enumerate(maze.grid):
        if len(row) != maze.width:
            raise ValueError(f"Grid width mismatch at row y={y}")


def _validate_cells_range(maze: Maze) -> None:
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            if not (0 <= cell <= 15):
                raise ValueError(
                    f"Cell out of range (0..15) at (x={x}, y={y}): {cell}"
                )


def _validate_entry_exit(maze: Maze) -> None:
    if maze.entry == maze.exit:
        raise ValueError("Entry and exit must be different")

    if not in_bounds(maze.width, maze.height, maze.entry):
        raise ValueError("Entry out of bounds")

    if not in_bounds(maze.width, maze.height, maze.exit):
        raise ValueError("Exit out of bounds")

    if maze.entry in maze.blocked:
        raise ValueError("Entry cannot be inside blocked (42) cells")

    if maze.exit in maze.blocked:
        raise ValueError("Exit cannot be inside blocked (42) cells")


def _validate_borders_closed(maze: Maze) -> None:
    g = maze.grid
    w = maze.width
    h = maze.height

    for x in range(w):
        if not has_wall(g[0][x], N):
            raise ValueError(f"Top border open to North at (x={x}, y=0)")
        if not has_wall(g[h - 1][x], S):
            raise ValueError(
                f"Bottom border open to South at (x={x}, y={h - 1})")

    for y in range(h):
        if not has_wall(g[y][0], W):
            raise ValueError(f"Left border open to West at (x=0, y={y})")
        if not has_wall(g[y][w - 1], E):
            raise ValueError(
                f"Right border open to East at (x={w - 1}, y={y})")


def _validate_neighbor_coherence(maze: Maze) -> None:
    g = maze.grid
    w = maze.width
    h = maze.height

    # E/W coherence
    for y in range(h):
        for x in range(w - 1):
            a = g[y][x]
            b = g[y][x + 1]
            if has_wall(a, E) != has_wall(b, W):
                raise ValueError(
                    "Inconsistent E/W walls between "
                    f"(x={x}, y={y}) and (x={x+1}, y={y})"
                )

    # N/S coherence
    for y in range(h - 1):
        for x in range(w):
            a = g[y][x]
            b = g[y + 1][x]
            if has_wall(a, S) != has_wall(b, N):
                raise ValueError(
                    "Inconsistent N/S walls between "
                    f"(x={x}, y={y}) and (x={x}, y={y+1})"
                )


def _validate_connectivity_except_blocked(maze: Maze) -> None:
    """
    Ensure all non-blocked cells are reachable from entry.
    Blocked cells (42 pattern) are allowed to be isolated.
    """
    start = maze.entry
    blocked: Set[Coord] = set(maze.blocked)

    # BFS over open passages
    q: Deque[Coord] = deque([start])
    seen: Set[Coord] = {start}

    directions = [N, E, S, W]

    while q:
        cur = q.popleft()
        cx, cy = cur
        cell = maze.grid[cy][cx]

        for d in directions:
            if has_wall(cell, d):
                continue
            nxt = neighbor(cur, d)
            if not in_bounds(maze.width, maze.height, nxt):
                continue
            if nxt in blocked:
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            q.append(nxt)

    total_non_blocked = (maze.width * maze.height) - len(blocked)
    if len(seen) != total_non_blocked:
        # Find one example unreachable cell to make error actionable
        for y in range(maze.height):
            for x in range(maze.width):
                c = (x, y)
                if c in blocked:
                    continue
                if c not in seen:
                    raise ValueError(
                        "Maze not fully connected:"
                        f"unreachable cell at (x={x}, y={y})"
                    )
        raise ValueError("Maze not fully connected")


def _edge_open(maze: Maze, a: Coord, b: Coord) -> bool:
    """
    Return True if the passage between adjacent a and b is open.
    Assumes adjacency.
    """
    ax, ay = a
    bx, by = b
    if bx == ax + 1 and by == ay:
        return not has_wall(maze.grid[ay][ax], E)
    if bx == ax - 1 and by == ay:
        return not has_wall(maze.grid[ay][ax], W)
    if by == ay + 1 and bx == ax:
        return not has_wall(maze.grid[ay][ax], S)
    if by == ay - 1 and bx == ax:
        return not has_wall(maze.grid[ay][ax], N)
    return False


def _validate_no_open_3x3(maze: Maze) -> None:
    """
    Reject a fully open 3x3 area (all internal adjacencies open).
    This matches the subject rule: never a 3x3 open area.
    """
    w = maze.width
    h = maze.height

    # Need at least 3x3 to check
    if w < 3 or h < 3:
        return

    # For each 3x3 window, test if all internal edges are open
    # Internal edges in 3x3: 6 horizontal + 6 vertical = 12
    for top in range(h - 2):
        for left in range(w - 2):
            all_open = True

            # horizontal internal edges
            for dy in range(3):
                y = top + dy
                for dx in range(2):
                    a = (left + dx, y)
                    b = (left + dx + 1, y)
                    if not _edge_open(maze, a, b):
                        all_open = False
                        break
                if not all_open:
                    break

            if not all_open:
                continue

            # vertical internal edges
            for dx in range(3):
                x = left + dx
                for dy in range(2):
                    a = (x, top + dy)
                    b = (x, top + dy + 1)
                    if not _edge_open(maze, a, b):
                        all_open = False
                        break
                if not all_open:
                    break

            if all_open:
                raise ValueError(
                    f"Forbidden open 3x3 area"
                    f"detected at top-left (x={left}, y={top})"
                )
