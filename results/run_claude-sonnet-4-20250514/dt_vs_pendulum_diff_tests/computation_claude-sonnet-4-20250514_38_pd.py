
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_friday_13th(date: pendulum.Date) -> pendulum.Date:
    # Start checking from the current month
    year = date.year
    month = date.month
    
    while True:
        # Create the 13th of the current month
        thirteenth = pendulum.date(year, month, 13)
        
        # Check if this 13th is after our starting date and is a Friday
        if thirteenth > date and thirteenth.day_of_week == pendulum.FRIDAY:
            return thirteenth
        
        # Move to next month
        month += 1
        if month > 12:
            month = 1
            year += 1

# Entry point: find_next_friday_13th(date: pendulum.Date) -> pendulum.Date

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_38_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_next_friday_13th(date):
    result = find_next_friday_13th(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
