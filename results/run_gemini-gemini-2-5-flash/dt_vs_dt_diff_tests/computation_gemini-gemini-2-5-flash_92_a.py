
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_mlk_day(year: int) -> date:
    # Step 1: Create a date object for January 1st of the given year.
    jan_1_date = date(year, 1, 1)
    
    # Step 2: Determine the day of the week for January 1st.
    # Monday is 0, Sunday is 6. We are looking for the 0 (Monday).
    jan_1_weekday = jan_1_date.weekday()
    
    # Step 3: Calculate how many days to add to jan_1_date to get the first Monday.
    # If jan_1_weekday is 0 (Monday), days_to_add will be 0.
    # If jan_1_weekday is 1 (Tuesday), days_to_add will be 6.
    # (0 - 1 + 7) % 7 = 6
    # If jan_1_weekday is 6 (Sunday), days_to_add will be 1.
    # (0 - 6 + 7) % 7 = 1
    days_to_add_for_first_monday = (0 - jan_1_weekday + 7) % 7
    
    # Step 4: Calculate the date of the first Monday in January.
    first_monday = jan_1_date + timedelta(days=days_to_add_for_first_monday)
    
    # Step 5: Martin Luther King Jr. Day is the third Monday of January.
    # This is exactly two weeks (14 days) after the first Monday.
    mlk_day = first_monday + timedelta(weeks=2)
    
    # Step 6: Return the date of MLK Day.
    return mlk_day

# Entry point: find_mlk_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_92_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_mlk_day(year):
    result = find_mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
