
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_first_day_of_iso_week(year: int, week: int) -> date:
    """
    Returns the first day (Monday) of the given ISO week in the specified year.
    Arguments:
        year: An integer specifying the year.
        week: An integer specifying the ISO week number.
    Returns:
        A date object representing the Monday of the desired ISO week.
    """
    # Use date.fromisocalendar to get the Monday of the desired week
    first_day = date.fromisocalendar(year, week, 1)
    return first_day

# Entry point: get_first_day_of_iso_week(year: int, week: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_79txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_get_first_day_of_iso_week(year, week):
    result = get_first_day_of_iso_week(year, week)
    formatted_result = format_value_dt(result, year, week)
    log_file.write(formatted_result + "\n")
