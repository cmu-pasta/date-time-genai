
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_age_in_ymd(d1: pendulum.Date, d2: pendulum.Date) -> pendulum.Duration:
    # Step 1: Get the absolute period difference between the two dates
    period = d1.diff(d2, absolute=True)
    
    # Step 2: Extract years, months, and days from the period
    years = period.years
    months = period.months
    days = period.days  # days remaining after years and months
    
    # Step 3: Return the result as a pendulum.Duration
    return pendulum.duration(years=years, months=months, days=days)

# Entry point: calculate_age_in_ymd(d1: pendulum.Date, d2: pendulum.Date) -> pendulum.Duration

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_6_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_in_ymd(d1, d2):
    result = calculate_age_in_ymd(d1, d2)
    formatted_result = format_value_pd(result, d1, d2)
    log_file.write(formatted_result + "\n")
