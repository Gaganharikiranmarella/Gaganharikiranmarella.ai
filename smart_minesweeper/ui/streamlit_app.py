import streamlit as st
import numpy as np
from ai.game_logic import MinesweeperGame
from ai.ai_agent import MinesweeperAI

def tile_color(heuristic, sub_heuristic, revealed, flagged):
    if flagged:
        return "#ff6961"  # Red for flagged
    if not revealed:
        return "#d3d3d3"  # Light gray for unrevealed
    # Gradient from yellow (low) to dark orange (high) based on heuristic/sub-heuristic
    val = heuristic if heuristic > 0 else sub_heuristic
    if val >= 2.5:
        return "#ff4500"
    elif val >= 2:
        return "#ff7f50"
    elif val >= 1.5:
        return "#ffa500"
    elif val >= 1:
        return "#ffd700"
    else:
        return "#ffffe0"

st.set_page_config(page_title="Smart Minesweeper", layout="wide")

st.title("Smart Minesweeper with Heuristic + Sub-Heuristic AI")

if "game" not in st.session_state:
    st.session_state.game = MinesweeperGame()
    st.session_state.ai = MinesweeperAI(st.session_state.game)

game = st.session_state.game
ai = st.session_state.ai

cols = st.columns(game.size)

status_txt = ""
if game.game_over:
    status_txt = "💥 Game Over! You hit a mine."
elif game.check_win():
    status_txt = "🏆 You Win! All mines flagged and safe tiles revealed."

st.markdown(f"### {status_txt}")

action = st.radio("Choose action:", options=["Reveal", "Flag"], horizontal=True, index=0)

if not game.game_over and not game.check_win():
    for i in range(game.size):
        with cols[i]:
            for j in range(game.size):
                label = "🚩" if game.flagged[i, j] else ("?" if not game.revealed[i, j] else f"{game.heuristic[i,j]:.1f}" if game.heuristic[i,j] > 0 else f"{game.sub_heuristic[i,j]:.1f}")
                color = tile_color(game.heuristic[i,j], game.sub_heuristic[i,j], game.revealed[i,j], game.flagged[i,j])
                if st.button(label, key=f"{i}-{j}", help=f"Heuristic: {game.heuristic[i,j]:.2f}\nSub-Heuristic: {game.sub_heuristic[i,j]:.2f}", use_container_width=True):
                    if action == "Reveal":
                        result = game.reveal(i, j)
                        if result == "hit_mine":
                            st.error("Boom! You hit a mine.")
                    else:
                        game.flag(i, j)

if st.button("AI Suggest Move"):
    move = ai.make_move()
    if move:
        act, (x, y) = move
        if act == "reveal":
            game.reveal(x, y)
            st.info(f"AI chooses to reveal tile ({x},{y})")
        elif act == "flag":
            game.flag(x, y)
            st.info(f"AI chooses to flag tile ({x},{y})")
    else:
        st.info("No moves available.")

if st.button("Restart Game"):
    st.session_state.game = MinesweeperGame()
    st.session_state.ai = MinesweeperAI(st.session_state.game)
    st.experimental_rerun()
