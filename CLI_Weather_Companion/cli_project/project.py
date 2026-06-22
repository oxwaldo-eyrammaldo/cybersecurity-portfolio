import sys
import requests

def main():
    print("--- CS50P Weather Companion ---")
    location = input("Enter a city or location: ").strip()
    if not location:
        sys.exit("Error: Location cannot be empty.")

    # 1. Fetch raw data
    data = fetch_weather_data(location)
    if not data:
        sys.exit("Error: Could not retrieve weather for that location.")

    # 2. Extract metrics
    temp, condition, wind = extract_metrics(data)

    # 3. Format and display
    output = format_weather_display(location, temp, condition, wind)
    print(output)


def fetch_weather_data(location):
    """Queries the wttr.in JSON API for a given location."""
    try:
        # Appending ?format=j1 requests a clean JSON schema
        url = f"https://wttr.in/{location}?format=j1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None
    return None


def extract_metrics(json_data):
    """Parses out the temperature, condition text, and wind speed from JSON."""
    try:
        current = json_data["current_condition"][0]
        temp_c = current["temp_C"]
        condition = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        return int(temp_c), condition, int(wind_speed)
    except (KeyError, IndexError, ValueError, TypeError):
        return None, None, None


def format_weather_display(loc, temp, cond, wind):
    """Assembles metrics into a clean, human-readable terminal dashboard."""
    if temp is None or cond is None or wind is None:
        return "Error parsing weather dashboard data."

    title = f" Weather Report: {loc.title()} "
    border = "=" * len(title)

    return (
        f"\n{border}\n"
        f"{title}\n"
        f"{border}\n"
        f"• Temperature:  {temp}°C\n"
        f"• Condition:    {cond}\n"
        f"• Wind Speed:   {wind} km/h\n"
        f"{border}\n"
    )


if __name__ == "__main__":
    main()
