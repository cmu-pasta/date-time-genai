
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_season(dt: datetime) -> int:
    # Extract month and day from the datetime
    month = dt.month
    day = dt.day
    
    # Determine season based on month and day
    # Spring: March 21 - June 20 (1)
    if (month == 3 and day >= 21) or (month == 4) or (month == 5) or (month == 6 and day <= 20):
        return 1
    
    # Summer: June 21 - September 22 (2)
    elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day <= 22):
        return 2
    
    # Autumn: September 23 - December 21 (3)
    elif (month == 9 and day >= 23) or (month == 10) or (month == 11) or (month == 12 and day <= 21):
        return 3
    
    # Winter: December 22 - March 20 (4)
    else:
        return 4

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_19txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_season(dt):
    result = determine_season(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
