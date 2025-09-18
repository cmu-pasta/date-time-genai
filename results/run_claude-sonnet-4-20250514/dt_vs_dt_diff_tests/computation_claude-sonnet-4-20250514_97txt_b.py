
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def gregorian_to_thai_buddhist(gregorian_date: date) -> date:
    # Convert Gregorian year to Thai Buddhist year by adding 543
    thai_buddhist_year = gregorian_date.year + 543
    
    # Create a new date object with the Thai Buddhist year
    # Keep the same month and day as the original Gregorian date
    thai_buddhist_date = date(thai_buddhist_year, gregorian_date.month, gregorian_date.day)
    
    return thai_buddhist_date

# Entry point: gregorian_to_thai_buddhist(gregorian_date: date) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_97txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_thai_buddhist(gregorian_date):
    result = gregorian_to_thai_buddhist(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
