from geopy.distance import geodesic
import streamlit as st

if "strike_log" not in st.session_state:
    st.session_state.strike_log = []

if "missile_paths" not in st.session_state:
    st.session_state.missile_paths = []

def simulate_strike(coords):
    st.warning("Satellite scanning for signal...")
    st.success("✅ Target locked. ICBM strike simulated.")
    st.session_state.strike_log.append(coords)
    st.session_state.missile_paths.append((get_command_hq_coords(), coords))

def calculate_distance(target_coords):
    return geodesic(get_command_hq_coords(), target_coords).km

def get_command_hq_coords():
    return (28.6139, 77.2090)  # New Delhi
