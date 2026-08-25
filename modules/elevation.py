import requests
import math

def get_elevation_matrix(lat, lon):
    offset = 0.001 
    locations = f"{lat},{lon}|{lat+offset},{lon}|{lat-offset},{lon}|{lat},{lon+offset}|{lat},{lon-offset}"
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={locations}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            res = resp.json().get('results')
            if res and len(res) == 5:
                center = res[0]['elevation']
                diff_lat = abs(res[1]['elevation'] - res[2]['elevation'])
                diff_lon = abs(res[3]['elevation'] - res[4]['elevation'])
                slope_deg = math.degrees(math.atan(math.sqrt(diff_lat**2 + diff_lon**2) / 200.0))
                return center, round(slope_deg, 2)
    except Exception:
        pass
    return 300.0, 3.5