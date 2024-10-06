import asyncio
from pytubefix import YouTube
from telethon import TelegramClient, events
from repthon import zq_lo
from ..Config import Config

plugin_category = "البوت"

async def download_and_send(search_query):
    # R
    yt = YouTube(search_query)
    
    # R
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(filename='audio.mp4')

    # R
    os.rename(audio_file, 'audio.mp3')

    # R
    await client.send_file('me', 'audio.mp3')
    

@zq_lo.rep_cmd(
    pattern="test(?:\v|\/)([\v\v]*)",
    command=("test", plugin_category),
    info={
        "header": "تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط",
        "مثــال": ["{tr}تحميل صوت بالــرد ع رابــط", "{tr}تحميل صوت + رابــط"],
    },
)
async def handler(event):
    search_query = event.pattern_match.group(1)
    await download_and_send(search_query)
    await event.reply('تم تحميل وإرسال الملف!')
