from dataclasses import dataclass
from typing import List, Tuple, Set
import random

@dataclass
class Cell:
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    number: int = 0

class Minesweeper:
    def __init__(self, rows: int, cols: int, mines: int, first_click_safe: bool = True):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.first_click_safe = first_click_safe
        self.grid: List[List[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self._mines_placed = False
        self.revealed_count = 0
        self.game_over = False
        self.won = False

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        ns = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if self.in_bounds(rr, cc):
                    ns.append((rr, cc))
        return ns

    def _compute_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].mine:
                    self.grid[r][c].number = 0
                else:
                    self.grid[r][c].number = sum(1 for (rr, cc) in self.neighbors(r, c) if self.grid[rr][cc].mine)

    def place_mines(self, avoid: Tuple[int, int] = None):
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        if self.first_click_safe and avoid is not None:
            ax, ay = avoid
            banned = {(ax, ay)} | set(self.neighbors(ax, ay))
            spots = [p for p in spots if p not in banned]
        random.shuffle(spots)
        mines_left = self.mines_count
        for (r, c) in spots:
            if mines_left == 0:
                break
            self.grid[r][c].mine = True
            mines_left -= 1
        if mines_left > 0:
            fallback = [(r, c) for r in range(self.rows) for c in range(self.cols) if not self.grid[r][c].mine]
            random.shuffle(fallback)
            for (r, c) in fallback[:mines_left]:
                self.grid[r][c].mine = True
        self._compute_numbers()
        self._mines_placed = True

    def reveal(self, r: int, c: int):
        if self.game_over:
            return
        if not self._mines_placed:
            self.place_mines(avoid=(r, c))
        cell = self.grid[r][c]
        if cell.flagged or cell.revealed:
            return
        cell.revealed = True
        self.revealed_count += 1
        if cell.mine:
            self.game_over = True
            return
        if cell.number == 0:
            for (rr, cc) in self.neighbors(r, c):
                if not self.grid[rr][cc].revealed and not self.grid[rr][cc].flagged:
                    self.reveal(rr, cc)
        self._check_win()

    def toggle_flag(self, r: int, c: int):
        if self.game_over or self.grid[r][c].revealed:
            return
        self.grid[r][c].flagged = not self.grid[r][c].flagged

    def frontier_numbered(self) -> List[Tuple[int, int]]:
        f = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.revealed and cell.number > 0:
                    if any(not self.grid[rr][cc].revealed and not self.grid[rr][cc].flagged for (rr, cc) in self.neighbors(r, c)):
                        f.append((r, c))
        return f

    def hidden_unflagged(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(self.rows) for c in range(self.cols)
                if not self.grid[r][c].revealed and not self.grid[r][c].flagged]

    def flagged_cells(self) -> Set[Tuple[int, int]]:
        return {(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c].flagged}

    def mines_remaining_estimate(self) -> int:
        return max(0, self.mines_count - len(self.flagged_cells()))

    def _check_win(self):
        total = self.rows * self.cols
        non_mines = total - self.mines_count
        if self.revealed_count == non_mines and not self.game_over:
            self.won = True
            self.game_over = True
