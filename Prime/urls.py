"""FirstCall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin, admindocs
from django.contrib.auth.views import login, logout_then_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from apps.tools.views import panel_view, Chats, Post, Message

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', login_required(panel_view), name='home'),
    url(r'^panel/', include('apps.tools.urls', namespace='panel')),
    url(r'^accounting/', include('apps.accounting.urls', namespace='accounting')),
    url(r'^services/', include('apps.services.urls', namespace='services')),
    url(r'^logistic/', include('apps.logistic.urls', namespace='logistic')),
    url(r'^accounts/login/', login, {'template_name':'Login/login.html'}, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^chat/$', login_required(Chats), name='chat'),
    url(r'^application/', include('apps.logistic.urls', namespace='application')),
    url(r'^post/$', login_required(Post), name='post'),
    url(r'^message/$', login_required(Message), name='message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


