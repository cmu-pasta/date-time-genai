
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
import math
def calculate_sunrise_time(date: datetime, latitude: float, longitude: float) -> datetime:
    # Step 1: Extract day of year
    day_of_year = date.timetuple().tm_yday
    
    # Step 2: Calculate solar declination (in radians)
    # Approximate formula for solar declination
    declination = math.radians(23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365)))
    
    # Step 3: Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Step 4: Calculate hour angle for sunrise
    # cos(hour_angle) = -tan(latitude) * tan(declination)
    cos_hour_angle = -math.tan(lat_rad) * math.tan(declination)
    
    # Check if sun rises (polar regions might not have sunrise)
    if cos_hour_angle < -1 or cos_hour_angle > 1:
        # Handle polar day/night cases - return noon as approximation
        sunrise_hour = 12.0
    else:
        hour_angle = math.acos(cos_hour_angle)
        # Convert hour angle to hours (sunrise occurs when hour angle is negative)
        sunrise_hour = 12.0 - (hour_angle * 12.0 / math.pi)
    
    # Step 5: Apply longitude correction (4 minutes per degree)
    longitude_correction = longitude / 15.0  # 15 degrees = 1 hour
    local_sunrise_hour = sunrise_hour - longitude_correction
    
    # Step 6: Convert to hours and minutes
    hours = int(local_sunrise_hour)
    minutes = int((local_sunrise_hour - hours) * 60)
    
    # Step 7: Create and return datetime object
    sunrise_time = datetime(date.year, date.month, date.day, hours, minutes)
    
    return sunrise_time

# Entry point: calculate_sunrise_time(date: datetime, latitude: float, longitude: float) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_78txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_sunrise_time(date, latitude, longitude):
    result = calculate_sunrise_time(date, latitude, longitude)
    formatted_result = format_value_dt(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
