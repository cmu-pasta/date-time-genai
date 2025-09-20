
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_columbus_day(year: int) -> date:
    # Step 1: Get the date for October 1st of the given year.
    october_1st = date(year, 10, 1)
    
    # Step 2: Find the weekday of October 1st. Monday is 0, Sunday is 6.
    weekday_of_october_1st = october_1st.weekday()
    
    # Step 3: Calculate how many days to add to october_1st to get to the first Monday.
    # If october_1st is Monday (0), days_to_add = (0 - 0 + 7) % 7 = 0.
    # If october_1st is Tuesday (1), days_to_add = (0 - 1 + 7) % 7 = 6.
    # If october_1st is Sunday (6), days_to_add = (0 - 6 + 7) % 7 = 1.
    days_to_first_monday = (0 - weekday_of_october_1st + 7) % 7
    
    # Step 4: Calculate the date of the first Monday in October.
    first_monday = october_1st + timedelta(days=days_to_first_monday)
    
    # Step 5: Columbus Day is the second Monday of October. Add 7 days to the first Monday.
    columbus_day = first_monday + timedelta(days=7)
    
    # Step 6: Return the calculated date.
    return columbus_day

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_77_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_columbus_day(year):
    result = find_columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
