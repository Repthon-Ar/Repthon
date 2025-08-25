import yt_dlp
import requests
import os
import glob
import random
import asyncio
from telethon import events
from telethon.errors import ChatSendMediaForbiddenError
from youtube_search import YoutubeSearch
from repthon import zq_lo
from ..Config import Config

plugin_category = "الادوات"

# --- دالة الحصول على الكوكيز (من عندك) ---
def get_cookies_file():
    """
    يبحث عن ملف .txt للكوكيز في مجلد rbaqir ويختار واحدًا عشوائيًا.
    """
    try:
        folder_path = f"{os.getcwd()}/rbaqir"
        txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
        if not txt_files:
            print(f"[!] No .txt files found in the specified folder: {folder_path}.")
            return None # أرجع None إذا لم يتم العثور على ملفات

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
    """يحذف الملف إذا كان موجودًا."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")



@zq_lo.on(events.NewMessage(pattern=".بحث3(?: |$)(.*)"))
async def download_youtube_audio(event):
    """
    يبحث عن مقطع فيديو على يوتيوب، يقوم بتنزيله وتحويله إلى صوت (m4a)،
    مع دعم ملفات تعريف الارتباط (cookies).
    الاستخدام: .صوت_يوتيوب [اسم الأغنية أو الفيديو]
    """
    input_message = event.pattern_match.group(1).strip()

    if not input_message:
        await event.reply("**• يرجى كتابة اسم الأغنية أو الفيديو بعد الأمر:** `.صوت_يوتيوب [اسم الأغنية]`")
        return

    processing_message = await event.reply("**• جاري البحث عن الفيديو... 🔍**")

    # الحصول على مسار ملف الكوكيز باستخدام دالتك
    cookie_file_path = get_cookies_file()

    # خيارات yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best', # أفضل صيغة صوتية متاحة
        'outtmpl': '%(title)s.%(ext)s', # قالب اسم الملف (سيتم تحويله إلى m4a)
        'postprocessors': [{ # معالجات لاحقة (للتحويل)
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a', # الصيغة المطلوبة للصوت
            'preferredquality': '192', # جودة الصوت (يمكنك تغييرها إذا أردت)
        }],
        'quiet': True, # إخفاء مخرجات yt-dlp (اجعلها False لرؤية التفاصيل)
        'noplaylist': True, # تجاهل قوائم التشغيل، خذ الفيديو فقط
        'ignoreerrors': True, # تجاهل الأخطاء البسيطة (مثل عدم إمكانية تنزيل صورة مصغرة)
        # 'proxy': 'socks5://user:password@host:port', # يمكنك إضافة بروكسي هنا إذا احتجت
    }

    # إضافة ملف الكوكيز إلى الخيارات إذا كان موجودًا
    if cookie_file_path:
        ydl_opts['cookiefile'] = cookie_file_path
        print(f"[*] yt-dlp will use cookie file: {cookie_file_path}")

    # ... داخل دالة download_youtube_audio ...
    try:
        search_results = YoutubeSearch(input_message, max_results=1).to_dict()

        if not search_results:
            await processing_message.edit(f"**• لم يتم العثور على نتائج لـ `{input_message}`**")
            return

        # تأكد من أننا حصلنا على نتيجة صالحة قبل محاولة الوصول إلى عناصرها
        first_result = search_results[0] # احصل على أول نتيجة في متغير واحد

        # تحقق من وجود المفاتيح المطلوبة قبل استخدامها
        if 'url_suffix' not in first_result:
            await processing_message.edit(f"**• مشكلة في بيانات البحث، لم يتم العثور على رابط الفيديو.**")
            return

        video_url = f"https://youtube.com{first_result['url_suffix']}"

        # تنزيل الصورة المصغرة
        # استخدم .get() ليكون أكثر أمانًا
        thumbnail_url = first_result.get('thumbnails', [{}])[0].get('url')
        thumb_name = None
        if thumbnail_url:
            safe_title_thumb = "".join([c if c.isalnum() or c in (' ', '_', '-') else '_' for c in first_result.get('title', 'thumbnail')[:40]])
            thumb_name = f"{safe_title_thumb}.jpg"
            try:
                response = requests.get(thumbnail_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    with open(thumb_name, "wb") as f:
                        f.write(response.content)
                else:
                    thumb_name = None # فشل التنزيل
            except Exception as e:
                print(f"[!] Error downloading thumbnail: {e}")
                thumb_name = None

        # ... بقية الكود (تنزيل الصوت والتحويل والإرسال) ...

            thumb_name = f"{search_results[0]['title'][:40].replace('/', '_').replace(':', '_').replace('?', '_')}.jpg" # تنظيف اسم الملف
            try:
                # استخدام requests للتنزيل، لا نحتاج لـ yt-dlp هنا
                response = requests.get(thumbnail_url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    with open(thumb_name, "wb") as f:
                        f.write(response.content)
                else:
                    thumb_name = None # فشل التنزيل
            except Exception as e:
                print(f"[!] Error downloading thumbnail: {e}")
                thumb_name = None

    except Exception as e:
        await processing_message.edit(f"**• حدث خطأ أثناء البحث:** `{str(e)}`")
        return

    await processing_message.edit("**• جاري تحميل وتحويل الصوت... ⏳**")

    downloaded_file = None # لنتأكد من تعريف المتغير
    try:
        # استخدام yt_dlp للتنزيل والتحويل
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

            # yt-dlp سيقوم بالتحويل إلى m4a إذا تم تحديد preferredcodec
            # نحتاج إلى الحصول على اسم الملف الذي تم إنشاؤه
            # قالب اسم الملف: %(title)s.%(ext)s -> Title.m4a
            # يجب استخلاص اسم الملف من info_dict أو استخدام القالب

            # الطريقة المباشرة لاستخلاص اسم الملف بعد التحويل
            # yt-dlp يضع المسار الكامل للملف المحول في 'requested_downloads'
            # إذا كان هناك أكثر من طلب، فإن الأول هو الملف الرئيسي
            if 'requested_downloads' in info_dict and info_dict['requested_downloads']:
                downloaded_file = info_dict['requested_downloads'][0]['filepath']
            else:
                # طريقة احتياطية إذا لم نجد 'requested_downloads'
                # نستخدم معلومات العنوان والامتداد المتوقع
                title_from_info = info_dict.get('title', 'unknown_title')
                # تنظيف العنوان ليكون صالحًا كاسم ملف
                safe_title = "".join([c if c.isalnum() or c in (' ', '_', '-') else '_' for c in title_from_info])
                safe_title = safe_title[:50].strip() # تحديد طول الاسم
                downloaded_file = f"{safe_title}.m4a"

            # التأكد من أن الملف موجود بالفعل
            if not os.path.exists(downloaded_file):
                 raise FileNotFoundError(f"Downloaded file '{downloaded_file}' not found after extraction.")

        # تم التحويل، الآن قم بإرسال الملف
        await processing_message.edit("**• جاري رفع الملف... ⬆️**")

        # استخلاص المعلومات من info_dict
        title = info_dict.get('title', 'Unknown Title')
        duration = info_dict.get('duration', 0)
        minutes, seconds = divmod(duration, 60)
        time_format = f"{minutes}:{seconds:02d}"

        caption_text = f"**🎶 صوت (yt-dlp):** `{title}`\n**• المدة:** `{time_format}`"

        # إرسال الملف إلى المحادثة
        await zq_lo.send_file(
            event.chat_id,
            downloaded_file,
            caption=caption_text,
            thumb=thumb_name, # الصورة المصغرة التي تم تنزيلها سابقًا
            force_document=False, # إرسال كملف صوتي عادي
        )
        await processing_message.delete() # حذف رسالة "جاري رفع الملف..."

    except yt_dlp.utils.DownloadError as e:
        # معالجة أخطاء yt-dlp المحددة
        error_message = f"**• فشل تحميل أو تحويل الملف باستخدام yt-dlp.**\n" \
                        f"**• الخطأ:** `{str(e)}`"
        await processing_message.edit(error_message)
    except FileNotFoundError as e:
        # معالجة خطأ عدم وجود الملف
        await processing_message.edit(f"**• خطأ: الملف الذي تم تنزيله غير موجود.**\n**• التفاصيل:** `{str(e)}`")
    except Exception as e:
        # معالجة أي أخطاء عامة أخرى
        error_message = f"**• حدث خطأ أثناء المعالجة.**\n" \
                        f"**• الخطأ:** `{str(e)}`\n" \
                        f"**• تأكد من تثبيت yt-dlp بشكل صحيح، وأن ملف الكوكيز صالح.**"
        await processing_message.edit(error_message)
    finally:
        # تنظيف الملفات بعد الإرسال أو في حالة حدوث خطأ
        if downloaded_file and os.path.exists(downloaded_file):
            remove_if_exists(downloaded_file)
        if thumb_name and os.path.exists(thumb_name):
            remove_if_exists(thumb_name)
