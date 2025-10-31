import flet as ft

# Hex strings are stable across Flet versions
BG = "#FFFFFF"
TEXT = "#000000"
MUTED = "#546E7A"     # blue_grey_600
BORDER = "#B0BEC5"    # blue_grey_200
TILE = "#ECEFF1"      # blue_grey_50
BOMB_BG = "#FFEBEE"   # red_50
BOMB_FG = "#B71C1C"   # red_900

def tile_container(content: ft.Control, bg: str, fg: str) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=bg,
        border=ft.border.all(2, BORDER),
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )
