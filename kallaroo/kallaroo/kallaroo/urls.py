"""kallaroo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.HomepageTemplateView.as_view(), name='home'),
    url(r'^how-it-works/$', views.HowItWorksTemplateView.as_view(), name='how-it-works'),
    url(r'^notifications/', include('apps.notifications.urls')),
    url(r'^reviews/', include('apps.reviews.urls')),
    url(r'^chats/', include('apps.chats.urls')),
    url(r'^categories/', include('apps.categories.urls')),
    url(r'^tasks/', include('apps.tasks.urls')),
	url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
