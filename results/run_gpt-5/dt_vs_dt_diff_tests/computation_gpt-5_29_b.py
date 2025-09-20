
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def thanksgiving_date(year: int) -> date:
    # Step 1: November 1st of the given year
    nov_first = date(year, 11, 1)
    # Step 2: Calculate offset to the first Thursday (weekday(): Monday=0, Thursday=3)
    offset_to_thursday = (3 - nov_first.weekday()) % 7
    first_thursday = nov_first + timedelta(days=offset_to_thursday)
    # Step 3: Fourth Thursday is three weeks after the first Thursday
    fourth_thursday = first_thursday + timedelta(days=21)
    # Step 4: Return the date of Thanksgiving
    return fourth_thursday

# Entry point: thanksgiving_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_29_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_thanksgiving_date(year):
    result = thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
