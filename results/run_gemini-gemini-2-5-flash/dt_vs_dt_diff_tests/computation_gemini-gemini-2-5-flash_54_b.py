
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_percentage_of_year_passed(date: datetime) -> float:
    # Step 3: Determine the start of the year for the given date
    start_of_year = datetime(date.year, 1, 1)

    # Step 4: Determine the start of the next year to find total days in current year
    start_of_next_year = datetime(date.year + 1, 1, 1)

    # Step 5: Calculate the total number of days in the current year
    total_days_in_year = (start_of_next_year - start_of_year).days

    # Step 6: Calculate the number of days that have passed up to and including the given date
    # (date - start_of_year).days gives the number of full days between them.
    # Adding 1 includes the current day in the count.
    days_passed_inclusive = (date - start_of_year).days + 1

    # Step 7: Calculate the percentage of the year that has passed
    percentage = (days_passed_inclusive / total_days_in_year) * 100

    # Step 8: Return the result as a float
    return percentage

# Entry point: calculate_percentage_of_year_passed(date: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_54_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_percentage_of_year_passed(date):
    result = calculate_percentage_of_year_passed(date)
    formatted_result = format_value_dt(result, date)
    log_file.write(formatted_result + "\n")
