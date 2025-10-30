import flet as ft
from typing import Callable
from game.board import Minesweeper
from .palette import tile_container, MUTED, TILE, BOMB_BG, BOMB_FG

def cell_tile(game: Minesweeper, r: int, c: int, on_reveal: Callable, on_flag: Callable) -> ft.Container:
    cell = game.grid[r][c]
    if cell.revealed:
        if cell.mine:
            face = ft.Text("💣", size=24, weight=ft.FontWeight.BOLD, color=BOMB_FG)
            tile = tile_container(face, BOMB_BG, BOMB_FG)
            aria = "Revealed bomb"
        else:
            label = str(cell.number) if cell.number > 0 else " "
            face = ft.Text(label, size=20, weight=ft.FontWeight.W_800)
            tile = tile_container(face, TILE, "black")
            aria = f"Revealed {'number ' + str(cell.number) if cell.number>0 else 'empty'}"
        actions = ft.Row(spacing=6, controls=[
            ft.IconButton(icon=ft.icons.SIGNPOST, tooltip="Reveal (disabled)", disabled=True),
            ft.IconButton(icon=ft.icons.FLAG, tooltip="Flag (disabled)", disabled=True),
        ])
    else:
        face = ft.Text("🚩" if cell.flagged else " ", size=20, weight=ft.FontWeight.W_800, color="white")
        tile = tile_container(face, MUTED, "white")
        aria = "Hidden cell" + (" flagged" if cell.flagged else "")
        actions = ft.Row(spacing=6, controls=[
            ft.IconButton(icon=ft.icons.SIGNPOST, tooltip=f"Reveal {r+1},{c+1}", on_click=lambda e,on_reveal=on_reveal: on_reveal(r, c)),
            ft.IconButton(icon=ft.icons.FLAG, tooltip=f"Flag {r+1},{c+1}", on_click=lambda e,on_flag=on_flag: on_flag(r, c)),
        ])
    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[tile, actions],
            ),
            padding=8,
            width=88,
        ),
        semantic_label=f"Cell {r+1},{c+1}. {aria}",
    )
    return card

def board_grid(game: Minesweeper, on_reveal: Callable, on_flag: Callable) -> ft.GridView:
    gv = ft.GridView(
        expand=True,
        runs_count=0,          # auto
        max_extent=110,        # each card max width
        child_aspect_ratio=0.95,
        spacing=10,
        run_spacing=10,
    )
    for r in range(game.rows):
        for c in range(game.cols):
            gv.controls.append(cell_tile(game, r, c, on_reveal, on_flag))
    return gv
