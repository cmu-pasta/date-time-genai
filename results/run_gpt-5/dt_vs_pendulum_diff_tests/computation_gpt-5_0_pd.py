
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def business_days_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Normalize to start of day to ensure full-day calculations
    s = dt1.start_of('day')
    e = dt2.start_of('day')

    # Ensure s <= e
    if s > e:
        s, e = e, s

    # Total days between (end-exclusive)
    total_days = e.diff(s).in_days()

    # Quick return if no span
    if total_days <= 0:
        return 0

    # Full weeks contribute 5 business days each
    full_weeks = total_days // 7
    business_days = full_weeks * 5

    # Remaining days after full weeks
    remaining = total_days % 7
    start_wd = s.day_of_week  # Monday=0 ... Sunday=6

    # Count weekdays in the remaining tail
    for i in range(remaining):
        wd = (start_wd + i) % 7
        if wd < 5:  # Monday-Friday
            business_days += 1

    return business_days

# Entry point: business_days_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_0_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_business_days_between(dt1, dt2):
    result = business_days_between(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
