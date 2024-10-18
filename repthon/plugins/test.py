import os
import asyncio
from telethon import TelegramClient, events
from youtube_search import YoutubeSearch
from repthon import zq_lo
from ..Config import Config

plugin_category = "البوت"


@zq_lo.on(events.NewMessage(pattern='.بحث3 (.*)'))
async def get_song(event):
    song_name = event.pattern_match.group(1)
    await event.reply(f"جاري البحث عن الأغنية: {song_name}...")

    # البحث عن الأغنية باستخدام youtube-search
    results = YoutubeSearch(song_name, max_results=1).to_dict()
    
    if results:
        video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
        await event.reply(f"تم العثور على الأغنية: {results[0]['title']}nرابط: {video_url}")
        
        # تنزيل الأغنية بصيغة MP3 بدون استخدام الكوكيز
        os.system(f'youtube-dl -x --audio-format mp3 {video_url} -o "{results[0]["title"]}.mp3"')
        
        # إرسال الأغنية في الدردشة
        await zq_lo.send_file(event.chat_id, f"{results[0]['title']}.mp3")
        
        # حذف الملف بعد الإرسال
        os.remove(f"{results[0]['title']}.mp3")
    else:
        await event.reply("لم يتم العثور على أي أغاني.")
