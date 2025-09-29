
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def labor_day_date(year: int) -> date:
    # Step 1: Start from September 1st of the given year
    sept_first = date(year, 9, 1)
    # Step 2: Determine how many days to add to reach the first Monday
    # Python's weekday(): Monday=0 ... Sunday=6
    days_to_add = (0 - sept_first.weekday()) % 7
    # Step 3: Compute and return the Labor Day date
    return sept_first + timedelta(days=days_to_add)

# Entry point: labor_day_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_68txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_labor_day_date(year):
    result = labor_day_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
