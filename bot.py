# puppy_bot

import bsky_client
from bot_logger import log
import bot_config as config

import random
import os
from collections import namedtuple
from time import sleep
import argparse

parser = argparse.ArgumentParser('puppy_bot')
parser.add_argument(
    'username',
    help='the username of the bot account',
    metavar='-u',
    type=str
)
parser.add_argument(
    'password',
    help='the password of the bot account',
    metavar='-p',
    type=str
)
args = parser.parse_args()



User = namedtuple('User', 'username, password')


def authenticate_connection_to_bsky():
    user = User(args.username, args.password)
    profile = bsky_client.authenticate(user)

    return profile


def start_taskmaster(profile):
    print(f'taskmaster is running press [{config.CMD_ESC}] to stop...')
    log.info('taskmaster is running...')

    posts = bsky_client.query_feed(config.QUERY)
    posts = dedupe_query(posts)

    len_posts = len(posts)

    if len_posts < 10:
        print(f'...[{len_posts} is lower than min limit, enabling spam protection]...')
        sleep(900)

    bsky_client.send_post(profile, random.choice(config.LEXICON))

    counter = 0
    for post in posts:
        counter += 1

        print(f'...[{counter} of {len_posts}]...')

        bsky_client.like_post(post)
        sleep(15)
        bsky_client.repost_post(post)
        sleep(75)

    restart_taskmaster()


def restart_taskmaster():
    log.info(f'restarting [{config.APP_NAME}]...')
    print(f'restarting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


def cache_init():
    if not os.path.exists(config.CACHE_DIR):
        os.makedirs(config.CACHE_DIR)

    with open(config.CACHE_PATH, 'w') as cache:
        cache.write('')


def cache_dump(uris):
    if not os.path.exists(config.CACHE_PATH):
        cache_init()

    with open(config.CACHE_PATH, 'a+') as cache:
        for uri in uris:
            cache.write(f'{uri}\n')


def read_cache() -> list:
    cached_uris = []

    if not os.path.exists(config.CACHE_PATH):
        cache_init()

    with open(config.CACHE_PATH, 'r') as cache:
        cached_uris = cache.read().splitlines()

    return cached_uris


def dedupe_query(posts) -> list:
    cached_uris = read_cache()

    uncached_uris = []
    deduped_posts = []

    for post in posts:
        if post['uri'] in cached_uris:
            continue

        deduped_posts.append(post)
        uncached_uris.append(post['uri'])

    len_posts = len(posts)
    len_deduped = len(deduped_posts)

    if len_posts != len_deduped:
        print(f'{len_posts - len_deduped} posts were already cached...')

    print(f'working through {len_deduped}...')

    cache_dump(uncached_uris)

    return deduped_posts


def main():
    log.info(f'starting [{config.APP_NAME}]...')
    print(f'starting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


if __name__ == '__main__':
    main()
