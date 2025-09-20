
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def memorial_day(year: int) -> date:
    """
    Compute Memorial Day (last Monday of May) for the given year.

    Args:
        year (int): The year for which to compute Memorial Day.

    Returns:
        date: The date of Memorial Day in the given year.
    """
    may_31 = date(year, 5, 31)
    # Monday is 0; compute days to subtract from May 31 to reach Monday
    offset = (may_31.weekday() - 0) % 7
    return may_31 - timedelta(days=offset)

# Entry point: memorial_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_47_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_memorial_day(year):
    result = memorial_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
