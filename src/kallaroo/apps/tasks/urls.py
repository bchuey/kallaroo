from django.conf.urls import url 
from .views import TaskDetailView
from . import views
from .forms import ChooseSubcategoryForm, SetAddressForm, AddTaskDetailsForm


app_name='tasks'

named_task_forms = (
	("subcategory", ChooseSubcategoryForm),
	("address", SetAddressForm),
	("details", AddTaskDetailsForm),
)

task_wizard = views.AddTaskWizard.as_view(named_task_forms, url_name="tasks:task_step")

urlpatterns = [

	url(r'^add_task/(?P<step>\w+)/$', task_wizard, name='task_step'),

	url(r'^start-task/$', views.start_task, name='start_task'),
	url(r'^end-task/$', views.end_task, name='end_task'),
	url(r'^send-payment/$', views.send_payment, name='send_payment'),

	# url(r'^create/$', views.CreateTaskView.as_view(), name='create'),
	# url(r'^(?P<id>\d+)/bid/$', views.CreateBidView.as_view(), name='bid'),
	url(r'^success/$', views.SuccessView.as_view(), name='success'),
	url(r'^$', views.TaskListView.as_view(), name='task_list'),
	url(r'^(?P<pk>\d+)/$', views.TaskDetailView.as_view(), name='task_detail'),

	url(r'^(?P<pk>\d+)/active/$', views.TaskMatchedView.as_view(), name='task_detail_active'),

	url(r'^bid/accepted/$', views.accept_bid, name='accept_bid'),
]