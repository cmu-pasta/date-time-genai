
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_next_nth_weekday(from_date: date, weekday: int, nth: int) -> date:
    """
    Finds the next date after `from_date` that is the nth occurrence
    of the given weekday (where Monday is 0 and Sunday is 6) in a month.

    Parameters:
        from_date (date): The starting date to search from (exclusive).
        weekday (int): The target weekday (Monday=0 ... Sunday=6).
        nth (int): The nth occurrence in a month (e.g., 3 for "third Thursday").

    Returns:
        date: The next date on or after from_date matching the nth occurrence of weekday.
    """
    if nth < 1 or weekday < 0 or weekday > 6:
        raise ValueError("nth must be >=1, weekday must be in 0...6")

    year = from_date.year
    month = from_date.month

    while True:
        # First day of the month
        first_day = date(year, month, 1)
        # What day of week is the first day?
        first_day_weekday = first_day.weekday()
        # Calculate the day difference to the target weekday
        days_until_target = (weekday - first_day_weekday + 7) % 7
        # The date of the first matching weekday in the month
        first_matching = first_day + timedelta(days=days_until_target)
        # The nth matching date:
        nth_matching = first_matching + timedelta(weeks=nth - 1)

        # Check that nth matching is in the same month
        if nth_matching.month == month and nth_matching > from_date:
            return nth_matching

        # Go to the next month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

# Entry point: get_next_nth_weekday(from_date: date, weekday: int, nth: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_42txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_next_nth_weekday(from_date, weekday, nth):
    result = get_next_nth_weekday(from_date, weekday, nth)
    formatted_result = format_value_dt(result, from_date, weekday, nth)
    log_file.write(formatted_result + "\n")
