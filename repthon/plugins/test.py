import os
import glob
import random
import asyncio
import aiohttp
from telethon import events
from repthon import zq_lo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from jiosaavn import Client as SaavnClient

plugin_category = "البوت"

def get_cookies_file():
    folder_path = os.path.join(os.getcwd(), "rbaqir")
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("لا توجد ملفات كوكيز في المجلد rbaqir")
    return random.choice(txt_files)

async def download_from_url(session: aiohttp.ClientSession, url: str, dest: str):
    async with session.get(url) as resp:
        if resp.status != 200:
            raise Exception(f"خطأ في تحميل الملف: الحالة {resp.status}")
        content = await resp.read()
        with open(dest, "wb") as f:
            f.write(content)

@zq_lo.on(events.NewMessage(pattern='.بحث3 (.*)'))
async def get_song(event):
    song_name = event.pattern_match.group(1).strip()
    await event.reply(f"🎵 جارٍ البحث عن: {song_name}")
    try:
        client = SaavnClient()
        result = await client.search(song_name)
        if not result or len(result.songs) == 0:
            raise ValueError("لم يُرجع API نتائج")
        song = result.songs[0]
        title = song.name
        artist = song.primary_artists
        image_url = song.image
        download_url = song.media_url

        filename = f"{title} - {artist}.mp3"

        async with aiohttp.ClientSession() as session:
            await download_from_url(session, download_url, filename)

        if os.path.exists(filename) and image_url:
            async with aiohttp.ClientSession() as sess2:
                async with sess2.get(image_url) as r2:
                    if r2.status == 200:
                        img_data = await r2.read()
                        audio = MP3(filename, ID3=ID3)
                        audio.tags.add(
                            APIC(
                                encoding=3,
                                mime='image/jpeg',
                                type=3,
                                desc='Cover',
                                data=img_data
                            )
                        )
                        audio.save()
        await zq_lo.send_file(event.chat_id, filename, caption=f"🎧 {title} — {artist}")
        os.remove(filename)
        return

    except Exception as e_api:
        await event.reply(f"⚠️ فشل API، سيتم استخدام yt_dlp كخطة بديلة.\n{str(e_api)[:100]}")

    import yt_dlp

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "outtmpl": "%(title)s.%(ext)s",
        "cookiefile": get_cookies_file(),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)

        if not info or 'entries' not in info or len(info['entries']) == 0:
            await event.reply("❌ لا نتائج من yt_dlp أيضًا.")
            return

        first = info['entries'][0]
        title = first.get('title')
        filename = f"{title}.mp3"

        await event.reply(f"✅ تم العثور عبر yt_dlp: {title}\n⏳ جاري الإرسال...")
        await zq_lo.send_file(event.chat_id, filename, caption=title)

    except Exception as e_yt:
        await event.reply(f"❌ فشل في yt_dlp أيضًا:\n{str(e_yt)[:200]}")
    finally:
        for fname in os.listdir():
            if fname.lower().endswith((".mp3", ".jpg", ".webp", ".m4a")):
                try:
                    os.remove(fname)
                except Exception:
                    pass
