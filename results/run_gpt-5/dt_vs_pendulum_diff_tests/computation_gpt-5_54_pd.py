
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def percentage_of_year_passed(dt: pendulum.DateTime) -> float:
    """
    Calculate the percentage of the year that has passed for the given pendulum.DateTime.
    Returns a float in the range [0.0, 100.0].
    """
    # Start of the current year in the same timezone as dt
    start_of_year = dt.start_of('year')
    # Start of the next year (exclusive end boundary)
    start_of_next_year = start_of_year.add(years=1)

    # Elapsed and total seconds as floats for precision
    elapsed_seconds = (dt - start_of_year).total_seconds()
    total_seconds = (start_of_next_year - start_of_year).total_seconds()

    # Compute ratio and clamp between 0 and 1
    ratio = elapsed_seconds / total_seconds
    if ratio < 0.0:
        ratio = 0.0
    elif ratio > 1.0:
        ratio = 1.0

    return ratio * 100.0

# Entry point: percentage_of_year_passed(dt: pendulum.DateTime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_54_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_percentage_of_year_passed(dt):
    result = percentage_of_year_passed(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
