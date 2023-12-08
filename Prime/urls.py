"""FirstCall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import HomeView
    2. Add a URL to urlpatterns:  path('', HomeView.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from apps.tools.views import panel_view, Chats, Post, Message
from apps.services.views import CustomerAplicCreate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', CustomerAplicCreate, name='aplic'),
    path('home/', login_required(panel_view), name='home'),
    path('panel/', include(('apps.tools.urls', 'tools'), namespace='panel')),
    path('accounting/', include(('apps.accounting.urls', 'accounting'), namespace='accounting')),
    path('services/', include(('apps.services.urls', 'services'), namespace='services')),
    path('logistic/', include(('apps.logistic.urls','logistic'), namespace='logistic')),
    path('accounts/login/', LoginView.as_view(template_name='Login/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chat/', login_required(Chats), name='chat'),
    path('application/', include(('apps.logistic.urls','logistic'), namespace='application')),
    path('post/', login_required(Post), name='post'),
    path('message/', login_required(Message), name='message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
