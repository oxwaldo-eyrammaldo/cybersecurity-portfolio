from project import extract_metrics, format_weather_display

def test_extract_metrics_valid():
    # Simulate a cropped version of the actual wttr.in JSON response structure
    mock_json = {
        "current_condition": [
            {
                "temp_C": "24",
                "weatherDesc": [{"value": "Partly cloudy"}],
                "windspeedKmph": "15"
            }
        ]
    }
    temp, cond, wind = extract_metrics(mock_json)
    assert temp == 24
    assert cond == "Partly cloudy"
    assert wind == 15

def test_extract_metrics_invalid():
    # Test how the function handles corrupted or missing keys gracefully
    bad_json = {"invalid_key": "bad_data"}
    temp, cond, wind = extract_metrics(bad_json)
    assert temp is None
    assert cond is None
    assert wind is None

def test_format_weather_display():
    output = format_weather_display("Accra", 28, "Sunny", 12)
    assert "Accra" in output
    assert "28°C" in output
    assert "Sunny" in output
    assert "12 km/h" in output

def test_format_weather_display_none():
    output = format_weather_display("Accra", None, "Sunny", 12)
    assert output == "Error parsing weather dashboard data."
