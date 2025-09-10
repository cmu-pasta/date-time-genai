
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def gregorian_to_buddhist_calendar(gregorian_date: date) -> date:
    # Step 1: Extract year, month, and day from the Gregorian date
    year = gregorian_date.year
    month = gregorian_date.month
    day = gregorian_date.day

    # Step 2: Convert the year to Buddhist calendar by adding 543
    buddhist_year = year + 543

    # Step 3: Construct and return the Buddhist calendar date
    buddhist_date = date(buddhist_year, month, day)
    return buddhist_date

# Entry point: gregorian_to_buddhist_calendar(gregorian_date: date) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_93txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_buddhist_calendar(gregorian_date):
    result = gregorian_to_buddhist_calendar(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
