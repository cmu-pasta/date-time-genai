
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_friday_13th(start_date: pendulum.DateTime) -> pendulum.DateTime:
    # Start checking from the day after the given start_date
    current_date = start_date.add(days=1)

    while True:
        # Check if the current date is the 13th of the month
        is_thirteenth = current_date.day == 13
        
        # Check if the current date is a Friday
        is_friday = current_date.day_of_week == pendulum.FRIDAY # pendulum.FRIDAY has a value of 5

        if is_thirteenth and is_friday:
            # If both conditions are met, this is our Friday the 13th
            return current_date
        
        # Move to the next day if conditions are not met
        current_date = current_date.add(days=1)

# Entry point: find_next_friday_13th(start_date: pendulum.DateTime) -> pendulum.DateTime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_38_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_friday_13th(start_date):
    result = find_next_friday_13th(start_date)
    formatted_result = format_value_pd(result, start_date)
    log_file.write(formatted_result + "\n")
