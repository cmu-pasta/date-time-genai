
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def calculate_solar_noon(date: datetime, longitude: float, latitude: float) -> datetime:
    # Step 1: Calculate day of year
    day_of_year = date.timetuple().tm_yday
    
    # Step 2: Calculate equation of time approximation (in minutes)
    # Simplified formula based on day of year
    B = 2 * math.pi * (day_of_year - 81) / 365
    equation_of_time = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    # Step 3: Calculate longitude correction (4 minutes per degree)
    # Assuming standard time zone meridian (approximate)
    time_zone_meridian = round(longitude / 15) * 15  # Nearest 15-degree meridian
    longitude_correction = (time_zone_meridian - longitude) * 4  # 4 minutes per degree
    
    # Step 4: Calculate solar noon adjustment in minutes
    total_adjustment_minutes = longitude_correction + equation_of_time
    
    # Step 5: Start with 12:00 PM (noon) and apply adjustments
    solar_noon = datetime.combine(date.date(), datetime.min.time().replace(hour=12))
    solar_noon += timedelta(minutes=total_adjustment_minutes)
    
    return solar_noon

# Entry point: calculate_solar_noon(date: datetime, longitude: float, latitude: float) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_60txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon(date, longitude, latitude):
    result = calculate_solar_noon(date, longitude, latitude)
    formatted_result = format_value_dt(result, date, longitude, latitude)
    log_file.write(formatted_result + "\n")
