
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def convert_datetime_to_12h(dt: datetime) -> time:
    """
    Convert a datetime in 24-hour time to a 12-hour time with AM/PM indication.
    The AM/PM information is encoded via the 'fold' attribute:
      - fold == 0 represents AM
      - fold == 1 represents PM
    The returned object is a datetime.time instance.
    """
    hour_24 = dt.hour
    is_pm = hour_24 >= 12
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12

    return time(
        hour=hour_12,
        minute=dt.minute,
        second=dt.second,
        microsecond=dt.microsecond,
        tzinfo=dt.tzinfo,
        fold=1 if is_pm else 0
    )

# Entry point: convert_datetime_to_12h(dt: datetime) -> time

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_46_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_datetime_to_12h(dt):
    result = convert_datetime_to_12h(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
