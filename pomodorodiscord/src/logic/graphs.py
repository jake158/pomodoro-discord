import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Making sure you can run `python3 src/logic/graphs.py`
current_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(src)

from src.utils import load_data


def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    date_range = [start_date + timedelta(days=x)
                  for x in range((end_date - start_date).days + 1)]
    return date_range


def fill_missing_dates(data, date_range):
    """Fill missing dates in data with zero values."""
    return [data.get(date.strftime("%Y-%m-%d"), 0) for date in date_range]


def adjust_date_ticks(ax, dates):
    """Adjust the x-axis to display a limited number of date labels."""
    num_days = (max(dates) - min(dates)).days + 1
    interval = max(1, num_days // 20)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)


def graph_pomodoro_sessions(data):
    original_dates = list(data.get('sessions_by_date', {}).keys())
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in original_dates]
    date_range = generate_date_range(min(dates), max(dates))
    sessions = fill_missing_dates(data['sessions_by_date'], date_range)

    plt.figure(figsize=(12, 8))
    plt.bar(date_range, sessions, color='blue', alpha=0.5, width=1)
    plt.title('Pomodoro Sessions per Day')
    plt.xlabel('Days')
    plt.ylabel('Pomodoro Sessions')

    ax = plt.gca()
    adjust_date_ticks(ax, date_range)
    plt.tight_layout()
    plt.show()


def graph_hours_studied(data):
    original_dates = list(data.get('seconds_by_date', {}).keys())
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in original_dates]
    date_range = generate_date_range(min(dates), max(dates))
    hours = [seconds / 3600 for seconds in fill_missing_dates(data['seconds_by_date'], date_range)]

    plt.figure(figsize=(12, 8))
    plt.bar(date_range, hours, color='blue', alpha=0.5, width=1)
    plt.title('Hours Studied per Day')
    plt.xlabel('Days')
    plt.ylabel('Hours Studied')

    ax = plt.gca()
    adjust_date_ticks(ax, date_range)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data = load_data()
    graph_pomodoro_sessions(data)
    graph_hours_studied(data)
