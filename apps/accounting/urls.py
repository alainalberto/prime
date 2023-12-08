from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from apps.accounting.views import *
from django.views.generic.dates import ArchiveIndexView
from apps.accounting.components.AccountingPDF import Receipt_pdf, Invoices_pdf

urlpatterns = [
    path('accounts/statistic/', login_required(AccountingPanel), name='panel_account'),

    # Account
    path('accounts/', login_required(permission_required('accounting.add_account')(AccountsViews)), name='accounts'),
    path('accounts/create/', login_required(permission_required('accounting.add_account')(AccountCreate.as_view())), name='account_create'),
    path('accounts/description/<int:pk>/', login_required(permission_required('accounting.add_accountdescrip')(AccountsDescViews)), name='account_descrip'),
    path('accounts/description/', login_required(permission_required('accounting.add_accountdescrip')(AccountsDescAllViews)), name='account_descripall'),
    path('accounts/document/<int:pk>/', login_required(permission_required('accounting')(AccountDocument)), name='account_document'),

    # Customers
    path('customers/', login_required(permission_required('accounting.add_customer')(CustomersView.as_view())), name='customers'),
    path('customers/create/', login_required(permission_required('accounting.add_customer')(CustomersCreate.as_view())), name='customer_create'),
    path('customers/edit/<int:pk>/', login_required(permission_required('accounting.change_customer')(CustomersEdit.as_view())), name='customer_edit'),
    path('customers/<int:pk>/', login_required(permission_required('accounting.delete_customer')(CustomersDelete.as_view())), name='customer_delete'),
    path('customers/view/<int:pk>/', login_required(permission_required('accounting.change_customer')(CustomerView)), name='customer_view'),
    path('customers/create/<str:popup>/', login_required(permission_required('accounting.add_customer')(CustomersCreate.as_view())), name='customer_popup'),

    # Receipts
    path('receipts/', login_required(permission_required('accounting.add_receipt')(ReceiptsView.as_view())), name='receipts'),
    path('receipts/view/<int:pk>/', login_required(permission_required('accounting.add_receipt')(ReceiptView)), name='receipts_view'),
    path('receipts/create/', login_required(permission_required('accounting.add_receipt')(ReceiptsCreate.as_view())), name='receipts_create'),
    path('receipts/edit/<int:pk>/', login_required(permission_required('accounting.change_receipt')(ReceiptsEdit.as_view())), name='receipts_edit'),
    path('receipts/<int:pk>/', login_required(permission_required('accounting.delete_receipt')(ReceiptsDelete.as_view())), name='receipts_delete'),
    path('receipts/print/<int:pk>/', login_required(permission_required('accounting.add_receipt')(Receipt_pdf)), name='receipts_pdf'),

    # Payments
    path('payments/', login_required(permission_required('accounting.add_payment')(PaymentViews)), name='payments'),
    path('payments/view/<int:pk>/', login_required(permission_required('accounting.add_payment')(PaymentView)), name='payments_view'),
    path('payments/print/<int:pk>/', login_required(permission_required('accounting.add_payment')(PaymentPrint)), name='payments_print'),
    path('payments/create/', login_required(permission_required('accounting.add_payment')(PaymentSelect)), name='create_payments'),
    path('payments/employee/<int:pk>&<str:start>&<str:end>/', login_required(permission_required('accounting.add_payment')(PaymentEmployeeCreate.as_view())), name='payments_employee'),
    path('payments/employee/edit/<int:pk>/', login_required(permission_required('accounting.change_payment')(PaymentEmployeeEdit.as_view())), name='payment_employee_edit'),
    path('payments/employee/<int:pk>/', login_required(permission_required('accounting.delete_payment')(PaymentEmployeeDelete.as_view())), name='payment_employee_delete'),
    path('payments/driver/<int:pk>&<str:start>&<str:end>/', login_required(permission_required('accounting.add_payment')(PaymentDriverCreate.as_view())), name='payments_driver'),
    path('payments/driver/edit/<int:pk>/', login_required(permission_required('accounting.change_payment')(PaymentDriverEdit.as_view())), name='payment_driver_edit'),
    path('payments/driver/<int:pk>/', login_required(permission_required('accounting.delete_payment')(PaymentDriverDelete.as_view())), name='payment_driver_delete'),
    path('payments/dispatch/<int:pk>&<str:start>&<str:end>/', login_required(permission_required('accounting.add_payment')(PaymentDispatchCreate.as_view())), name='payments_dispatch'),
    path('payments/dispatch/edit/<int:pk>/', login_required(permission_required('accounting.change_payment')(PaymentDispatchEdit.as_view())), name='payment_dispatch_edit'),
    path('payments/dispatch/<int:pk>/', login_required(permission_required('accounting.delete_payment')(PaymentDispatchDelete.as_view())), name='payment_dispatch_delete'),

    # Employees
    path('employees/', login_required(permission_required('accounting.add_employee')(EmployeesView.as_view())), name='employees'),
    path('employees/create/', login_required(permission_required('accounting.add_employee')(EmployeesCreate.as_view())), name='employees_create'),
    path('employees/edit/<int:pk>/', login_required(permission_required('accounting.change_employee')(EmployeesEdit.as_view())), name='employees_edit'),
    path('employees/<int:pk>/', login_required(permission_required('accounting.delete_employee')(EmployeesDelete.as_view())), name='employees_delete'),

    # Invoices
    path('invoices/', login_required(permission_required('accounting.add_invoice')(InvoicesView.as_view())), name='invoices'),
    path('invoices/create/', login_required(permission_required('accounting.add_invoice')(InvoicesCreate)), name='invoices_create'),
    path('invoices/edit/<int:pk>/', login_required(permission_required('accounting.change_invoice')(InvoicesEdit.as_view())), name='invoices_edit'),
    path('invoices/<int:pk>/', login_required(permission_required('accounting.delete_invoice')(InvoicesDelete.as_view())), name='invoices_delete'),
    path('invoices/print/<int:pk>/', login_required(permission_required('accounting.add_invoice')(Invoices_pdf)), name='invoices_pdf'),
    path('invoices/view/<int:pk>/', login_required(permission_required('accounting.add_invoice')(InvoiceView)), name='invoices_view'),

    # Customer Note
    path('customer/note/create/<int:pk>/', login_required(permission_required('accounting.add_note')(NoteCreate.as_view())), name='note_create'),
    path('customer/note/edit/<int:pk>/', login_required(permission_required('accounting.change_note')(NoteEdit.as_view())), name='note_edit'),
    path('customer/note/<int:pk>/', login_required(permission_required('accounting.delete_note')(NoteDelete.as_view())), name='note_delete'),
]