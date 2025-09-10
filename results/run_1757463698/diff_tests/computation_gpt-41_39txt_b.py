
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, timedelta
def business_hours_between(start_dt: datetime, end_dt: datetime) -> float:
    # Define standard business hours
    biz_start = time(9, 0)   # 9:00 AM
    biz_end = time(17, 0)    # 5:00 PM

    # Ensure consistent order
    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    total_hours = 0.0
    current_day = start_dt.date()
    end_day = end_dt.date()

    while current_day <= end_day:
        # Skip weekends
        if datetime.combine(current_day, time()).weekday() < 5:  # Monday=0, Sunday=6
            # For the first and last day, use start/end datetimes, else use business bounds
            if current_day == start_dt.date():
                day_start = max(datetime.combine(current_day, biz_start), start_dt)
            else:
                day_start = datetime.combine(current_day, biz_start)
                
            if current_day == end_dt.date():
                day_end = min(datetime.combine(current_day, biz_end), end_dt)
            else:
                day_end = datetime.combine(current_day, biz_end)

            # Only count positive intervals (avoid cases where day_start > day_end)
            if day_end > day_start:
                duration = (day_end - day_start).total_seconds() / 3600  # Convert to hours
                total_hours += duration

        # Move to next day
        current_day += timedelta(days=1)

    return total_hours

# Entry point: business_hours_between(start_dt: datetime, end_dt: datetime) -> float

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_39txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_business_hours_between(start_dt, end_dt):
    result = business_hours_between(start_dt, end_dt)
    formatted_result = format_value_dt(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
