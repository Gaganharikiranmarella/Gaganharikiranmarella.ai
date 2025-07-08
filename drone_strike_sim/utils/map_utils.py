import folium

def create_base_map():
    base_coords = [20.5937, 78.9629]  # India center
    m = folium.Map(location=base_coords, zoom_start=5)

    # Add Command HQ marker
    folium.Marker(
        location=[28.6139, 77.2090],
        tooltip="Command HQ (New Delhi)",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    # ✅ This enables coordinate capture on click
    folium.LatLngPopup().add_to(m)

    return m
