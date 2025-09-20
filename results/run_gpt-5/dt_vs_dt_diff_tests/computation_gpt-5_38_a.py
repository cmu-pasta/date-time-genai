
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def next_friday_13th(after: date) -> date:
    # Start strictly after the given date
    start = after + timedelta(days=1)

    y = start.year
    m = start.month

    # Determine the first candidate 13th to check
    if start.day > 13:
        m += 1
        if m > 12:
            m = 1
            y += 1

    candidate = date(y, m, 13)
    if candidate < start:
        # Safety adjustment if candidate is still before 'start'
        m += 1
        if m > 12:
            m = 1
            y += 1
        candidate = date(y, m, 13)

    # Advance by months until the 13th is a Friday (weekday() == 4)
    while candidate.weekday() != 4:
        m += 1
        if m > 12:
            m = 1
            y += 1
        candidate = date(y, m, 13)

    return candidate

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_38_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_friday_13th(after):
    result = next_friday_13th(after)
    formatted_result = format_value_dt(result, after)
    log_file.write(formatted_result + "\n")
