from flask import Flask, request, abort
import requests, json 
import linebot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, FollowEvent,PostbackEvent, 
    TextMessage, TextSendMessage, TemplateSendMessage, FlexSendMessage,
    ButtonsTemplate, ConfirmTemplate,CarouselTemplate, ImageCarouselTemplate,
    MessageAction, URIAction, PostbackAction, DatetimePickerAction,
    CarouselColumn,ImageCarouselColumn,
    BubbleContainer, 
    ImageComponent, BoxComponent, TextComponent, IconComponent, SeparatorComponent, SpacerComponent,
    ButtonComponent,BubbleStyle, BlockStyle
    )
from settings import *
channel_access_token = '+NDrhB64UvIyD5jLS/M7+ebrdu4dClfhWnD+geE1k0hw6dDxpwGHz/XoD8LohJAI38Id7zWJoZFYb5IyOn2dMUGXr8dINH6277oV1z9OZjDCAGQbUTkCBySv3OHpHfMCjSfRDz+T6I+RDkIUTRszuAdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(channel_access_token)



def logging_chat(event):
    if isinstance(event, PostbackEvent):
        message = event.postback.data
    else :
        message = event.message.text
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": message + '\nfrom ' + event.source.user_id,
        # "channel": "#incoming-test",
        "username": event.source.user_id,
        'link_names': 1, 
        }
        )
    )


def logging_auto_response(event, response):
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": response + '\nto ' + event.source.user_id,
        # "channel": "#incoming-test",
        "username": event.source.user_id,
        'link_names': 1, 
        }
        )
    )

def logging_user_image_upload(event):
    message_id = event.message.id
    print(type(line_bot_api.get_message_content(message_id)).content)
    param = {
    'token':SLACK_BOT_TOKEN, 
    'channels':'CBL74MZA9',
    'filename':"image",
    'initial_comment': "initial_comment",
    'title': "title"
    }

    files = {'file': line_bot_api.get_message_content(message_id).content}
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)
'''
https://api.line.me/v2/bot/message/{messageId}/content
'''
# def logging_push_response(response):
'''
PUSH APiを使うときに使う
'''