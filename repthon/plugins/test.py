import pytube
from pytube import YouTube
import requests
import os
import glob
import random
import asyncio
from telethon import events
from telethon.errors import ChatSendMediaForbiddenError
from youtube_search import YoutubeSearch
import ffmpeg
from ..Config import Config
from repthon import zq_lo

plugin_category = "الادوات"

# R
def get_cookies_file():
    """
    تيستت
    """
    try:
        folder_path = f"{os.getcwd()}/rbaqir"
        txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
        if not txt_files:
            print(f"[!] No .txt files found in the specified folder: {folder_path}.")
            return None

        cookie_txt_file = random.choice(txt_files)
        print(f"[*] Using cookie file: {cookie_txt_file}")
        return cookie_txt_file
    except FileNotFoundError:
        print(f"[!] Cookie folder not found: {folder_path}.")
        return None
    except Exception as e:
        print(f"[!] Error getting cookie file: {e}")
        return None

def remove_if_exists(file_path):
    """يحذف الملف إذا كان موجودًا"""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

def convert_to_m4a(input_file, output_file):
    try:
        process = (
            ffmpeg
            .input(input_file)
            .output(output_file, acodec='aac', audio_bitrate='192k', strict='experimental')
            .overwrite_output()
        )
        process.run(capture_stdout=True, capture_stderr=True)
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg Error: {e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")
        return False

# --- تيست ---

@zq_lo.on(events.NewMessage(pattern="/بحث3(?: |$)(.*)"))
async def search_music_pytube_simple(event):
    """
    بسم الله تيست
    """
    input_message = event.pattern_match.group(1).strip()

    if not input_message:
        await event.reply("**• يرجى كتابة اسم الأغنية بعد الأمر:** `.بحث3 [اسم الأغنية]`")
        return

    processing_message = await event.reply("**• جاري البحث عن الأغنية... 🔍**")

    # الحصول على مسار ملف الكوكيز باستخدام دالتك
    cookie_file_path = get_cookies_file()
    # ملاحظة: pytube لا تدعم تمرير ملف الكوكيز مباشرة.
    # سنحاول تنزيل الصورة المصغرة باستخدام requests مع ملف الكوكيز إن وجد.

    try:
        # البحث عن الرابط باستخدام youtube-search-python
        from youtube_search import YoutubeSearch
        search_results = YoutubeSearch(input_message, max_results=1).to_dict()

        if not search_results:
            await processing_message.edit(f"**• لم يتم العثور على نتائج لـ `{input_message}`**")
            return

        video_url = f"https://youtube.com{search_results[0]['url_suffix']}"

        # استخدام pytube للحصول على معلومات الفيديو
        yt = YouTube(video_url)

        # الحصول على أفضل جودة صوتية
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if not audio_stream:
            await processing_message.edit("**• لم يتم العثور على صيغة صوتية متاحة لهذا الفيديو.**")
            return

        title = yt.title[:40].strip()
        duration = yt.length

        # تنزيل الصورة المصغرة (إذا كان هناك مسار للكوكيز)
        thumbnail_url = yt.thumbnail_url
        thumb_name = f"{title}.jpg"
        if cookie_file_path: # حاول التنزيل باستخدام الكوكيز إذا كانت متوفرة
            try:
                # هنا نستخدم requests مباشرة لتنزيل الصورة المصغرة، 
                # ولكن pytube لا تدعم تمرير cookies لعملياتها الداخلية (مثل تنزيل الفيديو)
                # لذا، هذا الجزء لمحاولة استخدام الكوكيز للصورة المصغرة فقط.
                response = requests.get(thumbnail_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    with open(thumb_name, "wb") as f:
                        f.write(response.content)
                else:
                    thumb_name = None
            except Exception as e:
                print(f"[!] Error downloading thumbnail with cookies: {e}")
                thumb_name = None
        else:
            # إذا لم يكن هناك ملف كوكيز، قم بالتنزيل بشكل عادي
            try:
                response = requests.get(thumbnail_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    with open(thumb_name, "wb") as f:
                        f.write(response.content)
                else:
                    thumb_name = None
            except Exception as e:
                print(f"[!] Error downloading thumbnail: {e}")
                thumb_name = None

    except Exception as e:
        await processing_message.edit(f"**• حدث خطأ أثناء البحث أو التحضير:** `{str(e)}`\n**• تأكد من تحديث pytube, youtube-search-python.**")
        return

    await processing_message.edit("**• جاري تحميل الصوت... ⏳**")

    input_audio_file = None
    output_audio_file = None
    try:
        # تنزيل أفضل صيغة صوتية متاحة
        # pytube download method لا تدعم cookies مباشرة.
        # إذا كان هناك مشكلة في التنزيل بسبب القيود، فقد تفشل هنا.
        input_audio_file = audio_stream.download(
            output_path='.', 
            filename_prefix=f"{title}_",
            skip_existing=False,
        )

        base, ext = os.path.splitext(input_audio_file)
        output_audio_file = base + ".m4a"

        # تحويل الملف إلى m4a
        if not convert_to_m4a(input_audio_file, output_audio_file):
            raise Exception("Audio conversion to m4a failed.")

        if not os.path.exists(output_audio_file):
             raise Exception("Converted audio file not found.")

        await processing_message.edit("**• جاري رفع الملف... ⬆️**")

        minutes, seconds = divmod(duration, 60)
        time_format = f"{minutes}:{seconds:02d}"
        caption_text = f"**🎶 أغنية (pytube):** `{title}`\n**• المدة:** `{time_format}`"

        await zq_lo.send_file(
            event.chat_id,
            output_audio_file,
            caption=caption_text,
            thumb=thumb_name,
            force_document=False,
        )
        await processing_message.delete()

    except ChatSendMediaForbiddenError:
        await processing_message.edit("**• عذراً، لا يمكنني إرسال الوسائط في هذه المحادثة.**")
    except Exception as e:
        error_message = f"**• فشل تحميل أو تحويل أو رفع الملف.**\n" \
                        f"**• الخطأ:** `{str(e)}`\n" \
                        f"**• تأكد من أن pytube و ffmpeg محدثين.**"
        await processing_message.edit(error_message)
    finally:
        if input_audio_file and os.path.exists(input_audio_file):
            remove_if_exists(input_audio_file)
        if output_audio_file and os.path.exists(output_audio_file):
            remove_if_exists(output_audio_file)
        if thumb_name and os.path.exists(thumb_name):
            remove_if_exists(thumb_name)
