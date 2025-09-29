
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    # Validate inputs
    if weekday < 0 or weekday > 6:
        raise ValueError("weekday must be in range 0 (Monday) to 6 (Sunday).")
    if n < 1:
        raise ValueError("n must be a positive integer (>= 1).")
    
    # First day of the given month
    first_day = date(year, month, 1)
    
    # Compute days to the first desired weekday in the month
    # date.weekday(): Monday=0 ... Sunday=6
    days_to_first = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day + timedelta(days=days_to_first)
    
    # Compute the nth occurrence
    nth_occurrence = first_occurrence + timedelta(weeks=(n - 1))
    
    # Ensure the nth occurrence falls within the same month
    if nth_occurrence.month != month:
        raise ValueError("The requested nth occurrence does not exist in this month.")
    
    return nth_occurrence

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_17_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
