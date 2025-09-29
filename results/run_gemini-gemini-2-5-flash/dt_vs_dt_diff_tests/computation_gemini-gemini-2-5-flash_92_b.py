
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_mlk_day(year: int) -> datetime:
    # Step 1: Get the date of January 1st for the given year
    jan_1st = datetime(year, 1, 1)

    # Step 2: Determine the weekday of January 1st
    # Monday is 0, Tuesday is 1, ..., Sunday is 6
    jan_1st_weekday = jan_1st.weekday()

    # Step 3: Calculate the number of days to add to jan_1st to get to the first Monday
    # If jan_1st is Monday (0), add 0 days.
    # If jan_1st is Tuesday (1), add 6 days (0 - 1 + 7 = 6).
    # If jan_1st is Sunday (6), add 1 day (0 - 6 + 7 = 1).
    days_to_first_monday = (0 - jan_1st_weekday + 7) % 7
    
    # Step 4: Calculate the date of the first Monday in January
    first_monday_jan = jan_1st + timedelta(days=days_to_first_monday)

    # Step 5: Calculate the date of the third Monday in January (add two weeks)
    mlk_day = first_monday_jan + timedelta(weeks=2)

    # Step 6: Return the resulting datetime object
    return mlk_day

# Entry point: find_mlk_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_92_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_mlk_day(year):
    result = find_mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
