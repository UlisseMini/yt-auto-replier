import json
import random

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "auth.json"

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


replies = [
    "walnut*",
    "you mean walnut*",
    "uncultured swine, her name is walnut",
    "fuck you, their name is walnut",
    "they're not beanos, they're walnut",
    "who? i only know our lord and saviour walnut.",
    "please go jump into a fire, their name is walnut",
    "you make me want to kill myself, their name is walnut walnut. our lord and saviour. all shall bow down to our god",
]

with open('./comments.json') as f:
    comments = json.load(f)

# reply to a comment with a random response out of replies
def reply(comment_id, text):
    request = youtube.comments().insert(
        part = 'snippet',
        body = {
            'snippet': {
                "parentId": str(comment_id),
                "textOriginal": text,
            },
        },
    )
    response = request.execute()
    print(response)

for item in comments:
    snippet = item['snippet']
    comment = snippet['topLevelComment']
    comment_snip = comment['snippet']
    author = comment_snip["authorDisplayName"]
    text = comment_snip['textOriginal']
    if 'eanos' in text.lower():
        print(f'{author} is a sinner')
        reply_text = random.choice(replies)
        reply(comment['id'], reply_text)
        print(f'{author} has been smote')
