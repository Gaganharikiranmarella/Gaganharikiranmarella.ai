import flet as ft

# Use ft.Colors or hex strings to avoid attribute errors across versions
BG = ft.Colors.WHITE
TEXT = ft.Colors.BLACK
MUTED = ft.Colors.BLUE_GREY_600
BORDER = ft.Colors.BLUE_GREY_200
TILE = ft.Colors.BLUE_GREY_50
BOMB_BG = ft.Colors.RED_50
BOMB_FG = ft.Colors.RED_900

def tile_container(content: ft.Control, bg: str, fg: str) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=bg,
        border=ft.border.all(2, BORDER),
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )
