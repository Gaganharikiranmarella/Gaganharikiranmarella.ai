import numpy as np
import random

class MinesweeperGame:
    def __init__(self, size=16, mines_count=3):
        self.size = size
        self.mines_count = mines_count
        self.board = np.zeros((size, size), dtype=int)  # -1 for mines, 0 safe
        self.heuristic = np.zeros((size, size), dtype=float)
        self.sub_heuristic = np.zeros((size, size), dtype=float)
        self.revealed = np.full((size, size), False)
        self.flagged = np.full((size, size), False)
        self.game_over = False
        self.mines = []
        self.place_mines()
        self.assign_heuristics_and_subheuristics()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x, y] != -1:
                self.board[x, y] = -1
                self.mines.append((x,y))
                mines_placed += 1

    def get_neighbors(self, x, y, radius=1):
        neighbors = []
        for i in range(max(0, x - radius), min(self.size, x + radius + 1)):
            for j in range(max(0, y - radius), min(self.size, y + radius + 1)):
                if not (i == x and j == y):
                    neighbors.append((i, j))
        return neighbors

    def distance(self, x1, y1, x2, y2):
        # Chebyshev distance for adjacency in grid
        return max(abs(x1 - x2), abs(y1 - y2))

    def assign_heuristics_and_subheuristics(self):
        # Reset heuristic matrices
        self.heuristic.fill(0)
        self.sub_heuristic.fill(0)

        # Assign heuristic values near mines
        for (mx, my) in self.mines:
            for (nx, ny) in self.get_neighbors(mx, my, radius=2):
                dist = self.distance(mx, my, nx, ny)
                if dist == 1:
                    self.heuristic[nx, ny] = 3  # closest proximity
                elif dist == 2:
                    # Assign heuristic only if not set or lower than current
                    if self.heuristic[nx, ny] < 2:
                        self.heuristic[nx, ny] = 2

        # Assign sub-heuristic for all other tiles
        for i in range(self.size):
            for j in range(self.size):
                if self.heuristic[i, j] == 0 and (i, j) not in self.mines:
                    neighbors = self.get_neighbors(i, j, radius=3)
                    weighted_sum = 0
                    total_weight = 0
                    for (nx, ny) in neighbors:
                        dist = self.distance(i, j, nx, ny)
                        weight = 1 / (dist + 1)
                        weighted_sum += self.heuristic[nx, ny] * weight
                        total_weight += weight
                    self.sub_heuristic[i, j] = weighted_sum / total_weight if total_weight > 0 else 0

    def reveal(self, x, y):
        if self.game_over or self.revealed[x, y] or self.flagged[x, y]:
            return
        if self.board[x, y] == -1:
            self.game_over = True
            return "hit_mine"
        self.revealed[x, y] = True
        # If heuristic or sub-heuristic is very low, reveal neighbors recursively
        combined_value = self.heuristic[x, y] if self.heuristic[x, y] > 0 else self.sub_heuristic[x, y]
        if combined_value <= 1:
            self.reveal_neighbors(x, y)
        return "safe"

    def reveal_neighbors(self, x, y):
        for (nx, ny) in self.get_neighbors(x, y):
            if not self.revealed[nx, ny] and not self.flagged[nx, ny]:
                self.revealed[nx, ny] = True
                combined_value = self.heuristic[nx, ny] if self.heuristic[nx, ny] > 0 else self.sub_heuristic[nx, ny]
                if combined_value <= 1:
                    self.reveal_neighbors(nx, ny)

    def flag(self, x, y):
        if self.game_over or self.revealed[x, y]:
            return
        self.flagged[x, y] = not self.flagged[x, y]

    def check_win(self):
        mines_flagged_correctly = np.all((self.flagged == (self.board == -1)))
        all_safe_revealed = np.all(self.revealed | (self.board == -1))
        return mines_flagged_correctly and all_safe_revealed
