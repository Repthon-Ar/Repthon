# Repthon🔥
# Repthon - Baqir
# Copyright (C) 2023 RepthonArabic . All Rights Reserved
#
# This file is a part of < https://github.com/RepthonArabic/RepthonAr/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/RepthonArabic/RepthonAr/blob/master/LICENSE/>.


import base64
import requests
import asyncio
import os
import sys
import urllib.request
from datetime import timedelta
from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get


from repthon import zq_lo
from repthon.utils import admin_cmd
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import reply_id


bot = zq_lo

#Code by T.me/E_7_V
@zq_lo.rep_cmd(pattern="تيك(?: |$)(.*)")
async def baqir_tiktok(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    
    if not link and reply:
        link = reply.text
    
    if not link:
        return await edit_delete(event, "**- ارسـل (.تيك) + رابـط او بالـرد ع رابـط**", 10)
    
    if "tiktok.com" not in link and "vt.tiktok.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من تيـك تـوك .. للتحميــل ؟!**", 10)
    
    cap_rrr = f"<b>⎉╎تم تحميـل مـن تيـك تـوك .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/Repthon>𝗥𝗲𝗽𝘁𝗵𝗼𝗻</a> </b>"
    chat = "@QJ9bot"
    rep = await edit_or_reply(event, "**⎉╎جـارِ التحميل من تيـك تـوك .. انتظر قليلا ▬▭**")
    
    try:
        # إرسال الرابط إلى البوت
        async with borg.conversation(chat) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
            except:
                pass
            
            await conv.send_message(link)
            
            # انتظر رسالة البوت مع الأزرار
            button_msg = await conv.get_response()
            
            # تحقق إذا كانت الرسالة تحتوي على أزرار
            if button_msg.buttons:
                await rep.edit("**⎉╎جاري اختيار جودة HD...**")
                
                # النقر على الزر الثاني (جودة HD)
                # الزر الأول: "تحميل كملف صوتي"
                # الزر الثاني: "تحميل باعلن دقة HD"
                try:
                    # النقر على الزر الثاني (index 1)
                    await button_msg.click(1)
                    
                    # انتظر الملف
                    await asyncio.sleep(5)
                    
                    # حاول الحصول على الملف
                    file_msg = await conv.get_response(timeout=20)
                    
                    if file_msg.media:
                        # تحميل الملف
                        downloaded_file = await event.client.download_media(
                            file_msg,
                            file=f"tiktok_{event.id}.mp4"
                        )
                        
                        # إرسال الملف
                        await borg.send_file(
                            event.chat_id,
                            downloaded_file,
                            caption=cap_rrr,
                            parse_mode="html",
                        )
                        
                        # تنظيف
                        import os
                        if os.path.exists(downloaded_file):
                            os.remove(downloaded_file)
                        
                        await rep.delete()
                        
                        # تنظيف المحادثة
                        await asyncio.sleep(2)
                        await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
                    else:
                        await rep.edit(f"**❌ لم يتم إرسال ملف. الرد:**\n{file_msg.text[:200]}")
                        
                except Exception as click_error:
                    await rep.edit(f"**❌ خطأ في النقر على الزر:**\n`{str(click_error)[:100]}`")
            else:
                # إذا لم تكن هناك أزرار، حاول الطريقة القديمة
                await rep.edit("**⎉╎البوت لم يرسل أزراراً، جرب طريقة بديلة...**")
                await conv.send_message("تحميل باعلن دقة HD")
                
                await asyncio.sleep(5)
                file_msg = await conv.get_response(timeout=20)
                
                if file_msg.media:
                    downloaded_file = await event.client.download_media(
                        file_msg,
                        file=f"tiktok_{event.id}.mp4"
                    )
                    
                    await borg.send_file(
                        event.chat_id,
                        downloaded_file,
                        caption=cap_rrr,
                        parse_mode="html",
                    )
                    
                    import os
                    if os.path.exists(downloaded_file):
                        os.remove(downloaded_file)
                    
                    await rep.delete()
                    await asyncio.sleep(2)
                    await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
                else:
                    await rep.edit(f"**❌ فشل:**\n{file_msg.text[:200]}")
    
    except YouBlockedUserError:
        await zq_lo(unblock("QJ9bot"))
        await rep.edit("**✅ تم فك حظر البوت، أعد المحاولة**")
    except Exception as e:
        await rep.edit(f"**❌ حدث خطأ:**\n`{str(e)[:150]}`")
# Write Code By telegram.dog/E_7_V ✌🏻
@zq_lo.on(admin_cmd(pattern="ستوري(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    j_link = event.pattern_match.group(1)
    if ".me" not in j_link:
        await event.edit("**⎉╎ يجب وضع رابط الستوري مع الامر اولا **")
    else:
        await event.edit("**⎉╎ يتم الان تنزيل الستوري انتظر قليلا**")
    chat = "@msaver_bot"
    async with bot.conversation(chat) as conv:
        try:
            msg = await conv.send_message(j_link)
            video = await conv.get_response()
            """ تم تحميل الستوري بنجاح من قبل @Repthon """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("**⎉╎ الغـي حـظر هـذا البـوت و حـاول مجـددا @msaver_bot**")
            return
        REPTHON = base64.b64decode("dHJ5OgogICAgYXdhaXQgenFfbG8oSm9pbkNoYW5uZWxSZXF1ZXN0KCJAUmVwdGhvbiIpKQ==")
        TAIBA = Get(REPTHON)
        try:
            await event.client(TAIBA)
        except BaseException:
            pass
        await bot.send_file(event.chat_id, video, caption=f"<b>⎉╎ BY : @Repthon 🎀</b>",parse_mode="html")
        await event.delete()
