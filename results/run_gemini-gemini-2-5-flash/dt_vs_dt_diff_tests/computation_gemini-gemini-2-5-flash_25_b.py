
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def do_date_ranges_overlap(start_date1: datetime, end_date1: datetime, start_date2: datetime, end_date2: datetime) -> bool:
    """
    Determines if two date ranges overlap.
    A date range is defined by an inclusive start and end datetime.

    Args:
        start_date1: The start datetime of the first range.
        end_date1: The end datetime of the first range.
        start_date2: The start datetime of the second range.
        end_date2: The end datetime of the second range.

    Returns:
        True if the two date ranges overlap, False otherwise.
    """
    # Two ranges [start1, end1] and [start2, end2] overlap if:
    # the start of the first range is before or at the end of the second range AND
    # the start of the second range is before or at the end of the first range.
    # This correctly handles cases where ranges touch or one contains the other.
    overlap = (start_date1 <= end_date2) and (start_date2 <= end_date1)
    
    return overlap

# Entry point: do_date_ranges_overlap(start_date1: datetime, end_date1: datetime, start_date2: datetime, end_date2: datetime) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_25_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_do_date_ranges_overlap(start_date1, end_date1, start_date2, end_date2):
    result = do_date_ranges_overlap(start_date1, end_date1, start_date2, end_date2)
    formatted_result = format_value_dt(result, start_date1, end_date1, start_date2, end_date2)
    log_file.write(formatted_result + "\n")
