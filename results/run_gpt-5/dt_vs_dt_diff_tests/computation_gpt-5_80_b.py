
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    # Step 1: Compute the first day of the next month
    if month == 12:
        first_next_month = date(year + 1, 1, 1)
    else:
        first_next_month = date(year, month + 1, 1)
    
    # Step 2: Determine the last day of the given month
    last_day_of_month = first_next_month - timedelta(days=1)
    
    # Step 3: Calculate the offset to reach the target weekday (Monday=0 ... Sunday=6)
    offset = (last_day_of_month.weekday() - weekday) % 7
    
    # Step 4: Compute and return the last occurrence of the specified weekday
    return last_day_of_month - timedelta(days=offset)

# Entry point: last_weekday_of_month(year: int, month: int, weekday: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_80_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_last_weekday_of_month(year, month, weekday):
    result = last_weekday_of_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
