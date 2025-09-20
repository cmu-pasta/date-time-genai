
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def calculate_sunset_time(date: datetime, latitude: float, longitude: float) -> datetime:
    # Step 1: Get day of year
    day_of_year = date.timetuple().tm_yday
    
    # Step 2: Calculate solar declination
    P = math.asin(0.39795 * math.cos(0.98563 * (day_of_year - 173) * math.pi / 180))
    
    # Step 3: Calculate equation of time (in minutes)
    B = 2 * math.pi * (day_of_year - 81) / 365
    E = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    # Step 4: Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Step 5: Calculate hour angle for sunset
    argument = -math.tan(lat_rad) * math.tan(P)
    
    # Check if sun sets (polar regions may not have sunset on certain days)
    if argument < -1:
        argument = -1
    elif argument > 1:
        argument = 1
    
    hour_angle = math.acos(argument)
    
    # Step 6: Calculate sunset time in hours from solar noon
    sunset_hour = 12 + (hour_angle * 180 / math.pi) / 15
    
    # Step 7: Apply equation of time correction
    sunset_hour = sunset_hour + E / 60
    
    # Step 8: Apply longitude correction (4 minutes per degree)
    sunset_hour = sunset_hour - longitude / 15
    
    # Step 9: Convert to datetime
    hours = int(sunset_hour)
    minutes = int((sunset_hour - hours) * 60)
    seconds = int(((sunset_hour - hours) * 60 - minutes) * 60)
    
    sunset_time = datetime(date.year, date.month, date.day, hours, minutes, seconds)
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_84_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_sunset_time(date, latitude, longitude):
    result = calculate_sunset_time(date, latitude, longitude)
    formatted_result = format_value_dt(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
