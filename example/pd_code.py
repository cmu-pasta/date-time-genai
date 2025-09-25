import os

import pendulum
from hypothesis import given, seed, settings
from pendulum_generators import *


def calculate_days_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Calculate the difference in days
    difference = abs((dt2 - dt1).days)

    # Return the result as an integer
    return difference


# Entry point: calculate_days_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int


def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)


log_file = open("pd_log.txt", "w")


@seed(1234)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_days_difference(dt1, dt2):
    result = calculate_days_difference(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
