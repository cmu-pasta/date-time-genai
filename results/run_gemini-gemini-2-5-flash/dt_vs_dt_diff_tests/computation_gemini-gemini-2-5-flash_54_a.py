
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_percentage_of_year_passed(input_date: date) -> float:
    # Step 1: Get the first day of the year for the input date's year
    first_day_of_year = date(input_date.year, 1, 1)

    # Step 2: Calculate the day number of the input date
    # The difference in days gives elapsed days, add 1 for the current day number.
    day_of_year = (input_date - first_day_of_year).days + 1

    # Step 3: Calculate the total number of days in the year
    # Get January 1st of the next year
    first_day_of_next_year = date(input_date.year + 1, 1, 1)
    # The difference between Jan 1st of next year and Jan 1st of current year
    # gives the total number of days in the current year.
    total_days_in_year = (first_day_of_next_year - first_day_of_year).days

    # Step 4: Calculate the percentage
    percentage_passed = (day_of_year / total_days_in_year) * 100

    # Step 5: Return the result as a float
    return percentage_passed

# Entry point: calculate_percentage_of_year_passed(input_date: date) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_54_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_percentage_of_year_passed(input_date):
    result = calculate_percentage_of_year_passed(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")
