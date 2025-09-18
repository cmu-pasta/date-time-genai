
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    Find the nth occurrence of a specific weekday in a given month and year.

    Parameters:
        year (int): The four-digit year (e.g., 2025).
        month (int): The month number (1-12).
        weekday (int): The target weekday where Monday=0 and Sunday=6.
        n (int): The occurrence number (1 for first, 2 for second, etc.).

    Returns:
        date: The date corresponding to the nth occurrence of the specified weekday.

    Raises:
        ValueError: If inputs are out of range or the nth occurrence does not exist in the month.
    """
    # Basic input validation
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be in 0..6 where Monday=0 and Sunday=6")
    if n < 1:
        raise ValueError("n must be >= 1")

    # First day of the month
    first_of_month = date(year, month, 1)

    # Days to add to reach the first desired weekday in the month
    offset = (weekday - first_of_month.weekday()) % 7
    first_occurrence = first_of_month + timedelta(days=offset)

    # Compute the nth occurrence by adding (n-1) weeks
    nth_occurrence = first_occurrence + timedelta(days=(n - 1) * 7)

    # Ensure the computed date is still in the same month
    if nth_occurrence.month != month:
        raise ValueError("The requested nth occurrence does not exist in the given month.")

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_17txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
