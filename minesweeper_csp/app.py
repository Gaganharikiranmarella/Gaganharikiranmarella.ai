import flet as ft
from game.board import Minesweeper
from game.solver import next_actions, apply_actions
from ui.board_view import board_grid
from ui.toolbar import toolbar

def main(page: ft.Page):
    page.title = "Minesweeper + CSP (Flet)"
    page.padding = 16
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # Session-like state
    if not hasattr(page, "game"):
        page.game = None
        page.params = (9, 9, 10, True)

    # Sidebar-like controls
    def reset_game(rows, cols, mines, fc):
        page.game = Minesweeper(rows, cols, mines, first_click_safe=fc)
        page.update()

    r0, c0, m0, fc0 = page.params
    rows = ft.TextField(label="Rows", value=str(r0), width=150)
    cols = ft.TextField(label="Cols", value=str(c0), width=150)
    mines = ft.TextField(label="Mines", value=str(m0), width=150)
    fc_safe = ft.Switch(label="First click safe", value=fc0)

    def on_reset(e):
        try:
            rr = max(5, min(30, int(rows.value)))
            cc = max(5, min(30, int(cols.value)))
            mm = max(1, min(rr*cc-1, int(mines.value)))
            ff = bool(fc_safe.value)
            page.params = (rr, cc, mm, ff)
            reset_game(rr, cc, mm, ff)
        except Exception:
            pass

    settings_card = ft.Card(
        content=ft.Container(
            content=ft.Column(spacing=8, controls=[
                ft.Text("New Game", weight=ft.FontWeight.BOLD, size=16),
                ft.Row(spacing=8, controls=[rows, cols, mines]),
                fc_safe,
                ft.ElevatedButton("🔁 Reset", on_click=on_reset),
            ]),
            padding=12
        )
    )

    if page.game is None:
        reset_game(*page.params)

    # Handlers
    def on_reveal(r, c):
        if not page.game.game_over:
            page.game.reveal(r, c)
            refresh()

    def on_flag(r, c):
        if not page.game.game_over:
            page.game.toggle_flag(r, c)
            refresh()

    def do_step():
        if page.game.game_over:
            return
        safe, mines_to_flag, guess = next_actions(page.game)
        apply_actions(page.game, safe, mines_to_flag, guess)
        refresh()

    def do_auto():
        if page.game.game_over:
            return
        steps = 0
        while not page.game.game_over and steps < 500:
            safe, mines_to_flag, guess = next_actions(page.game)
            changed = apply_actions(page.game, safe, mines_to_flag, guess)
            steps += 1
            if not changed:
                break
        refresh()

    def do_reveal_all():
        for r in range(page.game.rows):
            for c in range(page.game.cols):
                if not page.game.grid[r][c].revealed and not page.game.grid[r][c].flagged:
                    page.game.grid[r][c].revealed = True
        refresh()

    # Layout containers
    header = ft.Text("Minesweeper + CSP", size=26, weight=ft.FontWeight.W_800)
    actions = toolbar(page.game, do_step, do_auto, do_reveal_all)
    status = ft.Text("", size=14)

    board_host = ft.Container(expand=True)

    def refresh():
        board_host.content = board_grid(page.game, on_reveal, on_flag)
        if page.game.won:
            status.value = "✅ You won! Board complete."
        elif page.game.game_over:
            status.value = "💥 Game over — a mine was revealed."
        else:
            status.value = f"ℹ️ Grid: {page.game.rows}×{page.game.cols} | Mines: {page.game.mines_count} | Flags: {len(page.game.flagged_cells())}"
        page.update()

    # First render
    refresh()

    page.add(
        header,
        settings_card,
        actions,
        board_host,
        status
    )

if __name__ == "__main__":
    ft.app(target=main)
