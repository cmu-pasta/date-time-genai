
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_work_weeks(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Normalize dates to the start of the day and ensure correct order
    # The time component doesn't affect the number of work weeks.
    date1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    date2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)

    start_date = min(date1, date2)
    end_date = max(date1, date2)

    # Step 2: Find the first Monday on or after the start_date
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    # To get to the next Monday, we calculate days_to_monday.
    # If it's already Monday (weekday() == 0), days_to_monday will be 0.
    days_to_monday = (7 - start_date.weekday()) % 7
    first_monday = start_date + timedelta(days=days_to_monday)

    # If the start_date itself is a Monday, and it's before end_date,
    # first_monday will be start_date.
    # If the start_date is, say, Tuesday, first_monday will be next Monday.

    # Step 3: Count the number of Mondays between first_monday and end_date (inclusive of first_monday if it falls within the range)
    work_weeks_count = 0
    current_monday = first_monday

    # Iterate while the current_monday is on or before the end_date.
    # We count each Monday as the start of a new work week.
    while current_monday <= end_date:
        # We only count this Monday if it's within the original date range.
        # This condition current_monday >= start_date is inherently true because first_monday is derived from start_date.
        # The main check is current_monday <= end_date.
        
        # If the original start_date itself is *after* current_monday (which is derived from start_date but might be advanced),
        # this logic handles it. However, the first_monday calculation already ensures current_monday >= start_date.
        # So, simply counting if current_monday <= end_date is sufficient.
        work_weeks_count += 1
        current_monday += timedelta(weeks=1)
            
    # Step 4: Return the result
    return work_weeks_count

# Entry point: calculate_work_weeks(dt1: datetime, dt2: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_57_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_work_weeks(dt1, dt2):
    result = calculate_work_weeks(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
