
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_presidents_day(year: int) -> pendulum.Date:
    # Step 1: Create a pendulum.Date object for February 1st of the given year.
    february_first = pendulum.date(year, 2, 1)

    # Step 2: Find the first Monday on or after February 1st.
    # If February 1st is a Monday, .next(pendulum.MONDAY) will return February 1st.
    # Otherwise, it will return the first Monday after February 1st.
    first_monday_of_february = february_first.next(pendulum.MONDAY)

    # Step 3: Add two weeks (14 days) to get the third Monday of February.
    presidents_day = first_monday_of_february.add(weeks=2)

    # Step 4: Return the calculated date.
    return presidents_day

# Entry point: find_presidents_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_86_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
