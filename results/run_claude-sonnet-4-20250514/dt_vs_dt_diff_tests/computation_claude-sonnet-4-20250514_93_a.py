
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def calculate_sidereal_time(dt: datetime, longitude: float) -> datetime:
    # Convert to UTC if timezone-aware, otherwise assume UTC
    if dt.tzinfo is not None:
        utc_dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        utc_dt = dt
    
    # Calculate Julian Day Number
    a = (14 - utc_dt.month) // 12
    y = utc_dt.year + 4800 - a
    m = utc_dt.month + 12 * a - 3
    
    jdn = utc_dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    # Add fractional day
    fractional_day = (utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0) / 24.0
    julian_day = jdn + fractional_day - 0.5
    
    # Calculate centuries since J2000.0
    t = (julian_day - 2451545.0) / 36525.0
    
    # Calculate Greenwich Mean Sidereal Time in degrees
    gmst_degrees = 280.46061837 + 360.98564736629 * (julian_day - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000.0
    
    # Normalize to 0-360 degrees
    gmst_degrees = gmst_degrees % 360.0
    
    # Convert to Local Sidereal Time by adding longitude
    lst_degrees = (gmst_degrees + longitude) % 360.0
    
    # Convert degrees to hours (360 degrees = 24 hours)
    lst_hours = lst_degrees / 15.0
    
    # Extract hours, minutes, and seconds
    hours = int(lst_hours)
    minutes = int((lst_hours - hours) * 60)
    seconds = int(((lst_hours - hours) * 60 - minutes) * 60)
    
    # Create a datetime object with the sidereal time
    # Use a reference date and only return the time portion
    base_date = datetime(2000, 1, 1)
    sidereal_time = base_date.replace(hour=hours % 24, minute=minutes % 60, second=seconds % 60)
    
    return sidereal_time

# Entry point: calculate_sidereal_time(dt: datetime, longitude: float) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_93_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_dt(result, dt, longitude)
    log_file.write(formatted_result + "\n")
