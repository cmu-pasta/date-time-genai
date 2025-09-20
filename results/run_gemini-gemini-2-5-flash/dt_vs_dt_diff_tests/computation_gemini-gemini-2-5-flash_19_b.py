
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_season(dt: datetime) -> int:
    """
    Determines the season (winter, spring, summer, autumn) for a given date
    based on meteorological definitions for the Northern Hemisphere.

    Args:
        dt (datetime): The date for which to determine the season.

    Returns:
        int: An integer representing the season:
             0 for Winter (Dec, Jan, Feb)
             1 for Spring (Mar, Apr, May)
             2 for Summer (Jun, Jul, Aug)
             3 for Autumn (Sep, Oct, Nov)
    """
    month = dt.month

    if 3 <= month <= 5:
        return 1  # Spring
    elif 6 <= month <= 8:
        return 2  # Summer
    elif 9 <= month <= 11:
        return 3  # Autumn
    else: # month 12, 1, 2
        return 0  # Winter

# Entry point: get_season(dt: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_19_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_season(dt):
    result = get_season(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
