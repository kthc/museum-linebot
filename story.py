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
            TextSendMessage(text="前情提要"),
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
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''請往史博館B1兒童創意空間''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='兒童創意空間',
                template=ButtonsTemplate(
                    title='兒童創意空間',
                    text='小城小南，哪裡有適合兒童的創意空間哩~請選擇',
                    actions=[
                        MessageTemplateAction(
                            label='找到了，準備開始!!',
                            text='找到了，準備開始!!'
                        ),
                        MessageTemplateAction(
                            label='我迷路了，請給提示',
                            text='我迷路了，請給提示'
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
        self.id = 2
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["(映入眼廉是垂掛一組的別緻透明玻璃球) 小城你數數有幾顆？"]
        self.ans = '15'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''你有輸入數字嗎?''',
            '''好像不太對，再數數看''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == "":
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
            elif ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[1])]
        return True, []

class S3(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 3
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '花環'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對!''']

    def get_main_message(self):
        return [
            TextSendMessage(text="哇，這有馬槽聖嬰的小造景耶，讓我想起了小時候在附近教會安親班的點滴，小南你猜這個節日是對應上面球裡的什麼哩？"),
            TemplateSendMessage(
                alt_text='馬槽聖嬰造景',
                template=ButtonsTemplate(
                    title='馬槽聖嬰造景',
                    text='選選看',
                    actions=[
                        MessageTemplateAction(
                            label='花環',
                            text='花環'
                        ),
                        MessageTemplateAction(
                            label='艾草束',
                            text='艾草束'
                        ),
                        MessageTemplateAction(
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
        ans = f"{ans}"
        if type(ans) is str:
            if ans == "":
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
            elif ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []


class S4(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 4
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["誒，旁邊的這個是什麼啊？（看向旁邊）原來是計時工具啊，小城你從小學琴，哪種是你最熟悉的計時工具？"]
        self.ans = '節拍器'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []


class S5(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 5
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '2'
        self.reply_messages_correct = ["Wow!! 這個親子空間寓教於樂又設計用心超棒的，下次我們再來玩。(步行上樓，經過了記憶中熟悉的老牌咖啡廳，改裝後的它更顯恬靜怡然的氛圍)"]
        self.reply_messages_wrong = [
            '''好像不太對!''']

    def get_main_message(self):
        return [
            TextSendMessage(text="小城小南，快看那邊的兒童彩繪圖好可愛呀，小南快來數數裡面有幾隻妳最愛的貓？"),
            TemplateSendMessage(
                alt_text='兒童彩繪',
                template=ButtonsTemplate(
                    title='兒童彩繪',
                    text='數數看',
                    actions=[
                        MessageTemplateAction(
                            label='2',
                            text='2'
                        ),
                        MessageTemplateAction(
                            label='3',
                            text='3'
                        ),
                        MessageTemplateAction(
                            label='4',
                            text='4'
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
        ans = f"{ans}"
        if type(ans) is str:
            if ans == "":
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
            elif ans == self.ans:
                return True, [TextSendMessage(text=msg) for msg in self.reply_messages_correct]
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S6(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 6
        self.story_name = 'na'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''請往史博館5F雕築史跡展''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='雕築史跡展',
                template=ButtonsTemplate(
                    title='雕築史跡展',
                    text='老爸我是學建築的，我們來找找有沒有介紹改建過程的展覽。',
                    actions=[
                        MessageTemplateAction(
                            label='找到了，準備開始!!',
                            text='找到了，準備開始!!'
                        ),
                        MessageTemplateAction(
                            label='我迷路了，請給提示',
                            text='我迷路了，請給提示'
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

class S7(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 7
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["小城你猜，史博館在1916年時曾作為台灣勸業共進會的什麼場地使用？"]
        self.ans = '迎賓館'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S8(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 8
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["原來史博館在1960年代早期的大廳上方有好細緻的龍鳳天花板，小南你看得出內圈是哪四個字嗎？"]
        self.ans = '吉祥如意'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def get_main_message(self):
        picture = [ImageSendMessage(original_content_url=f"{APP_URL}/static/img/S8.png",
                                    preview_image_url=f"{APP_URL}/static/img/S8.png")]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return picture + main_msg

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S9(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 9
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["史博館在整個日治時期，外觀始終以中央兩層樓為主，這日式木造建物的建材全採用哪裡出產的什麼木材？", "答案五個字，小城小南回憶一下，爸爸去年剛帶你們暑假去玩過也有見到唷。"]
        self.ans = '阿里山檜木'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S10(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 10
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["史博館雖經整修，但仍力求忠於原創", "我記得前棟門廳之門神板，就是委託了15年前負責繪製的國寶匠師，協助完成修復的","好像是叫做...?小城小南快幫我找找看那位大師叫什麼。"]
        self.ans = '莊武男'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S11(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 11
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["話說小時候，爸爸每次遠遠看到史博館的屋頂都很好奇", "上排除了有1-3隻不等的脊獸外，我一直很想知道那隻龍頭魚身、背部有劍把的圖騰是稱作什麼？"]
        self.ans = '螭吻'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']

    def get_main_message(self):
        picture = [ImageSendMessage(original_content_url=f"{APP_URL}/static/img/S11.jpg",
                                    preview_image_url=f"{APP_URL}/static/img/S11.jpg")]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return picture + main_msg

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S12(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 12
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = 'ㄔ'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']
        
    def get_main_message(self):
        return [
            TextSendMessage(text="這字到底怎麼念呀？google來查查...."),
            TemplateSendMessage(
                alt_text='到底怎麼念',
                template=ButtonsTemplate(
                    title='到底怎麼念',
                    text='Google的結果',
                    actions=[
                        MessageTemplateAction(
                            label='ㄌ一/',
                            text='ㄌ一/'
                        ),
                        MessageTemplateAction(
                            label='ㄔ',
                            text='ㄔ'
                        ),
                        MessageTemplateAction(
                            label='ㄌㄩˇ',
                            text='ㄌㄩˇ'
                        )
                    ]
                )
            )
        ]
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S13(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 13
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '龍溪亭'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']
        
    def get_main_message(self):
        return [
            TextSendMessage(text="小城小南，室內逛久了，我們出去館外透透氣吧，你們知道史博館外面有一個涼亭就是為了紀念首任館長包遵彭先生而命名的嗎，猜猜看它叫什麼名字呢？"),
            TemplateSendMessage(
                alt_text='涼亭命名由來',
                template=ButtonsTemplate(
                    title='涼亭命名由來',
                    text='猜猜看',
                    actions=[
                        MessageTemplateAction(
                            label='敬包亭',
                            text='敬包亭'
                        ),
                        MessageTemplateAction(
                            label='遵彭亭',
                            text='遵彭亭'
                        ),
                        MessageTemplateAction(
                            label='龍溪亭',
                            text='龍溪亭'
                        )
                    ]
                )
            )
        ]
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S14(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 14
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '6'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']
        
    def get_main_message(self):
        return [
            TextSendMessage(text="龍溪亭採六角形的建築設計，你們看上面的屋脊共有幾個我們剛剛才學到的螭吻哩？"),
            TemplateSendMessage(
                alt_text='屋脊螭吻有幾隻',
                template=ButtonsTemplate(
                    title='屋脊螭吻有幾隻',
                    text='猜猜看',
                    actions=[
                        MessageTemplateAction(
                            label='6',
                            text='6'
                        ),
                        MessageTemplateAction(
                            label='7',
                            text='7'
                        ),
                        MessageTemplateAction(
                            label='8',
                            text='8'
                        )
                    ]
                )
            )
        ]
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S15(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 15
        self.story_name = 'na'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''請往臺北當代工藝設計分館''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='圓頂建築在哪裡',
                template=ButtonsTemplate(
                    title='圓頂建築在哪裡',
                    text='咦？印象中，史博館旁有另一個圓頂建築非常特別，我們去找找在哪!!',
                    actions=[
                        MessageTemplateAction(
                            label='找到了，準備開始!!',
                            text='找到了，準備開始!!'
                        ),
                        MessageTemplateAction(
                            label='我迷路了，請給提示',
                            text='我迷路了，請給提示'
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

class S16(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 16
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["小城小南，你們知道這個分館的圓頂建築是仿北京祈年殿的哪個建物所設計的嗎？"]
        self.ans = '天壇'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S17(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 17
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '2'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''好像不太對''']
        
    def get_main_message(self):
        return [
            TextSendMessage(text="試著數數整棟建築本體上，共有幾層的屋頂也出現了剛剛我們看到的脊獸哩？"),
            TemplateSendMessage(
                alt_text='脊獸出沒共幾層',
                template=ButtonsTemplate(
                    title='脊獸出沒共幾層',
                    text='猜猜看',
                    actions=[
                        MessageTemplateAction(
                            label='1',
                            text='1'
                        ),
                        MessageTemplateAction(
                            label='2',
                            text='2'
                        ),
                        MessageTemplateAction(
                            label='3',
                            text='3'
                        )
                    ]
                )
            )
        ]
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return True, []

class S18(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 18
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["我記得戶外空間的最右側有一個特殊造型的拱門，你們看得出是什麼水果嗎？"]
        self.ans = '蘋果'
        self.reply_messages_correct = ['''太棒了，真是一場充實有趣的知性之旅，一邊回想兒時點滴又一邊體會著整修後的新意，頗有穿越時空的新舊融合感呀。時間還早，我們一起去逛逛外面的市集吧''']
        self.reply_messages_wrong = [
            '''好像不太對''']
    
    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        ans = f"{ans}"
        if force_correct:
            # force correct answer
            return True, []
        if type(ans) is str:
            if ans == self.ans:
                return True, []
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
        self.main_messages = ['''恭喜破關!! 請出示以下圖示至愛羊全人關懷協會攤位兌換小點心!!!''']
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['你已經闖關完畢囉！']
    
    def get_main_message(self):
        picture = [ImageSendMessage(original_content_url=f"{APP_URL}/static/img/SuccessLogo.jpg",
                                    preview_image_url=f"{APP_URL}/static/img/SuccessLogo.jpg")]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return picture + main_msg

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
