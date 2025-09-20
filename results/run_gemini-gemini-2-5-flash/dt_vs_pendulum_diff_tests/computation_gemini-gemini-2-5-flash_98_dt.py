
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_indigenous_peoples_day(year: int) -> date:
    # Step 1: Get the first day of October for the given year
    october_first = date(year, 10, 1)

    # Step 2: Calculate the number of days to add to reach the first Monday
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    # We want to find the first Monday (weekday 0)
    # The formula (target_weekday - current_weekday + 7) % 7 gives the days to add
    days_until_first_monday = (0 - october_first.weekday() + 7) % 7

    # Step 3: Find the date of the first Monday in October
    first_monday_of_october = october_first + timedelta(days=days_until_first_monday)

    # Step 4: Find the date of the second Monday in October by adding 7 days
    indigenous_peoples_day = first_monday_of_october + timedelta(days=7)

    # Step 5: Return the result as a date object
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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_98_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
