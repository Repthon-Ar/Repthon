import os
import re
import asyncio
from datetime import datetime

try:
    from akinator import Akinator
except ModuleNotFoundError:
    os.system("pip3 install akinator.py")
    from akinator import Akinator

from googletrans import Translator

from telethon import Button
from telethon.errors import BotMethodInvalidError
from telethon.events import CallbackQuery, InlineQuery

from repthon import zq_lo
from ..Config import Config
from ..core.decorators import check_owner

games = {}
translator = Translator()
aki_photo = "https://graph.org/file/b0ff07069e8637783fdae.jpg"

@zq_lo.rep_cmd(pattern="اكينوتر(?:\\s|$)([\\s\\S]*)")
async def start_aki_cmd(e):
    aki = Akinator()
    games.update({e.chat_id: {e.id: aki}})
    
    try:
        results = await e.client.inline_query(
            Config.TG_BOT_USERNAME, f"aki_{e.chat_id}_{e.id}"
        )
        await results[0].click(e.chat_id)
    except Exception as ex:
        return await e.reply(f"**⌔∮ عذراً، يجب تفعيل وضع الانلاين للبوت أولاً من @BotFather**")
    
    if e.out:
        await e.delete()

@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"aki_?(.*)")))
@check_owner
async def handle_start(e):
    adt = e.pattern_match.group(1).strip().decode("utf-8")
    dt = adt.split("_")
    ch, mid = int(dt[0]), int(dt[1])
    
    await e.edit("**⌔∮ جاري الاتصال بالمارد الازرق...**")
    
    try:
        loop = asyncio.get_event_loop()
        q = await loop.run_in_executor(None, lambda: games[ch][mid].start_game(language="ar"))
        
        buttons = [
            [Button.inline("✅ نعم", f"aka_{ch}_{mid}_0"), Button.inline("❌ لا", f"aka_{ch}_{mid}_1")],
            [Button.inline("❓ لا أعلم", f"aka_{ch}_{mid}_2"), Button.inline("🤔 ربما", f"aka_{ch}_{mid}_3")],
            [Button.inline("📉 ربما لا", f"aka_{ch}_{mid}_4")]
        ]
        await e.edit(f"**السؤال الأول:**\n\n`{q}`", buttons=buttons)
    except Exception as ex:
        await e.edit(f"**حدث خطأ في الاتصال:**\n`{ex}`")

@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"aka_?(.*)")))
@check_owner
async def process_answer(e):
    mk = e.pattern_match.group(1).decode("utf-8").split("_")
    if len(mk) < 3: return
    
    ch, mid, ans = int(mk[0]), int(mk[1]), mk[2]
    
    try:
        gm = games[ch][mid]
    except KeyError:
        return await e.answer("⚠️ انتهت الجلسة، ابدأ من جديد.", alert=True)

    await e.answer("جاري التفكير... 🤔")
    loop = asyncio.get_event_loop()
    
    try:
        # إرسال الإجابة للمارد
        q = await loop.run_in_executor(None, lambda: gm.answer(ans))
        
        # إذا وصلت نسبة التوقعات لأكثر من 80%
        if gm.progression >= 80:
            await loop.run_in_executor(None, gm.win)
            res = gm.first_guess
            
            # ترجمة الاسم والوصف للعربية
            name_ar = translator.translate(res['name'], dest='ar').text
            desc_ar = translator.translate(res['description'], dest='ar').text
            
            final_text = (
                f"**✨ لقد حزرت الشخصية! ✨**\n\n"
                f"**👤 الاسم:** `{name_ar}`\n"
                f"**📝 الوصف:** `{desc_ar}`\n\n"
                f"**نسبة التأكد:** `{gm.progression}%`"
            )
            return await e.edit(final_text, file=res['absolute_picture_path'], buttons=[Button.inline("لعب مرة أخرى 🔄", f"aki_{ch}_{mid}")])

        # عرض السؤال التالي
        buttons = [
            [Button.inline("✅ نعم", f"aka_{ch}_{mid}_0"), Button.inline("❌ لا", f"aka_{ch}_{mid}_1")],
            [Button.inline("❓ لا أعلم", f"aka_{ch}_{mid}_2"), Button.inline("🤔 ربما", f"aka_{ch}_{mid}_3")],
            [Button.inline("📉 ربما لا", f"aka_{ch}_{mid}_4")]
        ]
        await e.edit(f"**السؤال التالي:**\n\n`{q}`", buttons=buttons)
        
    except Exception as ex:
        await e.edit(f"**خطأ أثناء اللعب:**\n`{ex}`")

@zq_lo.tgbot.on(InlineQuery)
async def handle_inline(e):
    query_user_id = e.query.user_id
    query = e.text
    if (query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS) and query.startswith("aki"):
        ans = [
            await e.builder.photo(
                aki_photo,
                text="**مرحباً بك في لعبة أكينوتر!**\nفكر في شخصية وسأحاول معرفتها.",
                buttons=[Button.inline("❃ ابدأ اللعب الآن ❃", data=query)],
            )
        ]
        await e.answer(ans)
