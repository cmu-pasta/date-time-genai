
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def do_date_ranges_overlap(range1_start: datetime, range1_end: datetime, range2_start: datetime, range2_end: datetime) -> bool:
    # Step 1: Check if the first range starts before or at the same time as the second range ends.
    # Step 2: Check if the second range starts before or at the same time as the first range ends.
    # If both conditions are true, the ranges overlap.
    # This logic assumes inclusive start and end dates for the ranges.
    
    overlaps = (range1_start <= range2_end) and (range2_start <= range1_end)
    
    # Step 3: Return the boolean result
    return overlaps

# Entry point: do_date_ranges_overlap(range1_start: datetime, range1_end: datetime, range2_start: datetime, range2_end: datetime) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_25_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_do_date_ranges_overlap(range1_start, range1_end, range2_start, range2_end):
    result = do_date_ranges_overlap(range1_start, range1_end, range2_start, range2_end)
    formatted_result = format_value_dt(result, range1_start, range1_end, range2_start, range2_end)
    log_file.write(formatted_result + "\n")
