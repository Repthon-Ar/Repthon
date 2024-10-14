import re
from pytubefix import YouTube
from telethon import events
from repthon import zq_lo
import os

plugin_category = "البوت"

@zq_lo.on(events.NewMessage(pattern=r'!download (.+)'))
async def download_song(event):
    url = event.pattern_match.group(1)
    
    # التأكد من أن الرابط هو رابط يوتيوب صحيح
    if not re.match(r'(https?://)?(www.)?(youtube.com|youtu.?be)/.+$', url):
        await event.reply("يرجى إدخال رابط يوتيوب صحيح.")
        return
    
    await event.reply(f"جاري تحميل الأغنية من: {url}...")

    try:
        # ابحث عن الفيديو باستخدام pytubefix
        yt = YouTube(url)

        # احصل على رابط الصوت
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(filename="temp_audio")

        # تحويل إلى MP3
        mp3_file = f"{yt.title}.mp3"
        os.rename(audio_file, mp3_file)

        # إرسال الملف إلى المستخدم
        await event.reply(file=mp3_file)

        # حذف الملف بعد الإرسال
        os.remove(mp3_file)

    except Exception as e:
        await event.reply(f"حدث خطأ أثناء تنزيل الأغنية: {str(e)}")
