import streamlit as st
from streamlit_folium import st_folium
import folium
from utils.map_utils import create_base_map
from utils.strike_logic import simulate_strike, calculate_distance, get_command_hq_coords

# ──────────────────────────────────────────────
# 🔐 Load Secret Key from File
# ──────────────────────────────────────────────
try:
    with open("secret_key.txt", "r") as f:
        SECRET_CODE = f.read().strip()
except FileNotFoundError:
    st.error("🔐 Secret key file not found. Please add 'secret_key.txt'.")
    st.stop()

# ──────────────────────────────────────────────
# Page setup & session state init
# ──────────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("🛰️ AI‑Based Satellite Drone Strike Simulation")

init_state = {
    "marker_coords": None,
    "last_input": "",
    "strike_log": [],
    "missile_paths": [],
    "attempts_left": 3,
    "launch_locked": False,
    "launch_triggered": False
}

for key, default in init_state.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ──────────────────────────────────────────────
# Layout → 2 Columns: Map (left), Strike Console (right)
# ──────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

# 1️⃣ LEFT COLUMN – Mission Map
with col1:
    st.subheader("🗺️ Mission Control Map")
    m = create_base_map()

    # Draw existing strikes and paths
    for idx, coord in enumerate(st.session_state.strike_log):
        folium.CircleMarker(
            location=coord,
            radius=20,
            color="red",
            fill=True,
            fill_opacity=0.7,
            popup=f"Strike #{idx+1}",
        ).add_to(m)

    for path in st.session_state.missile_paths:
        folium.PolyLine(
            locations=[path[0], path[1]],
            color="orange",
            weight=4,
            dash_array="5,10",
            tooltip="Missile Trajectory",
        ).add_to(m)

    clicked_data = st_folium(m, width=750, height=500, key="main_map")

    if clicked_data and clicked_data.get("last_clicked"):
        coords = clicked_data["last_clicked"]
        st.session_state.marker_coords = (coords["lat"], coords["lng"])
        st.session_state.launch_triggered = False  # allow launch again
        st.success(f"📍 Marker placed at: {st.session_state.marker_coords}")

# 2️⃣ RIGHT COLUMN – Strike Console
with col2:
    st.subheader("🧨 Strike Console")

    if st.session_state.launch_locked:
        st.error("❌ Access denied. Launch permanently disabled after 3 failed attempts.")

    elif st.session_state.marker_coords:
        entered_key = st.text_input("Enter Launch Key and press Enter", key="input_key")

        if entered_key and not st.session_state.launch_triggered:
            if entered_key == SECRET_CODE:
                st.session_state.launch_triggered = True  # prevent re-launch
                st.session_state.last_input = entered_key
                simulate_strike(st.session_state.marker_coords)
                distance = calculate_distance(st.session_state.marker_coords)
                hq = get_command_hq_coords()
                st.session_state.missile_paths.append((hq, st.session_state.marker_coords))
                st.success("💥 Strike executed successfully!")
                st.info(f"📡 Distance from HQ: {distance:.2f} km")
            else:
                st.session_state.attempts_left -= 1
                if st.session_state.attempts_left <= 0:
                    st.session_state.launch_locked = True
                    st.error("❌ Wrong key. You have been locked out.")
                else:
                    st.warning(f"⚠️ Wrong key. Attempts left: {st.session_state.attempts_left}")
    else:
        st.text_input("Place a marker first…", disabled=True)

# 🧾 STRIKE HISTORY
if st.session_state.strike_log:
    st.markdown("### 📜 Strike History")
    for idx, coord in enumerate(st.session_state.strike_log, 1):
        st.write(f"{idx}. Lat/Lon → {coord}")
