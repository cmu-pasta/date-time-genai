
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_until_next_birthday(birth_date: date, today: date) -> int:
    # Step 1: Determine the candidate birthday in the current year
    year = today.year
    try:
        next_birthday = date(year, birth_date.month, birth_date.day)
    except ValueError:
        # Handles Feb 29 birthdays in non-leap years by using Feb 28
        next_birthday = date(year, 2, 28)

    # Step 2: If today's date is after this year's birthday, compute for next year
    if next_birthday < today:
        year += 1
        try:
            next_birthday = date(year, birth_date.month, birth_date.day)
        except ValueError:
            # Handles Feb 29 birthdays in non-leap years by using Feb 28
            next_birthday = date(year, 2, 28)

    # Step 3: Return the difference in days as an integer
    return (next_birthday - today).days

# Entry point: days_until_next_birthday(birth_date: date, today: date) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_21_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_days_until_next_birthday(birth_date, today):
    result = days_until_next_birthday(birth_date, today)
    formatted_result = format_value_dt(result, birth_date, today)
    log_file.write(formatted_result + "\n")
