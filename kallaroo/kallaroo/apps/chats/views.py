from django.shortcuts import render
from ..accounts.models import User
from .models import Chatroom, Chat, ChatSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session 
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from redis_collections import Dict
from django.utils.encoding import smart_text

from django.core import serializers
import json
import redis

import collections

def _convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    else:
        return data

@login_required
def home(request):
	chats = Chat.objects.select_related().all()[0:100]
	return render(request, 'chats/index.html', locals())

class ChatroomHomepage(ListView):
	model = Chatroom
	template_name = 'chats/chatroom_list.html'

class ChatroomDetailView(DetailView):
	model = Chatroom
	template_name = 'chats/chatroom_detail.html'

	def get_context_data(self, **kwargs):
		context = super(ChatroomDetailView, self).get_context_data(**kwargs)
		chatroom = self.object
		context['msgs'] = self.object.chat_set.all()
		return context





"""
1.)create_chatroom view is currently working
2.)creates a chatroom object in the backend
"""
@csrf_exempt
def create_chatroom(request):

	"""
	Probably want the session_key of User and Contractor rather than the IDs
	"""
	if request.method == "POST":
		user_id = request.POST['user_id']
		creator = User.objects.get(id=user_id)

		# contractor_id = request.POST['contractor_id']
		# contractor = Contractor.objects.get(id=contractor_id)
		participant = User.objects.get(id=request.POST['contractor_id'])

		chatroom = Chatroom.objects.create(creator=creator, participant=participant)

		# redirect to the chatroom, pass in the id of that chatroom in args=[chatroom.id]
		# return HttpResponse("everything worked")

		"""
		========
		Notes
		========
		Not redirecting to the ChatroomDetailView
		"""
		print("chatroom #" + str(chatroom.id) + " created")
		return HttpResponseRedirect('%s'%(reverse('chats:chatroom', args=[chatroom.id])))

@csrf_exempt
def send_message(request):

	if request.method == "POST":

		user = User.objects.get(id=request.POST.get('user_id'))
		chatroom = Chatroom.objects.get(id=request.POST.get('chatroom_id'))

		chatroom_id = request.POST.get('chatroom_id')
		print chatroom_id
		channel = "chatroom"+str(chatroom_id)
		print channel
		"""
		Is it better to set up a ManyToOne and use .add() => add chats to the chatroom?
		"""
		chat = Chat.objects.create(author=user, text=request.POST.get('msg'), chatroom=chatroom)

		# is this the chatroom part?
		r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

		context = ChatSerializer(chat)

		context = context.data
		print("==========")
		print("convert w/o 'u' ")
		print("==========")
		context = _convert(context)
		context = json.dumps(context)
		print(context)

		r.publish(channel, context)

		return HttpResponse("Everything worked!")




