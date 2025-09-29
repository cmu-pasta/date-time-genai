
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def presidents_day(year: int) -> date:
    # Step 1: Start from February 1st of the given year
    feb_first = date(year, 2, 1)
    
    # Step 2: Determine the weekday of February 1st (Monday=0, Sunday=6)
    wd = feb_first.weekday()
    
    # Step 3: Compute days to the first Monday in February
    days_to_first_monday = (0 - wd) % 7
    
    # Step 4: Get the first Monday of February
    first_monday = feb_first + timedelta(days=days_to_first_monday)
    
    # Step 5: Add 14 days to get the third Monday (Presidents' Day)
    third_monday = first_monday + timedelta(days=14)
    
    # Step 6: Return the computed date
    return third_monday

# Entry point: presidents_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_86_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_presidents_day(year):
    result = presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
