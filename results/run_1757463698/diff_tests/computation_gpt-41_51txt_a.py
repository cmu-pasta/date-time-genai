
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, date
def get_first_full_moon_of_year(year: int) -> date:
    """
    Calculate the date of the first full moon in the given year
    using a reference full moon and the synodic month length.
    """
    # Step 1: Use a known reference full moon date (2018-01-02 02:24 UTC)
    reference_full_moon = datetime(2018, 1, 2, 2, 24)
    
    # Step 2: Synodic month (lunar cycle) in days
    synodic_month = 29.530588853
    
    # Step 3: Estimate the number of full moons since the reference to the beginning of the target year
    first_jan = datetime(year, 1, 1)
    days_difference = (first_jan - reference_full_moon).days
    n_full_moons = int(days_difference // synodic_month)
    
    # Step 4: Find the date of the first full moon on or after Jan 1 of the target year
    while True:
        next_full_moon = reference_full_moon + timedelta(days=synodic_month * n_full_moons)
        if next_full_moon.year >= year:
            if next_full_moon.year == year:
                # Step 5: Return as a date object
                return next_full_moon.date()
            else:
                # If the next full moon is in a later year, it means there was no full moon in this year
                # (extremely unlikely, but for completeness)
                raise ValueError("Could not find a full moon in the given year.")
        n_full_moons += 1

# Entry point: get_first_full_moon_of_year(year: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_51txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_first_full_moon_of_year(year):
    result = get_first_full_moon_of_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
