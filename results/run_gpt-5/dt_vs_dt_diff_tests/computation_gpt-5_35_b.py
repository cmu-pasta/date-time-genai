
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_last_business_day(d: date) -> date:
    """
    Return the last business day (Mon-Fri) of the month for the given date's month.
    """
    # Step 2: Move to the first day of the next month
    first_of_next_month = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
    # Step 3: Get the last calendar day of the current month
    last_calendar_day = first_of_next_month - timedelta(days=1)
    # Step 4: Adjust backward if the last day is on a weekend (Saturday=5, Sunday=6)
    if last_calendar_day.weekday() == 6:  # Sunday
        return last_calendar_day - timedelta(days=2)
    if last_calendar_day.weekday() == 5:  # Saturday
        return last_calendar_day - timedelta(days=1)
    return last_calendar_day

# Entry point: find_last_business_day(d: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_35_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_last_business_day(d):
    result = find_last_business_day(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
