
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
def calculate_days_until_next_birthday(birth_date: datetime) -> int:
    # Step 1: Get today's date as a date object for comparison
    today = date.today()

    # Step 2: Extract birth month and day from the input birth_date
    birth_month = birth_date.month
    birth_day = birth_date.day

    # Step 3: Determine the candidate next birthday for the current year
    # We must handle February 29th carefully.
    try:
        current_year_birthday = date(today.year, birth_month, birth_day)
    except ValueError:
        # This occurs if birth_day is 29 and today.year is not a leap year.
        # In this case, the birthday in the current year doesn't exist on Feb 29th,
        # so we must assume the next birthday will be in a future leap year.
        current_year_birthday = date(today.year, 3, 1) # Arbitrary valid date for comparison

    # Step 4: Determine the actual next birthday
    next_birthday_year = today.year
    if current_year_birthday < today and not (birth_month == 2 and birth_day == 29 and current_year_birthday.day == 1):
        # If current year's birthday already passed (and not a Feb 29th non-leap year case that implicitly passed)
        next_birthday_year += 1

    # Step 5: Construct the final next birthday date, handling Feb 29th explicitly
    final_next_birthday = None
    if birth_month == 2 and birth_day == 29:
        # If the birth date is Feb 29th, we need to find the next leap year
        # where Feb 29th actually exists.
        current_check_year = next_birthday_year
        while True:
            try:
                final_next_birthday = date(current_check_year, 2, 29)
                break # Found a valid Feb 29th
            except ValueError:
                # current_check_year is not a leap year, try the next year
                current_check_year += 1
    else:
        # For all other birth dates, it's straightforward
        final_next_birthday = date(next_birthday_year, birth_month, birth_day)

    # Step 6: Calculate the difference in days
    days_difference = (final_next_birthday - today).days

    # Step 7: Return the result
    return days_difference

# Entry point: calculate_days_until_next_birthday(birth_date: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_21_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_days_until_next_birthday(birth_date):
    result = calculate_days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
