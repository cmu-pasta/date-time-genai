
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def mlk_day(year: int) -> date:
    # Step 1: Start with January 1st of the given year
    jan_first = date(year, 1, 1)
    # Step 2: Compute days to the first Monday (Monday=0)
    days_to_first_monday = (0 - jan_first.weekday()) % 7
    first_monday = jan_first + timedelta(days=days_to_first_monday)
    # Step 3: The third Monday is two weeks after the first Monday
    third_monday = first_monday + timedelta(days=14)
    # Step 4: Return the date of MLK Day
    return third_monday

# Entry point: mlk_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_92_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_mlk_day(year):
    result = mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
