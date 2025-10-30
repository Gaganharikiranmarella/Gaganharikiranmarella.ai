import flet as ft

def toolbar(game, on_step, on_auto, on_reveal_all) -> ft.Row:
    return ft.Row(
        spacing=12,
        controls=[
            ft.ElevatedButton("🧠 Step", on_click=lambda e: on_step(), disabled=game.game_over),
            ft.ElevatedButton("🤖 Auto", on_click=lambda e: on_auto(), disabled=game.game_over),
            ft.OutlinedButton("🪄 Reveal All", on_click=lambda e: on_reveal_all()),
        ],
    )
