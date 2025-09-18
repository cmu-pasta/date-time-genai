
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def calculate_sunset_time(date: datetime, latitude: float, longitude: float) -> datetime:
    # Convert date to day of year
    day_of_year = date.timetuple().tm_yday
    
    # Solar calculations
    # Solar declination angle (in radians)
    P = math.asin(0.39795 * math.cos(0.0172 * (day_of_year - 173)))
    
    # Equation of time (in minutes)
    B = 2 * math.pi * (day_of_year - 81) / 365
    E = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    # Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Calculate hour angle for sunset
    cos_hour_angle = -math.tan(lat_rad) * math.tan(P)
    
    # Check if sun sets (polar day/night conditions)
    if cos_hour_angle < -1:
        cos_hour_angle = -1  # Sun doesn't set (midnight sun)
    elif cos_hour_angle > 1:
        cos_hour_angle = 1   # Sun doesn't rise (polar night)
    
    hour_angle = math.degrees(math.acos(cos_hour_angle))
    
    # Calculate sunset time in minutes from solar noon
    sunset_minutes = 720 + 4 * (longitude + hour_angle) + E
    
    # Convert to hours and minutes
    sunset_hours = int(sunset_minutes // 60)
    sunset_mins = int(sunset_minutes % 60)
    
    # Create sunset datetime
    sunset_time = datetime(date.year, date.month, date.day, sunset_hours % 24, sunset_mins)
    
    # Handle day rollover
    if sunset_hours >= 24:
        sunset_time += timedelta(days=1)
    
    return sunset_time

# Entry point: calculate_sunset_time(date: datetime, latitude: float, longitude: float) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_84txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_sunset_time(date, latitude, longitude):
    result = calculate_sunset_time(date, latitude, longitude)
    formatted_result = format_value_dt(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
