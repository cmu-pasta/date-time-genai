
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_season(dt: datetime) -> int:
    # Extract the month from the datetime object
    month = dt.month
    
    # Determine season based on meteorological seasons
    # 0 = Winter, 1 = Spring, 2 = Summer, 3 = Autumn
    if month in [12, 1, 2]:  # December, January, February
        return 0  # Winter
    elif month in [3, 4, 5]:  # March, April, May
        return 1  # Spring
    elif month in [6, 7, 8]:  # June, July, August
        return 2  # Summer
    else:  # September, October, November
        return 3  # Autumn

# Entry point: determine_season(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_19_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_season(dt):
    result = determine_season(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
