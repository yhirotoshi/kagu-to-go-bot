import datetime
from flask import Flask, request, abort
import requests, json 
from slackclient import SlackClient
import pandas as pd
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
from IPython import embed
from settings import *
from Model import *


if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_access_token)
client = SlackClient(SLACK_API_TOKEN)

def _get_channel_id_from_list(user_id):
    channels = client.api_call("channels.list")
    channel_id = None
    for channel in channels['channels']:
        if user_id == channel['name']:
            channel_id = channel['id']
            break
    return channel_id

# def get_channel_id(user_id):
#     user_id = user_id[0:20].lower()
#     channel_id = _get_channel_id_from_list(user_id)
#     if channel_id:
#         return channel_id
#     else: 
#     # なかったら作ってからもう一回取得する
#     # TODO 作るのに失敗してる時の処理を書いていない
#         channel_id = _get_channel_id_from_list(user_id)
#         for invite_user in ['reply_deliver', 'Tai', 'Haru']:
#             client.api_call("channels.invite", channel=user_id, user=invite_user)
#         return channel_id

def get_channel_id(user_id):
    user_list = list(session.query(User).filter(User.uid==user_id))
    if len(user_list) > 0:
        return user_list[0].channel_id
    else: 
    # なかったら作ってからもう一回取得する
    # TODO 作るのに失敗してる時の処理を書いていない
        slack_id = user_id[0:20].lower()
        client.api_call("channels.create", channel=slack_id)

        user = User()
        user.uid = user_id
        user.slack_id = slack_id
        user.created_at = datetime.datetime.now()
        user.channel_id = channel_id
        session.add(user)
        session.commit()

        user_list = list(session.query(User).filter(User.uid==user_id))
        channel_id = user_list[0].channel_id
        for invite_user in ['reply_deliver', 'Tai', 'Haru']:
            client.api_call("channels.invite", channel=channel_id, user=invite_user)
        return channel_id


def logging_chat(event):
    if isinstance(event, PostbackEvent):
        message = event.postback.data
    else :
        message = event.message.text
    channel_id = get_channel_id(event.source.user_id)
    client.api_call(
      "chat.postMessage",
      channel=event.source.user_id[0:20].lower(),
      text=message,
      username='お客様'
    )

def logging_auto_response(event, response):
    # if isinstance(event, PostbackEvent):
    #     message = event.postback.data
    # else :
    #     message = event.message.text
    channel_id = get_channel_id(event.source.user_id)
    client.api_call(
      "chat.postMessage",
      channel=channel_id,
      text=response,
      username='KAGU TO GO 公式'
    )

def logging_user_image_upload(event):
    message_id = event.message.id
    channel_id = get_channel_id(event.source.user_id)
    param = {
    'token':SLACK_BOT_TOKEN, 
    'channels':channel_id,
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