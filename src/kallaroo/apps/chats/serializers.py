from .models import Chat

from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = ('author', 'text', 'chatroom', 'written_at')
		depth = 1