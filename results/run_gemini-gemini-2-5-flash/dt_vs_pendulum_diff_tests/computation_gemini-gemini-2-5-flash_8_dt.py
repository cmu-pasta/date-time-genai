
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_day_of_month(dt: datetime) -> datetime:
    # Step 1: Get the first day of the month after the input date's month.
    # We set the day to 1 to get the start of the current month.
    # Then we add 32 days to guarantee we land in the *next* month.
    # Finally, we set the day to 1 again to get the *first* day of that next month.
    first_day_of_next_month = (dt.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    # Step 2: Subtract one day from the first day of the next month
    # This gives us the last day of the original month.
    last_day = first_day_of_next_month - timedelta(days=1)
    
    # Step 3: Return the result
    return last_day

# Entry point: find_last_day_of_month(dt: datetime) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_8_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_day_of_month(dt):
    result = find_last_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
