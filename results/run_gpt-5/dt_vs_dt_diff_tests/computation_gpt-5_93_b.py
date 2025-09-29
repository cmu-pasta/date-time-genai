
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
def calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> time:
    # Step 1: Normalize datetime to UTC (assume naive datetimes are UTC)
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=ZoneInfo("UTC"))
    else:
        dt_utc = dt.astimezone(ZoneInfo("UTC"))

    # Step 2: Convert to Julian Date via Unix epoch
    epoch = datetime(1970, 1, 1, tzinfo=ZoneInfo("UTC"))
    seconds_since_epoch = (dt_utc - epoch).total_seconds()
    jd = seconds_since_epoch / 86400.0 + 2440587.5

    # Step 3: Compute GMST in degrees
    # Formula: GMST = 280.46061837 + 360.98564736629*(JD - 2451545.0)
    #                   + 0.000387933*T^2 - (T^3)/38710000
    # where T = (JD - 2451545.0)/36525
    t = (jd - 2451545.0) / 36525.0
    gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * (t * t) - (t * t * t) / 38710000.0

    # Normalize GMST to [0, 360)
    gmst_deg = gmst_deg % 360.0
    if gmst_deg < 0.0:
        gmst_deg += 360.0

    # Step 4: Local Sidereal Time (LST) in degrees, wrap to [0, 360)
    lst_deg = (gmst_deg + longitude_degrees) % 360.0
    if lst_deg < 0.0:
        lst_deg += 360.0

    # Step 5: Convert degrees to time-of-day
    # 360 degrees = 24 hours => 15 degrees = 1 hour
    lst_hours = lst_deg / 15.0

    # Extract hours, minutes, seconds, microseconds
    hour = int(lst_hours)
    rem_hours = lst_hours - hour
    minutes_total = rem_hours * 60.0
    minute = int(minutes_total)
    rem_minutes = minutes_total - minute
    seconds_total = rem_minutes * 60.0

    second = int(seconds_total)
    rem_seconds = seconds_total - second
    microsecond = int(round(rem_seconds * 1_000_000))

    # Handle rounding overflow (e.g., 59.9999999 -> 60 seconds)
    if microsecond >= 1_000_000:
        microsecond -= 1_000_000
        second += 1
    if second >= 60:
        second -= 60
        minute += 1
    if minute >= 60:
        minute -= 60
        hour += 1
    hour = hour % 24

    return time(hour=hour, minute=minute, second=second, microsecond=microsecond)

# Entry point: calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> time

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_93_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude_degrees):
    result = calculate_sidereal_time(dt, longitude_degrees)
    formatted_result = format_value_dt(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
