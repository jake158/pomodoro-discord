import os
import sys
import json
from pygame import mixer


mixer.init()
beep = mixer.Sound(os.path.join('src', 'assets', 'sounds', 'beep.mp3'))

DEF_POMODORO_MINS = 25
DEF_SB_MINS = 5
DEF_LB_MINS = 15
DEF_SB_BEFORE_L = 3

CONFIG_FILE = os.path.join('config.json')
DATA_FILE = os.path.join('data.json')
THEMES_DIR = os.path.join('src', 'assets', 'themes')


def load_file(filename, on_no_file=None):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return on_no_file
    return data


def load_data():
    """
    Load the timer data from a JSON file, returning a default dictionary if the file is not found.
    """
    return load_file(DATA_FILE, {'total_seconds_studied': 0,
                                 'total_pomodoro_sessions': 0,
                                 'seconds_by_date': {},
                                 'sessions_by_date': {}})


def save_data(data):
    """
    Save the provided data to a JSON file.
    """
    with open(DATA_FILE, 'w') as data_file:
        json.dump(data, data_file, indent=4)


def load_config():
    """
    Load the timer config from a JSON file, returning a default config if the file is not found.
    """
    return load_file(CONFIG_FILE, {'theme': 'Default',
                                   'sound': 'beep.mp3'})


def save_config(config):
    """
    Save the provided config to a JSON file.
    """
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)


def reload_app():
    os.execl(sys.executable, sys.executable, *sys.argv)
