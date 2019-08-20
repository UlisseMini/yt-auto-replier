# -*- coding: utf-8 -*-

import json
import googleapiclient.discovery
import sys
from iterencoder import IterEncoder

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = # Put your developer key here

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Return an iterator over the comments of a youtube video.
def comments(videoId):
    next_page_token = ''
    while True:
        request = youtube.commentThreads().list(
            part = 'snippet',
            maxResults = 100,
            videoId = videoId,
            pageToken = next_page_token,
        )
        response = request.execute()
        for item in response['items']:
            yield item

        next_page_token = response.get('nextPageToken')

        if not next_page_token: break

def status(iterator):
    n = 0
    for item in iterator:
        n += 1
        eprint(f'\rDownloaded {n} comments to comments.json', end = '')
        yield item
    eprint()

if __name__ == '__main__':
    with open('comments.json', 'w') as f:
        items = status(map(lambda s: comments(s.rstrip()), sys.stdin))
        json.dump(items, f, cls=IterEncoder)
