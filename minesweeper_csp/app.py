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

    # Persistent state containers on first run
    if not hasattr(page, "params"):
        page.params = (9, 9, 10, True)  # rows, cols, mines, first_click_safe [web:242]
    if not hasattr(page, "game") or page.game is None:
        r0, c0, m0, fc0 = page.params
        page.game = Minesweeper(r0, c0, m0, first_click_safe=fc0)  # ensure game exists before UI uses it [web:242]

    # Hosts
    header = ft.Text("Minesweeper + CSP", size=26, weight=ft.FontWeight.W_800)
    board_host = ft.Container(expand=True)
    status = ft.Text("", size=14)

    # Handlers that board controls will capture
    def on_reveal(r, c):
        g = page.game
        if g and not g.game_over:
            g.reveal(r, c)
            refresh()  # rebuild board after state change [web:185]

    def on_flag(r, c):
        g = page.game
        if g and not g.game_over:
            g.toggle_flag(r, c)
            refresh()  # rebuild board after state change [web:185]

    # Refresh UI tree from current game
    def refresh():
        board_host.content = board_grid(page.game, on_reveal, on_flag)  # new GridView from game state [web:262]
        g = page.game
        if g.won:
            status.value = "✅ You won! Board complete."
        elif g.game_over:
            status.value = "💥 Game over — a mine was revealed."
        else:
            status.value = f"ℹ️ Grid: {g.rows}×{g.cols} | Mines: {g.mines_count} | Flags: {len(g.flagged_cells())}"
        page.update()  # commit UI changes [web:242]

    # Create/replace the game instance and rebuild
    def reset_game(rows, cols, mines, fc):
        page.game = Minesweeper(rows, cols, mines, first_click_safe=fc)  # new state [web:242]
        refresh()

    # Settings card with robust Reset
    r0, c0, m0, fc0 = page.params
    rows_tf = ft.TextField(label="Rows", value=str(r0), width=120, keyboard_type=ft.KeyboardType.NUMBER)  # numeric input hint [web:239]
    cols_tf = ft.TextField(label="Cols", value=str(c0), width=120, keyboard_type=ft.KeyboardType.NUMBER)  # numeric input hint [web:239]
    mines_tf = ft.TextField(label="Mines", value=str(m0), width=120, keyboard_type=ft.KeyboardType.NUMBER)  # numeric input hint [web:239]
    fc_safe_sw = ft.Switch(label="First click safe", value=fc0)

    def on_reset(e):
        # Parse and clamp values to safe ranges
        try:
            rr = int(rows_tf.value)
            cc = int(cols_tf.value)
        except Exception:
            rr, cc = r0, c0
        rr = max(5, min(30, rr))
        cc = max(5, min(30, cc))
        try:
            mm = int(mines_tf.value)
        except Exception:
            mm = m0
        mm = max(1, min(rr * cc - 1, mm))
        ff = bool(fc_safe_sw.value)
        # Persist, normalize inputs, rebuild game and board
        page.params = (rr, cc, mm, ff)  # save params [web:242]
        rows_tf.value, cols_tf.value, mines_tf.value = str(rr), str(cc), str(mm)  # reflect clamped values [web:239]
        reset_game(rr, cc, mm, ff)  # recompose UI [web:185]

    # Enter-to-apply for quick changes
    rows_tf.on_submit = on_reset  # apply on Enter [web:239]
    cols_tf.on_submit = on_reset  # apply on Enter [web:239]
    mines_tf.on_submit = on_reset  # apply on Enter [web:239]

    settings_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("New Game", weight=ft.FontWeight.BOLD, size=16),
                    ft.Row(spacing=8, controls=[rows_tf, cols_tf, mines_tf]),
                    fc_safe_sw,
                    ft.ElevatedButton("🔁 Reset", on_click=on_reset),
                ],
            ),
            padding=12,
        )
    )

    # Solver actions
    def do_step():
        g = page.game
        if g and not g.game_over:
            safe, mines_to_flag, guess = next_actions(g)
            apply_actions(g, safe, mines_to_flag, guess)
            refresh()

    def do_auto():
        g = page.game
        if g and not g.game_over:
            steps = 0
            while not g.game_over and steps < 500:
                safe, mines_to_flag, guess = next_actions(g)
                changed = apply_actions(g, safe, mines_to_flag, guess)
                steps += 1
                if not changed:
                    break
            refresh()

    def do_reveal_all():
        g = page.game
        for r in range(g.rows):
            for c in range(g.cols):
                if not g.grid[r][c].revealed and not g.grid[r][c].flagged:
                    g.grid[r][c].revealed = True
        refresh()

    actions = toolbar(page.game, do_step, do_auto, do_reveal_all)  # simple toolbar row [web:178]

    # Initial composition
    refresh()  # build board and status now that handlers/state are ready [web:185]

    # Mount page
    page.add(
        header,
        settings_card,
        actions,
        board_host,
        status
    )

if __name__ == "__main__":
    ft.app(target=main)
