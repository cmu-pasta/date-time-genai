
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_biweekly_pay_periods(year: int, anchor_payday: date) -> int:
    """
    Count the number of bi-weekly payroll periods (paydays) that occur in the given calendar year,
    aligned to a known anchor payday. The anchor_payday can be any date that is on the employer's
    bi-weekly payday cycle.

    Args:
        year: The calendar year for which to count pay periods.
        anchor_payday: A date that is known to be a payday in the bi-weekly cycle.

    Returns:
        The number of bi-weekly paydays that fall within the specified year.
    """
    start_of_year = date(year, 1, 1)
    end_of_year = date(year, 12, 31)

    # Compute the first payday on or after Jan 1 by aligning to the 14-day cycle.
    # Python's modulo yields a non-negative remainder, suitable for alignment.
    delta_days = (start_of_year - anchor_payday).days
    remainder = delta_days % 14
    first_payday = start_of_year if remainder == 0 else (start_of_year + timedelta(days=(14 - remainder)))

    # Count how many 14-day intervals from first_payday fit within the year
    if first_payday > end_of_year:
        return 0

    span_days = (end_of_year - first_payday).days
    periods_after_first = span_days // 14
    return 1 + periods_after_first

# Entry point: count_biweekly_pay_periods(year: int, anchor_payday: date) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_72_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), date_strategy())
def test_count_biweekly_pay_periods(year, anchor_payday):
    result = count_biweekly_pay_periods(year, anchor_payday)
    formatted_result = format_value_dt(result, year, anchor_payday)
    log_file.write(formatted_result + "\n")
