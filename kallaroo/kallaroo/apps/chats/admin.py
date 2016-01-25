from django.contrib import admin
from .models import Chatroom, Chat

# Register your models here.
class ChatroomAdmin(admin.ModelAdmin):
	model = Chatroom
	list_display = ('id', 'creator', 'participant')

admin.site.register(Chatroom, ChatroomAdmin)
admin.site.register(Chat)
