import os,subprocess
import glob
import re
import soundfile as sf
from gtts import gTTS 


def rename_audio():
    files = glob.glob('./龍口錄音/*.wav')
    print(files)
    for f in files:
        filename = os.path.basename(f)
        dirname = os.path.dirname(f)
        matched = re.search(r'龍口錄音([\d]*).wav',filename)
        if matched:
            id_number = int(matched.groups()[0])
            os.rename(f, os.path.join(dirname, f"audio_{id_number:02d}.wav"))

def gen_audio_dict():
    files = glob.glob(r'C:\Users\super\Downloads\20221122\*.wav')
    print(files)
    sound_dict = {}
    for f in files:
        filename = os.path.basename(f)
        matched = re.search(r'audio_([\d]*).wav',filename)
        if matched:
            id_number = matched.groups()[0]
            f = sf.SoundFile(f)
            print('samples = {}'.format(f.frames))
            print('sample rate = {}'.format(f.samplerate))
            sec = f.frames / f.samplerate
            print('seconds = {}'.format(sec))
            ms = int(sec * 1000)
            sound = {'url':f"[ToBeReplaced]/static/story_audio/{filename}", 'duration': ms}
            sound_dict[id_number] = sound
    print(sound_dict)

def convert_2_m4a():
    files = glob.glob(r'C:\Users\super\Downloads\20221122\*.mp3')
    print(files)
    for f in files:
        filename = os.path.basename(f)
        dirname = os.path.dirname(f)
        matched = re.search(r'小亭錄音#([\d]*).mp3',filename)
        if matched:
            id_number = int(matched.groups()[0])
            subprocess.call([r"tool\ffmpeg.exe", '-i', f"{f}", os.path.join(dirname, f"audio_{id_number:02d}.m4a")])


def get_file_property():
    files = glob.glob('./static/audio/story_audio/*.m4a')
    for f in files:
        filename = os.path.basename(f)
        print(os.stat(f))

def convert_wav_2_m4a():
    subprocess.call([r"tool\ffmpeg.exe", '-i', f"C:\code\LongkouMarketLineBot\龍口錄音-20221111T062231Z-001\龍口錄音\龍口錄音26.wav", f'./static/audio/story_audio/audio_26.m4a'])

def test_q1():
    ans = '亞金，以律，以利亞撒，馬但，雅各，約瑟，耶穌'
    ans = ans.strip()
    pattern = r"[\s\W]"
    fixed_ans = re.sub(pattern, "，", ans)
    print(fixed_ans)

if __name__=='__main__':
    test_q1()