import os
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Making sure you can run `python3 src/graphs.py`
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.utils import load_data


def graph_pomodoro_sessions(data):
    dates = list(data.get('sessions_by_date', {}).keys())
    sessions = list(data.get('sessions_by_date', {}).values())

    plt.figure(figsize=(12, 8))
    plt.bar(dates, sessions, color='blue', alpha=0.5, width=1)

    plt.title('Pomodoro Sessions per Day')
    plt.xlabel('Days')
    plt.ylabel('Pomodoro Sessions')

    # Format x-axis to display dates properly
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(20))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def graph_hours_studied(data):
    dates = list(data.get('seconds_by_date', {}).keys())
    seconds = list(data.get('seconds_by_date', {}).values())
    hours = [s / 3600 for s in seconds]

    plt.figure(figsize=(12, 8))
    plt.bar(dates, hours, color='blue', alpha=0.5, width=1)

    plt.title('Hours Studied per Day')
    plt.xlabel('Days')
    plt.ylabel('Hours Studied')

    # Format x-axis to display dates properly
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(20))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data = load_data()
    graph_pomodoro_sessions(data)
    graph_hours_studied(data)
