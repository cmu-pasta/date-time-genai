
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_mlk_day(year: int) -> pendulum.Date:
    # Step 1: Get the first day of January for the given year.
    jan_first = pendulum.date(year, 1, 1)

    # Step 2: Calculate the number of days to add to reach the first Monday.
    # pendulum.MONDAY is 0, TUESDAY is 1, ..., SUNDAY is 6.
    # (pendulum.MONDAY - jan_first.day_of_week + 7) % 7 ensures a positive offset
    # that correctly shifts to the next Monday if jan_first is not Monday,
    # or stays at jan_first if it is Monday.
    days_to_add_for_first_monday = (pendulum.MONDAY - jan_first.day_of_week + 7) % 7

    # Step 3: Find the date of the first Monday in January.
    first_monday_jan = jan_first.add(days=days_to_add_for_first_monday)

    # Step 4: Martin Luther King Jr. Day is the third Monday.
    # Add two more weeks (14 days) to get to the third Monday.
    mlk_day = first_monday_jan.add(weeks=2)

    # Step 5: Return the calculated date.
    return mlk_day

# Entry point: find_mlk_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_92_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_mlk_day(year):
    result = find_mlk_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
