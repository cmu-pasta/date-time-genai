
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time
import math
def calculate_solar_noon(target_date: date, latitude: float, longitude: float) -> time:
    # Step 1: Calculate day of year
    day_of_year = target_date.timetuple().tm_yday
    
    # Step 2: Calculate the equation of time (in minutes)
    # This accounts for Earth's elliptical orbit and axial tilt
    n = day_of_year - 1
    L = (280.460 + 0.9856474 * n) % 360
    g = math.radians((357.528 + 0.9856003 * n) % 360)
    lambda_sun = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
    
    # Calculate equation of time in minutes
    alpha = math.atan2(math.tan(lambda_sun), math.cos(math.radians(23.439)))
    E = 4 * (L - math.degrees(alpha))
    E = E % 360
    if E > 180:
        E -= 360
    
    # Step 3: Calculate longitude correction (4 minutes per degree)
    longitude_correction = longitude * 4  # minutes
    
    # Step 4: Calculate solar noon time
    # Start with 12:00 (720 minutes from midnight)
    solar_noon_minutes = 720 - longitude_correction - E
    
    # Step 5: Convert to hours and minutes, handling overflow/underflow
    solar_noon_minutes = solar_noon_minutes % 1440  # 24 hours * 60 minutes
    
    hours = int(solar_noon_minutes // 60)
    minutes = int(solar_noon_minutes % 60)
    seconds = int((solar_noon_minutes % 1) * 60)
    
    # Step 6: Return as time object
    return time(hours, minutes, seconds)

# Entry point: calculate_solar_noon(target_date: date, latitude: float, longitude: float) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_60txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon(target_date, latitude, longitude):
    result = calculate_solar_noon(target_date, latitude, longitude)
    formatted_result = format_value_dt(result, target_date, latitude, longitude)
    log_file.write(formatted_result + "\n")
