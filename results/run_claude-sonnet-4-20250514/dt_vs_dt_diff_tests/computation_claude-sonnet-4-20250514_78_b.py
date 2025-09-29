
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def calculate_sunrise_time(date: datetime, latitude: float, longitude: float) -> datetime:
    # Step 1: Extract day of year
    day_of_year = date.timetuple().tm_yday
    
    # Step 2: Calculate solar declination (simplified formula)
    # Solar declination = 23.45 * sin(360 * (284 + day_of_year) / 365)
    declination_angle = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    
    # Step 3: Convert latitude to radians
    lat_radians = math.radians(latitude)
    decl_radians = math.radians(declination_angle)
    
    # Step 4: Calculate hour angle for sunrise
    # cos(hour_angle) = -tan(latitude) * tan(declination)
    cos_hour_angle = -math.tan(lat_radians) * math.tan(decl_radians)
    
    # Check if sun rises (polar day/night conditions)
    if cos_hour_angle > 1:
        cos_hour_angle = 1  # No sunrise (polar night)
    elif cos_hour_angle < -1:
        cos_hour_angle = -1  # Midnight sun (polar day)
    
    # Hour angle in radians
    hour_angle = math.acos(cos_hour_angle)
    
    # Step 5: Convert hour angle to hours
    sunrise_hour = 12 - (hour_angle * 180 / math.pi) / 15
    
    # Step 6: Adjust for longitude (4 minutes per degree)
    longitude_correction = longitude / 15
    local_sunrise_hour = sunrise_hour - longitude_correction
    
    # Step 7: Convert to datetime
    hours = int(local_sunrise_hour)
    minutes = int((local_sunrise_hour - hours) * 60)
    seconds = int(((local_sunrise_hour - hours) * 60 - minutes) * 60)
    
    # Create sunrise datetime
    sunrise_time = datetime(date.year, date.month, date.day, hours, minutes, seconds)
    
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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_78_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_sunrise_time(date, latitude, longitude):
    result = calculate_sunrise_time(date, latitude, longitude)
    formatted_result = format_value_dt(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
