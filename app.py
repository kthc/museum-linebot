'''
聖經OnLine v1.0
'''
import os
from dotenv import load_dotenv
load_dotenv()

from bible_database import db
from flask import Flask, request, abort
from app_global import line_bot_api, handler
import story_data_collection
from story_manager import Story_Manager
from helper import help

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    MessageEvent,
    TextMessage,
    PostbackEvent,
    FollowEvent
)

app = Flask(__name__)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def follow(event):
    print(f"FollowEvent: {event}")
    user_id=event.source.user_id
    profile=line_bot_api.get_profile(user_id)
    user_name=profile.display_name
    s_mang = Story_Manager(user_name, user_id)
    print(f"user_id: {user_id}")
    print(f"user_name: {user_name}")
    db.connect()
    if not db.check_user_exist(user_id):
        db.add_new_user(user_id)
        s_mang.show_welcome_story(event)
    db.close()
                
@handler.add(UnfollowEvent)
def unfollow(event):
    print(f"UnfollowEvent: {event}")
    user_id=event.source.user_id
    print(f"user_id: {user_id}")
    db.connect()
    db.delete_user(user_id)
    db.close()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id=event.source.user_id
    profile=line_bot_api.get_profile(user_id)
    user_name=profile.display_name
    msg = event.message.text
    print(f"user_id: {user_id}, user_name: {user_name}, input: {msg}")

    # check if user keyin helper keyword
    called_helper = help(event, key=msg)
    if called_helper:
        # means do some action inside the help function, so do not continue the following code
        print('finished help function')
        return

    # check answer for current stroy
    check_if_can_go_next_story(event, msg)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(f"PostbackEvent: {event}")
    user_id=event.source.user_id
    profile=line_bot_api.get_profile(user_id)
    user_name=profile.display_name
    msg = event.postback.data
    print(f"user_id: {user_id}, user_name: {user_name}, postback_input: {msg}")
    bypass = ['$Q3_Bypass', '$Q5_Bypass']
    db.connect()
    if msg in bypass:
        pass
    elif msg == '$Q6_reset':
        db.clear_retry_count(user_id)
        called_helper = help(event, key='-force-prev')
    else:
        check_if_can_go_next_story(event, msg)
    db.close()


'''
Common Functions
'''
def check_if_can_go_next_story(event, ans):
    '''check answer for current stroy'''
    user_id=event.source.user_id
    profile=line_bot_api.get_profile(user_id)
    user_name=profile.display_name
    s_mang = Story_Manager(user_name, user_id)
    db.connect()
    if not db.check_user_exist(user_id):
        db.add_new_user(user_id)
        s_mang.show_welcome_story(event)
    else:
        story_id = db.get_storyid_by_userid(user_id)
        cur_retry = db.get_retry_count_by_userid(user_id)
        end = s_mang.is_end_story(story_id)
        if end:
            db.close()
            return
        ok = s_mang.check_answer(event, story_id, ans, retry_count=cur_retry + 1 ) # add one because it start from 0, so the first trial will be 0+1 = 1 attempt
        if ok and not end:
            next_story_id = s_mang.next_story(story_id)
            db.update_story_id(user_id,next_story_id.id)
            db.clear_retry_count(user_id)
        elif not ok:
            db.increase_1_retry_count(user_id)
    db.close()

if __name__ == '__main__':
    '''
    host = '0.0.0.0'是讓flask server可以監聽所有裝置的IP(代表可以從手機或是任何其他電腦連線到flask server的這台電腦)
    host = '127.0.0.1'是只監聽你開發用的電腦上的client(瀏覽器就是client)
    port: 像是這個ip下的門牌,每一個server要有自己獨立的port
    '''
    port = os.getenv('PORT', default=5001)
    app.run(host='0.0.0.0', port=port, debug=True)
    # app = create_app()
    # app.run(host='0.0.0.0', port=5001, debug=True)  
