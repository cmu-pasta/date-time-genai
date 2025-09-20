
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def hours_in_month(year: int, month: int) -> int:
    # Step 3: Start of the given month
    start_of_month = date(year, month, 1)
    
    # Step 4: Start of the next month (handle December)
    if month == 12:
        start_of_next_month = date(year + 1, 1, 1)
    else:
        start_of_next_month = date(year, month + 1, 1)
    
    # Step 5: Compute number of days in the month
    days_in_month = (start_of_next_month - start_of_month).days
    
    # Step 6: Convert days to hours
    return days_in_month * 24

# Entry point: hours_in_month(year: int, month: int) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_42_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_hours_in_month(year, month):
    result = hours_in_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")
