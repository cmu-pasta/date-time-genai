
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_sundays_in_february(year: int) -> int:
    # Step 1: Determine the first day of February and the first day of March for the given year
    feb_first = date(year, 2, 1)
    mar_first = date(year, 3, 1)
    
    # Step 2: Calculate the number of days in February
    days_in_february = (mar_first - feb_first).days
    
    # Step 3: Count Sundays (weekday() == 6 corresponds to Sunday)
    sundays = 0
    one_day = timedelta(days=1)
    current_day = feb_first
    for _ in range(days_in_february):
        if current_day.weekday() == 6:
            sundays += 1
        current_day += one_day
    
    # Step 4: Return the count of Sundays in February
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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_49_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
