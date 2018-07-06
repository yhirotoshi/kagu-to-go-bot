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

WEB_HOOK_URL = os.environ['SLACK_URL']

def send_chat(event):
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": event.message.text + '\nfrom ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        )
    )

def send_set_response(event, response)
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": response + '\nto ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        )
    )

def send_auto_response(event, response)
    requests.post(WEB_HOOK_URL, data = json.dumps(
        {
        "text": response + '\nto ' + event.source.userId,
        # "channel": "#incoming-test",
        "username": event.source.userId,
        'link_names': 1, 
        }
        )
    )

def send_push_response(response):
    