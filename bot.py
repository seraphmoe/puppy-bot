# puppy_bot

import bsky_client
from bot_logger import log
import bot_config as config
import data_handler
import ollama

import random
from collections import namedtuple
from time import sleep
import argparse
import random

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
    replied_posts = data_handler.load_post_data()

    reply_to_notifications(replied_posts=replied_posts, profile=profile)

    reply_to_followers(replied_posts=replied_posts, profile=profile)

    if random.random() < 0.02:
        post_text = ollama.generate_reply(
            post_text='', 
            author_handle='',
            original_post=True
        )

        bsky_client.send_post(
            profile=profile, 
            post_text=post_text
        )

    sleep(270)

    restart_taskmaster()


def reply_to_followers(replied_posts, profile):
    if not profile:
        return

    followers = bsky_client.get_followers(profile)
    for follower in followers:
        try: # TODO: get rid of this ugly shit
            original_posts = bsky_client.get_original_posts(
                replied_posts,
                follower.handle, 
                limit=10
            )

            for original_post in original_posts:
                text = ollama.generate_reply(
                    post_text=original_post.record.text, 
                    author_handle=original_post.author.display_name,
                    original_post=False
                )

                reply_ref = bsky_client.create_reply_ref(original_post=original_post)

                bsky_client.like_post(
                    uri=original_post.uri, cid=original_post.cid
                )

                bsky_client.send_reply(
                    text=text,
                    reply_ref=reply_ref
                )

                replied_posts.append(original_post.uri)
                data_handler.save_post_data(replied_posts)
                
        except Exception as e:
            print(f"error processing {follower.handle}: {e}")

        sleep(15)


def reply_to_notifications(replied_posts, profile):
    notifications = bsky_client.get_notifications()
    all_notes = notifications.notifications
    sample_notes = all_notes[:10]
    for note in sample_notes:
        if note.reason == 'reply':
            if note.uri in replied_posts:
                continue

            print(f"replying to {note.uri}")

            text = ollama.generate_reply(
                post_text=note.record.text, 
                author_handle=note.author.display_name,
                original_post=False
            )

            reply_ref = bsky_client.create_reply_ref(original_post=note)

            bsky_client.like_post(
                uri=note.uri, cid=note.cid
            )

            bsky_client.send_reply(
                text=text,
                reply_ref=reply_ref
            )

            replied_posts.append(note.uri)
            data_handler.save_post_data(replied_posts)

        sleep(15)


def restart_taskmaster():
    log.info(f'restarting [{config.APP_NAME}]...')
    print(f'restarting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


def main():
    log.info(f'starting [{config.APP_NAME}]...')
    print(f'starting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


if __name__ == '__main__':
    main()
