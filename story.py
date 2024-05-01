from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    MessageEvent,
    TextMessage,
    TextSendMessage,
    StickerSendMessage,
    LocationMessage,
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    ConfirmTemplate,
    QuickReply,
    QuickReplyButton,
    PostbackAction,
    PostbackEvent,
    FollowEvent,
    DatetimePickerAction,
    MessageAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    AudioSendMessage,
    VideoSendMessage,
    ImageSendMessage,
    Sender,
    CarouselColumn,
    CarouselTemplate,
    FlexSendMessage,
    PostbackTemplateAction
)
import re
import uuid
import random
from app_global import APP_URL
from story_data_collection import roles, audio_dict, video_dict, img_dict
from bible_database import db


class Story:
    def __init__(self, *args, **kwargs) -> None:
        self.username = ''
        self.userid = ''
        self.story_name = ''
        self.id = -1
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_wrong = []

    def get_pre_message(self):
        return [TextSendMessage(text=text) for text in self.pre_messages]

    def get_main_message(self):
        return [TextSendMessage(text=text) for text in self.main_messages]

    def get_post_message(self):
        return [TextSendMessage(text=text) for text in self.post_messages]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans or force_correct:
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        else:
            return False, [TextSendMessage(text=msg, sender=None) for msg in self.reply_messages_wrong]

    def show_ans_if_force_correct(self, messages=[], pre_text='正確答案是：'):
        '''if messages not given, it will send the correct ans and post_messages of this instance'''
        if len(messages) == 0:
            return True, [TextSendMessage(text=f'''{pre_text}{self.ans}''', sender=None)] + [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        else:
            return True, messages

    def show_ans_over_try(self):
        '''if messages not given, it will send the correct ans and post_messages of this instance'''
        return True, [TextSendMessage(text=f'''（系統偵測已作答多次，為使遊戲順利進行，將直接報出答案。請將答案複製貼上於對話框並回傳。此題答案為：{self.ans}）''', sender=None)]


class SimplePostbackStory(Story):
    def __init__(self, id, *args, msg='', button_label='', text_after_clicked='', sender_name='', **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.data = '$Pass'
        self.label = button_label
        self.display_text = text_after_clicked
        self.main_messages = msg
        self.sender_name = sender_name

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=self.main_messages,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None)
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class AudioStory(Story):
    def __init__(self, id, *args, audio_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.audio_name = audio_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        audio = audio_dict.get(self.audio_name, None)
        if audio_dict.get(self.audio_name, None) is None:
            audio = audio_dict.get('not_found', None)
        print(audio)
        return [
            AudioSendMessage(
                original_content_url=audio['url'],
                duration=audio['duration'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class VideoStory(Story):
    def __init__(self, id, *args, video_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.video_name = video_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        video = video_dict.get(self.video_name, None)
        return [
            VideoSendMessage(
                original_content_url=video['url'],
                preview_image_url=video['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class ImageStory(Story):
    def __init__(self, id, *args, image_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.image_name = image_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        image = img_dict.get(self.image_name, None)
        return [
            ImageSendMessage(
                original_content_url=image['url'],
                preview_image_url=image['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Welcome(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 0
        self.story_name = 'Welcome2'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = []

    def get_main_message(self):
        return [
            TextSendMessage(
                text=f'前情提要:'
            ),
            TextSendMessage(
                text='夏日的午後，我帶著一雙兒女悠閒散步在南海路上，不同於以往目光總朝著第一學府瞧過去，這次我被對面【城南．那一味】的文宣所吸引，這不就是我兒時常玩耍的史博館嗎？成家立業後，少有機會來訪，沒想到它剛換上新裝、整修落成。小時候我曾想過，如果這裡能有更多適合親子的空間規劃該有多好，如今身為人父，懷著期待的興奮感，忍不住拉著小城和小南一探究竟去，準備好了嗎？Go!!',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='GO', text='GO')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, [TextSendMessage(text=msg) for msg in self.post_messages]


class S1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 1
        self.story_name = 'na'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = [
            f'''''']
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''請往史博館B1兒童創意空間''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='小城小南，那裡有適合兒童的創意空間哩~',
                    text='請選擇',
                    actions=[
                        PostbackTemplateAction(
                            label='找到了，準備開始!!',
                            text='找到了，準備開始!!',
                            data='S1&ready'
                        ),
                        PostbackTemplateAction(
                            label='我迷路了，請給提示',
                            text='我迷路了，請給提示',
                            data='S1&lost'
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        print(f"ans: {ans}")
        if force_correct:
            # force correct answer
            return True, []
        if ans == '找到了，準備開始!!':
            return True, []
        elif ans == '我迷路了，請給提示':
            return True, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]
        return False, []


class S2(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 16
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["(映入眼廉是垂掛一組的別緻透明玻璃球) 小城你數數有幾顆？"]
        self.ans = '15'
        self.reply_messages_correct = ['''你答對了''']
        self.reply_messages_wrong = [
            '''你有輸入數字嗎?''',
            '''好像不太對，再數數看''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == "":
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
            elif ans == self.ans:
                return True, [TextSendMessage(text=self.reply_messages_correct[0])]
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[1])]
        return True, []

class S3(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 16
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '花環'
        self.reply_messages_correct = ['''你答對了''']
        self.reply_messages_wrong = [
            '''好像不太對!''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='哇，這有馬槽聖嬰的小造景耶，讓我想起了小時候在附近教會安親班的點滴，小南你猜這個節日是對應上面球裡的什麼哩？',
                    text='請選擇',
                    actions=[
                        MessageTemplateAction(
                            label='花環',
                            text='花環'
                        ),
                        PostbackTemplateAction(
                            label='艾草束',
                            text='艾草束'
                        ),
                        PostbackTemplateAction(
                            label='花朵',
                            text='花朵'
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == "":
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
            elif ans == self.ans:
                return True, [TextSendMessage(text=self.reply_messages_correct[0])]
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []


class Ending(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 990
        self.story_name = 'Ending'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['你已經闖關完畢囉！']

    # def get_main_message(self):
    #     sticker = [StickerSendMessage(package_id=11537, sticker_id=52002745)]
    #     main_msg = [TextSendMessage(text=text) for text in self.main_messages]
    #     images = [
    #         ImageSendMessage(original_content_url = f"{APP_URL}/static/img/info.jpg", preview_image_url = f"{APP_URL}/static/img/info.jpg")
    #         ]
    #     return sticker + main_msg

    def get_main_message(self):
        contents = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "週六小組裡到底分享了甚麼信息呢？點選以下小組信息閱讀完整版。\n中間在哪一題卡住了嗎？點選解題思路，看看各題的解題辦法！",
                                "wrap": True
                            }
                        ],
                        "height": "150px",
                        "alignItems": "center",
                        "justifyContent": "flex-end"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "小組訊息",
                                    "text": "小組訊息\nhttps://drive.google.com/file/d/1Hgr4jnakPflcH1WV5F3EbUJ8PtN-vIVw/view?usp=share_link"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "解題思路",
                                    "text": "解題思路\nhttps://drive.google.com/file/d/1D7Ysl2IS_fTzHvCxvxpQoU59TwN6Rz5J/view?usp=share_link"
                                }
                            }
                        ],
                        "position": "relative"
                    },
                    "styles": {
                        "header": {
                            "separatorColor": "#dbdbdb",
                            "separator": True
                        },
                        "hero": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        },
                        "body": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        }
                    }
                },
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "歡迎點選以下連結更了解我們團隊，若您願意奉獻，也可參考奉獻資訊。",
                                "wrap": True
                            }
                        ],
                        "height": "150px",
                        "alignItems": "center",
                        "justifyContent": "flex-end"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "團隊介紹",
                                    "text": "團隊介紹\n我們是一群來自台北古亭聖教會的社青和青年。我們熱衷解謎，從某一青年就讀的高中設計了linebot解謎，促發這次活動的設計。歷經5個月的技術課程和題目劇情的討論，終於在今年底正式推出！"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "奉獻資訊",
                                    "text": '''奉獻資訊\n感謝您的擺上，奉獻資訊如下，煩請於備註中填寫"Line"，以利司庫同工辨認。\n第一銀行(銀行代碼：007)\n帳號：172-10-115645\n若您需要奉獻收據，請填寫以下表單。https://docs.google.com/forms/d/e/1FAIpQLSfKnLorNmQ00Vx_qKEPKgssHsZA3T0uHlN0RHHdiUDqdhmB1Q/viewform?usp=sharing'''
                                }
                            }
                        ],
                        "position": "relative"
                    },
                    "styles": {
                        "header": {
                            "separatorColor": "#dbdbdb",
                            "separator": True
                        },
                        "hero": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        },
                        "body": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        }
                    }
                }
            ]
        }
        # main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        main_msg = [
            TextSendMessage(text='''這些素材真是太可以了！'''),
            StickerSendMessage(package_id=11537, sticker_id=52002745),
            TextSendMessage(text='''作為福利，我讓你搶先看週六小組的信息內容'''),
            FlexSendMessage(alt_text='flex_contents', contents=contents),
            # TemplateSendMessage(
            #     alt_text='Buttons template',
            #     template=ButtonsTemplate(
            #         title='關於我們',
            #         text='想更深入了解我們團隊嗎？請點選下面按鈕',
            #         actions=[
            #             MessageTemplateAction(
            #                 label='搶先看週六小組的信息內容',
            #                 text=f'搶先看週六小組的信息內容:(牧師講章)'
            #             ),
            #             MessageTemplateAction(
            #                 label='解題思路',
            #                 text=f'解題思路:TBD'
            #             ),
            #             MessageTemplateAction(
            #                 label='團隊介紹',
            #                 text=f'團隊介紹:TBD'
            #             ),
            #             MessageTemplateAction(
            #                 label='奉獻資訊',
            #                 text=f'奉獻資訊:TBD'
            #             ),
            #         ]
            #     )
            # )
        ]
        return main_msg

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


def simple_msg_maker(id, msg='', button_label='', text_after_clicked='', sender_name=''):
    return SimplePostbackStory(id, msg=msg, button_label=button_label, text_after_clicked=text_after_clicked, sender_name=sender_name)


def simple_audio_maker(id, audio_name='', sender_name='', button_label='', text_after_clicked='',):
    return AudioStory(id, audio_name=audio_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_video_maker(id, video_name='', sender_name='', button_label='', text_after_clicked='',):
    return VideoStory(id, video_name=video_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_image_maker(id, image_name='', sender_name='', button_label='', text_after_clicked='',):
    return ImageStory(id, image_name=image_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)
