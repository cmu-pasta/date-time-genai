
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import re
def parse_iso8601_duration(iso_duration: str) -> timedelta:
    # This limited parser supports days (D), hours (H), minutes (M), seconds (S)
    pattern = r'P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$'
    match = re.fullmatch(pattern, iso_duration)
    if not match:
        raise ValueError("Invalid ISO 8601 duration format")
    days = int(match.group('days')) if match.group('days') else 0
    hours = int(match.group('hours')) if match.group('hours') else 0
    minutes = int(match.group('minutes')) if match.group('minutes') else 0
    seconds = int(match.group('seconds')) if match.group('seconds') else 0
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def add_or_subtract_iso8601_duration(dt: datetime, iso_duration: str, add: bool) -> datetime:
    # Step 1: Parse the ISO 8601 duration to a timedelta
    duration = parse_iso8601_duration(iso_duration)
    
    # Step 2: Add or subtract the duration
    if add:
        result = dt + duration
    else:
        result = dt - duration
    
    # Step 3: Return the new datetime object
    return result

# Entry point: add_or_subtract_iso8601_duration(dt: datetime, iso_duration: str, add: bool) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_63txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), string_strategy(), bool_strategy())
def test_add_or_subtract_iso8601_duration(dt, iso_duration, add):
    result = add_or_subtract_iso8601_duration(dt, iso_duration, add)
    formatted_result = format_value_dt(result, dt, iso_duration, add)
    log_file.write(formatted_result + "\n")
