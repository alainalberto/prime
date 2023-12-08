from django.urls import include, path
from django.contrib.auth.decorators import login_required
from apps.tools.views import *

urlpatterns = [
    path('', login_required(panel_view), name='panel'),
    path('calendar/list/', login_required(GetCalendar), name='calendar_list'),
    path('calendar/', login_required(Calendar_Panel.as_view()), name='calendar'),
    path('directory/', login_required(DirectoryTelephone.as_view()), name='directory'),
    path('directory/create/', login_required(DirectoryTelephoneCreate.as_view()), name='directory_create'),
    path('directory/edit/<int:pk>/', login_required(DirectoryTelephoneEdit.as_view()), name='directory_edit'),
    path('directory/delete/<int:pk>/', login_required(DirectoryTelephoneDelete.as_view()), name='directory_delete'),
    path('calendar/create/', login_required(PostCalendar.as_view()), name='calendar_create'),
    path('calendar/edit/<int:pk>/', login_required(UpdateCalendar.as_view()), name='calendar_edit'),
    path('calendar/delete/<int:pk>/', login_required(DeleteCalendar.as_view()), name='calendar_delete'),
    path('document/', login_required(panel_view), name='document'),
    path('notification/', login_required(NotificationView), name='notification'),
    path('alert/', login_required(AlertView), name='alert'),
    path('urgent/', login_required(UrgentView), name='urgent'),
    path('allalert/', login_required(AllalertView), name='allalert'),
    path('alerts/<int:pk>/', login_required(AlertsView), name='alert_view'),
    path('confirms/<int:pk>/', login_required(AlertsNot), name='alert_deact'),
    path('alerts/create/', login_required(AlertsCreate.as_view()), name='alert_create'),
    path('alerts/edit/<int:pk>/', login_required(AlertstEdit.as_view()), name='alert_edit'),
    path('alerts/delete/<int:pk>/', login_required(AlertsDelete.as_view()), name='alert_delete'),
    path('password/', login_required(change_password), name='password'),
]