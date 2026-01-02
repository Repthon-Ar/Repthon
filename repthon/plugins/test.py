import random
import glob
import os
import asyncio
import re
from yt_dlp import YoutubeDL
from repthon import zq_lo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from ..Config import Config

plugin_category = "البوت"

def clean_filename(filename):
    """Remove invalid characters from filename."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_cookies_file():
    """Get a random cookies file from the specified folder."""
    folder_path = f"{os.getcwd()}/rbaqir"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        print("⚠️ No .txt cookies files found in 'rbaqir' folder.")
        return None
    return random.choice(txt_files)

@zq_lo.rep_cmd(pattern="بحث3(?: |$)(.*)")
async def get_song(event):
    song_name = event.pattern_match.group(1)
    if not song_name:
        await event.reply("⚠️ يرجى كتابة اسم الأغنية بعد الأمر.\nمثال: `.بحث3 أغنية`")
        return
    
    message = await event.reply(f"🔍 جاري البحث عن: `{song_name}`...")
    
    try:
        # تنظيف اسم الملف
        safe_song_name = clean_filename(song_name)
        
        ydl_opts = {
            "format": "bestaudio/best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "convert_thumbnails": "jpg",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
            "outtmpl": f"%(id)s.%(ext)s", # استخدام ID بدلاً من العنوان لتجنب مشاكل الأسماء
            "quiet": True,
            "no_warnings": True,
            "embedthumbnail": True,  # تأكيد إضافة الصورة
            "embed_metadata": True,  # تأكيد إضافة البيانات الوصفية
            "already_have_thumbnail": False,
        }
        
        # إضافة cookies إذا وجدت
        cookies_file = get_cookies_file()
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            
            if not info or 'entries' not in info or not info['entries']:
                await message.edit("❌ لم أجد أي نتائج للبحث.")
                return
            
            video_info = info['entries'][0]
            video_id = video_info['id']
            title = video_info['title']
            uploader = video_info.get('uploader', 'غير معروف')
            
            # اسم الملف الذي تم تنزيله
            mp3_file = f"{video_id}.mp3"
            thumbnail_file = f"{video_id}.jpg"
            
            await message.edit(f"✅ تم العثور على: `{title}`\n📤 جاري الإرسال...")
            
            # إضافة الغلاف إذا وجد
            if os.path.exists(thumbnail_file):
                try:
                    audio = MP3(mp3_file, ID3=ID3)
                    # إضافة tags ID3 إذا لم تكن موجودة
                    if audio.tags is None:
                        audio.add_tags()
                    
                    with open(thumbnail_file, 'rb') as img_file:
                        audio.tags.add(
                            APIC(
                                encoding=3,
                                mime='image/jpeg',
                                type=3,
                                desc='Cover',
                                data=img_file.read()
                            )
                        )
                    audio.save()
                except Exception as e:
                    print(f"⚠️ خطأ في إضافة الغلاف: {e}")
            
            # إرسال الملف
            caption = (
                f"**🎵 {title}**\n"
                f"**👤 الناشر:** {uploader}\n"
                f"**🔍 البحث:** {song_name}\n"
                f"**⚡ بواسطة:** @Repthon"
            )
            
            await zq_lo.send_file(
                event.chat_id,
                mp3_file,
                caption=caption,
                supports_streaming=True
            )
            
            await message.delete()
            
            # تنظيف الملفات المؤقتة
            for file in [mp3_file, thumbnail_file]:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except:
                        pass
                        
    except Exception as e:
        error_msg = f"❌ حدث خطأ:\n`{str(e)}`"
        await message.edit(error_msg)
        print(f"Error in get_song: {e}")
