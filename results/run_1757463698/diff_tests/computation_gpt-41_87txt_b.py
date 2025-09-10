
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_weeknumber_of_last_day_of_year(year: int) -> int:
    # Step 3: Construct the last day of the given year
    last_day = date(year, 12, 31)
    
    # Step 4: Get the ISO week number using isocalendar()
    week_number = last_day.isocalendar()[1]
    
    # Step 5: Return the result as an integer
    return week_number

# Entry point: get_weeknumber_of_last_day_of_year(year: int) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_87txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_weeknumber_of_last_day_of_year(year):
    result = get_weeknumber_of_last_day_of_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
