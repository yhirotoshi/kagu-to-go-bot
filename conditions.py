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

channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_secret)

def kagu_select_conditions(event):
    if event.postback.data == 'ベッドを探す':
        send_chat(event)
        template_message = bed_size_check_flex_style()
        line_bot_api.reply_message(
            event.reply_token, template_message)

    if event.postback.data == 'ダイニングテーブルを探す':
        send_chat(event)
        template_message = diningtable_size_check_flex_style()
        line_bot_api.reply_message(
            event.reply_token, template_message)

    if event.postback.data == 'ソファを探す':
        send_chat(event)
        template_message = sofa_size_check_flex_style()
        line_bot_api.reply_message(
            event.reply_token, template_message)

    if event.postback.data == 'チェアを探す':
        send_chat(event)
        template_message = isu_price_select_flex_style()
        line_bot_api.reply_message(
            event.reply_token, template_message)

    if event.postback.data == 'ざっくり相談する':
        send_chat(event)
        template_message = confirm_room_style()
        line_bot_api.reply_message(
            event.reply_token, template_message)

def size_select_conditions(event):
    if event.postback.data in ['シングル','セミダブル','ダブル','2人用', '4人用','6人用','1人用', '3人用','それ以上']:
        send_chat(event)
        confirm_message = price_select_flex_style()
        line_bot_api.reply_message(
            event.reply_token, confirm_message)


def price_select_conditions(event):
    if event.postback.data in ['~1万円','1~2万円','2~3万円','3~5万円', '1~3万円','3~5万円','5~10万円', '10万円~',]:
        send_chat(event)
        confirm_message = confirm_room_style_flex_style()
        line_bot_api.reply_message(
            event.reply_token, confirm_message)


def image_upload_conditions(event):
    if event.postback.data in ['部屋の写真がある', '家具のイメージ写真がある']:
        send_chat(event)
         line_bot_api.reply_message(
           event.reply_token, TextSendMessage(text='画像をお見せいただけますか？'))
    elif event.postback.data == '選択肢から選ぶ':
        send_chat(event)
        confirm_message = room_style_select()
        line_bot_api.reply_message(
            event.reply_token, confirm_message)
    elif event.postback.data == '特にない':
        send_chat(event)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))

def image_add_conditions(event):
    if event.postback.data == 'まだある':
        send_chat(event)
        line_bot_api.reply_message(
           event.reply_token, TextSendMessage(text='画像をお送りください'))
    
    elif event.postback.data == 'もう大丈夫':
        send_chat(event)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))

def room_style_select_conditions(event):
    if event.postback.data in ['ナチュラル・北欧スタイル', 'カジュアルスタイル', 'モダンスタイル']:
        send_chat(event)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='入力お疲れ様でした. \nコンシェルジュがお客様にぴったりな家具をお探ししますので少々お待ち下さい.\n何か他にご要望ございましたらご自由にお申し付けください.'))
