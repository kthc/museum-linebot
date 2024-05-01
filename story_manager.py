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
    Sender
)
import uuid
from app_global import line_bot_api
import story
from story_data_collection import audio_dict, video_dict, img_dict

class Story_Manager:
    def __init__(self, user_name='USER', user_id='') -> None:
        self.user_name = user_name
        self.user_id = user_id
        self.stories = [
            story.Welcome(username=user_name),  
            story.simple_msg_maker(5, msg='死定了', button_label='？？？', text_after_clicked='？？？發生什麼事', sender_name=None),
            story.Welcome2(username=user_name),  
            story.simple_msg_maker(10, msg='真的可以嗎？\n（請務必使用手機或平板進行遊戲，並點選對話下方浮現的按鈕來推進劇情。）', button_label='但是', text_after_clicked='我要怎麼幫啊？'), 
            story.simple_msg_maker(15, msg='一起集思廣益啊！兩個腦袋比一個好用！', button_label='我想想喔…', text_after_clicked='對了，你暑假不是有參加一個營隊？'),
            story.P7(),
            # story.simple_msg_maker(20, msg='欸？對欸，好險有你幫忙，我去找一下營隊手冊\n我找到了！剛好營隊有很多內容也在馬太福音呢！', button_label='那我就幫你到這', text_after_clicked='接下來就靠你自己吧！'), 
            story.simple_msg_maker(25, msg='欸！等等啦！我發現我看不懂自己的筆記😅', button_label='不是吧！', text_after_clicked='你都不懂，我怎麼可能懂啊？'), 
            story.Question1(),
            story.simple_msg_maker(30, msg='喔喔！我想起來了！這或許能當其中一個信息呢！', button_label='嗯嗯..', text_after_clicked='那還要嗎？'), 
            story.simple_msg_maker(35, msg='當然啊！這才剛開始。我再翻一下，看看還有沒有其它寶藏', button_label='OK', text_after_clicked='好啊，我很期待'),
            story.simple_msg_maker(40, msg='那時候...有一個活動，有讓我們自己設計題目', button_label= '？？？', text_after_clicked='那跟小組有什麼關係？'),
            # story.simple_msg_maker(45, msg='你等我講完，答案是聖經裡的一個名詞\n我還留著當時的題目！翻到了！痾不過，沒有答案欸🤪', button_label='.....又來！', text_after_clicked='你的筆記要不是看不懂，就是缺漏...'),
            story.P12(),
            story.Question2(), 
            story.simple_msg_maker(46, msg='這本手冊真是個寶阿！我又找到了一個活動，想當初我可是秒答呢！你挑戰看看？', button_label='不會吧！', text_after_clicked='你竟然有秒答的一天？'), 
            story.Question3(userid=self.user_id),
            story.simple_msg_maker(50, msg='對了！我想把八福也加入這次的信息', button_label='可以呀！', text_after_clicked='但是你要怎麼帶？\n難道你要準備講章？'), 
            # story.simple_msg_maker(55, msg='怎麼可能，講章太像上課一定沒人理我😤\n我打算仿造之前玩過的解謎，讓大家動動腦', button_label='好啊！', text_after_clicked='設計完傳給我'),
            story.P17(),
            story.Question4(),
            story.simple_msg_maker(60, msg='趁你剛剛解題的時候，我又想到了一題', button_label='真的假的？', text_after_clicked='到底是你出題太快還是我解題太慢？'), 
            story.Question5(),
            story.simple_msg_maker(65, msg='對了欸！不錯嘛！題目沒問題吧？', button_label='嗯嗯！', text_after_clicked='只是好奇你上面的圖片哪來的？總不可能是你自己畫的吧'), 
            story.simple_msg_maker(70, msg='那當然不是啊！是得到了民間高手的幫助', button_label='我就說！', text_after_clicked='難怪這麼精美'), 
            story.simple_msg_maker(75, msg='欸欸好消息！我同學傳給我一題他自己設計的題目！', button_label='咦？', text_after_clicked='你還有請別人幫忙喔？'), 
            story.simple_msg_maker(80, msg='對啊！不然真的好累😞\n但是我是先找你的喔！別吃醋！', button_label='我才不會…', text_after_clicked='我才不會…'), 
            story.Question6_a(),
            story.Question6_b(userid=self.user_id),
            story.Question6_b_1(userid=self.user_id),
            story.simple_msg_maker(90, msg='同學補充說：和散那就是由Yasha(拯救、交付)以及Anna(懇求)這兩個希伯來語組成的，意思是"我求你來拯救"', button_label='天啊！', text_after_clicked='他出的也太複雜了吧！\n但很有深度耶！'),
            # story.simple_msg_maker(95, msg='😥對啊！我都解崩潰了，還是沒頭緒\n我覺得可以來收尾了！', button_label='對阿！', text_after_clicked='已經有不少素材了！'),
            story.P31(),
            story.Question7(),
            story.Ending()
        ]

    def set_username(self, username):
        self.user_name = username

    def get_story(self, story_id):
        '''return story instance if found'''
        for story in self.stories:
            if story_id == story.id:
                return story
        print(f'找不到Story_id:{story_id}')

    def last_story(self, story_id):
        '''return last story instance if found'''
        i = 0
        for i, story in enumerate(self.stories):
            if story_id == story.id:
                break
        if i-1 >= 0:
            last_story = self.stories[i-1]
            return last_story
        else:
            print(f'找不到上一個Story')
            return None

    def next_story(self, story_id):
        '''return next story instance if found'''
        for i, story in enumerate(self.stories):
            if story_id == story.id:
                break
        try:
            next_story = self.stories[i+1]
            return next_story
        except IndexError:
            print(f'找不到下一個Story')
            return None

    def is_end_story(self, story_id):
        '''check if this story is the last one'''
        story = self.next_story(story_id)
        if story:
            return False
        return True
    
    def show_welcome_story(self, event):
        story = self.get_story(0)
        messages = story.get_pre_message() + story.get_main_message()
        line_bot_api.reply_message(
                event.reply_token,
                messages=messages
                )

    def check_answer(self, event, story_id, ans, force_correct=False, retry_count=0) -> None:
        '''check answer and auto reply linebot
        return True if correct, else False
        '''
        story = self.get_story(story_id)
        correct, messages = story.check_ans(ans,force_correct,retry_count)
        if len(messages) > 5:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text='回應訊息數超過五則喔！要重新修改後才能正確回傳！')
                )
            return False
        if correct or force_correct:
            next_story = self.next_story(story_id)
            if next_story:
                next_story_messages = messages + next_story.get_pre_message() + next_story.get_main_message()
                if len(next_story_messages) > 5:
                    line_bot_api.reply_message(
                        event.reply_token,
                        messages=TextSendMessage(text='回應訊息數超過五則喔！要重新修改後才能正確回傳！')
                        )
                    return False
                line_bot_api.reply_message(
                        event.reply_token,
                        messages=next_story_messages
                        )
            else:
                line_bot_api.reply_message(
                        event.reply_token,
                        messages=messages
                        )
            return True
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=messages
                    )
            return False

    def show_story(self, event, story_id) -> None:
        '''show pre and main message of this story'''
        story = self.get_story(story_id)
        if story:
            messages = story.get_pre_message() + story.get_main_message()
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=messages
                    )

if __name__=='__main__':
    s = Story_Manager()
    s.get_story(2)