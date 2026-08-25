def estimate_water_depth(elevation, slope):
    """
    Elevation aur Slope ke aadhar par estimated groundwater depth (feet aur meters) calculate karta hai.
    """
    # Elevation aur slope baseline formula
    base_depth_m = 15.0 + (elevation * 0.05) + (slope * 2.5)
    
    # Cap boundaries (Realistic range: 10m to 120m)
    depth_m = max(10.0, min(base_depth_m, 120.0))
    depth_ft = depth_m * 3.28084
    
    if depth_m < 30:
        zone_color = "Green (Shallow / High Water Level)"
        water_risk = "Low Drilling Cost"
    elif depth_m < 60:
        zone_color = "Yellow (Moderate Water Level)"
        water_risk = "Moderate Drilling Depth"
    else:
        zone_color = "Red (Deep Water Table)"
        water_risk = "High Drilling Depth Required"
        
    return round(depth_m, 1), round(depth_ft, 1), zone_color, water_risk