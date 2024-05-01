
from linebot.models import (
    Sender
)
from app_global import APP_URL

roles = {
    '古亭智能小編': Sender(name='古亭智能小編', icon_url=f"{APP_URL}/static/img/admin.png"),
    '小亭': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/02.png"),
    '小古_02': Sender(name='小古', icon_url=f"{APP_URL}/static/img/small_ku.png"),
    '小亭_02': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/02.png"),
    '小亭_09': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/09.png"),
    '小亭_10': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/10.png"),
    '小亭_11': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/11.png"),
    '小亭_12': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/12.png"),
    '小亭_14': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/14.png"),
    '小亭_19': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/19.png"),
    '小亭_20': Sender(name='小亭', icon_url=f"{APP_URL}/static/img/small_ting/20.png"),
    '旁白': Sender(name='旁白', icon_url=f"{APP_URL}/static/img/admin.png"),
    'unknown': Sender(name='??', icon_url=f"{APP_URL}/static/img/unknown.png"),
    # 'BG': Sender(name=None, icon_url=f"{APP_URL}/static/img/bg.png"),
}

audio_dict = {
    'not_found': {'url': f"{APP_URL}/static/audio/not_found.m4a", 'duration': 1700},
    'test': {'url': f"{APP_URL}/static/audio/test.m4a", 'duration': 2400},
    '01': {'url': f'{APP_URL}/static/audio/story_audio/audio_01.m4a', 'duration': 32757}, 
    '02': {'url': f'{APP_URL}/static/audio/story_audio/audio_02.m4a', 'duration': 27689}, 
    '03': {'url': f'{APP_URL}/static/audio/story_audio/audio_03.m4a', 'duration': 22935}, 
    '04': {'url': f'{APP_URL}/static/audio/story_audio/audio_04.m4a', 'duration': 12199}, 
    '05': {'url': f'{APP_URL}/static/audio/story_audio/audio_05.m4a', 'duration': 11650}, 
    '06': {'url': f'{APP_URL}/static/audio/story_audio/audio_06.m4a', 'duration': 20323}, 
    '07': {'url': f'{APP_URL}/static/audio/story_audio/audio_07.m4a', 'duration': 6817}, 
    '08': {'url': f'{APP_URL}/static/audio/story_audio/audio_08.m4a', 'duration': 19826}, 
    '09': {'url': f'{APP_URL}/static/audio/story_audio/audio_09.m4a', 'duration': 17319}, 
    '10': {'url': f'{APP_URL}/static/audio/story_audio/audio_10.m4a', 'duration': 11311}, 
    '11': {'url': f'{APP_URL}/static/audio/story_audio/audio_11.m4a', 'duration': 15568}, 
    '12': {'url': f'{APP_URL}/static/audio/story_audio/audio_12.m4a', 'duration': 17763}, 
    '13': {'url': f'{APP_URL}/static/audio/story_audio/audio_13.m4a', 'duration': 47464}, 
    '14': {'url': f'{APP_URL}/static/audio/story_audio/audio_14.m4a', 'duration': 12382}, 
    '15': {'url': f'{APP_URL}/static/audio/story_audio/audio_15.m4a', 'duration': 12617}, 
    '16': {'url': f'{APP_URL}/static/audio/story_audio/audio_16.m4a', 'duration': 17057}, 
    '17': {'url': f'{APP_URL}/static/audio/story_audio/audio_17.m4a', 'duration': 20662}, 
    '18': {'url': f'{APP_URL}/static/audio/story_audio/audio_18.m4a', 'duration': 13844}, 
    '19': {'url': f'{APP_URL}/static/audio/story_audio/audio_19.m4a', 'duration': 8045}, 
    '20': {'url': f'{APP_URL}/static/audio/story_audio/audio_20.m4a', 'duration': 16509}, 
    '21': {'url': f'{APP_URL}/static/audio/story_audio/audio_21.m4a', 'duration': 16222}, 
    '22': {'url': f'{APP_URL}/static/audio/story_audio/audio_22.m4a', 'duration': 15934}, 
    '23': {'url': f'{APP_URL}/static/audio/story_audio/audio_23.m4a', 'duration': 9639}, 
    '24': {'url': f'{APP_URL}/static/audio/story_audio/audio_24.m4a', 'duration': 13035}, 
    '25': {'url': f'{APP_URL}/static/audio/story_audio/audio_25.m4a', 'duration': 15882}, 
    '26': {'url': f'{APP_URL}/static/audio/story_audio/audio_26.m4a', 'duration': 36911}, 
    '27': {'url': f'{APP_URL}/static/audio/story_audio/audio_27.m4a', 'duration': 17397}, 
    '28': {'url': f'{APP_URL}/static/audio/story_audio/audio_28.m4a', 'duration': 19957}, 
    '29': {'url': f'{APP_URL}/static/audio/story_audio/audio_29.m4a', 'duration': 11859},
    'Q5': {'url': f'{APP_URL}/static/audio/Q5.m4a', 'duration': 10000}
}

video_dict = {
    'Q1': {'url': f"{APP_URL}/static/video/Video1.mp4", 'preview': f"{APP_URL}/static/img/Video1_preview.png"},
    'Q2': {'url': f"{APP_URL}/static/video/Video2.mp4", 'preview': f"{APP_URL}/static/img/Video2_preview.png"},
    'Q3': {'url': f"{APP_URL}/static/video/Video3.mp4", 'preview': f"{APP_URL}/static/img/Video3_preview.png"},
    'OneHourLater':  {'url': f"{APP_URL}/static/video/raining.mp4", 'preview': f"{APP_URL}/static/video/raining.mp4"},
}

img_dict = {
    'Q1':  {'url': f"{APP_URL}/static/img/Q1_handwritten_note.jpg", 'preview': f"{APP_URL}/static/img/Q1_handwritten_note.jpg"},
    'Q6_normal':  {'url': f"{APP_URL}/static/img/6_b_Hosannah_vme_w_word.png", 'preview': f"{APP_URL}/static/img/6_b_Hosannah_vme_w_word.png"},
    'Q6_challeng':  {'url': f"{APP_URL}/static/img/6_b_Hosannah_vme_no_word.png", 'preview': f"{APP_URL}/static/img/6_b_Hosannah_vme_no_word.png"},
    'Q6_normal_grid':  {'url': f"{APP_URL}/static/img/6_b_easy.png", 'preview': f"{APP_URL}/static/img/6_b_easy.png"},
    'Q6_challeng_grid':  {'url': f"{APP_URL}/static/img/6_b_hard.jpg", 'preview': f"{APP_URL}/static/img/6_b_hard.jpg"},
}
