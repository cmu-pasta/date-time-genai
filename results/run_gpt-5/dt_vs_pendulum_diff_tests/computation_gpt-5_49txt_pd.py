
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_sundays_in_february(year: int) -> int:
    # Step 1: Create a Pendulum Date for February 1st of the given year
    feb_first = pendulum.date(year, 2, 1)
    
    # Step 2: Get number of days in February for the given year
    days_in_feb = feb_first.days_in_month  # 28 or 29 depending on leap year
    
    # Step 3: Compute offset to the first Sunday in February
    # pendulum day_of_week: Monday=0 ... Sunday=6
    offset_to_sunday = (pendulum.SUNDAY - feb_first.day_of_week) % 7
    first_sunday_day = 1 + offset_to_sunday  # Day number within February
    
    # Step 4: Count Sundays: first Sunday plus every 7th day within the month
    count = 0
    if first_sunday_day <= days_in_feb:
        count = 1 + (days_in_feb - first_sunday_day) // 7
    
    # Step 5: Return the count as an integer
    return int(count)

# Entry point: count_sundays_in_february(year: int) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_49txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
