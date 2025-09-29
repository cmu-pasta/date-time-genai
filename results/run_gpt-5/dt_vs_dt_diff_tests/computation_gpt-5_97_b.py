
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def to_thai_buddhist_date(g_date: date) -> date:
    """
    Convert a Gregorian date to the Thai Buddhist calendar date.
    BE year = AD year + 543; month and day remain the same.

    Note:
    - The datetime module uses the proleptic Gregorian calendar. Some BE years that
      correspond to Gregorian leap days (e.g., 2016-02-29 -> 2559-02-29) are not
      considered leap years under simple Gregorian divisibility rules when using the
      BE year number. In such cases, constructing the BE date is not representable
      and a ValueError is raised.
    """
    year_be = g_date.year + 543
    try:
        return date(year_be, g_date.month, g_date.day)
    except ValueError as e:
        raise ValueError(
            "The mapped Buddhist Era date is not representable with datetime.date "
            "(e.g., 29 February in a BE year that is not a leap year under the "
            "proleptic Gregorian rules)."
        ) from e

# Entry point: to_thai_buddhist_date(g_date: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_97_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_to_thai_buddhist_date(g_date):
    result = to_thai_buddhist_date(g_date)
    formatted_result = format_value_dt(result, g_date)
    log_file.write(formatted_result + "\n")
