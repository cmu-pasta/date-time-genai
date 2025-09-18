
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
import math
def calculate_sidereal_time(dt: datetime, longitude: float) -> float:
    # Step 1: Calculate Julian Day Number
    # Julian Day formula: JD = 367*Y - 7*(Y + (M+9)/12)/4 + 275*M/9 + D + 1721013.5 + UT/24
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    
    # Convert time to decimal hours (UT)
    ut = hour + minute/60.0 + second/3600.0
    
    # Julian Day calculation
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5 + ut/24.0
    
    # Step 2: Calculate Greenwich Mean Sidereal Time (GMST)
    # Calculate days since J2000.0
    t = (jd - 2451545.0) / 36525.0
    
    # GMST at 0h UT in hours
    gmst0 = 6.697374558 + 0.06570982441908 * (jd - 2451545.0) + 0.000026 * t * t
    
    # Add the time of day contribution
    gmst = gmst0 + 1.00273790935 * ut
    
    # Step 3: Normalize to 0-24 hours
    gmst = gmst % 24.0
    if gmst < 0:
        gmst += 24.0
    
    # Step 4: Convert to Local Sidereal Time using longitude
    # Longitude in hours (divide degrees by 15)
    longitude_hours = longitude / 15.0
    lst = gmst + longitude_hours
    
    # Step 5: Normalize LST to 0-24 hours
    lst = lst % 24.0
    if lst < 0:
        lst += 24.0
    
    return lst

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_93txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_dt(result, dt, longitude)
    log_file.write(formatted_result + "\n")
