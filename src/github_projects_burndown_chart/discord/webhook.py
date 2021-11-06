import requests

from config import secrets

def post_burndown_chart(chart_path):
    requests.post(
        secrets['discord_webhook'],
        json={'content': "Today's Burndown Chart"}
    )
    requests.post(
        secrets['discord_webhook'],
        files={'file': open(chart_path, 'rb')},
    )