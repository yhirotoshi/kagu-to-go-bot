import numpy as np
from flask import Flask, request, abort
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


def button(choice, button_color):
    button = ButtonComponent(
        style='primary',
        color=button_color,
        height='sm',
        action=PostbackAction(label=choice, data=choice, text=choice),
    )
    return button

def button_container_1x(choice, button_color):
    choice = choice
    button_container = BoxComponent(
                         layout='horizontal',
                         spacing='sm',
                         contents=[
                                 # callAction, separator, websiteAction
                                 SpacerComponent(size='sm'),
                                 # callAction
                                 button(choice, button_color),
                             ]
                         )
    return button_container

def button_container_2x(choice, button_color):
    button_container = BoxComponent(
                         layout='horizontal',
                         spacing='sm',
                         contents=[
                                 # callAction, separator, websiteAction
                                 SpacerComponent(size='sm'),
                                 # callAction
                                 button(choice[0], button_color),
                                 # separator
                                 SeparatorComponent(),
                                 # websiteAction
                                 button(choice[1], button_color)
                             ]
                         )
    return button_container

def button_choice_generater(description, choice_list, layout='2x', background_color='#ecb68a', button_color='#a5591b'):
    '''
    description 質問文
    choice_list 選択肢
    layout 1列か2列かを指定
    '''
    if layout=='2x':
        choice_list = np.array(choice_list).reshape(int(len(choice_list)/2), 2)
        bubble_choice = BubbleContainer(
                direction='ltr',
                styles=BubbleStyle(
                    body=BlockStyle(background_color=background_color),
                    footer=BlockStyle(background_color=background_color)
                    ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text=description, weight='bold', size='md', align='center'),
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    color='#f2cdae',
                    contents=[button_container_2x(choice, button_color) for choice in choice_list],
            ))
        return bubble_choice

    else:
        bubble_choice = BubbleContainer(
                direction='ltr',
                styles=BubbleStyle(
                    body=BlockStyle(background_color=background_color),
                    footer=BlockStyle(background_color=background_color)),
                
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text=description, weight='bold', size='md', align='center'),
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    color='#f2cdae',
                    contents=[button_container_1x(choice, button_color) for choice in choice_list],
            ))
        return bubble_choice

def image_carousel_generater(image_action_list):
    image_action_list = np.array(image_action_list)
    action_list = [PostbackAction(label=action, data=action, text=action) for action in image_action_list[:,0]]
    image_url_list = image_action_list[:,1]
    columns = [ImageCarouselColumn(action, image_url) for image_url, action in zip(action_list, image_url_list)]
    image_carousel_template = ImageCarouselTemplate(columns=columns)
    return image_carousel_template


def simple_choice_generater(title, description, choice_list):
    actions = [PostbackAction(label=choice, data=choice, text=choice) for choice in choice_list]
    buttons = ButtonsTemplate(title=title, text=description, actions=buttons)
    return buttons