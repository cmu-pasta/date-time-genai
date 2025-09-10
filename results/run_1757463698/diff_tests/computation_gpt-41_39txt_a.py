
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, time
def elapsed_business_hours(dt1: datetime, dt2: datetime) -> float:
    # Define business hours: 9 AM to 5 PM
    BUSINESS_START = time(9, 0)
    BUSINESS_END = time(17, 0)
    BUSINESS_HOURS_PER_DAY = (datetime.combine(datetime.min, BUSINESS_END) - 
                              datetime.combine(datetime.min, BUSINESS_START)).seconds / 3600.0

    # Swap if dt1 after dt2
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1

    total_hours = 0.0
    current_day = dt1.date()
    last_day = dt2.date()

    while current_day <= last_day:
        # Default business interval on this day
        b_start = datetime.combine(current_day, BUSINESS_START)
        b_end = datetime.combine(current_day, BUSINESS_END)
        
        # If weekend, skip
        if b_start.weekday() >= 5:  # 5=Saturday, 6=Sunday
            current_day += timedelta(days=1)
            continue
        
        # Effective interval for this day
        interval_start = max(b_start, dt1) if current_day == dt1.date() else b_start
        interval_end = min(b_end, dt2) if current_day == dt2.date() else b_end
        
        # Only accumulate if the interval is valid
        if interval_end > interval_start:
            hours = (interval_end - interval_start).total_seconds() / 3600.0
            total_hours += hours
        
        current_day += timedelta(days=1)

    return total_hours

# Entry point: elapsed_business_hours(dt1: datetime, dt2: datetime) -> float

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_39txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_elapsed_business_hours(dt1, dt2):
    result = elapsed_business_hours(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
