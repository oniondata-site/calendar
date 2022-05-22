import os
import json


config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './config.json'))
local_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './local_config.json'))
config_dict = None


def load():
    global config_dict

    with open(config_file) as f:
        config_dict = json.load(f)

    # local config
    if os.path.exists(local_config_file):
        with open(local_config_file) as f:
            config_dict.update(json.load(f))


def get(key, default_value=None):
    if config_dict is None:
        load()

    if key in config_dict:
        return config_dict[key]

    return default_value


def set(key, value):
    if config_dict is None:
        load()

    config_dict[key] = value


def save():
    if config_dict is None:
        return

    with open(config_file, 'w') as f:
        json.dump(config_dict, f, indent=4)
