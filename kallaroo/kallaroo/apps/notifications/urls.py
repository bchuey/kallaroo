from django.conf.urls import url
from . import views
app_name = 'notifications'

urlpatterns = [
	url(r'^send-notification', views.create_notification, name='notification'),
]