
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
from astral import LocationInfo, Observer, sun
def calculate_sunset_time(
    date: pendulum.Date,
    latitude: float,
    longitude: float
) -> pendulum.Time:
    """
    Calculates the sunset time for a given date and geographic coordinates.

    Args:
        date: The date for which to calculate the sunset.
        latitude: The latitude of the location (e.g., 34.05 for Los Angeles).
        longitude: The longitude of the location (e.g., -118.25 for Los Angeles).

    Returns:
        A pendulum.Time object representing the sunset time.
    """
    # Step 1: Create an astral.Observer object with the given coordinates.
    # While astral.LocationInfo can be used, Observer directly takes lat/lon.
    observer = Observer(latitude=latitude, longitude=longitude)

    # Step 2: Get solar events for the specified date.
    # The astral library works with standard datetime objects for date input.
    # We convert pendulum.Date to a standard datetime.date object.
    solar_events = sun(observer, date=date.to_datetime_date())

    # Step 3: Extract the sunset time.
    # astral returns datetime.datetime objects.
    sunset_dt = solar_events['sunset']

    # Step 4: Convert the datetime.datetime sunset time to a pendulum.Time object.
    # pendulum.Time represents a time-of-day without date or timezone.
    sunset_pendulum_time = pendulum.time(
        hour=sunset_dt.hour,
        minute=sunset_dt.minute,
        second=sunset_dt.second,
        microsecond=sunset_dt.microsecond
    )
    
    # Step 5: Return the pendulum.Time object.
    return sunset_pendulum_time

# Entry point: calculate_sunset_time(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.Time

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_84_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_sunset_time(date, latitude, longitude):
    result = calculate_sunset_time(date, latitude, longitude)
    formatted_result = format_value_pd(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
