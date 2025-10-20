import requests

def get_solar_forecast(api_key, lat, lon, simulate=False):
    """
    Fetch hourly solar output from NREL PVWatts API or simulate it for testing.
    Returns a list of 24 hourly kWh values.
    """
    if simulate or not api_key:
        # Simulated solar output: bell curve peaking at noon
        return [0.2 * (12 - abs(i - 12)) for i in range(24)]

    url = (
        f"https://developer.nrel.gov/api/pvwatts/v6.json?"
        f"api_key={api_key}&lat={lat}&lon={lon}"
        f"&system_capacity=5&azimuth=180&tilt=40"
        f"&array_type=1&module_type=1&losses=10"
    )

    try:
        response = requests.get(url)
        data = response.json()
        print("🔍 NREL API response:", data)

        if 'outputs' in data and 'ac' in data['outputs']:
            # Convert watts to kilowatt-hours
            return [val / 1000 for val in data['outputs']['ac'][:24]]
        else:
            print("⚠️ Missing 'ac' key in outputs. Full response:", data)
            return [0] * 24
    except Exception as e:
        print("❌ Error fetching solar data:", e)
        return [0] * 24