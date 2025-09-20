
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def columbus_day(year: int) -> date:
    # Step 1: Start from October 1st of the given year
    oct_first = date(year, 10, 1)
    
    # Step 2: Determine the weekday of October 1st (Monday=0, Sunday=6)
    w = oct_first.weekday()
    
    # Step 3: Calculate the day number of the first Monday in October
    # If Oct 1 is Monday (w=0), offset is 0 -> first Monday is the 1st
    first_monday_day = 1 + ((7 - w) % 7)
    
    # Step 4: The second Monday (Columbus Day) is 7 days after the first Monday
    second_monday_day = first_monday_day + 7
    
    # Step 5: Return the date of Columbus Day
    return date(year, 10, second_monday_day)

# Entry point: columbus_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_77_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_columbus_day(year):
    result = columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
