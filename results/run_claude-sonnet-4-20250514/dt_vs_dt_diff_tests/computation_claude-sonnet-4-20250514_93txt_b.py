
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
import math
def calculate_sidereal_time(dt: datetime, longitude: float) -> float:
    # Step 1: Convert to UTC if not already
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)
    
    # Step 2: Calculate Julian Day Number
    # Formula for Julian Day calculation
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second + dt_utc.microsecond / 1000000.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    jd += (hour + minute / 60.0 + second / 3600.0) / 24.0
    
    # Step 3: Calculate number of centuries since J2000.0
    t = (jd - 2451545.0) / 36525.0
    
    # Step 4: Calculate Greenwich Mean Sidereal Time in degrees
    # Formula: GMST = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933 * T^2 - T^3 / 38710000
    gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000.0
    
    # Step 5: Normalize to 0-360 degrees
    gmst_deg = gmst_deg % 360.0
    
    # Step 6: Convert to Local Sidereal Time by adding longitude
    lst_deg = gmst_deg + longitude
    lst_deg = lst_deg % 360.0
    
    # Step 7: Convert to hours (divide by 15 since 360 degrees = 24 hours)
    sidereal_time_hours = lst_deg / 15.0
    
    return sidereal_time_hours

# Entry point: calculate_sidereal_time(dt: datetime, longitude: float) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_93txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_dt(result, dt, longitude)
    log_file.write(formatted_result + "\n")
