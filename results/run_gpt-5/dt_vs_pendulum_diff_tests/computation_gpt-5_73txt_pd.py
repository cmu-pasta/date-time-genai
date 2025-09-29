
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def is_within_business_hours(moment: pendulum.DateTime) -> bool:
    """
    Determine if the given moment falls within business hours.
    Business hours are defined as [09:00, 17:00) on the same day and timezone.
    
    Args:
        moment (pendulum.DateTime): The datetime to evaluate.
        
    Returns:
        bool: True if within business hours, False otherwise.
    """
    # Define the start (inclusive) and end (exclusive) of business hours on the same day and timezone
    start = moment.replace(hour=9, minute=0, second=0, microsecond=0)
    end = moment.replace(hour=17, minute=0, second=0, microsecond=0)

    return start <= moment < end

# Entry point: is_within_business_hours(moment: pendulum.DateTime) -> bool

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_73txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_is_within_business_hours(moment):
    result = is_within_business_hours(moment)
    formatted_result = format_value_pd(result, moment)
    log_file.write(formatted_result + "\n")
