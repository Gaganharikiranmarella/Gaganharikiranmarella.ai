import numpy as np

class MinesweeperAI:
    def __init__(self, game):
        self.game = game

    def get_safe_moves(self):
        """
        Returns a list of tiles (x, y) that are safe to reveal based on heuristic and sub-heuristic values.
        We consider tiles with low combined heuristic values as safer.
        """
        safe_moves = []
        for i in range(self.game.size):
            for j in range(self.game.size):
                if not self.game.revealed[i, j] and not self.game.flagged[i, j]:
                    combined_value = self.game.heuristic[i, j] if self.game.heuristic[i, j] > 0 else self.game.sub_heuristic[i, j]
                    # Threshold can be tuned; here <=1.5 considered safe-ish
                    if combined_value <= 1.5:
                        safe_moves.append((i, j))
        return safe_moves

    def get_mine_flags(self):
        """
        Returns a list of tiles (x, y) that are likely mines and can be flagged.
        We consider tiles with high heuristic values as probable mines.
        """
        mine_flags = []
        for i in range(self.game.size):
            for j in range(self.game.size):
                if not self.game.flagged[i, j] and not self.game.revealed[i, j]:
                    if self.game.heuristic[i, j] >= 2.5:  # heuristic max is 3
                        mine_flags.append((i, j))
        return mine_flags

    def make_move(self):
        """
        Decide next move: prioritize flagging likely mines, otherwise reveal safest tile.
        """
        if self.game.game_over:
            return None

        mines_to_flag = self.get_mine_flags()
        if mines_to_flag:
            # Flag first mine candidate
            return ("flag", mines_to_flag[0])

        safe_moves = self.get_safe_moves()
        if safe_moves:
            # Reveal first safe candidate
            return ("reveal", safe_moves[0])

        # If no safe or flag moves found, pick random unrevealed tile (least preferred)
        candidates = [(i, j) for i in range(self.game.size) for j in range(self.game.size)
                      if not self.game.revealed[i, j] and not self.game.flagged[i, j]]
        if candidates:
            return ("reveal", candidates[0])

        return None  # no moves left
