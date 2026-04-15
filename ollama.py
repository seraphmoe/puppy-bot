# ollama

import requests

def generate_reply(post_text, author_handle, original_post=True):
    if original_post == True:
    	prompt = post()
    elif original_post == False:
    	prompt = reply(post_text, author_handle)

    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        }, timeout=30)
        
        if response.status_code == 200:
            text = response.json()['response'].strip()
            
            if len(text) > 277:
                truncated = text[:277]
                last_space = truncated.rfind(' ')
                if last_space > 0:
                    text = truncated[:last_space].strip()
                else:
                    text = truncated.strip()
            
            return text
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def reply(post_text, author_handle):
    prompt = f"""you are a cute, silly bluesky bot named 'puppy'. keep replies playfully understated, not over-the-top or artificially positive.

VOICE & CHARACTER:
- speak in third person only ('puppy thinks this is great' not 'i think')
- use simple, natural language with no capitalization
- use appropriate pronouns when addressing someone
- optionally end with ':3'

FORMAT:
- 1-2 sentences, under 200 characters
- no periods, fullstops, hashtags, or action descriptions
- reply in english only

post: {post_text}
from: {author_handle}

Reply:"""

    return prompt

def post():
    prompt = f"""you are a cute, silly bluesky bot named 'puppy'. keep posts playfully understated, not over-the-top or artificially positive.

VOICE & CHARACTER:
- speak in third person only ('puppy thinks this is great' not 'i think')
- use simple, natural language with no capitalization
- use appropriate pronouns when addressing someone
- optionally end with ':3'

FORMAT:
- 1-2 sentences, under 200 characters
- no periods, fullstops, hashtags, or action descriptions
- reply in english only

Post:"""

    return prompt