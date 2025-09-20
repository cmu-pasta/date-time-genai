
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_sundays_in_february(year: int) -> int:
    # Step 1: Create the start date for February
    feb_start = date(year, 2, 1)
    
    # Step 2: Create the start date for March to determine February length
    mar_start = date(year, 3, 1)
    
    # Step 3: Compute the number of days in February
    feb_days = (mar_start - feb_start).days
    
    # Step 4: Count Sundays in February
    sundays = 0
    for i in range(feb_days):
        current_day = feb_start + timedelta(days=i)
        if current_day.weekday() == 6:  # Monday=0 ... Sunday=6
            sundays += 1
    
    # Step 5: Return the count as an integer
    return sundays

# Entry point: count_sundays_in_february(year: int) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_49_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
