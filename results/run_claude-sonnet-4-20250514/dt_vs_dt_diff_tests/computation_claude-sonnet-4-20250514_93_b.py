
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_sidereal_time(dt: datetime, longitude: float) -> datetime:
    # Step 1: Calculate Julian Date
    # Julian Date for January 1, 2000, 12:00 UT is 2451545.0
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    delta = dt - j2000
    julian_date = 2451545.0 + delta.total_seconds() / 86400.0
    
    # Step 2: Calculate days since J2000.0
    days_since_j2000 = julian_date - 2451545.0
    
    # Step 3: Calculate Greenwich Mean Sidereal Time (GMST) in hours
    # Formula: GMST = 18.697374558 + 24.06570982441908 * D
    gmst_hours = 18.697374558 + 24.06570982441908 * days_since_j2000
    
    # Step 4: Normalize GMST to 24-hour format
    gmst_hours = gmst_hours % 24.0
    
    # Step 5: Calculate Local Sidereal Time
    # LST = GMST + (longitude in degrees / 15)
    lst_hours = gmst_hours + (longitude / 15.0)
    lst_hours = lst_hours % 24.0
    
    # Step 6: Convert to datetime object (using base date for time representation)
    base_date = datetime(dt.year, dt.month, dt.day)
    hours = int(lst_hours)
    minutes = int((lst_hours - hours) * 60)
    seconds = int(((lst_hours - hours) * 60 - minutes) * 60)
    
    sidereal_datetime = base_date + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    return sidereal_datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_93_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_dt(result, dt, longitude)
    log_file.write(formatted_result + "\n")
