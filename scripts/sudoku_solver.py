#!/usr/bin/env python3
"""
sudoku_solver.py

A general-purpose 9x9 Sudoku solver using backtracking. Useful when a
puzzle has few enough givens that manual solving is unreliable, but
still has a unique solution.

Edit the `grid` below (0 = empty cell) and run the script, or import
`solve()` into your own code.

Usage:
    python3 sudoku_solver.py
"""

from typing import Optional

Grid = list[list[int]]


def is_valid(grid: Grid, row: int, col: int, value: int) -> bool:
    if any(grid[row][c] == value for c in range(9)):
        return False
    if any(grid[r][col] == value for r in range(9)):
        return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == value:
                return False
    return True


def find_empty(grid: Grid) -> Optional[tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def solve(grid: Grid) -> bool:
    """Solves the grid in place. Returns True if solved."""
    pos = find_empty(grid)
    if pos is None:
        return True
    row, col = pos
    for value in range(1, 10):
        if is_valid(grid, row, col, value):
            grid[row][col] = value
            if solve(grid):
                return True
            grid[row][col] = 0
    return False


def print_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(str(v) for v in row))


if __name__ == "__main__":
    # Example puzzle (replace with your own — 0 = empty cell)
    grid: Grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    if solve(grid):
        print("Solved:")
        print_grid(grid)
    else:
        print("No solution exists for this grid.")
