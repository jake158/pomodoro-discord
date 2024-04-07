import json
import os
import sys
from pygame import mixer


mixer.init()
beep = mixer.Sound('src/assets/sounds/beep.mp3')


DEF_POMODORO_MINS = 25
DEF_SB_MINS = 5
DEF_LB_MINS = 15
DEF_SB_BEFORE_L = 3

CONFIG_FILE = 'config.json'
DATA_FILE = 'data.json'
THEMES_DIR = 'src/assets/themes'


def load_file(filename, on_no_file=None):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return on_no_file
    return data


def load_data():
    return load_file(DATA_FILE, {'total_seconds_studied': 0,
                                 'total_pomodoro_sessions': 0,
                                 'seconds_by_date': {},
                                 'sessions_by_date': {}})


def save_data(data):
    with open(DATA_FILE, 'w') as data_file:
        json.dump(data, data_file, indent=4)


def load_config():
    return load_file(CONFIG_FILE, {'theme': 'Default',
                                   'sound': 'beep.mp3'})


def save_config(config):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)


def reload_app():
    os.execl(sys.executable, sys.executable, *sys.argv)
