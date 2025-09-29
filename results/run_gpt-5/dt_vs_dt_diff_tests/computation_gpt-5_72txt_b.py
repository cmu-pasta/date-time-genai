
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_biweekly_pay_periods_in_year(year: int, anchor_period_start: date) -> int:
    """
    Calculate the number of bi-weekly payroll periods in a given year,
    based on a known anchor date that starts a bi-weekly pay period.

    Args:
        year: The calendar year for which to count periods.
        anchor_period_start: A date known to be the start of a bi-weekly pay period on the schedule.

    Returns:
        An integer count of bi-weekly payroll periods whose start dates fall within the given year.
    """
    # Define the boundaries of the year
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    # Length of one bi-weekly period
    period = timedelta(days=14)

    # Compute the first pay period start on or after Jan 1 of the given year
    delta_days = (year_start - anchor_period_start).days
    remainder = delta_days % 14  # alignment relative to the anchor
    if remainder == 0:
        first_start_in_year = year_start
    else:
        first_start_in_year = year_start + timedelta(days=(14 - remainder))

    # If no period starts within the year, return 0
    if first_start_in_year > year_end:
        return 0

    # Count how many starts occur from the first_start_in_year through Dec 31 inclusive
    count = 1 + ((year_end - first_start_in_year).days // 14)
    return int(count)

# Entry point: count_biweekly_pay_periods_in_year(year: int, anchor_period_start: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_72txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), date_strategy())
def test_count_biweekly_pay_periods_in_year(year, anchor_period_start):
    result = count_biweekly_pay_periods_in_year(year, anchor_period_start)
    formatted_result = format_value_dt(result, year, anchor_period_start)
    log_file.write(formatted_result + "\n")
