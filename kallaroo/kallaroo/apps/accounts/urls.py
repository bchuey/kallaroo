from django.conf.urls import url
from . import views
from ..tasks.views import AllTaskListView, ActiveTaskListView, OpenTaskListView, CompletedTaskListView

app_name = 'accounts'

urlpatterns = [

	url(r'^register/profile/$', views.RegisterProfileView.as_view(), name='register-profile'),
	url(r'^register/address/$', views.RegisterAddressView.as_view(), name='register-address'),
	url(r'^register/payment/$', views.RegisterPaymentView.as_view(), name='register-payment'),



	# url(r'^register/(?P<step>\w+)/$', account_wizard, name='register_step'),

	url(r'^(?P<pk>\d+)/tasks/$', views.UserTaskView.as_view(), name='my_tasks'),
	url(r'^(?P<pk>\d+)/profile/$', views.UserProfileDetailView.as_view(), name='profile'),
	url(r'^(?P<pk>\d+)/dashboard/$', views.DashboardTemplateView.as_view(), name='dashboard'),
	url(r'^$', views.AccountView.as_view(), name='main'),

	url(r'^login/$', views.login_user, name='login'),
	url(r'^success/$', views.SuccessView.as_view(), name='success'),
	url(r'^all/$', views.UsersListView.as_view(), name='users_all'),
	url(r'^logout/$', views.logout_view, name='logout'),
	
	url(r'^contractor/main/$', views.ContractorAccountView.as_view(), name='main_contractor'),
	url(r'^contractor/register/$', views.register_contractor, name='register_contractor'),
	url(r'^contractor/login/$', views.login_contractor, name='login_contractor'),
	url(r'^contractor/all/$', views.ContractorListView.as_view(), name='contractors_all'),
	url(r'^contractor/(?P<pk>\d+)/$', views.ContractorDetailView.as_view(), name='detail_contractor'),
	url(r'^contractor/logout/$', views.logout_contractor, name='logout_contractor'),

	url(r'^(?P<pk>\d+)/tasks/all/$', AllTaskListView.as_view(), name='all-tasks'),
	url(r'^(?P<pk>\d+)/tasks/active/$', ActiveTaskListView.as_view(), name='active-tasks'),
	url(r'^(?P<pk>\d+)/tasks/open/$', OpenTaskListView.as_view(), name='open-tasks'),
	url(r'^(?P<pk>\d+)/tasks/completed/$', CompletedTaskListView.as_view(), name='completed-tasks'),
] 