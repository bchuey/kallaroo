from django.conf.urls import url 
from . import views

app_name = 'reviews'

urlpatterns = [

	url(r'^task/(?P<task_id>\d+)/add-review/$', views.AddTaskReview.as_view(), name='add_task_review'),
	url(r'^task/(?P<task_id>\d+)/add-rating/$', views.AddTaskRating.as_view(), name='add_task_rating'),
	# url(r'^contractor/(?P<contractor_id>\d+)/add-review/$', views.AddContractorReview.as_view(), name='add-contractor-review'),
	# url(r'^contractor/(?P<contractor_id>\d+)/add-rating/$', views.AddContractorRating.as_view(), name='add-contractor-rating'),
]