
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta
def midpoint_date(d1: date, d2: date) -> date:
    """
    Find the date that falls exactly in the middle of two given dates.
    The midpoint is computed as the earlier date plus half the interval between them.
    If the interval has odd days, the midpoint instant falls at noon of the earlier day's date,
    and the resulting date is that earlier date (since we return a date).
    """
    # Ensure we work from the earlier date to the later date
    if d1 <= d2:
        start = d1
        end = d2
    else:
        start = d2
        end = d1

    # Convert to datetime at midnight to handle half-day intervals precisely
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.min.time())

    # Compute midpoint instant
    delta = end_dt - start_dt
    midpoint_dt = start_dt + (delta / 2)

    # Return the date component of the midpoint instant
    return midpoint_dt.date()

# Entry point: midpoint_date(d1: date, d2: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_32_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_midpoint_date(d1, d2):
    result = midpoint_date(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")
