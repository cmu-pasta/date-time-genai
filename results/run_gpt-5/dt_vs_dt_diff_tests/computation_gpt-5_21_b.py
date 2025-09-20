
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_until_next_birthday(birth_date: date, today: date) -> int:
    """
    Calculate the number of days until the next birthday given a birth date and today's date.
    Leap day (Feb 29) birthdays are observed on March 1 in non-leap years.
    If today is the birthday, returns 0.
    """
    # Build the next birthday date for the given year, adjusting Feb 29 to Mar 1 if needed
    def birthday_in_year(bd: date, yr: int) -> date:
        try:
            return date(yr, bd.month, bd.day)
        except ValueError:
            # Handles Feb 29 on non-leap years by observing on March 1
            return date(yr, 3, 1)

    # Candidate birthday this year
    this_year_bday = birthday_in_year(birth_date, today.year)

    # Determine the next birthday date
    if this_year_bday < today:
        next_bday = birthday_in_year(birth_date, today.year + 1)
    else:
        next_bday = this_year_bday

    # Days until next birthday
    return (next_bday - today).days

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_21_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_days_until_next_birthday(birth_date, today):
    result = days_until_next_birthday(birth_date, today)
    formatted_result = format_value_dt(result, birth_date, today)
    log_file.write(formatted_result + "\n")
