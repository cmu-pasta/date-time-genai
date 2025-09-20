
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_friday_13th(after_dt: pendulum.DateTime) -> pendulum.Date:
    # Convert the input to a pendulum.Date for day-based comparison
    start_date: pendulum.Date = after_dt.date()
    
    # Determine the first 13th strictly after the given datetime
    if start_date.day < 13:
        candidate: pendulum.Date = pendulum.date(start_date.year, start_date.month, 13)
    else:
        # Move to the 13th of the next month
        candidate = pendulum.date(start_date.year, start_date.month, 13).add(months=1)
    
    # Iterate month by month until the 13th is a Friday
    while not candidate.is_friday():
        candidate = candidate.add(months=1)
    
    return candidate

# Entry point: next_friday_13th(after_dt: pendulum.DateTime) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_38_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_friday_13th(after_dt):
    result = next_friday_13th(after_dt)
    formatted_result = format_value_pd(result, after_dt)
    log_file.write(formatted_result + "\n")
