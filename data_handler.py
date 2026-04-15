# data handler

import json
from pathlib import Path

import bot_config as config



def load_post_data():
    if Path(config.DATA_FILE).exists():
        with open(config.DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_post_data(posts):
    with open(config.DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)
