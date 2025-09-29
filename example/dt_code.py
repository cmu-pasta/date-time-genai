import os
from datetime import date, datetime, time, timedelta, timezone

from datetime_generators import *
from hypothesis import given, seed, settings


def calculate_days_difference(dt1: datetime, dt2: datetime) -> int:
    # Calculate the difference in days
    difference = abs((dt2 - dt1).days)

    # Return the result as an integer
    return difference


# Entry point: calculate_days_difference(dt1: datetime, dt2: datetime) -> int


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


log_file = open("dt_log.txt", "w")


@seed(1234)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_days_difference(dt1, dt2):
    result = calculate_days_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
