from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *
 
# @receiver(post_save, sender=Event)
# def create_event_chatroom(sender, instance, created, **kwargs):
#     if created:
#         chatroom = ChatRoom.objects.create(
#             name=f'{instance.event_name} chatroom',
#             type=ChatRoom.Type.GROUP
#         )
#         instance.chatroom = chatroom
#         instance.save()
