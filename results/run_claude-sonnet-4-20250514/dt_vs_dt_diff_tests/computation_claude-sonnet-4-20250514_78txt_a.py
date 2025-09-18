
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, time
import math
def calculate_sunrise_time(date_input: date, latitude: float, longitude: float) -> time:
    # Step 1: Calculate day of year
    day_of_year = date_input.timetuple().tm_yday
    
    # Step 2: Calculate solar declination angle in radians
    # Using simplified formula: declination = 23.45 * sin(360 * (284 + n) / 365)
    declination_degrees = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    declination_radians = math.radians(declination_degrees)
    
    # Step 3: Calculate latitude in radians
    latitude_radians = math.radians(latitude)
    
    # Step 4: Calculate hour angle for sunrise
    # cos(hour_angle) = -tan(latitude) * tan(declination)
    try:
        cos_hour_angle = -math.tan(latitude_radians) * math.tan(declination_radians)
        
        # Handle polar day/night cases
        if cos_hour_angle > 1:
            cos_hour_angle = 1  # Polar night - no sunrise
        elif cos_hour_angle < -1:
            cos_hour_angle = -1  # Polar day - midnight sun
            
        hour_angle_radians = math.acos(cos_hour_angle)
        hour_angle_degrees = math.degrees(hour_angle_radians)
        
    except:
        hour_angle_degrees = 90  # Default fallback
    
    # Step 5: Calculate sunrise time
    # Sunrise occurs when hour angle is negative (morning)
    sunrise_hour_utc = 12 - (hour_angle_degrees / 15)
    
    # Step 6: Adjust for longitude (4 minutes per degree)
    longitude_correction = longitude / 15  # Convert longitude to hours
    sunrise_hour_local = sunrise_hour_utc - longitude_correction
    
    # Step 7: Normalize to 24-hour format
    sunrise_hour_local = sunrise_hour_local % 24
    
    # Step 8: Convert to hours and minutes
    hours = int(sunrise_hour_local)
    minutes = int((sunrise_hour_local - hours) * 60)
    seconds = int(((sunrise_hour_local - hours) * 60 - minutes) * 60)
    
    # Step 9: Create and return time object
    return time(hours, minutes, seconds)

# Entry point: calculate_sunrise_time(date_input: date, latitude: float, longitude: float) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_78txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_sunrise_time(date_input, latitude, longitude):
    result = calculate_sunrise_time(date_input, latitude, longitude)
    formatted_result = format_value_dt(result, date_input, latitude, longitude)
    log_file.write(formatted_result + "\n")
