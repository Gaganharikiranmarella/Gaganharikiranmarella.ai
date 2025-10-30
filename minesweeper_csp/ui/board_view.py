import flet as ft
from typing import Callable
from game.board import Minesweeper
from .palette import tile_container, MUTED, TILE, BOMB_BG, BOMB_FG

# Global flag mode toggle will be provided by app via context if desired; here we just expose both actions.

def _square_grid(rows: int, cols: int) -> ft.GridView:
    # Use equal max_extent and child_aspect_ratio=1.0 for perfect squares [web:167][web:272][web:279]
    return ft.GridView(
        expand=True,
        runs_count=0,
        max_extent=96,          # tile+padding width target; tweak for density
        child_aspect_ratio=1.0, # squares
        spacing=8,
        run_spacing=8,
    )

def cell_tile(game: Minesweeper, r: int, c: int, on_reveal: Callable, on_flag: Callable) -> ft.Control:
    cell = game.grid[r][c]

    # Build the visual tile face
    if cell.revealed:
        if cell.mine:
            face = ft.Text("💣", size=28, weight=ft.FontWeight.BOLD, color=BOMB_FG)
            tile = tile_container(face, BOMB_BG, BOMB_FG)
            aria = "Revealed bomb"
        else:
            label = str(cell.number) if cell.number > 0 else " "
            face = ft.Text(label, size=22, weight=ft.FontWeight.W_800)
            tile = tile_container(face, TILE, "black")
            aria = f"Revealed {'number ' + str(cell.number) if cell.number > 0 else 'empty'}"
        # Revealed tiles: no actions
        content = tile
    else:
        # Hidden/flagged tile – single large tap target reveals; a small flag button is included at corner
        face = ft.Text("🚩" if cell.flagged else " ", size=22, weight=ft.FontWeight.W_800, color="white")
        base = tile_container(face, MUTED, "white")
        aria = "Hidden cell" + (" flagged" if cell.flagged else "")

        rr, cc = r, c
        reveal_btn = ft.Container(  # full-tile tap area for reveal
            content=base,
            on_click=lambda e, r=rr, c=cc: on_reveal(r, c),
            ink=True,  # ripple feedback
        )
        # Small corner flag button to avoid misclicks on the main area
        flag_btn = ft.IconButton(
            icon="flag",
            tooltip=f"Flag {rr+1},{cc+1}",
            on_click=lambda e, r=rr, c=cc: on_flag(r, c),
            style=ft.ButtonStyle(
                padding=0,
                bgcolor={"": ft.colors.with_opacity(0.15, ft.Colors.BLACK)},
                shape=ft.RoundedRectangleBorder(radius=6),
            ),
            icon_size=16,
            width=28,
            height=28,
        )
        overlay = ft.Stack(  # place flag button over the top-right corner of the tile
            controls=[
                reveal_btn,
                ft.Container(
                    content=flag_btn,
                    right=4,
                    top=4,
                ),
            ],
        )
        content = overlay

    # Wrap in Semantics for SRs
    return ft.Semantics(label=f"Cell {r+1},{c+1}. {aria}", content=ft.Container(content=content, width=96, height=96))

def board_grid(game: Minesweeper, on_reveal: Callable, on_flag: Callable) -> ft.GridView:
    gv = _square_grid(game.rows, game.cols)
    for r in range(game.rows):
        for c in range(game.cols):
            gv.controls.append(cell_tile(game, r, c, on_reveal, on_flag))
    return gv
