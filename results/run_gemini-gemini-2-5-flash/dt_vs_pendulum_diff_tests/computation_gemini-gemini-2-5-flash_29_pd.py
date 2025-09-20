
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_thanksgiving_date(year: int) -> pendulum.Date:
    # Step 1: Get the first day of November for the given year.
    november_first = pendulum.datetime(year, 11, 1)

    # Step 2: Find the first Thursday on or after November 1st.
    # pendulum.next(pendulum.THURSDAY) will return november_first itself if it's a Thursday,
    # or the next Thursday otherwise.
    first_thursday_of_november = november_first.next(pendulum.THURSDAY)

    # Step 3: Thanksgiving is the fourth Thursday. To get from the first to the fourth,
    # we need to add 3 more weeks (3 * 7 = 21 days).
    thanksgiving_date_time = first_thursday_of_november.add(days=21)

    # Step 4: Return the result as a pendulum.Date object.
    return thanksgiving_date_time.date()

# Entry point: find_thanksgiving_date(year: int) -> pendulum.Date

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_29_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
