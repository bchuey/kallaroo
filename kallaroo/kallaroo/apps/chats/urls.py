from django.conf.urls import url
from . import views
# import views


app_name = 'chats'

urlpatterns = [

	url(r'^create-chatroom', views.create_chatroom, name='create-chatroom'),
	url(r'^chatroom/(?P<pk>\d+)/$', views.ChatroomDetailView.as_view(), name='chatroom'),
	url(r'^send-message', views.send_message, name='send_message'),
]