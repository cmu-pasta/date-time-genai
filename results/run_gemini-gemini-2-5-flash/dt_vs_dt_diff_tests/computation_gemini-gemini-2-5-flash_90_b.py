
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_lunar_age(current_date: date) -> int:
    # Step 1: Define a reference new moon date (e.g., New Moon on 2000-01-06)
    # This date is a fixed astronomical reference point for the calculation.
    reference_new_moon = date(2000, 1, 6)
    
    # Step 2: Define the average synodic month length (in days)
    # This is the average period from one new moon to the next.
    synodic_month_length = 29.530588

    # Step 3: Calculate the total number of days between the reference new moon and the current date
    # This gives us the total elapsed days over multiple lunar cycles.
    total_days_since_reference = (current_date - reference_new_moon).days
    
    # Step 4: Calculate the lunar age
    # The lunar age is the number of days into the current lunar cycle.
    # We use the modulo operator (%) to find the remainder after dividing by the synodic month length.
    # Taking the absolute value ensures correct calculation for dates before the reference.
    lunar_age_float = total_days_since_reference % synodic_month_length
    
    # Ensure the result is non-negative and within the [0, synodic_month_length) range
    if lunar_age_float < 0:
        lunar_age_float += synodic_month_length

    # Step 5: Convert the result to an integer (days)
    return int(lunar_age_float)

# Entry point: calculate_lunar_age(current_date: date) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_90_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_lunar_age(current_date):
    result = calculate_lunar_age(current_date)
    formatted_result = format_value_dt(result, current_date)
    log_file.write(formatted_result + "\n")
