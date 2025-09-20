
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_thanksgiving_date(year: int) -> date:
    # Step 1: Get the date for November 1st of the given year
    nov_1st = date(year, 11, 1)
    
    # Step 2: Determine the weekday of November 1st (Monday=0, Sunday=6)
    # We are looking for Thursday, which is weekday 3.
    nov_1st_weekday = nov_1st.weekday()
    
    # Step 3: Calculate how many days to add to nov_1st to get to the first Thursday
    # (3 - nov_1st_weekday) calculates the difference.
    # Adding 7 and then modulo 7 handles cases where nov_1st_weekday is already past Thursday
    # For example, if nov_1st is Friday (4), (3-4) = -1. (-1 + 7) % 7 = 6 days to add.
    # If nov_1st is Thursday (3), (3-3) = 0. (0 + 7) % 7 = 0 days to add.
    days_to_first_thursday = (3 - nov_1st_weekday + 7) % 7
    
    # Step 4: Find the date of the first Thursday in November
    first_thursday = nov_1st + timedelta(days=days_to_first_thursday)
    
    # Step 5: Thanksgiving is the fourth Thursday.
    # To get from the first Thursday to the fourth, we add 3 full weeks (3 * 7 days).
    thanksgiving_date = first_thursday + timedelta(days=21)
    
    # Step 6: Return the calculated date
    return thanksgiving_date

# Entry point: find_thanksgiving_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_29_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
