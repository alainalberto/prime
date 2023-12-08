from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *
from apps.services.components.ServicePDF import *

urlpatterns = [
    path('service/pending/', login_required(PendingListPDF), name='pending_pdf'),
    path('service/select/<int:pk>/', login_required(SelectView), name='service_select'),
    path('email/<int:pk>&<str:fl>/', login_required(EmailSend), name='email_send'),
    path('email/<int:pk>/', login_required(Email), name='email_send'),

    # Permit
    path('permit/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_permit')(PermitView)), name='permit'),
    path('permit/create/', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create'),
    path('permit/create/<int:pk>/', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create'),
    path('permit/edit/<int:pk>/', login_required(permission_required('services.change_permit')(PermitEdit.as_view())), name='permit_edit'),
    path('permit/<int:pk>/', login_required(permission_required('services.delete_permit')(PermitDelete.as_view())), name='permit_delete'),

    # Forms
    path('forms/', login_required(FormView.as_view()), name='forms'),
    path('forms/create/', login_required(permission_required('tools.add_file')(FormCreate.as_view())), name='file_create'),
    path('forms/edit/<int:pk>/', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit'),
    path('forms/<int:pk>/', login_required(permission_required('tools.delete_file')(FormDelete.as_view())), name='file_delete'),

    # Folder
    path('folder/', login_required(permission_required('tools.add_file')(FolderView.as_view())), name='folder'),
    path('folder/create/', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    path('folder/create/<int:pk>/', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    path('folder/edit/<int:pk>/', login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit'),
    path('folder/<int:pk>/', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete'),

    # Equipment
    path('equipment/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_equipment')(EquipmentView)), name='equipment'),
    path('equipment/create/', login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())), name='equipment_create'),
    path('equipment/create/<int:pk>/', login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())), name='equipment_create'),
    path('equipment/edit/<int:pk>/', login_required(permission_required('services.change_equipment')(EquipmentEdit.as_view())), name='equipment_edit'),
    path('equipment/<int:pk>/', login_required(permission_required('services.delete_equipment')(EquipmentDelete.as_view())), name='equipment_delete'),

    # Insurance
    path('insurance/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_insurance')(InsuranceView)), name='insurance'),
    path('insurance/create/', login_required(permission_required('services.add_insurance')(InsuranceCreate.as_view())), name='insurance_create'),
    path('insurance/create/<int:pk>/', login_required(permission_required('services.add_insurance')(InsuranceCreate.as_view())), name='insurance_create'),
    path('insurance/edit/<int:pk>/', login_required(permission_required('services.change_insurance')(InsuranceEdit.as_view())), name='insurance_edit'),
    path('insurance/<int:pk>/', login_required(permission_required('services.delete_insurance')(InsuranceDelete.as_view())), name='insurance_delete'),

    # Driver
    path('driver/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_driver')(DriverView)), name='driver'),
    path('driver/create/', login_required(permission_required('services.add_driver')(DriverCreate.as_view())), name='driver_create'),
    path('driver/create/<int:pk>/', login_required(permission_required('services.add_driver')(DriverCreate.as_view())), name='driver_create'),
    path('driver/edit/<int:pk>/', login_required(permission_required('services.change_driver')(DriverEdit.as_view())), name='driver_edit'),
    path('driver/<int:pk>/', login_required(permission_required('services.delete_driver')(DriverDelete.as_view())), name='driver_delete'),

    # Ifta
    path('ifta/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_ifta')(IftaView)), name='ifta'),
    path('ifta/create/', login_required(permission_required('services.add_ifta')(IftaCreate.as_view())), name='ifta_create'),
    path('ifta/create/<int:pk>/', login_required(permission_required('services.add_ifta')(IftaCreate.as_view())), name='ifta_create'),
    path('ifta/edit/<int:pk>/', login_required(permission_required('services.change_ifta')(IftaEdit.as_view())), name='ifta_edit'),
    path('ifta/<int:pk>/', login_required(permission_required('services.delete_ifta')(IftaDelete.as_view())), name='ifta_delete'),

    # Audit
    path('audit/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_audit')(AuditView)), name='audit'),
    path('audit/create/', login_required(permission_required('services.add_audit')(AuditCreate.as_view())), name='audit_create'),
    path('audit/create/<int:pk>/', login_required(permission_required('services.add_audit')(AuditCreate.as_view())), name='audit_create'),
    path('audit/edit/<int:pk>/', login_required(permission_required('services.change_audit')(AuditEdit.as_view())), name='audit_edit'),
    path('audit/<int:pk>/', login_required(permission_required('services.delete_audit')(AuditDelete.as_view())), name='audit_delete'),

    # Contract
    path('contract/view/<int:pk>&<str:popup>/', login_required(permission_required('services.add_contract')(ContractView)), name='contract'),
    path('contract/create/', login_required(permission_required('services.add_contract')(ContractCreate.as_view())), name='contract_create'),
    path('contract/create/<int:pk>/', login_required(permission_required('services.add_contract')(ContractCreate.as_view())), name='contract_create'),
    path('contract/edit/<int:pk>/', login_required(permission_required('services.change_contract')(ContractEdit.as_view())), name='contract_edit'),
    path('contract/<int:pk>/', login_required(permission_required('services.delete_contract')(ContractDelete.as_view())), name='contract_delete'),

    # Companies Dispatch
    path('dispatch/select/', login_required(permission_required('services.add_dispatchload')(CompanyLoadSelect)), name='dispatch_select'),
    path('dispatch/select/<int:pk>/', login_required(permission_required('services.add_dispatchload')(CompanyLoadSelectCoust)), name='dispatch_select_coust'),
    path('dispatch/invoice/create/<int:pk>&<str:start>&<str:end>/', login_required(permission_required('services.add_dispatchload')(InvoicesLogCreate.as_view())), name='dispatch_invoice_create'),
    path('dispatch/invoice/edit/<int:pk>&<str:bill>/', login_required(permission_required('services.change_dispatchload')(InvoicesLogEdit.as_view())), name='dispatch_invoice_edit'),
    path('dispatch/invoices/<int:pk>/', login_required(permission_required('services.delete_dispatchload')(InvoicesLogDelete.as_view())), name='dispatch_invoice_delete'),
    path('dispatch/invoices/print/<int:pk>/', login_required(permission_required('services.add_dispatchload')(InvoicesLog)), name='dispatch_invoice_pdf'),

    # Service Application
    path('application/newcustomer/', login_required(permission_required('services.add_processaplic')(CustomerAplicView.as_view())), name='customer_aplic'),
    path('application/process/<int:pk>/', login_required(permission_required('services.add_processaplic')(CustomerAplicProce)), name='customer_process'),
    path('application/process/<int:pk>&<str:popup>/', login_required(permission_required('services.add_processaplic')(CustomerProce)), name='customer_view'),
]