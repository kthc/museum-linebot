

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
    ImageSendMessage,
    AudioSendMessage,
    VideoSendMessage,
    Sender
)
import os, glob
from bible_database import db
from app_global import line_bot_api, APP_URL
from story_manager import Story_Manager

_HELP_DICT = {
    "-reset / reset": "重置你的ID，讓故事從頭開始",
    "-stage": "列出你當前在哪個故事",
    "-force-next / sos": "強制跳下一關",
    "-force-prev": "強制回上一關",                                                                                                                             
    "-test-img": "秀出測試image",                                                                                                                             
    "-test-audio": "秀出測試audio",                                                                                                                             
    "-test-video": "秀出測試video"
}

def help(event, key=None):
    '''return True if processed helper actions, otherwise return False'''
    help_done = False
    if key == "-h":
        print(f"{key} help function")
        helptext = ""
        for k,v in _HELP_DICT.items():
            helptext += f'''{k}: {v}\n'''
        line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage(text=helptext, sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"))]
                )
        help_done = True
    elif key == "-reset" or key.lower() == 'reset':
        print(f"{key} help function")
        user_id=event.source.user_id
        profile=line_bot_api.get_profile(user_id)
        user_name=profile.display_name
        s_mang = Story_Manager(user_name, user_id=user_id)
        db.delete_user(user_id)
        db.add_new_user(user_id)
        s_mang.show_welcome_story(event)
        help_done = True
    elif key == "-stage":
        print(f"{key} help function")
        user_id=event.source.user_id
        profile=line_bot_api.get_profile(user_id)
        user_name=profile.display_name
        s_mang = Story_Manager(user_name, user_id=user_id)
        db.connect()
        story_id = db.get_storyid_by_userid(user_id)
        story = s_mang.get_story(story_id)
        if story:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage(text=f"你目前的故事在第{story.id}關:{story.story_name}", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"))]
                    )
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage(text=f"找不到你的關卡!?", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"))]
                    )
        help_done = True
        db.close()

    elif key == "-force-next" or key.lower() == "skip":
        print(f"{key} help function")
        user_id=event.source.user_id
        profile=line_bot_api.get_profile(user_id)
        user_name=profile.display_name
        s_mang = Story_Manager(user_name, user_id=user_id)
        db.connect()
        story_id = db.get_storyid_by_userid(user_id)
        cur_retry = db.get_retry_count_by_userid(user_id)
        end = s_mang.is_end_story(story_id)
        if end:
            return
        ok = s_mang.check_answer(event, story_id, "", force_correct=True, retry_count=cur_retry+1) # add one because it start from 0, so the first trial will be 0+1 = 1 attempt
        if ok and not end:
            next_story = s_mang.next_story(story_id)
            db.update_story_id(user_id, next_story.id)
            db.clear_retry_count(user_id)
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage(text=f"已經沒有下一關囉!", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"))]
                    )
        help_done = True
        db.close()

    elif key == "-force-prev" or key == "--p":
        print(f"{key} help function")
        user_id=event.source.user_id
        profile=line_bot_api.get_profile(user_id)
        user_name=profile.display_name
        s_mang = Story_Manager(user_name, user_id=user_id)
        db.connect()
        story_id = db.get_storyid_by_userid(user_id)
        last_story = s_mang.last_story(story_id)
        if last_story:
            db.update_story_id(user_id, last_story.id)
            s_mang.show_story(event, last_story.id)
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage(text=f"已經沒有上一關囉!", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"))]
                    )
        help_done = True
        db.close()
        
    elif key == "-test-img":
        print(f"{key} help function")
        line_bot_api.reply_message(
            event.reply_token, 
            ImageSendMessage(original_content_url = f"{APP_URL}/static/img/icon_300x300.jpeg", preview_image_url = f"{APP_URL}/static/img/icon_48x48.jpeg", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png")))
        help_done = True
    elif key == "-test-audio":
        print(f"{key} help function")
        line_bot_api.reply_message(
            event.reply_token, 
            AudioSendMessage(original_content_url = f"{APP_URL}/static/audio/audio-final.m4a", duration=34000, sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png")))
        help_done = True
    elif key == "-test-video":
        print(f"{key} help function")
        line_bot_api.reply_message(
            event.reply_token, 
            VideoSendMessage(original_content_url = f"{APP_URL}/static/video/Video1.mp4", preview_image_url=f"{APP_URL}/static/img/Video1_preview.png", sender=Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png")))
        help_done = True
    return help_done