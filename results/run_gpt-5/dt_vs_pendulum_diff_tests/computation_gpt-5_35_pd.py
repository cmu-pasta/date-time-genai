
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def last_business_day_of_month(dt: pendulum.DateTime) -> pendulum.Date:
    # Step 1: Get the end of the given month
    current = dt.end_of('month')
    # Step 2: Move backwards until we land on a weekday (Mon-Fri)
    while not current.is_weekday():
        current = current.subtract(days=1)
    # Step 3: Return the date component as a pendulum.Date
    return current.date()

# Entry point: last_business_day_of_month(dt: pendulum.DateTime) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_35_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_last_business_day_of_month(dt):
    result = last_business_day_of_month(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
