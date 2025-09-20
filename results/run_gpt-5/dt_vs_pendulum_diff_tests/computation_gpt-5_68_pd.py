
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def labor_day(year: int) -> pendulum.Date:
    # Step 3: Start with September 1st of the given year
    sept_first = pendulum.date(year, 9, 1)
    # Step 4: Determine the weekday (0=Monday,...,6=Sunday)
    weekday = sept_first.weekday()
    # Step 5: Compute days to add to reach the first Monday
    days_to_monday = (0 - weekday) % 7
    # Step 6: Add the computed offset
    labor_day_date = sept_first.add(days=days_to_monday)
    # Step 7: Return the pendulum.Date
    return labor_day_date

# Entry point: labor_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_68_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_labor_day(year):
    result = labor_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
