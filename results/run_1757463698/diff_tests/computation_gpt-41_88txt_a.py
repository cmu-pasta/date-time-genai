
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_months_with_five_weekends(start_date: date, end_date: date) -> int:
    # Ensure proper order regardless of input
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Move to the first day of the start month
    current = date(start_date.year, start_date.month, 1)
    # Move to the first day of the month after the end date
    if end_date.month == 12:
        after_end = date(end_date.year + 1, 1, 1)
    else:
        after_end = date(end_date.year, end_date.month + 1, 1)
    
    count = 0
    while current < after_end:
        # Find last day of current month
        if current.month == 12:
            next_month = date(current.year + 1, 1, 1)
        else:
            next_month = date(current.year, current.month + 1, 1)
        last_day = next_month - timedelta(days=1)
        # Only consider months that the dates actually cover
        month_start = max(current, start_date)
        month_end = min(last_day, end_date)
        # Only process full months
        if (month_start == current) and (month_end == last_day):
            # Count number of Saturdays and Sundays in the month
            saturdays = 0
            sundays = 0
            for day in range(1, last_day.day + 1):
                this_day = date(current.year, current.month, day)
                weekday = this_day.weekday() # Monday=0, Sunday=6
                if weekday == 5:
                    saturdays += 1
                elif weekday == 6:
                    sundays += 1
            if saturdays == 5 and sundays == 5:
                count += 1
        current = next_month
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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_88txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_months_with_five_weekends(start_date, end_date):
    result = count_months_with_five_weekends(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
