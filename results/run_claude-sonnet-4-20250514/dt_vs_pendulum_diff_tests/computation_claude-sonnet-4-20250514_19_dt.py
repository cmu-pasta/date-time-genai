
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_season(dt: datetime) -> str:
    # Extract month and day from the datetime object
    month = dt.month
    day = dt.day
    
    # Define season boundaries (using approximate dates)
    # Spring: March 20 - June 20
    # Summer: June 21 - September 21  
    # Autumn: September 22 - December 20
    # Winter: December 21 - March 19
    
    if (month == 3 and day >= 20) or (month in [4, 5]) or (month == 6 and day <= 20):
        return "spring"
    elif (month == 6 and day >= 21) or (month in [7, 8]) or (month == 9 and day <= 21):
        return "summer"
    elif (month == 9 and day >= 22) or (month in [10, 11]) or (month == 12 and day <= 20):
        return "autumn"
    else:  # Winter
        return "winter"

# Entry point: determine_season(dt: datetime) -> str

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_19_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_season(dt):
    result = determine_season(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
