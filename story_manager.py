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
            story.S1(),
            story.S2(),
            story.S3(),
            story.S4(),
            story.S5(),
            story.S6(),
            story.S7(),
            story.S8(),
            story.S9(),
            story.S10(),
            story.S11(),
            story.S12(),
            story.S13(),
            story.S14(),
            story.S15(),
            story.S16(),
            story.S17(),
            story.S18(),
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