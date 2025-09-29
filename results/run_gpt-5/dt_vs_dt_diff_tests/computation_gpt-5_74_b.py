
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
def next_new_moon_after(given_dt: datetime) -> date:
    # Reference new moon: 2000-01-06 18:14:00 UTC (widely used epoch)
    reference_new_moon = datetime(2000, 1, 6, 18, 14, 0)

    # Mean synodic month length in days (average time between new moons)
    synodic_month_days = 29.530588853

    # Convert synodic month length to seconds to avoid floating drift with timedelta(days=...)
    seconds_per_day = 86400.0
    synodic_month_seconds = synodic_month_days * seconds_per_day

    # Elapsed time in seconds from reference to the given datetime
    elapsed_seconds = (given_dt - reference_new_moon).total_seconds()

    # Number of completed lunations since the reference (floor division for correct handling of negatives)
    completed_lunations = int(elapsed_seconds // synodic_month_seconds)

    # Next lunation index strictly after the given datetime
    next_lunation_index = completed_lunations + 1

    # Compute the datetime of the next new moon
    next_new_moon_dt = reference_new_moon + timedelta(seconds=next_lunation_index * synodic_month_seconds)

    # Return the calendar date of the next new moon
    return next_new_moon_dt.date()

# Entry point: next_new_moon_after(given_dt: datetime) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_74_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon_after(given_dt):
    result = next_new_moon_after(given_dt)
    formatted_result = format_value_dt(result, given_dt)
    log_file.write(formatted_result + "\n")
