import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.inquiry_id = self.scope['url_route']['kwargs']['inquiry_id']
        self.room_group_name = f'chat_{self.inquiry_id}'

        # Check user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        # Check user has access to this inquiry
        has_access = await self.check_access()
        if not has_access:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()

        if not message:
            return

        # Save to database
        reply = await self.save_reply(message)
        if not reply:
            return

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_role': reply['sender_role'],
                'sender_name': reply['sender_name'],
                'avatar': reply['avatar'],
                'timestamp': reply['timestamp'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_role': event['sender_role'],
            'sender_name': event['sender_name'],
            'avatar': event['avatar'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def check_access(self):
        from properties.models import Inquiry
        try:
            inquiry = Inquiry.objects.select_related('property__owner', 'buyer').get(pk=self.inquiry_id)
            user = self.scope['user']
            return inquiry.property.owner == user or inquiry.buyer == user
        except Inquiry.DoesNotExist:
            return False

    @database_sync_to_async
    def save_reply(self, message):
        from properties.models import Inquiry, InquiryReply
        try:
            inquiry = Inquiry.objects.select_related('property__owner', 'buyer').get(pk=self.inquiry_id)
            user = self.scope['user']

            is_seller = inquiry.property.owner == user
            role = 'seller' if is_seller else 'buyer'

            reply = InquiryReply.objects.create(
                inquiry=inquiry,
                sender=user,
                sender_role=role,
                message=message,
            )

            inquiry.status = 'replied'
            inquiry.save(update_fields=['status', 'updated_at'])

            sender_name = inquiry.property.owner.full_name if is_seller else inquiry.seeker_name
            avatar = sender_name[0].upper() if sender_name else '?'

            return {
                'sender_role': role,
                'sender_name': sender_name,
                'avatar': avatar,
                'timestamp': reply.created_at.strftime('%b %d, %Y %H:%M'),
            }
        except Exception:
            return None