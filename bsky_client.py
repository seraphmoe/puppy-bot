# setup client for bsky bot

from time import gmtime, strftime, sleep

from bot_logger import log
from atproto import Client, IdResolver, models
from ollama import generate_reply
import random
import bot_config as config


client = Client()
resolver = IdResolver()


def authenticate(user):
    profile = None

    try:
        log.info('connecting to bsky...')
        profile = client.login(user.username, user.password)

    except Exception as e:
        log.info(e)
        log.info('failed to connect...')

    return profile


def resolve_handle(handle):
    did = resolver.handle.resolve(handle)
    did_doc = resolver.did.resolve(did)
    return did

def send_post(profile, post_text):
    current_date = strftime('%B %d, %Y', gmtime())
    current_time = strftime('%I:%M %p', gmtime())

    post = client.send_post(post_text)

    post_info = f'''
        posted as {profile.display_name}
        {current_date} at {current_time}

        uri: {post.uri}
        cid: {post.cid}
    '''

    log.info(post_info)
    print(post_info)

    return post


def send_reply(text, reply_ref):
    client.send_post(
        text=text,
        reply_to=reply_ref
    )


def get_original_posts(replied_posts, handle, limit=10):
    posts = client.get_author_feed(
        actor=handle, 
        limit=limit,
        filter='posts_no_replies'
    )

    original_posts = []
    if posts.feed:
        original_post = None
        for post in posts.feed:
            if post.post.uri not in replied_posts:
                original_post = post.post
                break
            else:
                print(f'already found post {post.post.uri}, skipping...')
        
        if not original_post:
            print("no post found")
            return []

        py_type = ''

        # if not hasattr(original_post, 'embed'):
        #     print('go fuck urself')
        #     py_type = 'repost'

        # if not hasattr(original_post.embed, 'py_type'):
        #     print('also go fuck urself')
        #     py_type = 'repost'

        try: # TODO: change this to hasattr()
            py_type = original_post.embed.py_type
        except:
            py_type = 'repost'

        if py_type == 'app.bsky.embed.record#view':
            print(f'original post (non-repost) from {original_post.author.handle}')
            original_posts.append(original_post)

    return original_posts


def get_notifications():
    notifications = client.app.bsky.notification.list_notifications()
    return notifications


def create_reply_ref(original_post):
    reply_ref = models.app.bsky.feed.post.ReplyRef(
        root=models.ComAtprotoRepoStrongRef.Main(
            uri=original_post.uri,
            cid=original_post.cid
        ),
        parent=models.ComAtprotoRepoStrongRef.Main(
            uri=original_post.uri,
            cid=original_post.cid
        )
    )
    return reply_ref


def like_post(uri, cid):
    try:
        uri = client.like(uri=uri, cid=cid).uri
    except Exception as e:
        log.info(e)

    print(f'liked {uri}')
    return uri


def repost_post(post):
    cid = post['cid']
    uri = post['uri']

    try:
        uri = client.repost(uri=uri, cid=cid).uri
    except Exception as e:
        log.info(e)

    print(f'reposted {uri}')
    return uri


def get_followers(profile):
    client_followers = client.get_followers(actor=profile.did, limit=50)
    followers = client_followers.followers
    followers = random.sample(followers, 20)

    return followers
