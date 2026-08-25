import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from components.map_ui import render_map
from modules.elevation import get_elevation_matrix
from modules.report_service import generate_pdf_report
from modules.depth_engine import estimate_water_depth
from modules.ml_engine import train_and_predict

st.set_page_config(page_title="Groundwater AI Finder", layout="wide")
st.title("🌊 Advanced Groundwater AI Analytics Engine")
st.write("Modular Architecture Version - Enterprise ML Ready")

# Sidebar Controls
st.sidebar.header("⚙️ Ground Parameters")
soil_type = st.sidebar.selectbox("Soil Type", ["Alluvial (Best Infiltration)", "Sandy Soil", "Basalt/Hard Rock", "Clay Soil"])
season = st.sidebar.selectbox("Season", ["Post-Monsoon (High Water)", "Pre-Monsoon (Low Water)", "Monsoon"])

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📍 Satellite Location Map")
    map_data = render_map()

with col2:
    st.subheader("📊 Hydrogeological Real-Time Data")
    if map_data and map_data.get("last_clicked"):
        click_lat = map_data["last_clicked"]["lat"]
        click_lon = map_data["last_clicked"]["lng"]
        
        st.info(f"**Target Location:**\nLat: `{click_lat:.5f}`, Lon: `{click_lon:.5f}`")
        
        with st.spinner("Running Random Forest ML Model..."):
            elevation, slope = get_elevation_matrix(click_lat, click_lon)
            depth_m, depth_ft, confidence = train_and_predict(elevation, slope, soil_type, season)
            _, _, zone, risk = estimate_water_depth(elevation, slope)
            
        m1, m2 = st.columns(2)
        m1.metric(label="🏔️ Elevation", value=f"{elevation} m")
        m2.metric(label="📐 Terrain Slope", value=f"{slope}°")
        
        st.markdown("---")
        st.subheader("🤖 AI Predicted Water Depth")
        d1, d2 = st.columns(2)
        d1.metric(label="📏 Depth (Feet)", value=f"{depth_ft} ft")
        d2.metric(label="🌐 Depth (Meters)", value=f"{depth_m} m")
        
        st.caption(f"**Zone:** {zone} | **Drilling:** {risk}")
        
        status_text = "High Potential Zone" if confidence >= 70 else "Moderate Potential Zone"
        st.progress(confidence / 100, text=f"AI Prediction Confidence: {confidence}%")
        
        pdf_file = generate_pdf_report(
            click_lat, click_lon, elevation, slope, 
            confidence, status_text, depth_m, depth_ft, risk
        )
        st.download_button(
            label="📄 Download Full Hydrogeology PDF Report",
            data=pdf_file,
            file_name=f"Groundwater_Report_{click_lat:.3f}_{click_lon:.3f}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("👈 Map par click karein ya location search karein.")