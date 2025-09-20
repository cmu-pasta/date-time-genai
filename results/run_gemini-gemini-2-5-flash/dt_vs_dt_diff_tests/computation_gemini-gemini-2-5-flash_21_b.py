
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def calculate_days_until_next_birthday(birth_date: date) -> int:
    # Step 1: Get today's date
    today = date.today()

    # Step 2: Construct the birthday for the current year
    # We use birth_date.month and birth_date.day for the month and day,
    # and today.year for the year.
    # We need to handle potential errors if birth_date.day is 29 and today.year is not a leap year.
    # A simple way to handle this for calculation is to construct the date directly.
    # If the original birth_date was valid, constructing a date for a non-existent day
    # (e.g., Feb 29 in a non-leap year) will raise a ValueError.
    # However, the problem implies valid dates as input.
    try:
        current_year_birthday = date(today.year, birth_date.month, birth_date.day)
    except ValueError:
        # This handles cases like a leap day birthday (Feb 29) in a non-leap year.
        # In such a case, we can treat the birthday as Mar 1 for calculation purposes,
        # or simply adjust to Feb 28 if it's considered to "fall back".
        # For simplicity and common interpretation, if Feb 29 falls in a non-leap year,
        # we consider the birthday to be on March 1st.
        # This is a common way to handle "non-existent" dates for recurring events.
        if birth_date.month == 2 and birth_date.day == 29:
            current_year_birthday = date(today.year, 3, 1) # Treat as March 1st
        else:
            raise # Re-raise for other unexpected ValueError

    # Step 3: Determine the next birthday date
    if current_year_birthday < today:
        # If the birthday for the current year has already passed, the next one is next year.
        try:
            next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
        except ValueError:
            # Handle Feb 29 for next year if next year is not a leap year
            if birth_date.month == 2 and birth_date.day == 29:
                next_birthday = date(today.year + 1, 3, 1) # Treat as March 1st
            else:
                raise
    else:
        # The birthday for the current year is today or in the future.
        next_birthday = current_year_birthday

    # Step 4: Calculate the difference in days
    difference_timedelta = next_birthday - today
    
    # Step 5: Return the number of days as an integer
    return difference_timedelta.days

# Entry point: calculate_days_until_next_birthday(birth_date: date) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_21_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_days_until_next_birthday(birth_date):
    result = calculate_days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
