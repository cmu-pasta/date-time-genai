
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_sidereal_time(dt: pendulum.DateTime, longitude: float) -> float:
    # Step 1: Convert datetime to UTC if not already
    dt_utc = dt.in_timezone('UTC')
    
    # Step 2: Calculate Julian Date
    # Julian Date calculation for the given datetime
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second
    
    # Convert time to decimal hours
    decimal_hours = hour + minute/60.0 + second/3600.0
    
    # Julian Date calculation
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    jd += decimal_hours / 24.0
    
    # Step 3: Calculate Greenwich Sidereal Time
    # Number of days since J2000.0
    t = (jd - 2451545.0) / 36525.0
    
    # Greenwich Mean Sidereal Time at 0h UT
    gmst_0h = 6.697374558 + 0.06570982441908 * (jd - 2451545.0) + 0.000026 * t * t
    
    # Add the contribution from the current time of day
    gmst = gmst_0h + 1.00273790935 * decimal_hours
    
    # Step 4: Calculate Local Sidereal Time
    # Convert longitude from degrees to hours (divide by 15)
    longitude_hours = longitude / 15.0
    
    # Local Sidereal Time = Greenwich Sidereal Time + longitude in hours
    lst = gmst + longitude_hours
    
    # Step 5: Normalize to 0-24 hours
    lst = lst % 24.0
    if lst < 0:
        lst += 24.0
    
    return lst

# Entry point: calculate_sidereal_time(dt: pendulum.DateTime, longitude: float) -> float

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_93_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_pd(result, dt, longitude)
    log_file.write(formatted_result + "\n")
