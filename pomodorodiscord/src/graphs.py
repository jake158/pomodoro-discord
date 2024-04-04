import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Making sure you can run `python3 src/graphs.py`
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.utils import load_data


def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    date_range = [start_date + timedelta(days=x)
                  for x in range((end_date - start_date).days + 1)]
    return date_range


def fill_missing_dates(data, date_range):
    """Fill missing dates in data with zero values."""
    return [data.get(date.strftime("%Y-%m-%d"), 0) for date in date_range]


def graph_pomodoro_sessions(data):
    original_dates = list(data.get('sessions_by_date', {}).keys())

    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in original_dates]

    # Generate a complete date range
    date_range = generate_date_range(min(dates), max(dates))

    # Fill missing dates with zero sessions
    sessions = fill_missing_dates(data['sessions_by_date'], date_range)

    plt.figure(figsize=(12, 8))
    plt.bar(date_range, sessions, color='blue', alpha=0.5, width=1)

    plt.title('Pomodoro Sessions per Day')
    plt.xlabel('Days')
    plt.ylabel('Pomodoro Sessions')
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def graph_hours_studied(data):
    original_dates = list(data.get('seconds_by_date', {}).keys())

    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in original_dates]

    # Generate a complete date range
    date_range = generate_date_range(min(dates), max(dates))

    # Fill missing dates with zero hours
    hours = [seconds / 3600 for seconds in fill_missing_dates(data['seconds_by_date'], date_range)]

    plt.figure(figsize=(12, 8))
    plt.bar(date_range, hours, color='blue', alpha=0.5, width=1)

    plt.title('Hours Studied per Day')
    plt.xlabel('Days')
    plt.ylabel('Hours Studied')
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data = load_data()
    graph_pomodoro_sessions(data)
    graph_hours_studied(data)
