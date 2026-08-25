import requests

def get_elevation(lat, lon):
    """
    Open-Elevation Public API se exact satellite elevation (sea level height in meters) fetch karta hai.
    """
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            elevation = data['results'][0]['elevation']
            return float(elevation)
        else:
            return 250.0  # Fallback default elevation
    except Exception as e:
        print(f"Elevation API Error: {e}")
        return 250.0