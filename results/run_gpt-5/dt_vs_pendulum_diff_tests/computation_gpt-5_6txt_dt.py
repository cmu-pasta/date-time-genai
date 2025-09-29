
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def _days_in_month(year: int, month: int) -> int:
    """Return the number of days in a given month/year."""
    if month == 12:
        next_month_first = date(year + 1, 1, 1)
    else:
        next_month_first = date(year, month + 1, 1)
    return (next_month_first - timedelta(days=1)).day

def _add_years_months(d: date, years: int, months: int) -> date:
    """
    Add full years and months to a date, clamping the day to the month's length.
    """
    total_month = d.month + months
    year = d.year + years + (total_month - 1) // 12
    month = ((total_month - 1) % 12) + 1
    day = min(d.day, _days_in_month(year, month))
    return date(year, month, day)

def calculate_age_ymd(start: date, end: date) -> date:
    """
    Calculate the age difference between two dates as years, months, and days.

    Return value encoding (to comply with allowed types):
    - A date object where:
      - year   = full years
      - month  = full months + 1  (so 1..12 represents 0..11 months)
      - day    = remaining days + 1 (so 1..31 represents 0..30 days)

    To interpret the result:
      years  = result.year
      months = result.month - 1
      days   = result.day - 1
    """
    # Ensure chronological order
    if end < start:
        start, end = end, start

    # Compute full years
    years = end.year - start.year
    if (end.month, end.day) < (start.month, start.day):
        years -= 1

    # Compute full months after removing years
    # Tentative month difference relative to the anniversary this year
    months = end.month - start.month
    if end.day < start.day:
        months -= 1
    months = (months + 12) % 12

    # Compute remaining days after removing years and months
    anchor = _add_years_months(start, years, months)
    days = (end - anchor).days  # non-negative

    # Encode into a date object (see docstring for decoding)
    return date(year=years, month=months + 1, day=days + 1)

# Entry point: calculate_age_ymd(start: date, end: date) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_6txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_ymd(start, end):
    result = calculate_age_ymd(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
