import os
import sys
import subprocess

from flask import Flask, request, abort
import linebot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent,
    TextMessage, ImageMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, ConfirmTemplate,ImageCarouselTemplate, 
    MessageAction, URIAction, PostbackAction, DatetimePickerAction,
    CarouselColumn, ImageCarouselColumn, 
    )

from message import * 
from conditions import * 
from settings import *
from slack_webhook import *

app = Flask(__name__)
channel_secret='c44bcc1f07daafb3cb13ade4c4c1aeae'
channel_access_token='mmPNqkrq4bCggaF4krhhp3rt8db3jyvpF+yOZCmmNHvflOW8taBpXR+QfPvh/8eqGbg09PULrIYidJjRGZmsb/6tX4wXIWu6XOZqD9yrs85Bf4A9ZmkTsxgFcYlTiqck89BwaE9U62kVGB7S8jNTZwdB04t89/1O/w1cDnyilFU='
SLACK_WEBHOOK_URL='https://hooks.slack.com/services/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'
SLACK_BOT_TOKEN='xoxb-393549495281-394265761810-dvUhS7oi8FSaeDufKTmKC9RX'

# channel_access_token = '+NDrhB64UvIyD5jLS/M7+ebrdu4dClfhWnD+geE1k0hw6dDxpwGHz/XoD8LohJAI38Id7zWJoZFYb5IyOn2dMUGXr8dINH6277oV1z9OZjDCAGQbUTkCBySv3OHpHfMCjSfRDz+T6I+RDkIUTRszuAdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('signature error')
        abort(400)

    return 'OK'
  
@app.route("/callback", methods=['POST'])
def push_repy():

# handler
'''
フロー
TODO 後でまとめる
'''
@handler.add(FollowEvent)
def handle_follow(event):
    template_message = kagu_select_carousel()
    line_bot_api.reply_message(
        event.reply_token, template_message)

@handler.add(PostbackEvent)
def handle_postback(event):
    try:
        kagu_select_conditions(event)
        size_select_conditions(event)
        price_select_conditions(event)
        image_upload_conditions(event)
        image_add_conditions(event)
        room_style_select_conditions(event)
    except linebot.exceptions.LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == '家具を探す':
        template_message = kagu_select_carousel()
        line_bot_api.reply_message(
            event.reply_token, template_message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    confirm_message = confirm_image_add_flex_style()
    logging_auto_response(event, confirm_message.alt_text)
    line_bot_api.reply_message(event.reply_token, confirm_message)
    logging_user_image_upload(event) # 遅いので後ろに回す



if __name__ == "__main__":
    app.run() 
# handler
'''
フロー
TODO 後でまとめる
'''
# @handler.add(FollowEvent)
# def handle_follow(event):
#     confirm_message = room_style_select()
#     line_bot_api.reply_message(
#         event.reply_token, confirm_message)

# @handler.add(MessageEvent, message=TextMessage)
# def handle_text_message(event):
#     if event.message.text == '画像がある':
#         line_bot_api.reply_message(
#            event.reply_token, TextSendMessage(text='画像をお見せいただけますか？'))

#     elif event.message.text == '画像は特にない':
#         template_message = kagu_select_button()
#         line_bot_api.reply_message(
#             event.reply_token, template_message)

#     elif event.message.text == 'まだある':
#         line_bot_api.reply_message(
#            event.reply_token, TextSendMessage(text='画像をお見せいただけますか？'))
#     elif event.message.text == 'もう大丈夫':
#         template_message = kagu_select_button()
#         line_bot_api.reply_message(
#             event.reply_token, template_message)

#     elif event.message.text == '家具選択テスト':
#         template_message = kagu_select_carousel()
#         line_bot_api.reply_message(event.reply_token, template_message)
    
#     elif event.message.text == '部屋選択テスト':
#         template_message = room_style_select()
#         line_bot_api.reply_message(
#         event.reply_token, template_message)


# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image_message(event):
# 	confirm_message = confirm_image_add()
# 	line_bot_api.reply_message(event.reply_token, confirm_message)


# @handler.add(PostbackEvent)
# def handle_postback(event):
#     if event.postback.data == '家具の選択を終了':#['ダイニングテーブル','ベッド','ソファ']:
#         template_message = kakaku_select_button()
#         print(template_message)
#         line_bot_api.reply_message(
#             event.reply_token, template_message)

#     if event.postback.data == '予算の選択を終了':
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.'))

# if __name__ == "__main__":
#     app.run()