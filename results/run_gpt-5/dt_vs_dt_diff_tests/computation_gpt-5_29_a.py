
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def thanksgiving_date(year: int) -> date:
    # Step 1: Start from November 1st of the given year
    nov_first = date(year, 11, 1)
    
    # Step 2: Compute offset to the first Thursday (Thursday is weekday 3)
    weekday_nov_first = nov_first.weekday()  # Monday=0, Sunday=6
    days_to_first_thursday = (3 - weekday_nov_first) % 7
    first_thursday = nov_first + timedelta(days=days_to_first_thursday)
    
    # Step 3: The fourth Thursday is three weeks after the first Thursday
    fourth_thursday = first_thursday + timedelta(days=21)
    
    # Step 4: Return the date of Thanksgiving
    return fourth_thursday

# Entry point: thanksgiving_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_29_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_thanksgiving_date(year):
    result = thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
