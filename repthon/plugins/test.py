import os
import re
from pytube import YouTube, Search
from telethon import events
from repthon import zq_lo

plugin_category = "البوت"

@zq_lo.on(events.NewMessage(pattern=r'.بحث3 (.+)'))
async def download_song(event):
    video_name = event.pattern_match.group(1)
    if not re.match(r'(https?://)?(www.)?(youtube.com|youtu.?be)/.+$', video_name):
        await event.reply("يرجى إدخال رابط يوتيوب صحيح.")
        return
    await event.reply(f"جاري البحث عن الفيديو: {video_name}...")

    try:
        # البحث عن الفيديو باستخدام اسم الفيديو
        search_results = Search(video_name)
        if search_results.results:
            yt = search_results.results[0]  # Baq

            await event.reply(f"جاري تحميل الفيديو: {yt.title}...")

            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(filename="temp_audio")

            # R
            mp3_file = f"{yt.title}.mp3"
            os.rename(audio_file, mp3_file)

            # R
            await event.reply(file=mp3_file)

            os.remove(mp3_file)

        else:
            await event.reply("لم يتم العثور على أي فيديو بهذا الاسم.")
            
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء تنزيل الأغنية: {str(e)}")
