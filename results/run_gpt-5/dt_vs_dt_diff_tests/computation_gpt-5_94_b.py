
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def datetime_to_mjd(dt: datetime) -> float:
    # Step 1: Work in UTC (assume naive datetimes are UTC)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    
    # Step 2: Extract components and compute fractional day
    y = dt.year
    m = dt.month
    # Fractional part of the day
    frac_day = (dt.hour + (dt.minute + (dt.second + dt.microsecond / 1_000_000.0) / 60.0) / 60.0) / 24.0
    d = dt.day + frac_day

    # Step 3: Algorithm adjustment for months Jan/Feb
    if m <= 2:
        y -= 1
        m += 12

    # Step 4: Gregorian calendar correction
    A = y // 100
    B = 2 - A + (A // 4)

    # Step 5: Compute Julian Date (JD)
    # Using int() as floor because all terms are positive here
    JD = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5

    # Step 6: Convert to Modified Julian Date (MJD)
    MJD = JD - 2400000.5

    return float(MJD)

# Entry point: datetime_to_mjd(dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_94_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
