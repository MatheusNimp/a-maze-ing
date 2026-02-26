from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List, Optional

from .grid import Maze, Coord, N, E, S, W, has_wall, in_bounds, neighbor


def solve(maze: Maze) -> List[Coord]:
    """
    Return shortest path from maze.entry to maze.exit as a list of Coord.
    Includes entry as first and exit as last.

    Raises RuntimeError if no path exists.
    """
    start = maze.entry
    goal = maze.exit

    if start == goal:
        return [start]

    # BFS queue
    q: Deque[Coord] = deque([start])

    # came_from maps each visited node to its predecessor
    came_from: Dict[Coord, Optional[Coord]] = {start: None}

    directions = [N, E, S, W]

    while q:
        cur = q.popleft()

        if cur == goal:
            return _reconstruct_path(came_from, goal)

        cx, cy = cur
        cell = maze.grid[cy][cx]

        for d in directions:
            # If there is a wall CLOSED in that direction, you can't go there
            if has_wall(cell, d):
                continue

            nxt = neighbor(cur, d)
            if not in_bounds(maze.width, maze.height, nxt):
                continue

            if nxt in came_from:
                continue

            came_from[nxt] = cur
            q.append(nxt)

    raise RuntimeError("No path from entry to exit")


def _reconstruct_path(
        came_from: Dict[Coord, Optional[Coord]], goal: Coord) -> List[Coord]:
    path: List[Coord] = []
    cur: Optional[Coord] = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
