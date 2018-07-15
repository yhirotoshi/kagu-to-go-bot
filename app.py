import os
import sys
import subprocess

from flask import Flask, request, abort
import linebot # 1.7.2じゃないとバグるから注意
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent,
    TextMessage, ImageMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, ConfirmTemplate,ImageCarouselTemplate, 
    MessageAction, URIAction, PostbackAction, DatetimePickerAction,
    CarouselColumn, ImageCarouselColumn, 
    )
from IPython import embed

from settings import *
from message import * 
from conditions import * 
from slack_webhook import *
app = Flask(__name__)
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
  
@app.route("/push_reply", methods=['POST'])
def push_reply():
    body = json.loads(request.get_data(as_text=True))
    channel_id = body['channel_id']
    user = list(session.query(User).filter(User.channel_id==channel_id))[0]
    to = user.uid
    text = body['text']
    line_bot_api.push_message(to, TextSendMessage(text=text))

@handler.add(FollowEvent)
def handle_follow(event):
    template_message = kagu_select_carousel()
    logging_auto_response(event, template_message.alt_text)
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

from slackeventsapi import SlackEventAdapter
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events", app)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event):
  emoji = event.get("reaction")
  print(emoji)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=5000)
