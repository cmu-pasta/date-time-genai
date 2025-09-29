
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def business_days_remaining_in_month(dt: pendulum.DateTime) -> int:
    """
    Calculate the number of business days (Mon-Fri) remaining in the current month,
    including the given date if it is a business day.
    """
    # Start from the beginning of the given day
    current = dt.start_of('day')
    # End at the last day of the current month (normalized to start of day for iteration)
    end = dt.end_of('month').start_of('day')

    count = 0
    # Iterate each day from current to end (inclusive)
    for d in pendulum.period(current, end).range('days'):
        # day_of_week: Monday=0 ... Sunday=6
        if d.day_of_week < 5:
            count += 1

    return count

# Entry point: business_days_remaining_in_month(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_45_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_business_days_remaining_in_month(dt):
    result = business_days_remaining_in_month(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
