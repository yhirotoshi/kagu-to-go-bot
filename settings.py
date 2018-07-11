import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
WEB_HOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_BOT_TOKEN=os.environ.get('SLACK_BOT_TOKEN')
SLACK_API_TOKEN=os.environ.get('SLACK_API_TOKEN')