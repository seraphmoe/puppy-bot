# setup client for bsky bot

from time import gmtime, strftime, sleep

from bot_logger import log
from atproto import Client, IdResolver


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


def query_feed(query):
    response = client.app.bsky.feed.search_posts(
        {
            'q': query,
            'sort': 'latest'
        }
    )

    feed = response.posts

    posts = []
    for post in feed:
        posts.append(
            {
                'did': post.author.did,
                'handle': post.author.handle,
                'uri': post.uri,
                'cid': post.cid,
                'text': post.record.text
            }
        )

    print(f'collected {len(posts)} posts...')
    return posts


def like_post(post):
    cid = post['cid']
    uri = post['uri']

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
