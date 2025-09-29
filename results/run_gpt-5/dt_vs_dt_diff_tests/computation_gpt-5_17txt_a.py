
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    # Validate inputs
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be in 0..6 where 0=Monday and 6=Sunday")
    if n <= 0:
        raise ValueError("n must be a positive integer")

    # First day of the month
    first_day = date(year, month, 1)
    first_day_weekday = first_day.weekday()  # 0=Monday .. 6=Sunday

    # Days to add to reach the first desired weekday in the month
    days_to_first_target = (weekday - first_day_weekday) % 7
    first_occurrence = first_day + timedelta(days=days_to_first_target)

    # Compute the nth occurrence
    nth_occurrence = first_occurrence + timedelta(weeks=n - 1)

    # Ensure the nth occurrence is within the same month
    if nth_occurrence.month != month:
        raise ValueError("The specified nth occurrence does not exist in this month.")

    return nth_occurrence

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_17txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
