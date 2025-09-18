
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def next_friday_13th(start: date) -> date:
    """
    Find the next occurrence of Friday the 13th strictly after the given date.

    Parameters:
    - start: date - the starting date (the search begins after this date)

    Returns:
    - date - the next Friday the 13th after the given date
    """
    # Start searching from the day after the given date to ensure "after"
    current = start + timedelta(days=1)
    y, m = current.year, current.month

    while True:
        candidate = date(y, m, 13)
        # Ensure the candidate is not before our search start and is a Friday
        if candidate >= current and candidate.weekday() == 4:  # Monday=0 ... Friday=4
            return candidate

        # Move to the next month
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1

# Entry point: next_friday_13th(start: date) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_38txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_friday_13th(start):
    result = next_friday_13th(start)
    formatted_result = format_value_dt(result, start)
    log_file.write(formatted_result + "\n")
