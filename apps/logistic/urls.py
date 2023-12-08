from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from apps.logistic.components.LogisticPDF import *
from apps.logistic.views import *

urlpatterns = [

    # Application
    path('', ApplicationCreate.as_view(), name='apply'),
    path('views/', login_required(permission_required('services.add_application')(ApplicationViews.as_view())), name='apply_views'),
    path('edit/<int:pk>/', login_required(permission_required('services.change_application')(ApplicationEdit.as_view())), name='apply_edit'),
    path('delete/<int:pk>/', login_required(permission_required('services.delete_application')(ApplicationDelete.as_view())), name='apply_delete'),

    # Invoices
    path('invoices/select', login_required(permission_required('services.add_dispatchload')(InvoicesLoadSelect)), name='create_select'),
    path('invoices/load', login_required(permission_required('accounting.add_invoice')(InvoicesLogView.as_view())), name='invoices_log'),
    path('invoices/load/create/<str:start>&<str:end>/', login_required(permission_required('accounting.add_invoice')(InvoicesLogCreate.as_view())),
        name='invoiceslog_create'),
    path('invoices/load/edit/<int:pk>&<str:bill>/', login_required(permission_required('accounting.change_invoice')(InvoicesLogEdit.as_view())),
        name='invoiceslog_edit'),
    path('invoices/load/<int:pk>/', login_required(permission_required('accounting.delete_invoice')(InvoicesLogDelete.as_view())),
        name='invoiceslog_delete'),
    path('invoices/load/print/<int:pk>/', login_required(permission_required('accounting.add_invoice')(InvoicesLod_pdf)), name='invoiceslog_pdf'),

    # Load
    path('loads/', login_required(permission_required('logistic.add_load')(LoadsView.as_view())), name='loads'),
    path('loads/create', login_required(permission_required('logistic.add_load')(LoadsCreate.as_view())), name='load_create'),
    path('loads/edit/<int:pk>/', login_required(permission_required('logistic.change_load')(LoadsEdit.as_view())), name='load_edit'),
    path('loads/<int:pk>/', login_required(permission_required('logistic.delete_load')(LoadsDelete.as_view())), name='load_delete'),
    path('loads/print/<int:pk>/', login_required(permission_required('logistic.add_load')(LoadPDF)), name='load_pdf'),

    # Driver
    path('drivers/', login_required(permission_required('logistic.add_driverslogt')(DriversView.as_view())), name='drivers'),
    path('drivers/create', login_required(permission_required('logistic.add_driverslogt')(DriversCreate.as_view())), name='drivers_create'),
    path('drivers/edit/<int:pk>/', login_required(permission_required('logistic.change_driverslogt')(DriversEdit.as_view())), name='drivers_edit'),
    path('drivers/<int:pk>/', login_required(permission_required('logistic.delete_driverslogt')(DriversDelete.as_view())), name='drivers_delete'),

    # Dispatch
    path('dispatch/', login_required(permission_required('logistic.add_dispatchlogt')(DispatchView.as_view())), name='dispatch'),
    path('dispatch/create', login_required(permission_required('logistic.add_dispatchlogt')(DispatchCreate.as_view())), name='dispatch_create'),
    path('dispatch/edit/<int:pk>/', login_required(permission_required('logistic.change_dispatchlogt')(DispatchEdit.as_view())), name='dispatch_edit'),
    path('dispatch/<int:pk>/', login_required(permission_required('logistic.delete_dispatchlogt')(DispatchDelete.as_view())), name='dispatch_delete'),

    # Diesel
    path('diesel/', login_required(permission_required('logistic.add_diesel')(DieselView.as_view())), name='diesel'),
    path('diesel/create', login_required(permission_required('logistic.add_diesel')(DieselCreate.as_view())), name='diesel_create'),
    path('diesel/edit/<int:pk>/', login_required(permission_required('logistic.change_diesel')(DieselEdit.as_view())), name='diesel_edit'),
    path('diesel/<int:pk>/', login_required(permission_required('logistic.delete_diesel')(DieselDelete.as_view())), name='diesel_delete'),

    path('trucks/', login_required(), name='trucks'),
    path('travel/', login_required(), name='travel'),
    path('infcompany/', login_required(), name='infcompany'),
]