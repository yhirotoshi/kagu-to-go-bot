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
SLACK_BOT_TOKEN="xoxb-393549495281-394265761810-dvUhS7oi8FSaeDufKTmKC9RX"
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
    print(SLACK_BOT_TOKEN)
    param = {
    'token':SLACK_BOT_TOKEN, 
    'channels':'CBL74MZA9',
    'filename':event.source.user_id,
    'initial_comment': "部屋のイメージ uploaded by " + event.source.user_id,
    'title': "部屋のイメージ"
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