
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_friday_13th(after: date) -> date:
    # Start from the same month and year as the given date
    year = after.year
    month = after.month

    while True:
        # Advance year when month exceeds December
        if month > 12:
            month = 1
            year += 1

        # Construct the 13th of the current month
        candidate = date(year, month, 13)

        # Check if it's strictly after the given date and is a Friday
        if candidate > after and candidate.weekday() == 4:  # Monday=0 ... Friday=4
            return candidate

        # Move to the next month
        month += 1

# Entry point: next_friday_13th(after: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_38_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_friday_13th(after):
    result = next_friday_13th(after)
    formatted_result = format_value_dt(result, after)
    log_file.write(formatted_result + "\n")
