
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> time:
    """
    Converts a time represented in 12-hour format (with an AM/PM indicator)
    into a time object in 24-hour format.

    :param hour: int, hour in 12-hour format (1-12)
    :param minute: int, minute (0-59)
    :param second: int, second (0-59)
    :param is_pm: bool, True if PM, False if AM
    :return: time, Python standard library datetime.time object in 24-hour format
    """
    if hour < 1 or hour > 12:
        raise ValueError("Hour must be in range 1-12 for 12-hour format.")
    if is_pm:
        if hour != 12:
            hour_24 = hour + 12
        else:
            hour_24 = 12
    else:
        if hour == 12:
            hour_24 = 0
        else:
            hour_24 = hour
    return time(hour_24, minute, second)

# Entry point: convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> time

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_48txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), bool_strategy())
def test_convert_12_to_24_hour(hour, minute, second, is_pm):
    result = convert_12_to_24_hour(hour, minute, second, is_pm)
    formatted_result = format_value_dt(result, hour, minute, second, is_pm)
    log_file.write(formatted_result + "\n")
