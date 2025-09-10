
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def datetime_to_relative(dt: datetime) -> str:
    """
    Convert a datetime to a human-readable relative time string.
    """
    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    delta = now - dt
    seconds = int(delta.total_seconds())
    abs_seconds = abs(seconds)

    if abs_seconds < 60:
        if abs_seconds < 1:
            return "just now"
        unit = "second" if abs_seconds == 1 else "seconds"
        return f"{abs_seconds} {unit} ago" if seconds >= 0 else f"in {abs_seconds} {unit}"
    elif abs_seconds < 3600:
        minutes = abs_seconds // 60
        unit = "minute" if minutes == 1 else "minutes"
        if minutes == 1:
            return "a minute ago" if seconds >= 0 else "in a minute"
        return f"{minutes} {unit} ago" if seconds >= 0 else f"in {minutes} {unit}"
    elif abs_seconds < 86400:
        hours = abs_seconds // 3600
        unit = "hour" if hours == 1 else "hours"
        if hours == 1:
            return "an hour ago" if seconds >= 0 else "in an hour"
        return f"{hours} {unit} ago" if seconds >= 0 else f"in {hours} {unit}"
    elif abs_seconds < 172800:
        if seconds > 0:
            return "yesterday"
        else:
            return "tomorrow"
    elif abs_seconds < 604800:
        days = abs_seconds // 86400
        unit = "day" if days == 1 else "days"
        return f"{days} {unit} ago" if seconds >= 0 else f"in {days} {unit}"
    elif abs_seconds < 2592000:
        weeks = abs_seconds // 604800
        if weeks == 1:
            return "a week ago" if seconds >= 0 else "in a week"
        unit = "weeks"
        return f"{weeks} {unit} ago" if seconds >= 0 else f"in {weeks} {unit}"
    elif abs_seconds < 31536000:
        months = abs_seconds // 2592000  # 30 days = 2592000 seconds
        if months == 1:
            return "a month ago" if seconds >= 0 else "in a month"
        unit = "months"
        return f"{months} {unit} ago" if seconds >= 0 else f"in {months} {unit}"
    else:
        years = abs_seconds // 31536000  # 365 days = 31536000 seconds
        if years == 1:
            return "a year ago" if seconds >= 0 else "in a year"
        unit = "years"
        return f"{years} {unit} ago" if seconds >= 0 else f"in {years} {unit}"

# Entry point: datetime_to_relative(dt: datetime) -> str

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_32txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_relative(dt):
    result = datetime_to_relative(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
