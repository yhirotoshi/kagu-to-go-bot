from flask import Flask, request, abort
import requests, json 
import linebot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, FollowEvent,
    TextMessage, TextSendMessage, TemplateSendMessage, FlexSendMessage,
    ButtonsTemplate, ConfirmTemplate,CarouselTemplate, ImageCarouselTemplate,
    MessageAction, URIAction, PostbackAction, DatetimePickerAction,
    CarouselColumn,ImageCarouselColumn,
    BubbleContainer, 
    ImageComponent, BoxComponent, TextComponent, IconComponent, SeparatorComponent, SpacerComponent,
    ButtonComponent,BubbleStyle, BlockStyle
    )
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

line_bot_api = LineBotApi(channel_secret)

WEB_HOOK_URL = os.environ['SLACK_URL']

WEB_HOOK_URL = ''
def logging_chat(event):
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": event.message.text + '\nfrom ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        )
    )


def logging_auto_response(event, response)
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": response + '\nto ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        )
    )

def logging_user_image_upload(event):
    message_id = event.message.id
    file = line_bot_api.get_message_content(message_id, )
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": response + '\nto ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        ),
    files=files
    )
'''
https://api.line.me/v2/bot/message/{messageId}/content
'''
# def logging_push_response(response):
'''
PUSH APiを使うときに使う
'''