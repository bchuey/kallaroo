from django.shortcuts import render
from ..accounts.models import User
from ..tasks.models import Task
from .models import Notification
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

"""
Should this be a View, with a GET and POST method???
"""
@csrf_exempt
def create_notification(request):
	
	if request.method == "POST":
		
		user_id = request.POST.get('user_id')

		task_id = request.POST.get('task_id')
		task = Task.objects.get(id=task_id)

		user_id = request.POST.get('user_id')

		"""
		Must pass in a dict if you don't want to serialize data
		Cannot pass objects unless it's serialized => research how to do
		"""
		context = {
			'id': task.id,
			'title': task.title,
			'creator': task.user.username,
		}
		return JsonResponse(context)
	# elif request.method == "GET":
	# 	# if request.is_ajax():

	# 		# run a query and send data back to server.js
	# 	print("goodbye")
	# 	return HttpResponse("GET request made it to the django view")
	# 	# return HttpResponse("Failed2")
	# return HttpResponse("Failed3")