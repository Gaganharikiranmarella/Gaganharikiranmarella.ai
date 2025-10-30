import flet as ft

# Centralized colors and styles so UI is consistent
BG = ft.colors.WHITE
TEXT = ft.colors.BLACK
MUTED = ft.colors.BLUE_GREY_600
BORDER = ft.colors.BLUE_GREY_200
TILE = ft.colors.BLUE_GREY_50
BOMB_BG = ft.colors.RED_50
BOMB_FG = ft.colors.RED_900

def tile_container(content: ft.Control, bg: str, fg: str) -> ft.Container:
    return ft.Container(
        content,
        bgcolor=bg,
        border=ft.border.all(2, BORDER),
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )
