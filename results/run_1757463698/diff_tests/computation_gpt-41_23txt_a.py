
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def round_up_to_next_quarter_hour(dt: datetime) -> datetime:
    # Step 1: Check if the datetime is already on a quarter hour (and exactly at 0 seconds/microseconds)
    if (dt.minute % 15 == 0) and dt.second == 0 and dt.microsecond == 0:
        return dt.replace(second=0, microsecond=0)
    
    # Step 2: Calculate minutes to add to get to next quarter (ceiling division)
    minutes_past = dt.minute % 15
    minutes_to_add = 15 - minutes_past if minutes_past != 0 else 0
    
    # If it's 14:59 (1 minute to 15:00), we want to add (15 - 14) = 1 min, for example.
    # But if second/microsecond are not 0, always round up even if at a quarter.
    # Therefore, we round up if not already on a quarter hour.
    # If not at 0s/0μs, need to add 1 to minutes_to_add if minutes_to_add == 0
    if minutes_to_add == 0 or dt.second != 0 or dt.microsecond != 0:
        minutes_to_add = (15 - minutes_past) if minutes_past != 0 else 15

    # Step 3: Set seconds and microsecond to zero and add the minutes_to_add
    dt_rounded = dt.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
    return dt_rounded

# Entry point: round_up_to_next_quarter_hour(dt: datetime) -> datetime

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_23txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_round_up_to_next_quarter_hour(dt):
    result = round_up_to_next_quarter_hour(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
