import os
import sys

from flask import Flask, request, abort
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

from message import * 
from settings import * 
from slack_webhook import *
# channel_access_token = '+NDrhB64UvIyD5jLS/M7+ebrdu4dClfhWnD+geE1k0hw6dDxpwGHz/XoD8LohJAI38Id7zWJoZFYb5IyOn2dMUGXr8dINH6277oV1z9OZjDCAGQbUTkCBySv3OHpHfMCjSfRDz+T6I+RDkIUTRszuAdB04t89/1O/w1cDnyilFU='

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_access_token)

def kagu_select_conditions(event):
    if event.postback.data == 'ベッドを探す':
        logging_chat(event)
        message = bed_size_check_flex_style()
        logging_auto_response(event, message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, message)

    if event.postback.data == 'ダイニングテーブルを探す':
        logging_chat(event)
        message = diningtable_size_check_flex_style()
        logging_auto_response(event, message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, message)

    if event.postback.data == 'ソファを探す':
        logging_chat(event)
        message = sofa_size_check_flex_style()
        logging_auto_response(event, message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, message)

    if event.postback.data == 'チェアを探す':
        logging_chat(event)
        message = isu_price_select_flex_style()
        logging_auto_response(event, message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, message)

    if event.postback.data == 'ざっくり相談する':
        logging_chat(event)
        message = confirm_room_style()
        logging_auto_response(event, message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, message)

def size_select_conditions(event):
    if event.postback.data in ['シングル','セミダブル','ダブル','2人用', '4人用','6人用','1人用', '3人用','それ以上']:
        logging_chat(event)
        confirm_message = price_select_flex_style()
        logging_auto_response(event, confirm_message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, confirm_message)


def price_select_conditions(event):
    if event.postback.data in ['~1万円','1~2万円','2~3万円','3~5万円', '1~3万円','3~5万円','5~10万円', '10万円~',]:
        logging_chat(event)
        confirm_message = confirm_room_style_flex_style()
        logging_auto_response(event, confirm_message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, confirm_message)


def image_upload_conditions(event):
    if event.postback.data in ['部屋の写真がある', '家具のイメージ写真がある']:
        logging_chat(event)
        logging_auto_response(event, '画像をお見せいただけますか？')
        line_bot_api.reply_message(
          event.reply_token, TextSendMessage(text='画像をお見せいただけますか？'))
    elif event.postback.data == '選択肢から選ぶ':
        logging_chat(event)
        confirm_message = room_style_select()
        logging_auto_response(event, confirm_message.alt_text)
        line_bot_api.reply_message(
            event.reply_token, confirm_message)
    elif event.postback.data == '特にない':
        logging_chat(event)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))

def image_add_conditions(event):
    if event.postback.data == 'まだある':
        logging_chat(event)
        logging_auto_response(event, '画像をお送りください')
        line_bot_api.reply_message(
           event.reply_token, TextSendMessage(text='画像をお送りください'))
    
    elif event.postback.data == 'もう大丈夫':
        logging_chat(event)
        logging_auto_response(event, '入力お疲れ様でした~~~')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))

def room_style_select_conditions(event):
    if event.postback.data in ['ナチュラル・北欧スタイル', 'カジュアルスタイル', 'モダンスタイル']:
        logging_chat(event)
        logging_auto_response(event, '入力お疲れ様でした~~~')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))
