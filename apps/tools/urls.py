from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from apps.tools.views import *

urlpatterns = [

url(r'^$', login_required(panel_view), name='panel'),
url(r'^calendar/list/$', login_required(GetCalendar), name='calendar_list'),
url(r'^calendar/$', login_required(Calendar_Panel.as_view()), name='calendar'),
url(r'^directory/$', login_required(DirectoryTelephone.as_view()), name='directory'),
url(r'^directory/create$', login_required(DirectoryTelephoneCreate.as_view()), name='directory_create'),
url(r'^directory/edit/(?P<pk>\d+)/$', login_required(DirectoryTelephoneEdit.as_view()), name='directory_edit'),
url(r'^directory/delete/(?P<pk>\d+)/$', login_required(DirectoryTelephoneDelete.as_view()), name='directory_delete'),
url(r'^calendar/create$', login_required(PostCalendar.as_view()), name='calendar_create'),
url(r'^calendar/edit/(?P<pk>\d+)/$', login_required(UpdateCalendar.as_view()), name='calendar_edit'),
url(r'^calendar/delete/(?P<pk>\d+)/$', login_required(DeleteCalendar.as_view()), name='calendar_delete'),
url(r'^document/$', login_required(panel_view), name='document'),
url(r'^notification/$', login_required(NotificationView), name='notification'),
url(r'^alert/$', login_required(AlertView), name='alert'),
url(r'^urgent/$', login_required(UrgentView), name='urgent'),
url(r'^allalert/$', login_required(AllalertView), name='allalert'),
url(r'^alerts/(?P<pk>\d+)/$', login_required(AlertsView), name='alert_view'),
url(r'^alerts/create$', login_required(AlertsCreate.as_view()), name='alert_create'),
url(r'^alerts/edit/(?P<pk>\d+)/$', login_required(AlertstEdit.as_view()), name='alert_edit'),
url(r'^alerts/delete/(?P<pk>\d+)/$', login_required(AlertsDelete.as_view()), name='alert_delete'),
url(r'^password/$', login_required(change_password), name='password'),
]