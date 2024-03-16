import matplotlib.pyplot as plt
from utils import load_data


def graph_pomodoro_sessions(data):
    dates = list(data.get('sessions_by_date', {}).keys())
    sessions = list(data.get('sessions_by_date', {}).values())
    print(sessions)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, sessions, marker='o')
    plt.title('Pomodoro Sessions per Day')
    plt.xlabel('Days')
    plt.ylabel('Pomodoro Sessions')
    plt.xticks(rotation=45)
    plt.yticks(sessions)
    plt.tight_layout()
    plt.show()

def graph_hours_studied(data):
    dates = list(data.get('seconds_by_date', {}).keys())
    seconds = list(data.get('seconds_by_date', {}).values())
    hours = [s / 3600 for s in seconds]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, hours, marker='o', color='red')
    plt.title('Hours Studied per Day')
    plt.xlabel('Days')
    plt.ylabel('Hours Studied')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    data = load_data()
    graph_pomodoro_sessions(data)
    graph_hours_studied(data)
