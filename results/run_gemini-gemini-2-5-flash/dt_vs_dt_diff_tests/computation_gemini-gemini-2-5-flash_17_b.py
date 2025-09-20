
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, occurrence_n: int) -> date:
    # Step 1: Create a date object for the first day of the given month
    first_day_of_month = date(year, month, 1)

    # Step 2: Calculate the offset to find the first occurrence of the target weekday
    # weekday() returns 0 for Monday, 6 for Sunday.
    # The formula (weekday - current_weekday + 7) % 7 gives the days to add.
    days_to_first_occurrence = (weekday - first_day_of_month.weekday() + 7) % 7

    # Step 3: Find the date of the first occurrence of the target weekday in the month
    first_occurrence_date = first_day_of_month + timedelta(days=days_to_first_occurrence)

    # Step 4: Calculate the date of the nth occurrence
    # Add (occurrence_n - 1) weeks (each week is 7 days) to the first occurrence
    nth_occurrence_date = first_occurrence_date + timedelta(weeks=(occurrence_n - 1))

    # Step 5: Validate that the resulting date is still within the given month.
    # If occurrence_n is too large, nth_occurrence_date might fall into the next month.
    # The problem implies we return the date if found. If not found (i.e., it's in the next month),
    # it's an invalid input for 'occurrence_n' for the given month.
    # We will assume valid 'occurrence_n' such that the date falls within the month.
    if nth_occurrence_date.month != month:
        # This case handles scenarios where the nth occurrence does not exist in the month.
        # As per the problem constraints, we should return a standard library type.
        # Raising an error is often appropriate for invalid inputs.
        raise ValueError(f"The {occurrence_n}th occurrence of weekday {weekday} does not exist in {month}/{year}.")

    # Step 6: Return the resulting date
    return nth_occurrence_date

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday: int, occurrence_n: int) -> date

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_17_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, occurrence_n):
    result = find_nth_weekday_in_month(year, month, weekday, occurrence_n)
    formatted_result = format_value_dt(result, year, month, weekday, occurrence_n)
    log_file.write(formatted_result + "\n")
