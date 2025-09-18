
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def to_thai_buddhist_date(gregorian: date) -> date:
    """
    Convert a Gregorian calendar date to the Thai Buddhist calendar date.
    - Thai Buddhist Era (BE) year = Common Era (CE) year + 543
    - Month and day remain the same.

    Note:
    This returns a datetime.date object with the BE year. This is a representation
    of the Thai Buddhist calendar date using the standard datetime date type.
    """
    return date(gregorian.year + 543, gregorian.month, gregorian.day)

def to_thai_buddhist_datetime(gregorian: datetime) -> datetime:
    """
    Convert a Gregorian calendar datetime to the Thai Buddhist calendar datetime,
    preserving time and tzinfo.
    """
    return datetime(
        gregorian.year + 543,
        gregorian.month,
        gregorian.day,
        gregorian.hour,
        gregorian.minute,
        gregorian.second,
        gregorian.microsecond,
        tzinfo=gregorian.tzinfo,
    )

# Entry point: to_thai_buddhist_date(gregorian: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_97txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_to_thai_buddhist_date(gregorian):
    result = to_thai_buddhist_date(gregorian)
    formatted_result = format_value_dt(result, gregorian)
    log_file.write(formatted_result + "\n")
