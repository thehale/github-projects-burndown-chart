import requests
from slack_sdk import WebClient

from config import secrets


def post_burndown_chart(chart_path):
    client = WebClient(secrets["slack_bot_token"])  
    new_file = client.files_upload(
        channels="#burndown",
        title="Today's Awan Burndown Chart - Auto generated from Imad's PC",
        file=open(chart_path, 'rb'),
    )
