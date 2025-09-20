
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def fiscal_year_for_date(d: date) -> int:
    """
    Determine the fiscal year for an April-start fiscal year.
    Fiscal year runs Apr 1 to Mar 31 and is labeled by the year it ends.
    Example: 2024-04-01 to 2025-03-31 => fiscal year 2025.
    """
    return d.year + 1 if d.month >= 4 else d.year

# Entry point: fiscal_year_for_date(d: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_31_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_fiscal_year_for_date(d):
    result = fiscal_year_for_date(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
