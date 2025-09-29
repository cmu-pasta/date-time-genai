
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_valentines_day(after_dt: pendulum.DateTime) -> pendulum.DateTime:
    """
    Find the next Valentine's Day (February 14) strictly after the given datetime.
    The returned datetime is set to 00:00:00 on that date in the same timezone as the input.
    """
    # Construct candidate for this year's Valentine's Day at midnight in the same timezone
    candidate = after_dt.replace(month=2, day=14, hour=0, minute=0, second=0, microsecond=0)

    # If the given datetime is on or after this year's Valentine's Day, use next year's
    if after_dt >= candidate:
        candidate = candidate.add(years=1)

    return candidate

# Entry point: next_valentines_day(after_dt: pendulum.DateTime) -> pendulum.DateTime

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_56txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_valentines_day(after_dt):
    result = next_valentines_day(after_dt)
    formatted_result = format_value_pd(result, after_dt)
    log_file.write(formatted_result + "\n")
