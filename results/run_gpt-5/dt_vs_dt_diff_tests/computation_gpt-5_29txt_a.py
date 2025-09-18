
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def thanksgiving_date(year: int) -> date:
    """
    Compute the date of Thanksgiving (fourth Thursday of November) for a given year.
    """
    # Step 1: Start at November 1st of the given year
    nov_first = date(year, 11, 1)

    # Step 2: Compute the offset to the first Thursday (weekday(): Monday=0 ... Sunday=6, Thursday=3)
    thursday_weekday = 3
    offset = (thursday_weekday - nov_first.weekday()) % 7

    # Step 3: First Thursday of November
    first_thursday = nov_first + timedelta(days=offset)

    # Step 4: Fourth Thursday (Thanksgiving) = first Thursday + 3 weeks
    thanksgiving = first_thursday + timedelta(weeks=3)

    # Step 5: Return the Thanksgiving date
    return thanksgiving

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_29txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_thanksgiving_date(year):
    result = thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
