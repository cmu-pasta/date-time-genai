
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def gregorian_to_thai_buddhist(gregorian_date: date) -> date:
    """
    Convert a Gregorian date to its Thai Buddhist calendar equivalent.
    
    The Thai Buddhist calendar is Gregorian with the year offset by +543.
    Months and days are identical.
    
    Parameters:
    - gregorian_date: date (or datetime; if datetime, its date component is used)
    
    Returns:
    - date in the Thai Buddhist calendar (year = Gregorian year + 543)
    
    Raises:
    - ValueError if the resulting year is outside Python's supported date range.
    """
    # If a datetime is inadvertently provided, use its date component
    if isinstance(gregorian_date, datetime):
        gregorian_date = gregorian_date.date()
    
    be_year = gregorian_date.year + 543
    
    # Ensure the result is within the valid range for datetime.date
    if not (1 <= be_year <= 9999):
        raise ValueError("Resulting Thai Buddhist year is out of supported range for datetime.date.")
    
    return date(be_year, gregorian_date.month, gregorian_date.day)

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_97txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_thai_buddhist(gregorian_date):
    result = gregorian_to_thai_buddhist(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
