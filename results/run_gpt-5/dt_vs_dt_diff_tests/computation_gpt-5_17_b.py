
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    # Validate inputs
    if month < 1 or month > 12:
        raise ValueError("Month must be in 1..12.")
    if weekday < 0 or weekday > 6:
        raise ValueError("Weekday must be in 0..6 where Monday=0 and Sunday=6.")
    if n < 1:
        raise ValueError("n must be a positive integer.")

    # First day of the month
    first_day = date(year, month, 1)

    # Offset to the first desired weekday in the month
    offset = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day + timedelta(days=offset)

    # Compute the nth occurrence
    nth_date = first_occurrence + timedelta(days=(n - 1) * 7)

    # Ensure the nth occurrence is within the same month
    if nth_date.month != month:
        raise ValueError("The requested nth occurrence does not exist in the given month.")

    return nth_date

# Entry point: nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_17_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_nth_weekday_of_month(year, month, weekday, n):
    result = nth_weekday_of_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
