import flet as ft
from dataclasses import dataclass
from typing import List, Tuple
import random

@dataclass
class Cell:
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    number: int = 0

class Minesweeper:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self._place_mines()
        self._compute_numbers()
    
    def _place_mines(self):
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        random.shuffle(spots)
        for r, c in spots[:self.mines_count]:
            self.grid[r][c].mine = True
    
    def _compute_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].mine:
                    count = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            rr, cc = r + dr, c + dc
                            if 0 <= rr < self.rows and 0 <= cc < self.cols:
                                if self.grid[rr][cc].mine:
                                    count += 1
                    self.grid[r][c].number = count
    
    def reveal(self, r: int, c: int):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        if cell.mine:
            self.game_over = True
            return
        # Check win
        revealed_safe = sum(1 for row in self.grid for cell in row if cell.revealed and not cell.mine)
        total_safe = self.rows * self.cols - self.mines_count
        if revealed_safe == total_safe:
            self.won = True
            self.game_over = True
        # Auto-reveal neighbors if 0
        if cell.number == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols:
                        self.reveal(rr, cc)
    
    def toggle_flag(self, r: int, c: int):
        if not self.game_over and not self.grid[r][c].revealed:
            self.grid[r][c].flagged = not self.grid[r][c].flagged
    
    def get_flag_count(self):
        return sum(1 for row in self.grid for cell in row if cell.flagged)

def main(page: ft.Page):
    page.title = "Minesweeper"
    page.padding = 40
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    game = Minesweeper(4, 4, 3)
    board_container = ft.Container()
    
    def make_cell_button(r, c):
        cell = game.grid[r][c]
        
        if cell.revealed:
            if cell.mine:
                return ft.Container(
                    content=ft.Text("💣", size=24),
                    width=70, height=70,
                    bgcolor="#ffebee",
                    border_radius=8,
                    alignment=ft.alignment.center
                )
            else:
                label = str(cell.number) if cell.number > 0 else ""
                return ft.Container(
                    content=ft.Text(label, size=24, weight=ft.FontWeight.BOLD, color="#000000"),
                    width=70, height=70,
                    bgcolor="#eceff1",
                    border_radius=8,
                    alignment=ft.alignment.center
                )
        else:
            # Hidden cell with super tight buttons
            return ft.Container(
                content=ft.Column([
                    ft.Text("🚩" if cell.flagged else "", size=14),
                    ft.Row([
                        ft.Container(
                            content=ft.IconButton(
                                icon="touch_app",
                                icon_size=20,
                                on_click=lambda e, rr=r, cc=c: reveal_click(rr, cc),
                                tooltip="Reveal",
                            ),
                            width=32,
                            height=32,
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon="flag",
                                icon_size=20,
                                on_click=lambda e, rr=r, cc=c: flag_click(rr, cc),
                                tooltip="Flag",
                            ),
                            width=32,
                            height=32,
                        ),
                    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
                ], 
                spacing=0, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
                ),
                width=70, height=70,
                bgcolor="#546e7a",
                border_radius=8,
                alignment=ft.alignment.center,
                padding=6
            )
    
    def reveal_click(r, c):
        game.reveal(r, c)
        rebuild()
        # Auto-generate new board if game ended
        if game.game_over:
            page.run_task(auto_new_game)
    
    def flag_click(r, c):
        game.toggle_flag(r, c)
        rebuild()
    
    async def auto_new_game():
        import asyncio
        await asyncio.sleep(2)  # Wait 2 seconds before new game
        reset_game(None)
    
    def rebuild():
        rows = []
        for r in range(game.rows):
            row = ft.Row(
                [make_cell_button(r, c) for c in range(game.cols)],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER
            )
            rows.append(row)
        
        board_container.content = ft.Column(
            rows,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        if game.won:
            status.value = "✅ You won! 🎉 (New game in 2s...)"
            status.color = "#2e7d32"
        elif game.game_over:
            status.value = "💥 Game Over! (New game in 2s...)"
            status.color = "#c62828"
        else:
            flags = game.get_flag_count()
            status.value = f"🚩 Flags: {flags}/{game.mines_count}"
            status.color = "#546e7a"
        
        page.update()
    
    status = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    
    def reset_game(e):
        nonlocal game
        game = Minesweeper(4, 4, 3)
        rebuild()
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("💣 Minesweeper", size=32, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                board_container,
                ft.Container(height=20),
                status,
                ft.Container(height=10),
                ft.ElevatedButton("🔄 New Game", on_click=reset_game, width=150),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    )
    
    rebuild()

if __name__ == "__main__":
    ft.app(target=main)
