from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *
from apps.services.components.ServicePDF import *

urlpatterns = [

    url(r'^service/pending/$', login_required((PendingListPDF)),name='pending_pdf'),
    url(r'^email/(?P<pk>\d+)&(?P<fl>[^/]+)/$', login_required((EmailSend)),name='email_send'),

    #Permit
    url(r'^permit/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_permit')(PermitView)), name='permit'),
    url(r'^permit/create$', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create'),
    url(r'^permit/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create_popup'),
    url(r'^permit/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_permit')(PermitEdit.as_view())), name='permit_edit'),
    url(r'^permit/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_permit')(PermitEdit.as_view())), name='permit_edit_popup'),
    url(r'^permit/(?P<pk>\d+)/$', login_required(permission_required('services.delete_permit')(PermitDelete.as_view())), name='permit_delete'),

    #Forms
    url(r'^forms/$', login_required(FormView.as_view()), name='forms'),
    url(r'^forms/create$', login_required(permission_required('tools.add_file')(FormCreate.as_view())), name='file_create'),
    url(r'^forms/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit'),
    url(r'^forms/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit_popup'),
    url(r'^forms/(?P<pk>\d+)/$', login_required(permission_required('tools.delete_file')(FormDelete.as_view())), name='file_delete'),

    #Folder
    url(r'^folder/$', login_required(permission_required('tools.add_file')(FolderView.as_view())), name='folder'),
    url(r'^folder/create$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    url(r'^folder/create/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create_popup'),
    url(r'^folder/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit'),
    url(r'^folder/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit_popup'),
    url(r'^folder/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete'),

    #Equipment
    url(r'^equipment/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_equipment')(EquipmentView)), name='equipment'),
    url(r'^equipment/create$', login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())), name='equipment_create'),
    url(r'^equipment/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$',
        login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())), name='equipment_create_popup'),
    url(r'^equipment/edit/(?P<pk>\d+)/$',
        login_required(permission_required('services.change_equipment')(EquipmentEdit.as_view())), name='equipment_edit'),
    url(r'^equipment/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',
        login_required(permission_required('services.change_equipment')(EquipmentEdit.as_view())), name='equipment_edit_popup'),
    url(r'^equipment/(?P<pk>\d+)/$', login_required(permission_required('services.delete_equipment')(EquipmentDelete.as_view())),
        name='equipment_delete'),
    #Insurance
    url(r'^insurance/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_insurance')(InsuranceView)), name='insurance'),
    url(r'^insurance/create$', login_required(permission_required('services.add_insurance')(InsuranceCreate.as_view())), name='insurance_create'),
    url(r'^insurance/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_insurance')(InsuranceEdit.as_view())), name='insurance_edit'),
    url(r'^insurance/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_insurance')(InsuranceEdit.as_view())), name='insurance_edit'),
    url(r'^insurance/(?P<pk>\d+)/$', login_required(permission_required('services.delete_insurance')(InsuranceDelete.as_view())), name='insurance_delete'),

    #Driver
    url(r'^driver/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.add_driver')(DriverView)), name='driver'),
    url(r'^driver/create$', login_required(permission_required('services.add_driver')(DriverCreate.as_view())),name='driver_create'),
    url(r'^driver/edit/(?P<pk>\d+)/$',login_required(permission_required('services.change_driver')(DriverEdit.as_view())),name='driver_edit'),
    url(r'^driver/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.change_driver')(DriverEdit.as_view())),name='driver_edit'),
    url(r'^driver/(?P<pk>\d+)/$',login_required(permission_required('services.delete_driver')(DriverDelete.as_view())),name='driver_delete'),

    #Ifta
    url(r'^ifta/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.add_ifta')(IftaView)), name='ifta'),
    url(r'^ifta/create$', login_required(permission_required('services.add_ifta')(IftaCreate.as_view())), name='ifta_create'),
    url(r'^ifta/edit/(?P<pk>\d+)/$',login_required(permission_required('services.change_ifta')(IftaEdit.as_view())), name='ifta_edit'),
    url(r'^ifta/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.change_ifta')(IftaEdit.as_view())), name='ifta_edit'),
    url(r'^ifta/(?P<pk>\d+)/$', login_required(permission_required('services.delete_ifta')(IftaDelete.as_view())), name='ifta_delete'),

    #Audit
    url(r'^audit/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.add_audit')(AuditView)), name='audit'),
    url(r'^audit/create$', login_required(permission_required('services.add_audit')(AuditCreate.as_view())),name='audit_create'),
    url(r'^audit/edit/(?P<pk>\d+)/$',login_required(permission_required('services.change_audit')(AuditEdit.as_view())),name='audit_edit'),
    url(r'^audit/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.change_audit')(AuditEdit.as_view())),name='audit_edit'),
    url(r'^audit/(?P<pk>\d+)/$',login_required(permission_required('services.delete_audit')(AuditDelete.as_view())),name='audit_delete'),

    #Contract
    url(r'^contract/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.add_contract')(ContractView)), name='contract'),
    url(r'^contract/create$', login_required(permission_required('services.add_contract')(ContractCreate.as_view())),name='contract_create'),
    url(r'^contract/edit/(?P<pk>\d+)/$',login_required(permission_required('services.change_contract')(ContractEdit.as_view())),name='contract_edit'),
    url(r'^contract/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('services.change_contract')(ContractEdit.as_view())),name='contract_edit'),
    url(r'^contract/(?P<pk>\d+)/$',login_required(permission_required('services.delete_contract')(ContractDelete.as_view())),name='contract_delete'),

    #Companies Dispatch
    url(r'^dispatch/select$', login_required(permission_required('services.add_dispatch')(CompanyLoadSelect)),name='dispatch_select'),
    url(r'^dispatch/invoice/loads/(?P<pk>\d+)&(?P<start>[^/]+)&(?P<end>[^/]+)/$', login_required(permission_required('services.add_dispatch')(InvoicesLogCreate)), name='dispatch_loads'),



]