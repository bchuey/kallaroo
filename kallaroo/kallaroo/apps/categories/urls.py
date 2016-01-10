from django.conf.urls import url 
from . import views

app_name = 'categories'

urlpatterns = [
	url(r'^subcategories/$', views.SubcategoryListView.as_view(), name='subcategories'),
	url(r'^subcategories/(?P<pk>\d+)/$', views.SubcategoryDetailView.as_view(), name='subcategory'),

	url(r'^subcategories/(?P<pk>\d+)/tasks/$', views.SubcategoryTaskDetailView.as_view(), name='subcategory-task-list'),
	url(r'^subcategories/(?P<pk>\d+)/contractors/$', views.SubcategoryContractorDetailView.as_view(), name='subcategory-contractor-list'),
]