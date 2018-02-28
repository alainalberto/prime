from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.logistic.components.LogisticPDF import *
from apps.logistic.views import *

urlpatterns = [

    #Application
    url(r'^$', ApplicationCreate.as_view(), name='apply'),
    url(r'^views/$', login_required(permission_required('services.add_application')(ApplicationViews.as_view())), name='apply_views'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_application')(ApplicationEdit.as_view())), name='apply_edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(permission_required('services.delete_application')(ApplicationDelete.as_view())), name='apply_delete'),


    # Load
    url(r'^loads/$', login_required(permission_required('logistic.add_load')(LoadsView.as_view())), name='loads'),
    url(r'^loads/create$', login_required(permission_required('logistic.add_load')(LoadsCreate.as_view())), name='load_create'),
    url(r'^loads/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_load')(LoadsEdit.as_view())), name='load_edit'),
    url(r'^loads/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_load')(LoadsDelete.as_view())), name='load_delete'),
    url(r'^loads/print/(?P<pk>\d+)/$', login_required(permission_required('logistic.add_load')(LoadPDF)), name='load_pdf'),

    # Driver
    url(r'^drivers/$', login_required(permission_required('logistic.add_driverslogt')(DriversView.as_view())), name='drivers'),
    url(r'^drivers/create$', login_required(permission_required('logistic.add_driverslogt')(DriversCreate.as_view())), name='drivers_create'),
    url(r'^drivers/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_driverslogt')(DriversEdit.as_view())), name='drivers_edit'),
    url(r'^drivers/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_driverslogt')(DriversDelete.as_view())), name='drivers_delete'),

    #Dispatch
    url(r'^dispatch/$', login_required(permission_required('logistic.add_dispatchlogt')(DispatchView.as_view())), name='dispatch'),
    url(r'^dispatch/create$', login_required(permission_required('logistic.add_dispatchlogt')(DispatchCreate.as_view())), name='dispatch_create'),
    url(r'^dispatch/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_dispatchlogt')(DispatchEdit.as_view())), name='dispatch_edit'),
    url(r'^dispatch/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_dispatchlogt')(DispatchDelete.as_view())), name='dispatch_delete'),

    #Diesel
    url(r'^diesel/$', login_required(permission_required('logistic.add_diesel')(DieselView.as_view())), name='diesel'),
    url(r'^diesel/create$', login_required(permission_required('logistic.add_diesel')(DieselCreate.as_view())), name='diesel_create'),
    url(r'^diesel/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_diesel')(DieselEdit.as_view())), name='diesel_edit'),
    url(r'^diesel/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_diesel')(DieselDelete.as_view())), name='diesel_delete'),

    url(r'^trucks/$', login_required(), name='trucks'),
    url(r'^travel/$', login_required(), name='travel'),
    url(r'^infcompany/$', login_required(), name='infcompany'),
]