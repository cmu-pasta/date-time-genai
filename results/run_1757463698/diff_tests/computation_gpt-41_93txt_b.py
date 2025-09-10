
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def convert_to_buddhist_calendar(gregorian_date: date) -> date:
    """
    Converts a Gregorian date to the corresponding Buddhist calendar date.
    The month and day remain the same; the year is increased by 543.
    Limits: datetime.date supports years 1-9999, so input year must be <= 9456.
    """
    buddhist_year = gregorian_date.year + 543
    # Check that the resulting year is valid for datetime.date
    if not (1 <= buddhist_year <= 9999):
        raise ValueError("Resulting Buddhist year out of supported range for datetime.date (1-9999).")
    return date(buddhist_year, gregorian_date.month, gregorian_date.day)

# Entry point: convert_to_buddhist_calendar(gregorian_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_93txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_convert_to_buddhist_calendar(gregorian_date):
    result = convert_to_buddhist_calendar(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
