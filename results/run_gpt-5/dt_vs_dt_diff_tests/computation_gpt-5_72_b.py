
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_biweekly_periods_in_year(year: int, anchor_date: date) -> int:
    # Step 1: Define the start and end dates of the target year.
    jan1 = date(year, 1, 1)
    dec31 = date(year, 12, 31)

    # Step 2: Compute the first payday on or after Jan 1 that aligns with the bi-weekly cycle.
    # The cycle is every 14 days from 'anchor_date'.
    # Compute offset to the next aligned date >= Jan 1 using modulo arithmetic on day counts.
    delta_days = (jan1 - anchor_date).days
    remainder = delta_days % 14  # Python's % yields a non-negative result
    if remainder == 0:
        first_payday = jan1
    else:
        first_payday = jan1 + timedelta(days=(14 - remainder))

    # Step 3: Count all aligned paydays within the year (<= Dec 31).
    count = 0
    current = first_payday
    while current <= dec31:
        count += 1
        current += timedelta(days=14)

    # Step 4: Return the total number of bi-weekly payroll periods (paydays) in the given year.
    return count

# Entry point: count_biweekly_periods_in_year(year: int, anchor_date: date) -> int

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_72_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), date_strategy())
def test_count_biweekly_periods_in_year(year, anchor_date):
    result = count_biweekly_periods_in_year(year, anchor_date)
    formatted_result = format_value_dt(result, year, anchor_date)
    log_file.write(formatted_result + "\n")
