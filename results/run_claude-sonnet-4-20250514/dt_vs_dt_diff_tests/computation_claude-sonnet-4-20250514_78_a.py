
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def calculate_sunrise_time(date: datetime, latitude: float, longitude: float) -> datetime:
    # Step 1: Calculate day of year
    day_of_year = date.timetuple().tm_yday
    
    # Step 2: Calculate solar declination angle (in radians)
    solar_declination = math.radians(23.45) * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    
    # Step 3: Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Step 4: Calculate hour angle for sunrise
    # Using the sunrise equation: cos(hour_angle) = -tan(latitude) * tan(solar_declination)
    hour_angle_cos = -math.tan(lat_rad) * math.tan(solar_declination)
    
    # Step 5: Handle extreme cases (polar day/night)
    if hour_angle_cos > 1:
        # No sunrise (polar night)
        hour_angle = math.pi
    elif hour_angle_cos < -1:
        # Sun never sets (polar day)
        hour_angle = 0
    else:
        hour_angle = math.acos(hour_angle_cos)
    
    # Step 6: Calculate sunrise time in hours
    sunrise_hour = 12 - (math.degrees(hour_angle) / 15) - (longitude / 15)
    
    # Step 7: Convert to datetime
    hours = int(sunrise_hour)
    minutes = int((sunrise_hour - hours) * 60)
    seconds = int(((sunrise_hour - hours) * 60 - minutes) * 60)
    
    # Step 8: Create the sunrise datetime
    sunrise_time = date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    )
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_78_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_sunrise_time(date, latitude, longitude):
    result = calculate_sunrise_time(date, latitude, longitude)
    formatted_result = format_value_dt(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
