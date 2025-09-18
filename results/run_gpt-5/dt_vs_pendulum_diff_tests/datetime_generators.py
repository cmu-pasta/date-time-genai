from datetime import date, datetime, timedelta

from hypothesis import strategies as st


@st.composite
def datetime_strategy(draw):
    # Generate a datetime within reasonable bounds
    dt = draw(
        st.datetimes(
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2100, 12, 31),
            # timezones=st.timezones(),
        )
    )
    return dt


@st.composite
def date_strategy(draw):
    # Generate a date within reasonable bounds
    dt_date = draw(st.dates(min_value=date(1900, 1, 1), max_value=date(2100, 12, 31)))
    return dt_date


@st.composite
def time_strategy(draw):
    # Generate a time
    dt_time = draw(st.times())
    return dt_time


@st.composite
def duration_strategy(draw):
    # Generate a timedelta
    days = draw(st.integers(min_value=0, max_value=365))
    hours = draw(st.integers(min_value=0, max_value=23))
    minutes = draw(st.integers(min_value=0, max_value=59))
    seconds = draw(st.integers(min_value=0, max_value=59))

    dt_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return dt_delta


@st.composite
def timestamp_strategy(draw):
    # Generate a datetime
    dt = draw(
        st.datetimes(min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    )
    # Convert to integer timestamp (seconds since epoch)
    ts_int = int(dt.timestamp())
    return ts_int


@st.composite
def string_strategy(draw):
    # Generate a string value.
    s = draw(st.text())
    return s


@st.composite
def bool_strategy(draw):
    # Generate a boolean value.
    b = draw(st.booleans())
    return b


@st.composite
def float_strategy(draw):
    # Generate a float value within a reasonable range.
    f = draw(
        st.floats(
            min_value=-1e10, max_value=1e10, allow_nan=False, allow_infinity=False
        )
    )
    return f


@st.composite
def int_strategy(draw):
    # Generate an integer value.
    i = draw(st.integers())
    return i
