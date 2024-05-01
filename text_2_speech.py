# Import the Gtts module for text  
# to speech conversion 
from gtts import gTTS 
  
# import Os module to start the audio file
import os, subprocess, threading

dialogs = [
    "喂喂喂？齁～～終於打通了，我跟你講喔，你肯定不相信我經歷了什麼，我好像掉到了過去，掉到了一片草地上，身邊一大堆牛，忽然，好像是放牛的阿伯，問我能不能幫他去打點水，我也不知道發生了什麼就去做了，把水給阿伯之後，忽然之間身邊的景物開始轉變，然後……嘟嘟嘟",
    "小古？我是小亭，反正就像剛剛講的我掉到了過去，我需要靠幫忙解決問題，才能回到2022，你必須幫幫我，我現在在民國56年，老闆要我幫他把東西送到龍口市場附近的雜貨店，我根本不知道在哪裡，快幫我想想辦法。",
    "我真的是小亭啦，我們本來約好今天要出去，我們約在古亭站，這樣夠了吧，唉，沒時間廢話了，反正你先想辦法幫我找找資訊，我先去找找有沒有公共電話，看看30分鐘後我再打給你。……嘟嘟嘟",
    "怎麼樣，你有找到嗎？我花了好久才找到公用電話，耽擱了一陣子，抱歉，都快重死我了。",
    "太厲害了果然是你，沒指望錯人，我馬上去找找，趕快把這袋重的要死的東西送到那裡，那我先掛了喔……",
    "喂？是我，我現在掉到另一個時代了，有一個姊姊給了我一封信，裡面全是英文，我根本看不懂，她希望我幫他把內容解開，我真的要死了，這也未免太難了，但是不解開我又回不去，到底怎麼辦啊？",
    "一阿嚕呼阿辜",
    "就沒辦法啊，我英文被當到大的，你又不是不知道，痾年代的話，好像是民國68年，我好像還是在龍口市場附近，那位姊姊說她叫陳美華的樣子，阿你問這些幹嘛，你不如幫我趁機補補英文。",
]

def convert(dialog, ouput_filename):
    tts = gTTS(dialog, lang="zh-tw")
    tts.save(f"{ouput_filename}.mp3")
    subprocess.call([r"tool\ffmpeg.exe", '-i', f"{ouput_filename}.mp3", f'{ouput_filename}.m4a'])


for i, dialog in enumerate(dialogs):
    t = threading.Thread(target=convert, args=[dialog, f"ting_{i+1}" ])
    t.start()