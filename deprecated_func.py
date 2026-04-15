# DO NOT USE - THIS IS FOR SAVING FUNCS FOR LATER

def query_feed(query):
    response = client.app.bsky.feed.search_posts({'q': query})
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