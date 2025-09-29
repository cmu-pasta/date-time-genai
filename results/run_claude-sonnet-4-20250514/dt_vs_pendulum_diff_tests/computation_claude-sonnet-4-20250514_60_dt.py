
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
import math
def calculate_solar_noon(target_date: date, latitude: float, longitude: float) -> datetime:
    # Step 1: Calculate day of year
    day_of_year = target_date.timetuple().tm_yday
    
    # Step 2: Calculate the equation of time (in minutes)
    # This accounts for Earth's orbital eccentricity and axial tilt
    B = 2 * math.pi * (day_of_year - 81) / 365
    equation_of_time = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    # Step 3: Calculate time correction for longitude (in minutes)
    # 15 degrees longitude = 1 hour time difference
    longitude_correction = 4 * longitude  # 4 minutes per degree
    
    # Step 4: Calculate solar noon time
    # Solar noon in UTC is 12:00 minus corrections
    solar_noon_minutes = 12 * 60 - equation_of_time - longitude_correction
    
    # Step 5: Convert to hours and minutes
    solar_noon_hours = int(solar_noon_minutes // 60)
    solar_noon_mins = int(solar_noon_minutes % 60)
    
    # Step 6: Create datetime object for solar noon
    solar_noon_time = datetime.combine(target_date, datetime.min.time().replace(
        hour=solar_noon_hours, 
        minute=solar_noon_mins
    ))
    
    return solar_noon_time

# Entry point: calculate_solar_noon(target_date: date, latitude: float, longitude: float) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_60_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon(target_date, latitude, longitude):
    result = calculate_solar_noon(target_date, latitude, longitude)
    formatted_result = format_value_dt(result, target_date, latitude, longitude)
    log_file.write(formatted_result + "\n")
