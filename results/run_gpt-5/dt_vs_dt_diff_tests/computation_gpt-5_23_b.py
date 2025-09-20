
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta
def next_full_moon_after(d: date) -> date:
    # Step 1: Known full moon reference (UTC) and synodic month length
    reference_full_moon = datetime(2000, 1, 21, 16, 41, 0)  # Jan 21, 2000 16:41 UTC (full moon)
    synodic_month = timedelta(days=29.530588853)  # Average time between full moons

    # Step 2: Convert input date to a datetime at start of day
    target_dt = datetime(d.year, d.month, d.day, 0, 0, 0)

    # Step 3: Compute cycles elapsed as a float
    cycles_elapsed = (target_dt - reference_full_moon) / synodic_month

    # Step 4: Compute the next cycle index strictly after target_dt
    # floor via // 1 works for negatives as well; add 1 to get the first full moon after target_dt
    next_cycle_index = int(cycles_elapsed // 1) + 1

    # Step 5: Compute the next full moon datetime and return its date
    next_full_moon_dt = reference_full_moon + next_cycle_index * synodic_month
    return next_full_moon_dt.date()

# Entry point: next_full_moon_after(d: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_23_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_full_moon_after(d):
    result = next_full_moon_after(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
