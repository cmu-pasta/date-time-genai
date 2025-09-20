
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_japanese_calendar_year(dt: datetime) -> int:
    # Define the start dates for each Japanese era
    reiwa_start = datetime(2019, 5, 1)
    heisei_start = datetime(1989, 1, 8)
    showa_start = datetime(1926, 12, 25)
    taisho_start = datetime(1912, 7, 30)
    meiji_start = datetime(1868, 1, 25)
    
    # Determine which era the date falls into and calculate the year
    if dt >= reiwa_start:
        # Reiwa era (2019-present)
        japanese_year = (dt.year - reiwa_start.year) + 1
        if dt.month < reiwa_start.month or (dt.month == reiwa_start.month and dt.day < reiwa_start.day):
            japanese_year -= 1
    elif dt >= heisei_start:
        # Heisei era (1989-2019)
        japanese_year = (dt.year - heisei_start.year) + 1
        if dt.month < heisei_start.month or (dt.month == heisei_start.month and dt.day < heisei_start.day):
            japanese_year -= 1
    elif dt >= showa_start:
        # Showa era (1926-1989)
        japanese_year = (dt.year - showa_start.year) + 1
        if dt.month < showa_start.month or (dt.month == showa_start.month and dt.day < showa_start.day):
            japanese_year -= 1
    elif dt >= taisho_start:
        # Taisho era (1912-1926)
        japanese_year = (dt.year - taisho_start.year) + 1
        if dt.month < taisho_start.month or (dt.month == taisho_start.month and dt.day < taisho_start.day):
            japanese_year -= 1
    elif dt >= meiji_start:
        # Meiji era (1868-1912)
        japanese_year = (dt.year - meiji_start.year) + 1
        if dt.month < meiji_start.month or (dt.month == meiji_start.month and dt.day < meiji_start.day):
            japanese_year -= 1
    else:
        # Pre-Meiji era - return 0 to indicate unsupported
        japanese_year = 0
    
    return japanese_year

# Entry point: get_japanese_calendar_year(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_85_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_japanese_calendar_year(dt):
    result = get_japanese_calendar_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
