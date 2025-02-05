# bot_config

import os

script_path = os.path.dirname(os.path.abspath(__file__))

APP_NAME = 'puppy-bot'
CMD_ESC = 'Ctrl+C'

QUERY = 'puppy(girl|boy) art'

LEXICON = [
    'so puppy',
    'puppy',
    'wehhhh puppy',
    'puppy likes u',
    'puppy thinks that being silly is the meaning of life !',
    'haiiiii',
    'haihaiiiii :3',
    'puppy doesnt know many words wehhh',
    'puppy doesnt have a brain',
    'wehhhh, puppy is hungry,,,',
    'haiiiii ! puppy wants to go on an adventure~',
    'bellyrubs and headpats,,,,,',
    'wagwagwag',
    'puppy is convinced it can fly if it flaps its ears hard enough'
]

CACHE_DIR = f'{script_path}/.cache'
CACHE_PATH = f'{CACHE_DIR}/{APP_NAME}.data'
