import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium

def render_map(lat=None, lon=None, zone_color="yellow"):
    start_lat = lat if lat else 24.5
    start_lon = lon if lon else 81.5
    start_zoom = 10 if lat else 7

    m = folium.Map(location=[start_lat, start_lon], zoom_start=start_zoom, tiles=None)
    
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google Satellite Hybrid',
        name='Google Satellite + Roads',
        overlay=False,
        control=True
    ).add_to(m)

    Geocoder(position='topleft', add_marker=True).add_to(m)
    m.add_child(folium.LatLngPopup())
    
    if lat and lon:
        hex_color = "#22c55e" if "Green" in str(zone_color) else ("#eab308" if "Yellow" in str(zone_color) else "#ef4444")
        
        folium.Marker(
            [lat, lon],
            popup=f"Target: {lat:.4f}, {lon:.4f}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        folium.Circle(
            radius=1500,
            location=[lat, lon],
            color=hex_color,
            fill=True,
            fill_color=hex_color,
            fill_opacity=0.3
        ).add_to(m)
    
    return st_folium(m, width=700, height=520, key="water_map")