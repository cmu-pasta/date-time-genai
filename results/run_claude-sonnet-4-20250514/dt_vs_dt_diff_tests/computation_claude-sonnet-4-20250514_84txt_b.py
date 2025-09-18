
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, time
import math
def calculate_sunset_time(target_date: date, latitude: float, longitude: float) -> time:
    # Step 1: Calculate day of year
    day_of_year = target_date.timetuple().tm_yday
    
    # Step 2: Calculate solar declination angle (simplified formula)
    solar_declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    
    # Step 3: Convert latitude to radians
    lat_rad = math.radians(latitude)
    decl_rad = math.radians(solar_declination)
    
    # Step 4: Calculate hour angle for sunset
    # Using the formula: cos(hour_angle) = -tan(latitude) * tan(declination)
    try:
        cos_hour_angle = -math.tan(lat_rad) * math.tan(decl_rad)
        
        # Check for polar day/night conditions
        if cos_hour_angle > 1:
            # Polar night - sun doesn't rise
            return time(0, 0, 0)
        elif cos_hour_angle < -1:
            # Polar day - sun doesn't set
            return time(23, 59, 59)
        
        hour_angle = math.degrees(math.acos(cos_hour_angle))
    except:
        # Handle edge cases
        return time(18, 0, 0)  # Default sunset time
    
    # Step 5: Calculate sunset time in hours from solar noon
    sunset_hour_offset = hour_angle / 15.0  # Convert degrees to hours
    
    # Step 6: Calculate solar noon time accounting for longitude
    solar_noon = 12.0 - (longitude / 15.0)  # Longitude correction
    
    # Step 7: Calculate actual sunset time
    sunset_decimal_hour = solar_noon + sunset_hour_offset
    
    # Step 8: Handle day overflow/underflow
    if sunset_decimal_hour >= 24:
        sunset_decimal_hour -= 24
    elif sunset_decimal_hour < 0:
        sunset_decimal_hour += 24
    
    # Step 9: Convert to hours, minutes, seconds
    hours = int(sunset_decimal_hour)
    minutes = int((sunset_decimal_hour - hours) * 60)
    seconds = int(((sunset_decimal_hour - hours) * 60 - minutes) * 60)
    
    # Step 10: Return as time object
    return time(hours, minutes, seconds)

# Entry point: calculate_sunset_time(target_date: date, latitude: float, longitude: float) -> time

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_84txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_sunset_time(target_date, latitude, longitude):
    result = calculate_sunset_time(target_date, latitude, longitude)
    formatted_result = format_value_dt(result, target_date, latitude, longitude)
    log_file.write(formatted_result + "\n")
