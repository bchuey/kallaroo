from __future__ import unicode_literals
from django.db import models
from ..accounts.models import User
# Create your models here.

class Chatroom(models.Model):
	creator = models.ForeignKey(User, related_name='chatroom_host')
	participant = models.ForeignKey(User, related_name='chatroom_participant')
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		db_table = 'chatrooms'

	def __str__(self):
		return str(self.id)



class Chat(models.Model):
	author = models.ForeignKey(User, blank=True, null=True, related_name='author_user')
	# author = models.ForeignKey(Contractor, blank=True, null=True, related_name='author_contractor')
	text = models.CharField(max_length=255)
	chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
	written_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
	class Meta:
		db_table = 'chats'

	def __str__(self):
		return str(self.id)

# """
# Chat serializer 
# """
# from rest_framework import serializers

# class ChatSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Chat
# 		fields = ('author', 'text', 'chatroom', 'written_at')
# 		depth = 1





