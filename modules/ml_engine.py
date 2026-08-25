import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_and_predict(elevation, slope, soil_type, season):
    # Dummy Training Data for Ground Water Depth Prediction
    # Features: [elevation, slope, soil_factor, season_factor]
    X_train = np.array([
        [100, 2.0, 1.0, 1.0], [500, 12.0, 0.5, 0.5],
        [200, 5.0, 0.8, 1.2], [50, 1.0, 1.2, 0.8],
        [300, 8.0, 0.6, 1.0], [150, 3.5, 0.9, 1.1]
    ])
    # Target: Depth in meters
    y_train = np.array([18.5, 45.0, 28.0, 12.0, 35.0, 22.0])
    
    # Train Model
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Feature Mappings
    soil_map = {"Alluvial (Best Infiltration)": 1.2, "Sandy Soil": 1.0, "Clay Soil": 0.7, "Basalt/Hard Rock": 0.5}
    season_map = {"Post-Monsoon (High Water)": 0.8, "Monsoon": 0.7, "Pre-Monsoon (Low Water)": 1.2}
    
    sf = soil_map.get(soil_type, 1.0)
    seaf = season_map.get(season, 1.0)
    
    # Predict Depth
    pred_m = round(float(model.predict([[elevation, slope, sf, seaf]])[0]), 1)
    pred_ft = round(pred_m * 3.28084, 1)
    
    # Confidence Score
    confidence = int(max(60, min(95, 100 - (slope * 2) - (pred_m * 0.5))))
    
    return pred_m, pred_ft, confidence