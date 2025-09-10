
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def _first_of_month(d: date) -> date:
    return date(d.year, d.month, 1)

def _add_one_month(d: date) -> date:
    # Get to the first of the next month
    if d.month == 12:
        return date(d.year + 1, 1, 1)
    else:
        return date(d.year, d.month + 1, 1)

def _count_weekends_in_month(year: int, month: int) -> (int, int):
    from calendar import monthrange
    days_in_month = monthrange(year, month)[1]
    d = date(year, month, 1)
    saturdays = 0
    sundays = 0
    for day in range(days_in_month):
        weekday = (d.weekday() + day) % 7 # 0=Monday, 5=Saturday, 6=Sunday
        if weekday == 5:
            saturdays += 1
        if weekday == 6:
            sundays += 1
    return saturdays, sundays

def count_months_with_five_weekends(start_date: date, end_date: date) -> int:
    # Ensure start_date <= end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    count = 0
    current = date(start_date.year, start_date.month, 1)
    # go up to and including the end month
    last_month = date(end_date.year, end_date.month, 1)

    while current <= last_month:
        saturdays, sundays = _count_weekends_in_month(current.year, current.month)
        # Only months with both 5 Saturdays and 5 Sundays count
        if saturdays == 5 and sundays == 5:
            count += 1
        current = _add_one_month(current)

    return count

# Entry point: count_months_with_five_weekends(start_date: date, end_date: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_88txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_months_with_five_weekends(start_date, end_date):
    result = count_months_with_five_weekends(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
