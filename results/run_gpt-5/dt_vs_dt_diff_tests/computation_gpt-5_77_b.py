
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_columbus_day(year: int) -> date:
    # Step 1: Start from October 1st of the given year
    oct_first = date(year, 10, 1)
    # Step 2: Get the weekday of October 1st (Monday=0, Sunday=6)
    weekday_oct_first = oct_first.weekday()
    # Step 3: Compute days to the first Monday in October
    days_to_first_monday = (0 - weekday_oct_first) % 7
    first_monday = oct_first + timedelta(days=days_to_first_monday)
    # Step 4: Second Monday is 7 days after the first Monday
    second_monday = first_monday + timedelta(days=7)
    # Step 5: Return the date of Columbus Day
    return second_monday

# Entry point: find_columbus_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_77_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_columbus_day(year):
    result = find_columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
