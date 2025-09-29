
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_biweekly_payroll_periods_in_year(year: int, anchor_period_start: date) -> int:
    """
    Count the number of bi-weekly payroll periods that overlap the given calendar year.

    Definitions:
    - A bi-weekly payroll period is 14 days long: [start, start + 13].
    - Periods repeat every 14 days from the provided anchor_period_start.
    - A payroll period is counted if any day in that period falls within the given year.

    Inputs:
    - year: The calendar year to evaluate (e.g., 2025).
    - anchor_period_start: A known start date of a payroll period on the same 14-day schedule.

    Output:
    - Integer count of overlapping bi-weekly payroll periods in the specified year.
    """
    # Boundaries of the target year
    jan1 = date(year, 1, 1)
    dec31 = date(year, 12, 31)

    # Align to the cadence: find the period start on or before Jan 1 that matches the anchor cadence
    # Compute days between Jan 1 and the anchor, then shift back by the remainder modulo 14
    delta_days = (jan1 - anchor_period_start).days
    remainder = delta_days % 14  # Python's modulo handles negatives as well
    first_aligned_start = jan1 - timedelta(days=remainder)  # This is <= Jan 1 and on the same cadence

    # Iterate through starts until we pass Dec 31, counting periods that overlap the year
    count = 0
    period_start = first_aligned_start
    period_length = timedelta(days=13)  # inclusive end offset for a 14-day period
    step = timedelta(days=14)

    while period_start <= dec31:
        period_end = period_start + period_length
        if period_end >= jan1:
            count += 1
        period_start += step

    return count

# Entry point: count_biweekly_payroll_periods_in_year(year: int, anchor_period_start: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_72txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), date_strategy())
def test_count_biweekly_payroll_periods_in_year(year, anchor_period_start):
    result = count_biweekly_payroll_periods_in_year(year, anchor_period_start)
    formatted_result = format_value_dt(result, year, anchor_period_start)
    log_file.write(formatted_result + "\n")
