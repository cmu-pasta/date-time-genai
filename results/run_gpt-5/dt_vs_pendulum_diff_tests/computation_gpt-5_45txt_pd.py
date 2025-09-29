
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def business_days_remaining_in_month(d: pendulum.Date) -> int:
    """
    Calculate the number of business days (Mon-Fri) remaining in the current month,
    including the given date if it is a business day.
    """
    # Start from the given date
    start = d

    # Compute the last day of the same month
    month_start = pendulum.date(d.year, d.month, 1)
    last_day = month_start.add(months=1).subtract(days=1)

    # Count business days from start to last_day (inclusive)
    count = 0
    current = start
    while current <= last_day:
        if current.day_of_week < 5:  # 0=Mon, ..., 4=Fri
            count += 1
        current = current.add(days=1)

    return count

# Entry point: business_days_remaining_in_month(d: pendulum.Date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_45txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_business_days_remaining_in_month(d):
    result = business_days_remaining_in_month(d)
    formatted_result = format_value_pd(result, d)
    log_file.write(formatted_result + "\n")
