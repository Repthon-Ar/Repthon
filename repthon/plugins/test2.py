import contextlib
import io
import os
import re
import glob
import random

from telethon import types
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import reply_id
from . import zq_lo, song_download

plugin_category = "البحث"
LOGS = logging.getLogger(__name__)

def get_cookies_file():
    folder_path = f"{os.getcwd()}/rbaqir"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@zq_lo.rep_cmd(
    pattern=r"بحث4(320)?(?:\s|$)([\s\S]*)",
    command=("بحث", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def song(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "What I am Supposed to find ")
    
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING)
    video_link = await yt_search(str(query))
    
    if not url(video_link):
        return await catevent.edit(f"Sorry!. I can't find any related video/audio for {query}")
    cmd = event.pattern_match.group(1) if event.pattern_match.group(1) else None
    q = "320k" if cmd == "320" else "128k"
    cookies_path = get_cookies_file()
    song_file, catthumb, title = await song_download(video_link, catevent, quality=q, cookies_path=cookies_path)
    
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"**بحثك:** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    
    await catevent.delete()
    
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)
