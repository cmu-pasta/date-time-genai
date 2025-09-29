
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_season(day: date) -> int:
    """
    Determine the meteorological season (Northern Hemisphere) for a given date.
    Returns an integer code:
      1 = spring, 2 = summer, 3 = autumn, 4 = winter
    """
    y = day.year
    spring_start = date(y, 3, 1)
    summer_start = date(y, 6, 1)
    autumn_start = date(y, 9, 1)
    winter_start = date(y, 12, 1)

    if day >= winter_start or day < spring_start:
        return 4  # winter
    elif day >= autumn_start:
        return 3  # autumn
    elif day >= summer_start:
        return 2  # summer
    else:
        return 1  # spring

# Entry point: determine_season(day: date) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_19txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_season(day):
    result = determine_season(day)
    formatted_result = format_value_dt(result, day)
    log_file.write(formatted_result + "\n")
