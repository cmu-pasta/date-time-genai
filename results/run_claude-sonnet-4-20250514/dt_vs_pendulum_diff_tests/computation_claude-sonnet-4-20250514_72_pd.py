
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_biweekly_payroll_periods(year: int) -> int:
    # Step 1: Get the start of the year (January 1st)
    year_start = pendulum.date(year, 1, 1)
    
    # Step 2: Get the end of the year (December 31st)
    year_end = pendulum.date(year, 12, 31)
    
    # Step 3: Calculate the total days in the year
    total_days = year_end.diff(year_start).in_days() + 1  # +1 to include both start and end dates
    
    # Step 4: Calculate the number of complete bi-weekly periods (14 days each)
    biweekly_periods = total_days // 14
    
    # Step 5: Return the result as an integer
    return biweekly_periods

# Entry point: calculate_biweekly_payroll_periods(year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_72_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_payroll_periods(year):
    result = calculate_biweekly_payroll_periods(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
