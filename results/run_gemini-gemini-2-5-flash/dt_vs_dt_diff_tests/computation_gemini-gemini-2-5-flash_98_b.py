
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_indigenous_peoples_day(year: int) -> date:
    # Step 1: Start with the first day of October for the given year.
    first_october = date(year, 10, 1)

    # Step 2: Determine the weekday of October 1st.
    # Monday is 0, Sunday is 6. We are looking for Monday (0).
    current_weekday = first_october.weekday()

    # Step 3: Calculate how many days to add to reach the first Monday.
    # If first_october is already a Monday (current_weekday == 0), days_to_add will be 0.
    # Otherwise, it will be the number of days until the next Monday.
    # For example, if current_weekday is Tuesday (1), (0 - 1 + 7) % 7 = 6, so add 6 days.
    # If current_weekday is Sunday (6), (0 - 6 + 7) % 7 = 1, so add 1 day.
    days_to_add_for_first_monday = (0 - current_weekday + 7) % 7

    # Step 4: Find the date of the first Monday of October.
    first_monday_of_october = first_october + timedelta(days=days_to_add_for_first_monday)

    # Step 5: Indigenous Peoples' Day is the second Monday of October.
    # Add 7 days (one week) to the first Monday to get the second Monday.
    indigenous_peoples_day = first_monday_of_october + timedelta(weeks=1)
    
    # Step 6: Return the calculated date.
    return indigenous_peoples_day

# Entry point: find_indigenous_peoples_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_98_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
