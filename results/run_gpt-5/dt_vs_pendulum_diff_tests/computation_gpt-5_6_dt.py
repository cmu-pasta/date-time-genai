
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def _last_day_of_month(y: int, m: int) -> int:
    # Works for 1 <= m <= 12
    if m == 12:
        next_month_first = date(y + 1, 1, 1)
    else:
        next_month_first = date(y, m + 1, 1)
    return (next_month_first - timedelta(days=1)).day

def _add_years(d: date, years: int) -> date:
    # Add years; clamp day if needed (e.g., Feb 29 to Feb 28 on non-leap years)
    y = d.year + years
    m = d.month
    day = d.day
    max_day = _last_day_of_month(y, m)
    if day > max_day:
        day = max_day
    return date(y, m, day)

def _add_months(d: date, months: int) -> date:
    # Add months; clamp day to the last valid day of the target month
    total_month_index = (d.month - 1) + months
    y = d.year + total_month_index // 12
    m = (total_month_index % 12) + 1
    day = d.day
    max_day = _last_day_of_month(y, m)
    if day > max_day:
        day = max_day
    return date(y, m, day)

def calculate_age_ymd(start: date, end: date) -> date:
    """
    Calculate the age difference between two dates as years, months, and days.
    Returns a date object encoding:
      - years  = return.year - 1
      - months = return.month - 1  (0..11)
      - days   = return.day - 1    (>= 0)
    """
    # Ensure start <= end
    if end < start:
        start, end = end, start

    # Whole years
    tentative_years = end.year - start.year
    t = _add_years(start, tentative_years)
    if t > end:
        tentative_years -= 1
        t = _add_years(start, tentative_years)

    # Whole months after years
    tentative_months = (end.year - t.year) * 12 + (end.month - t.month)
    t2 = _add_months(t, tentative_months)
    if t2 > end:
        tentative_months -= 1
        t2 = _add_months(t, tentative_months)

    # Remaining days
    remaining_days = (end - t2).days

    # Encode result as a date: add 1 to each component to satisfy date constraints
    # Decode as: years = year-1, months = month-1, days = day-1
    return date(tentative_years + 1, tentative_months + 1, remaining_days + 1)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_6_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_ymd(start, end):
    result = calculate_age_ymd(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
