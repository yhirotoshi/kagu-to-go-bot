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

from button_templates import *
from settings import *


def kagu_select_carousel():
    image_action_list = [
    ('ベッドを探す', 'https://c1.staticflickr.com/9/8036/8021698960_f5ed81eb20.jpg'),
    ('ソファを探す', 'https://c1.staticflickr.com/3/2132/2188019418_7b1c9db4e1.jpg'),
    ('ダイニングテーブルを探す', 'https://c2.staticflickr.com/4/3014/2805553009_db32284691.jpg'), 
    ('チェアを探す', 'https://www.westelm.com/weimgs/ab/images/wcm/products/201824/0074/classic-cafe-upholstered-dining-chair-c.jpg'),
    ('ざっくり相談する', 'https://c1.staticflickr.com/5/4030/4305286550_c6be5e8cd0_o.jpg'),
    ]
    image_carousel_template = image_carousel_generater(image_action_list, )
    template_message = TemplateSendMessage(
            alt_text='検討している家具を教えてください', template=image_carousel_template)
    return template_message


def room_style_select():# todo
    image_action_list = [
    ('ナチュラル・北欧スタイル', 'https://c1.staticflickr.com/9/8207/8229127955_4b4a7621ba.jpg'),
    ('カジュアルスタイル', 'https://c2.staticflickr.com/4/3293/2916794464_f96404201b.jpg'), 
    ('モダンスタイル', 'https://c1.staticflickr.com/5/4403/36522135820_e7a371387c.jpg'),
    ]
    image_carousel_template = image_carousel_generater(image_action_list, )
    template_message = TemplateSendMessage(
            alt_text='イメージに近いスタイルを選択してください', template=image_carousel_template)
    return template_message


def bed_size_check_flex_style():
    description = 'サイズを教えてください'
    choice_list = ['シングル', 'セミダブル', 'ダブル', 'それ以上']

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="お求めのサイズを教えてください", contents=button_choice)
    return message


def diningtable_size_check_flex_style():
    description = 'サイズを教えてください'
    choice_list = ['2人用', '4人用', '6人用', 'それ以上']

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="お求めのサイズを教えてください", contents=button_choice)
    return message


def sofa_size_check_flex_style():
    description = 'サイズを教えてください'
    choice_list =['1人用', '2人用','3人用', 'それ以上']

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="お求めのサイズを教えてください", contents=button_choice)
    return message


def price_select_flex_style():
    description = 'ご希望の予算を教えてください'
    choice_list = ['1~3万円', '3~5万円','5~10万円','10万円~']

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="ご希望の予算を教えてください", contents=button_choice)
    return message


def isu_price_select_flex_style():
    description = 'ご希望の予算を教えてください'
    choice_list = ['~1万円', '1~2万円','2~3万円','3~5万円']

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="ご希望の予算を教えてください", contents=button_choice)
    return message


def confirm_room_style_flex_style():
    description = 'お部屋や家具のイメージはありますか'
    choice_list = ['選択肢から選ぶ', '部屋の写真がある', '家具のイメージ写真がある','特にない']

    button_choice = button_choice_generater(description=description, choice_list=choice_list, layout='1x')
    message = FlexSendMessage(alt_text="お部屋や家具のイメージはありますか", contents=button_choice)
    return message


def confirm_image_add_flex_style():
    description = '他に画像はございますか?'
    choice_list = ['まだある', 'もう大丈夫',]

    button_choice = button_choice_generater(description=description, choice_list=choice_list)
    message = FlexSendMessage(alt_text="他に画像はございますか？", contents=button_choice)
    return message



def confirm_room_style():
    confirm_template = ButtonsTemplate(text='お部屋の写真やしたいイメージ,画像などはございますか？', actions=[
        PostbackAction(label='写真がある', data='写真がある', text='写真がある'),
        PostbackAction(label='選択肢から選ぶ', data='選択肢から選ぶ', text='選択肢から選ぶ'),
        PostbackAction(label='特にない', data='特にない', text='特にない'),
    ])
    confirm_message = TemplateSendMessage(
        alt_text='お部屋のイメージを教えてください', template=confirm_template)
    return confirm_message

def kagu_select_button():
    title = 'お求めの家具はなんですか?'
    description = 'お求めの家具を選択してください.選択し終わったら[家具の選択を終了]ボタンを押してください.'
    choice_list = ['ベッド', 'ソファ', 'ダイニングテーブル', 'チェア']
    buttons_template = simple_choice_generater(title, description, choice_list)
    template_message = TemplateSendMessage(alt_text='家具の選択', template=buttons_template)
    return template_message

def kakaku_select_button():
    title = 'およその予算を教えてください?'
    description = '予算を選択してください'
    choice_list = ['1~3万円', '3~5万円', '5~10万円']
    buttons_template = simple_choice_generater(title, description, choice_list)
    template_message = TemplateSendMessage(alt_text='家具の選択', template=buttons_template)
    return template_message


def isu_kakaku_select_button():
    title = 'およその予算を教えてください?'
    description = '予算を選択してください'
    choice_list = ['~1万円', '1~3万円', '3~5万円']
    buttons_template = simple_choice_generater(title, description, choice_list)
    template_message = TemplateSendMessage(alt_text='家具の選択', template=buttons_template)
    return template_message


def confirm_image_upload():
    confirm_template = ConfirmTemplate(text='お部屋の画像やこうしたいイメージなどはございますか？', actions=[
        MessageAction(label='写真がある', text='写真がある'),
        MessageAction(label='特にない', text='写真は特にない'),
    ])
    confirm_message = TemplateSendMessage(
        alt_text='お部屋のイメージを教えてください', template=confirm_template)
    return confirm_message


def confirm_image_add():
    confirm_template = ConfirmTemplate(text='写真はもうありませんか', actions=[
        PostbackAction(label='もう大丈夫', data='もう大丈夫', text='もう大丈夫'),
        PostbackAction(label='まだある', data='まだある', text='まだある'),
    ])
    confirm_message = TemplateSendMessage(
        alt_text='confirm_image_add', template=confirm_template)
    return confirm_message
