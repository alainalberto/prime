from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.forms import modelform_factory, inlineformset_factory, formset_factory, BaseModelFormSet
from django.contrib import messages
from Prime.util import accion_user
from apps.accounting.components.AccountingForm import *
from apps.accounting.models import *
from apps.accounting.components.AccountingPDF import PayDriverPDF, PayDispatchPDF, PayEmployeePDF
from apps.logistic.models import Load, DispatchHasPayment, DriversHasPayment, LoadsHasFee, InvoicesHasLoad, DriversLogt, DispatchLogt, Diesel, PaymentHasLoad, CustomerHasLoad
from apps.services.components.ServicesForm import *
from apps.tools.components.AlertForm import AlertForm
from apps.services.models import *
from apps.tools.models import Folder, Alert
from datetime import datetime, date, time, timedelta
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
# Create your views here.

def pagination(request, objects):
    paginator = Paginator(objects, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
    return objs


def AccountingPanel(request):
    incomes = []
    expenses = []
    balance = []
    balance_total = []
    account_business = []
    cash_i_total = {'total': 0}
    credit_i_total = {'total': 0}
    check_i__total = {'total': 0}
    cash_e_total = {'total': 0}
    credit_e_total = {'total': 0}
    check_e__total = {'total': 0}
    income_total = {'total': 0}
    expenses_total = {'total': 0}
    business = Busines.objects.filter(deactivated=False)
    inc_list = Account.objects.filter(primary=False, accounts_id=1)
    exp_list = Account.objects.filter(primary=False, accounts_id=2)

    for i in inc_list:
        cash_i = {'total': 0}
        credit_i = {'total': 0}
        check_i = {'total': 0}

        if AccountDescrip.objects.filter(accounts_id=i.id_acn, waytopay='Cash'):
            cash_i = AccountDescrip.objects.get_waytopay('Cash', i.id_acn)
        if AccountDescrip.objects.filter(accounts_id=i.id_acn, waytopay='Check'):
            check_i = AccountDescrip.objects.get_waytopay('Check', i.id_acn)
        if AccountDescrip.objects.filter(accounts_id=i.id_acn, waytopay='Credit Card'):
            credit_i = AccountDescrip.objects.get_waytopay('Credit Card', i.id_acn)
        total_i = (cash_i['total']) + (check_i['total']) + (credit_i['total'])
        incomes.append({'account': i, 'cash': cash_i, 'check': check_i, 'credit': credit_i, 'total': total_i})
        cash_i_total['total'] += cash_i['total']
        credit_i_total['total'] += credit_i['total']
        check_i__total['total'] += check_i['total']
        income_total['total'] = (cash_i_total['total']) + (credit_i_total['total']) + (check_i__total['total'])
    for e in exp_list:
        credit_e = {'total': 0}
        cash_e = {'total': 0}
        check_e = {'total': 0}
        if AccountDescrip.objects.filter(accounts_id=e.id_acn, waytopay='Cash'):
            cash_e = AccountDescrip.objects.get_waytopay('Cash', e.id_acn)
        if AccountDescrip.objects.filter(accounts_id=e.id_acn, waytopay='Check'):
            check_e = AccountDescrip.objects.get_waytopay('Check', e.id_acn)
        if AccountDescrip.objects.filter(accounts_id=e.id_acn, waytopay='Credit Card'):
            credit_e = AccountDescrip.objects.get_waytopay('Credit Card', e.id_acn)
        total_e = (cash_e['total']) + (check_e['total']) + (credit_e['total'])
        expenses.append({'account': e, 'cash': cash_e, 'check': check_e, 'credit': credit_e, 'total': total_e})
        cash_e_total['total'] += cash_e['total']
        credit_e_total['total'] += credit_e['total']
        check_e__total['total'] += check_e['total']
        expenses_total['total'] = (cash_e_total['total']) + (credit_e_total['total']) + (check_e__total['total'])

    for bus in business:
        inc = 0
        exp = 0
        for i in inc_list:
               if i.business == bus:
                  for desc in AccountDescrip.objects.filter(accounts_id=i.id_acn):
                        inc += desc.value
        for e in exp_list:
                if e.business == bus:
                    for desc in AccountDescrip.objects.filter(accounts_id=e.id_acn):
                        exp += desc.value
        ear = inc - exp
        balance.append({'incomes':inc, 'expenses':exp, 'earning':ear, 'business':bus})


    for bus in business:
        i_account = []
        i_total = 0
        e_account = []
        e_total = []
        if inc_list:
               for i in inc_list:
                  if i.business_id == bus.id_bus:
                     for desc in AccountDescrip.objects.filter(accounts_id=i.id_acn):
                        for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                          date = desc.date
                          value_total = 0
                          if date.month == month:
                              value_total += desc.value
                          i_account.append({'account':i, 'month':month, 'value':value_total})
        if exp_list:
               for e in exp_list:
                   if e.business_id == bus.id_bus:
                       for desc in AccountDescrip.objects.filter(accounts_id=e.id_acn):
                          for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                            date = desc.date
                            value_total = 0
                            if date.month == month:
                                value_total += desc.value
                            e_account.append({'account': e, 'month': month, 'value': value_total})


        account_business.append({'incomes':i_total, 'expenses':e_total, 'earning':0, 'business':bus.id_bus})




    context = {
        'incomes': incomes,
        'expenses': expenses,
        'cash_i_total': cash_i_total,
        'credit_i_total': credit_i_total,
        'check_i_total': check_i__total,
        'cash_e_total': cash_e_total,
        'credit_e_total': credit_e_total,
        'check_e_total': check_e__total,
        'expenses_total': expenses_total,
        'income_total': income_total,
        'earning_total': (income_total['total'] - expenses_total['total']),
        'expenses_total_j': json.dumps(float(expenses_total['total'])),
        'income_total_j': json.dumps(float(income_total['total'])),
        'earning_total_J': json.dumps(float(income_total['total'] - expenses_total['total'])),
        'business': business,
        'balance':  balance,
        'balance_total':balance_total,
        'account_business':account_business
    }
    return render(request, 'accounting/statistic/principalPanel.html', context)
#Account
class AccountCreate(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Account'})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
           account = form.save(commit=False)
           account.users = user
           account.save()
           messages.success(request,"Account saved with an extension")
           accion_user(account, ADDITION, request.user)
           return HttpResponseRedirect(reverse_lazy('accounting:accounts'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)

def AccountsViews(request):
    primary = Account.objects.filter(primary=True)
    lisexp = Account.objects.filter(primary=False)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(request, 'accounting/accounts/accountsViews.html', contexto)


def AccountsDescViews(request, pk):
    contexto = {}
    accounts = AccountDescrip.objects.filter(accounts_id=pk)
    if accounts:
        contexto = {'accounts': accounts}
    return render(request, 'accounting/accounts/accountsDescrp.html', contexto)

def AccountsDescAllViews(request):
    contexto = {}
    accounts = AccountDescrip.objects.all()
    if accounts:
        contexto = {'accounts': accounts}
    return render(request, 'accounting/accounts/accountsDescrp.html', contexto)

def AccountDocument(request, pk):
    accountDescrp = AccountDescrip.objects.get(id_acd=pk)
    if accountDescrp:
        if accountDescrp.type:
            return redirect('/accounting/'+accountDescrp.type.lower()+'/view/'+str(accountDescrp.document)+'/')
    return redirect('accounting:accounts')

# Customers
def CustomerView(request, pk):
       customer = Customer.objects.get(id_cut=pk)
       permit = Permit.objects.filter(customers=customer)
       insurance = Insurance.objects.filter(customers=customer)
       equipment = Equipment.objects.filter(customers=customer)
       ifta = Ifta.objects.filter(customers=customer)
       contract = Contract.objects.filter(customers=customer)
       audit = Audit.objects.filter(customers=customer)
       dispatch = DispatchLoad.objects.filter(customers=customer)
       driver = Driver.objects.filter(customers=customer)
       files = File.objects.filter(folders=customer.folders).order_by('category')
       date_now = datetime.now().date()
       alert = CustomerHasAlert.objects.filter(customers=customer)
       note = Note.objects.filter(customers=customer)
       context = {
           'customer': customer,
           'files': files,
           'categories': ['Company', 'Insurance', 'COI', 'Quote', 'Accidents', 'Endorsments', 'Misselenious'],
           'permits': permit,
           'insurances': insurance,
           'equipments': equipment,
           'contracts': contract,
           'iftas': ifta,
           'driver': driver,
           'audits': audit,
           'dispatch': dispatch,
           'notes': note,
           'alert': pagination(request, alert),
           'permit_pending': Permit.objects.is_state('Pending', customer),
           'equipment_pending': Equipment.objects.is_state('Pending', customer),
           'insurance_pending': Insurance.objects.is_state('Pending', customer),
           'ifta_pending': Ifta.objects.is_state('Pending', customer),
           'contract_pending': Contract.objects.is_state('Pending', customer),
           'audit_pending': Audit.objects.is_state('Pending', customer),
           'driver_pending': Driver.objects.is_state('Pending', customer),
           'dispatch_pending': DispatchLoad.objects.filter(customers=customer, paid=False).count(),
           'title': 'Customer Folder',
           'date_now': date_now
       }
       return render(request, 'accounting/customer/customerView.html', context)

class CustomersView(ListView):
    model = Customer
    template_name = 'accounting/customer/customerViews.html'

    def get(self, request, *args, **kwargs):
        customer = self.model.objects.all().order_by('company_name')
        context ={'title': 'List Customer', 'object_list': customer}
        return render(request, self.template_name, context)

class CustomersCreate(CreateView):
     model = Customer
     form_class = CustomerForm
     template_name = 'accounting/customer/customerViews.html'
     success_url = reverse_lazy('accounting:customers')

     def get(self, request, *args, **kwargs):
         if kwargs.__contains__('popup'):
             popup = kwargs['popup']
         else:
             popup = 0
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create new Customer'})

     def post(self, request, *args, **kwargs):
         """user = User.objects.filter(username=request.POST['email'])
            if user_exist:
              user = User.objects.get(username=request.POST['email'])
            else:
                user = User.objects.create_user(username=request.POST['email'],email=request.POST['email'], password=request.POST['phone'],  is_staff=False, is_active=True)"""
         if kwargs.__contains__('popup'):
             popup = kwargs['popup']
         else:
             popup = 0
         form = self.form_class(request.POST)
         if form.is_valid():
             customer_exist = Customer.objects.filter(email=form.data['email'], fullname=form.data['fullname'])
             if customer_exist:
                 messages.error(request,'The customer already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create new Customer'})
             else:
                 folder = Folder.objects.create(name=form.data['fullname'] + "_Customer",
                                                description=form.data['fullname'] + "_Customer",
                                                )
                 customer = form.save(commit=False)
                 customer.folders_id = folder.id_fld
                 customer.users_id = request.user.id
                 if customer.deactivated:
                     customer.date_deactivated = datetime.now().strftime("%Y-%m-%d")
                 customer.save()
                 customer.business = self.request.POST.getlist('business')
                 accion_user(customer, ADDITION, request.user)
                 messages.success(request,'The customer was saved successfully')
                 return HttpResponseRedirect(self.success_url)
         else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'is_popup': popup,  'title': 'Create new Customer'})


class CustomersEdit(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerViews.html'
    success_url = reverse_lazy('accounting:customers')

    def get_context_data(self, **kwargs):
        context = super(CustomersEdit, self).get_context_data(**kwargs)
        if kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        customer = Customer.objects.get(id_cut=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=customer)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Customer'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cut = kwargs['pk']
        customer = self.model.objects.get(id_cut=id_cut)
        form = self.form_class(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            if customer.deactivated:
                customer.date_deactivated = datetime.today().strftime("%Y-%m-%d")
            else:
                customer.date_deactivated = None
            customer.save()
            customer.business = self.request.POST.getlist('business')
            accion_user(customer, CHANGE, request.user)
            messages.success(request, 'The customer was update successfully')
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Customer'})


class CustomersDelete(DeleteView):
    model = Customer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cut = kwargs['pk']
        customer = self.model.objects.get(id_cut=id_cut)
        Audit.objects.filter(customers=customer).delete()
        Contract.objects.filter(customers=customer).delete()
        Driver.objects.filter(customers=customer).delete()
        Equipment.objects.filter(customers=customer).delete()
        Ifta.objects.filter(customers=customer).delete()
        Insurance.objects.filter(customers=customer).delete()
        folder = Folder.objects.get(id_fld=customer.folders_id)
        File.objects.filter(folders_id=folder.id_fld).delete()
        load = CustomerHasLoad.objects.filter(customers=customer)
        for l in load:
            Load.objects.filter(id_lod=l.id_lod).delete()
        load.delete()
        alerts = CustomerHasAlert.objects.filter(customers=customer)
        for a in alerts:
            Alert.objects.filter(id_alr=a.alert.id_alt).delete()
            a.delete()
        accion_user(customer, DELETION, request.user)
        customer.delete()
        messages.success(request, 'The customer was delete successfully')
        return HttpResponseRedirect(self.success_url)


#Employees

class EmployeesView(ListView):
    model = Employee
    template_name = 'accounting/employees/employeesViews.html'

class EmployeesCreate(CreateView):
     model = Employee
     form_class = EmployeesForm
     template_name = 'accounting/employees/employeesForm.html'
     success_url = reverse_lazy('accounting:employees')

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             employee_exist = Employee.objects.filter(email=form.data['email'], social_no=form.data['social_no'])
             if employee_exist:
                 messages.error(request, 'The employee already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})
             else:
               employee=form.save(commit=False)
               if employee.deactivated:
                   employee.date_deactivated = datetime.now().strftime("%Y-%m-%d")
               else:
                   employee.date_deactivated = None
               employee.save()
               accion_user(employee, ADDITION, request.user)
               messages.success(request, 'The employee was saved successfully')
               return HttpResponseRedirect(self.success_url)
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})


class EmployeesEdit(UpdateView):
    model = Employee
    form_class = EmployeesForm
    template_name = 'accounting/employees/employeesForm.html'
    success_url = reverse_lazy('accounting:employees')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_emp = kwargs['pk']
        employee = self.model.objects.get(id_emp=id_emp)
        form = self.form_class(request.POST, instance=employee)
        if form.is_valid():
            employee =form.save(commit=False)
            if employee.deactivated:
                employee.date_deactivated = datetime.now().strftime("%Y-%m-%d")
            else:
                employee.date_deactivated = None
            employee.save()
            accion_user(employee, CHANGE, request.user)
            messages.success(request, "Employee update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit new Employee'})

class EmployeesDelete(DeleteView):
    model = Employee
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:employees')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_emp = kwargs['pk']
        employee = self.model.objects.get(id_emp=id_emp)
        accion_user(employee, DELETION, request.user)
        employee.delete()
        messages.success(request, "Employee delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Invoices
class InvoicesView(ListView):
    model = Invoice
    template_name = 'accounting/invoices/invoicesViews.html'

    def get_context_data(self, **kwargs):
        context = super(InvoicesView, self).get_context_data(**kwargs)
        invoice = self.model.objects.filter(type='service').order_by('-start_date')
        context['title'] = 'List Invoices'
        context['object_list'] = invoice
        return context


def InvoiceView(request, pk):
        invoice = Invoice.objects.get(id_inv=pk)
        invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
        items = Item.objects.all()
        InvLod = InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv)
        loads = []
        for d in InvLod:
            loads.append(Load.objects.get(id_lod=d.loads_id))
        context = {'invoice': invoice,
                   'invitems': invitem,
                    'id': pk,
                    'items' :items,
                    'description': loads,
                    'title': 'Invoice',
                   }
        return render(request,'accounting/invoices/invoicesView.html', context)

def InvoicesCreate(request):
    ItemFormSet = inlineformset_factory(
                          Invoice,
                          InvoicesHasItem,
                          form=ItemHasInvoiceForm,
                          fields=['quantity',
                                  'description',
                                  'accounts',
                                  'value',
                                  'tax',
                                  'subtotal'],
                          extra=10
    )

    form = InvoicesForm()
    formset = ItemFormSet()
    items = Item.objects.all()
    customer = Customer.objects.filter(deactivated=False)
    accounts = []
    inc = Account.objects.get(primary=True, name='Income')
    inc_acconts = Account.objects.filter(accounts_id_id=inc.id_acn)
    for i in inc_acconts:
        accounts.append(i)
    for a in inc_acconts:
        exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
        if exp_accont != None:
            for ac in exp_accont:
                accounts.append(ac)
    if request.method == 'POST':
        form = InvoicesForm(request.POST)
        formset = ItemFormSet(request.POST)
        user = request.user
        invs = Invoice.objects.filter(business_id=form.data['business']).order_by('-serial')
        serial = 1
        serials = []
        for s in invs:
            serials.append(s.serial)
        if form.is_valid() and formset.is_valid():
            if serials:
                serial = int(serials[0]) + 1
            invoice = form.save(commit=False)
            invoice.customers = Customer.objects.get(id_cut=request.POST['customers'])
            invoice.serial = serial
            invoice.users_id = user.id
            invoice.type = 'service'
            accion_user(invoice, ADDITION, request.user)
            itemhasInv = formset.save(commit=False)
            if not itemhasInv:
                messages.error(request, "ERROR: Insert one Items ")
                return render(request, 'accounting/invoices/invoicesForm.html', {
                        'form': form,
                        'formset': formset,
                        'items': items,
                        'accounts': accounts,
                        'customers': customer,
                        'title': 'Create new Invoice'
                    })
            else:
                invoice.save()
                for itinv in itemhasInv:
                    if Item.objects.filter(name=itinv.description, value=itinv.value):
                         item = Item.objects.get(name=itinv.description, value=itinv.value)
                    else:
                        item = Item.objects.create(name=itinv.description, accounts=itinv.accounts, value=itinv.value)
                    itinv.items_id = item.id_ite
                    itinv.invoices = invoice
                    itinv.save()
                    if invoice.paid:
                       AccountDescrip.objects.create(date=invoice.start_date,
                                                                  value=itinv.subtotal,
                                                                  accounts_id=itinv.accounts_id,
                                                                  document=invoice.id_inv,
                                                                  waytopay=invoice.waytopay,
                                                                  users_id=user.id,
                                                                  type='Invoices')
            messages.success(request, "Invoice saved with an extension")

            return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
        else:
            for er in form.errors:
                messages.error(request, er)
            for er in formset.errors:
                messages.error(request, er)

    return render(request, 'accounting/invoices/invoicesForm.html', {
        'form': form,
        'formset': formset,
        'items': items,
        'accounts': accounts,
        'customers': customer,
        'title': 'Create new Invoice'
    })

class ItemInlineFormSet(BaseModelFormSet):
    def clean(self):
        super(ItemInlineFormSet, self).clean()

        for form in self.forms:
            name = form.cleaned_data['name'].upper()
            form.cleaned_data['name'] = name
            # update the instance value.
            form.instance.name = name

class InvoicesEdit(UpdateView):
    model = Invoice
    sec_model = InvoicesHasItem
    template_name = 'accounting/invoices/invoicesForm.html'
    form_class = InvoicesForm
    form_class_item = inlineformset_factory(
                          Invoice,
                          InvoicesHasItem,
                          form=ItemHasInvoiceForm,
                          fields=['id_ind',
                                  'quantity',
                                  'description',
                                  'accounts',
                                  'value',
                                  'tax',
                                  'subtotal'],
                          extra=3
    )

    def get_context_data(self, **kwargs):
        context = super(InvoicesEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        invoice = self.model.objects.get(id_inv=pk)
        items = Item.objects.all()
        loads = Load.objects.all().order_by('number')
        customer = Customer.objects.all()
        accounts = []
        inv = Account.objects.get(primary=True, name='Income')
        inv_acconts = Account.objects.filter(accounts_id_id=inv.id_acn)
        for e in inv_acconts:
         accounts.append(e)
         for a in inv_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
               for ac in exp_accont:
                  accounts.append(ac)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'formset' not in context:
            context['formset'] = self.form_class_item(instance=invoice)

        context['id'] = pk
        context['invoice'] = invoice
        context['items'] = items
        context['loads'] = loads
        context['accounts'] = accounts
        context['customers'] = customer
        context['title'] = 'Edit new Invoice'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_inv = kwargs['pk']
        invoice = self.model.objects.get(id_inv=id_inv)
        formset = self.form_class_item(request.POST, instance=invoice)
        form = self.form_class(request.POST, instance=invoice)
        if form.is_valid():
                form.save()
                InvoicesHasItem.objects.filter(invoice=invoice).delete()
                itemhasInv = formset.save(commit=False)

                for itinv in itemhasInv:
                    if Item.objects.filter(name=itinv.description, value=itinv.value):
                         item = Item.objects.get(name=itinv.description, value=itinv.value)
                    else:
                        item = Item.objects.create(name=itinv.description, accounts=itinv.accounts, value=itinv.value)
                    itinv.items = item
                    itinv.invoices = invoice
                    itinv.save()
                    if invoice.paid:
                       accounts = AccountDescrip.objects.filter(document=int(invoice.id_inv), accounts=itinv.accounts, type='Invoices')
                       if accounts:
                           accounts.delete()
                       AccountDescrip.objects.create(date=invoice.start_date,
                                                                    value=itinv.subtotal,
                                                                    accounts=itinv.accounts,
                                                                    document=invoice.id_inv,
                                                                    waytopay=invoice.waytopay,
                                                                    users=invoice.users,
                                                                    type='Invoices')
                accion_user(invoice, CHANGE, request.user)
                messages.success(request, "Invoice update with an extension")
                return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            for er in formset.errors:
                messages.error(request, "ERROR: " + er)

class InvoicesDelete(DeleteView):
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_inv = kwargs['pk']
        invoice = self.model.objects.get(id_inv=id_inv)
        accounts = AccountDescrip.objects.filter(type='Invoices', document=int(invoice.id_inv))
        if accounts:
            accounts.delete()
        invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
        accion_user(invoice, DELETION, request.user)
        invoice.delete()
        for it in invitem:
            item = InvoicesHasItem.objects.get(id_ind=it.id_ind)
            item.delete()
        messages.success(request, "Invoice delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Receipts
class ReceiptsView(ListView):
    model = Receipt
    template_name = 'accounting/receipts/receiptsViews.html'


def ReceiptView(request, pk):
        receipt = Receipt.objects.get(id_rec=pk)
        context = {}
        context['form'] = receipt
        context['account'] = receipt.accounts
        context['title'] = 'View Receipt'
        return render(request, 'accounting/receipts/receiptsView.html', context)

class ReceiptsCreate(CreateView):
     model = Receipt
     form_class = ReceiptsForm
     template_name = 'accounting/receipts/receiptsForm.html'

     def get_context_data(self, **kwargs):
         context = super(ReceiptsCreate, self).get_context_data(**kwargs)
         if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
         account = []
         exp = Account.objects.get(primary=True, name='Expenses')
         exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
         for e in exp_acconts:
             account.append(e)
         for a in exp_acconts:
             exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
             if exp_accont != None:
                 for ac in exp_accont:
                     account.append(ac)
         context['accounts'] = account
         context['title'] = 'Create new Receipt'
         return context

     def post(self, request, *args, **kwargs):
         self.object = self.get_object
         user = request.user
         form = self.form_class(request.POST)
         recs = Receipt.objects.filter(business_id=form.data['business']).order_by('-serial')
         serial = 1
         serials = []
         for s in recs:
             serials.append(s.serial)
         if form.is_valid():
             if serials:
               serial = int(serials[0])+1
             receipt = form.save(commit=False)
             receipt.serial = serial
             receipt.users_id = user.id
             receipt.accounts_id = request.POST['accounts']
             receipt.save()
             accion_user(receipt, ADDITION, request.user)
             if receipt.paid:
                 AccountDescrip.objects.create(date=form.data['start_date'],
                                                         value=form.data['total'],
                                                         accounts=receipt.accounts,
                                                         document=receipt.id_rec,
                                                         users_id=user.id,
                                                         waytopay=receipt.waytopay,
                                                         type='Receipts'
                                                         )
             messages.success(request, "Receipt save with an extension")
             return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return self.get_context_data()

class ReceiptsEdit(UpdateView):
    model = Receipt
    form_class = ReceiptsForm
    template_name = 'accounting/receipts/receiptsForm.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptsEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        receipt = self.model.objects.get(id_rec=pk)
        account = Account.objects.filter(id_acn=receipt.accounts_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['accounts'] = account
        context['id'] = pk
        context['accounts'] = account
        context['title'] = 'Edit Receipt'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rec = kwargs['pk']
        receipt = self.model.objects.get(id_rec=id_rec)
        acountDescp = AccountDescrip.objects.filter(accounts_id=receipt.accounts_id, document=int(receipt.id_rec))
        form = self.form_class(request.POST, instance=receipt)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.save()
            if receipt.paid:
               if acountDescp:
                   acountDescp.delete()
               AccountDescrip.objects.create(date=form.data['start_date'],
                                             value=form.data['total'],
                                             accounts=receipt.accounts,
                                             document=receipt.id_rec,
                                             users_id=request.user.id,
                                             waytopay=receipt.waytopay,
                                             type='Receipts'
                                             )
            accion_user(receipt, CHANGE, request.user)
            messages.success(request, "Receipt update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get_context_data()



class ReceiptsDelete(DeleteView):
    model = Receipt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:receipts')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rec = kwargs['pk']
        receipt = self.model.objects.get(id_rec=id_rec)
        acountDescp = AccountDescrip.objects.get(accounts_id=receipt.accounts_id, document=int(receipt.id_rec))
        if acountDescp:
           acountDescp.delete()
        accion_user(receipt, DELETION, request.user)
        receipt.delete()
        messages.success(request, "Receipt delete with an extension")
        return HttpResponseRedirect(self.success_url)


#Payment

def PaymentViews(request):

    payment_driver = DriversHasPayment.objects.all()
    payment_dispatch = DispatchHasPayment.objects.all()
    payment_employee = EmployeeHasPayment.objects.all()
    context = {
            'payment_driver': payment_driver,
            'payment_dispatch': payment_dispatch,
            'payment_employee': payment_employee,
        }
    return render(request, 'accounting/payments/paymentsViews.html', context)
def PaymentView(request, pk):
    payDriver = None
    dispatch = None
    driver = None
    loads = None
    employee= None
    payment = Payment.objects.get(id_sal=pk)
    if DriversHasPayment.objects.filter(payments=payment):
        payDriver = DriversHasPayment.objects.get(payments=payment)
        payLoad = PaymentHasLoad.objects.filter(payments=payment)
        loads = []
        for l in payLoad:
            load = Load.objects.get(id_lod=l.loads_id)
            loads.append(load)
        driver = DriversLogt.objects.get(id_dr=payDriver.driver_id)

    if DispatchHasPayment.objects.filter(payments=payment):
        payDispatch = DispatchHasPayment.objects.get(payments=payment)
        payLoad = PaymentHasLoad.objects.filter(payments=payment)
        loads = []
        for l in payLoad:
            load = Load.objects.get(id_lod=l.loads_id)
            loads.append(load)
        dispatch = DispatchLogt.objects.get(id_dsp=payDispatch.dispatch_id)

    if EmployeeHasPayment.objects.filter(payments=payment):
        payEmployee = EmployeeHasPayment.objects.get(payments=payment)
        employee = Employee.objects.get(id_emp=payEmployee.employee_id)

    context = {
            'form': payment,
            'title': 'View Payment',
            'form2':payDriver,
            'driver': driver,
            'loads': loads,
            'dispatch': dispatch,
            'employee': employee,
        }
    return render(request, 'accounting/payments/paymentsView.html', context)

def PaymentPrint(request, pk):
    pdf = None
    payment = Payment.objects.get(id_sal=pk)
    if DriversHasPayment.objects.filter(payments=payment):
        pdf = PayDriverPDF(request,pk)

    if DispatchHasPayment.objects.filter(payments=payment):
        pdf = PayDispatchPDF(request, pk)

    if EmployeeHasPayment.objects.filter(payments=payment):
        pdf = PayEmployeePDF(request, pk)
    return pdf

def PaymentSelect(request):

    employee = Employee.objects.filter(deactivated=False)
    driver = DriversLogt.objects.filter(deactivate=False)
    dispatch = DispatchLogt.objects.filter(deactivate=False)

    context = {
        'employees': employee,
        'drivers': driver,
        'dispatchs': dispatch,
    }
    if request.method == 'POST':
       if request.POST['type'] == 'employee':
          id = request.POST.get('lstemployee', None)
          start = request.POST.get('start', None)
          end = request.POST.get('end', None)
          return HttpResponseRedirect('/accounting/payments/employee/'+id+'&'+start+'&'+end)

       if request.POST['type'] == 'driver':
          id = request.POST.get('lstdriver', None)
          start = request.POST.get('start', None)
          end = request.POST.get('end', None)
          return HttpResponseRedirect('/accounting/payments/driver/'+id+'&'+start+'&'+end)

       if request.POST['type'] == 'dispatch':
          id = request.POST.get('lstdispatch', None)
          start = request.POST.get('start', None)
          end = request.POST.get('end', None)
          return HttpResponseRedirect('/accounting/payments/dispatch/'+id+'&'+start+'&'+end)

    return render(request, 'accounting/payments/paymentsForm.html', context)



class PaymentEmployeeCreate(CreateView):
     model = Payment
     form_class = PaymentForm
     template_name = 'accounting/payments/employeeForm.html'

     def get(self, request, *args, **kwargs):
         id = self.kwargs.get('pk',0)
         employee = Employee.objects.get(id_emp=id)
         form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end'), 'business':employee.business})
         account = []
         exp = Account.objects.get(primary=True, name='Expenses')
         exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn, business= employee.business)
         for e in exp_acconts:
            account.append(e)
         for a in exp_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
                for ac in exp_accont:
                    account.append(ac)
         return render(request, self.template_name, {'id':id, 'form': form, 'title': 'Create new Employee Payment', 'employee':employee, 'accounts':account})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         employee = Employee.objects.get(id_emp=kwargs['pk'])
         pay = self.model.objects.filter(business_id=form.data['business']).order_by('-serial')
         serial = 1
         serials = []
         for s in pay:
             serials.append(s.serial)
         if form.is_valid():
             if serials:
               serial = int(serials[0])+1
             payment = form.save(commit=False)
             payment.serial = serial
             payment.users_id = user.id
             payment.accounts_id = request.POST['accounts']
             payment.gross = request.POST['subtotal']
             payment.save()
             EmployeeHasPayment.objects.create(payments=payment, employee=employee)
             if payment.paid:
                AccountDescrip.objects.create(date=payment.pay_date,
                                           value=payment.value,
                                           accounts=payment.accounts,
                                           document=payment.id_sal,
                                           users_id=user.id,
                                           waytopay=payment.waytopay,
                                           type='Payments'
                                           )
             accion_user(payment, ADDITION, request.user)
             messages.success(request, "Payment save with an extension")
             return HttpResponseRedirect(reverse_lazy('accounting:payments'))
         else:
             for er in form.errors:
                 form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end')})
                 id = kwargs.get('pk', 0)
                 employee = Employee.objects.get(id_emp=id)
                 account = []
                 exp = Account.objects.get(primary=True, name='Expenses')
                 exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn, business= employee.business)
                 for e in exp_acconts:
                     account.append(e)
                 for a in exp_acconts:
                     exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
                     if exp_accont != None:
                         for ac in exp_accont:
                             account.append(ac)
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name,
                           {'accounts': account, 'employee':employee, 'form': form, 'title': 'Create new Employee Payment'})


class PaymentEmployeeEdit(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'accounting/payments/employeeForm.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentEmployeeEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        payment = self.model.objects.get(id_sal=pk)
        account = Account.objects.get(id_acn=payment.accounts_id)
        payemp = EmployeeHasPayment.objects.get(payments=payment)

        if 'form' not in context:
            context['form'] = self.form_class()
        context['employee'] = payemp.employee
        context['id'] = pk
        context['account'] = account
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sal = kwargs['pk']
        payment = self.model.objects.get(id_sal=id_sal)
        form = self.form_class(request.POST, instance=payment)
        acountDescp = AccountDescrip.objects.filter(accounts=payment.accounts, document=int(payment.id_sal))
        if form.is_valid():
            payment = form.save(commit=False)
            payment.gross = request.POST['subtotal']
            payment.save()
            if payment.paid:
                if acountDescp:
                    acountDescp.delete()
                AccountDescrip.objects.create(date=payment.pay_date,
                                              value=payment.value,
                                              accounts=payment.accounts,
                                              document=payment.id_sal,
                                              users_id=request.user.id,
                                              waytopay=payment.waytopay,
                                              type='Payments'
                                              )
            accion_user(payment, CHANGE, request.user)
            messages.success(request, "Payment update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:payments'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get_context_data()



class PaymentEmployeeDelete(DeleteView):
    model = Payment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:payments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sal = kwargs['pk']
        payment = self.model.objects.get(id_sal=id_sal)
        EmployeeHasPayment.objects.get(payments_id=payment.id_sal).delete()
        accounDescr = AccountDescrip.objects.get(accounts=payment.accounts, document=int(payment.id_sal))
        if accounDescr:
            accounDescr.delete()
        accion_user(payment, DELETION, request.user)
        payment.delete()
        messages.success(request, "Payment delete with an extension")
        return HttpResponseRedirect(self.success_url)


class PaymentDriverCreate(View):
    model = Payment
    form_class = PaymentForm
    form_driver_class = PaymentDriverForm
    template_name = 'accounting/payments/driverpayForm.html'

    def get(self, request, *args, **kwargs):
            id = self.kwargs.get('pk', 0)
            driver = DriversLogt.objects.get(id_dr=id)
            diesels = Diesel.objects.filter(driver=driver)
            loads = Load.objects.filter(driver=driver)
            load_driver = []
            diesel_total = 0
            start = datetime.strptime(str(kwargs.get('start')),'%Y-%m-%d')
            end = datetime.strptime(str(kwargs.get('end')),'%Y-%m-%d')
            for d in diesels:
                date_start = datetime.strptime(str(d.date_start),'%Y-%m-%d')
                date_end = datetime.strptime(str(d.date_end),'%Y-%m-%d')
                if date_start >= start and date_end <= end:
                    diesel_total += d.total
            for l in loads:
                pickup_date = datetime.strptime(str(l.pickup_date), '%Y-%m-%d')
                deliver_date = datetime.strptime(str(l.deliver_date), '%Y-%m-%d')
                if pickup_date >= start and deliver_date <= end:
                    load_driver.append(l)
            form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end')})
            form_driver = self.form_driver_class()
            account = []
            income_account = []
            exp = Account.objects.get(primary=True, name='Expenses')
            exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
            for e in exp_acconts:
                account.append(e)
            for a in exp_acconts:
                exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
                if exp_accont != None:
                    for ac in exp_accont:
                        account.append(ac)
            inv = Account.objects.get(primary=True, name='Income')
            inv_acconts = Account.objects.filter(accounts_id_id=inv.id_acn)
            for e in inv_acconts:
                income_account.append(e)
                for a in inv_acconts:
                    exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
                    if exp_accont != None:
                        for ac in exp_accont:
                            income_account.append(ac)
            context = {'form': form,
                       'form2': form_driver,
                       'title': 'Create new Driver Payment',
                       'loads': load_driver,
                       'driver': driver,
                       'diesel': diesel_total,
                       'accounts': account,
                       'income_accounts': income_account
                       }
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
            user = request.user
            form = self.form_class(request.POST)
            form2 = self.form_driver_class(request.POST)
            pay = Payment.objects.filter(business_id=form.data['business']).order_by('-serial')
            loads = Load.objects.all()
            driver = DriversLogt.objects.get(id_dr=kwargs['pk'])
            serial = 1
            serials = []
            loadPay = []
            total_pay = 0
            total_income = 0
            for s in pay:
                serials.append(s.serial)
            for l in loads:
                load = request.POST.get('id_'+str(l.id_lod), None)
                if load:
                    loadPay.append(l)
            if form.is_valid() and loadPay and form2.is_valid():
                if serials:
                    serial = int(serials[0]) + 1
                payment = form.save(commit=False)
                payment.serial = serial
                payment.users_id = user.id
                payment.accounts_id = request.POST['accounts']
                payment.gross = request.POST['subtotal']
                payment.save()
                driverpay = form2.save(commit=False)
                driverpay.driver = driver
                driverpay.payments = payment
                driverpay.save()
                for load in loadPay:
                    PaymentHasLoad.objects.create(loads=load, payments=payment)
                if payment.paid:
                  if driver.type == 'Driver':
                    total_pay = driverpay.total_driver
                    total_income = driverpay.total_owner
                    AccountDescrip.objects.create(date=payment.pay_date,
                                                  value=total_income,
                                                  accounts_id=int(request.POST['accounts_income']),
                                                  document=payment.id_sal,
                                                  users_id=user.id,
                                                  waytopay=payment.waytopay,
                                                  type='Payments'
                                                  )
                  else:
                    total_pay = payment.value
                  AccountDescrip.objects.create(date=payment.pay_date,
                                              value=total_pay,
                                              accounts=payment.accounts,
                                              document=payment.id_sal,
                                              users_id=user.id,
                                              waytopay=payment.waytopay,
                                              type='Payments'
                                              )

                  income = Account.objects.get(primary=True, name='Income')
                  if driverpay.company_fee:
                    if Account.objects.filter(name='COMPANY FEE', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.company_fee,
                                                        accounts=Account.objects.get(name='COMPANY FEE', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                  if driverpay.pre_pass:
                    if Account.objects.filter(name='PRE PASS', accounts_id_id=income.id_acn ):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.pre_pass,
                                                        accounts=Account.objects.get(name='PRE PASS', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                  if driverpay.down_payment:
                    if Account.objects.filter(name='DOWN PAYMENT', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.down_payment,
                                                        accounts=Account.objects.get(name='DOWN PAYMENT', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                          donw_payment = 0
                          if driver.dow_payment:
                              donw_payment = driver.dow_payment
                          total_esc = donw_payment + driverpay.down_payment
                          driver.dow_payment=total_esc
                          driver.save()
                  if driverpay.escrow:
                    if Account.objects.filter(name='ESCROW', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.escrow,
                                                        accounts=Account.objects.get(name='ESCROW', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                          escrow = 0
                          if driver.escrow:
                              escrow = driver.escrow
                          total_esc = escrow + driverpay.escrow
                          driver.escrow = total_esc
                          driver.save()
                  if driverpay.insurance:
                    if Account.objects.filter(name='INSURANCE', accounts_id_id=income.id_acn ):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.insurance,
                                                        accounts=Account.objects.get(name='INSURANCE', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )

                  if driverpay.diesel:
                    if Account.objects.filter(name='DIESEL', accounts_id_id=income.id_acn ):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.diesel,
                                                        accounts=Account.objects.get(name='DIESEL', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                  if driverpay.other:
                    if Account.objects.filter(name='MISCELLANEOUS', accounts_id_id=income.id_acn ):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                        value=driverpay.other,
                                                        accounts=Account.objects.get(name='MISCELLANEOUS', accounts_id_id=income.id_acn),
                                                        document=payment.id_sal,
                                                        users_id=user.id,
                                                        waytopay=payment.waytopay,
                                                        type='Payments'
                                                        )
                accion_user(payment, ADDITION, request.user)
                messages.success(request, "Payment save with an extension")
                return HttpResponseRedirect(reverse_lazy('accounting:payments'))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                for e in form2.errors:
                    messages.error(request, "ERROR: " + e)
                return self.get(request)



class PaymentDriverEdit(UpdateView):
    model = Payment
    form_class = PaymentForm
    form_driver_class = PaymentDriverForm
    template_name = 'accounting/payments/driverpayForm.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentDriverEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        payment = self.model.objects.get(id_sal=pk)
        payDriver = DriversHasPayment.objects.get(payments=payment)
        payLoad = PaymentHasLoad.objects.filter(payments=payment)
        loads = []
        for l in payLoad:
            load = Load.objects.get(id_lod=l.loads_id)
            loads.append(load)
        driver = DriversLogt.objects.get(id_dr=payDriver.driver_id)
        accounts = []
        income_account = []
        exp = Account.objects.get(primary=True, name='Expenses')
        exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
        for e in exp_acconts:
            accounts.append(e)
        for a in exp_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
                for ac in exp_accont:
                    accounts.append(ac)
        inv = Account.objects.get(primary=True, name='Income')
        inv_acconts = Account.objects.filter(accounts_id_id=inv.id_acn)
        for e in inv_acconts:
            income_account.append(e)
            for a in inv_acconts:
                exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
                if exp_accont != None:
                    for ac in exp_accont:
                        income_account.append(ac)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.form_driver_class(initial={
                'porc_company':payDriver.porc_company,
                'company_fee':payDriver.company_fee,
                'pre_pass':payDriver.pre_pass,
                'escrow':payDriver.escrow,
                'down_payment':payDriver.down_payment,
                'insurance':payDriver.insurance,
                'diesel':payDriver.diesel,
                'other':payDriver.other,
                'total_owner':payDriver.total_owner,
                'total_driver':payDriver.total_driver
            })
        context['title'] = 'Edit Driver Payment'
        context['loads'] = loads
        context['driver']= driver
        context['accounts']= accounts
        context['account'] = payment.accounts
        context['income_accounts']= income_account
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sal = kwargs['pk']
        payment = self.model.objects.get(id_sal=id_sal)
        payDriver = DriversHasPayment.objects.get(payments=payment)
        driver = DriversLogt.objects.get(id_dr=payDriver.driver_id)
        last_down = payDriver.down_payment
        last_escrow = payDriver.escrow
        form = self.form_class(request.POST, instance=payment)
        form2 = self.form_driver_class(request.POST, instance=payDriver)
        acountDescp = AccountDescrip.objects.filter(document=int(payment.id_sal), type='Payments' )
        if form.is_valid() and form2.is_valid():
            payment = form.save(commit=False)
            payment.gross = request.POST['subtotal']
            payment.save()
            driverpay = form2.save()
            income = Account.objects.get(primary=True, name='Income')
            if payment.paid:
               if acountDescp:
                   acountDescp.delete()
                   if driver.type == 'Driver':
                     total_pay = driverpay.total_owner
                   else:
                     total_pay = payment.value
                   AccountDescrip.objects.create(date=payment.pay_date,
                                              value=total_pay,
                                              accounts=payment.accounts,
                                              document=payment.id_sal,
                                              users_id=request.user.id,
                                              waytopay=payment.waytopay,
                                              type='Payments'
                                              )

                   income = Account.objects.get(primary=True, name='Income')
                   if driverpay.company_fee:
                      if Account.objects.filter(name='COMPANY FEE', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.company_fee,
                                                      accounts=Account.objects.get(name='COMPANY FEE',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
                   if driverpay.pre_pass:
                      if Account.objects.filter(name='PRE PASS', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.pre_pass,
                                                      accounts=Account.objects.get(name='PRE PASS',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
                   if driverpay.down_payment:
                      if Account.objects.filter(name='DOWN PAYMENT', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.down_payment,
                                                      accounts=Account.objects.get(name='DOWN PAYMENT',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
                          donw_payment = 0
                          if driver.dow_payment:
                             donw_payment = driver.dow_payment
                          total_esc = donw_payment + driverpay.down_payment
                          driver.dow_payment = total_esc
                          driver.save()
                   if driverpay.escrow:
                      if Account.objects.filter(name='ESCROW', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.escrow,
                                                      accounts=Account.objects.get(name='ESCROW',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
                          escrow = 0
                          if driver.escrow:
                             escrow = driver.escrow
                          total_esc = escrow + driverpay.escrow
                          driver.escrow = total_esc
                          driver.save()
                   if driverpay.insurance:
                      if Account.objects.filter(name='INSURANCE', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.insurance,
                                                      accounts=Account.objects.get(name='INSURANCE',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )

                   if driverpay.diesel:
                      if Account.objects.filter(name='DIESEL', accounts_id_id=income.id_acn):
                         AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.diesel,
                                                      accounts=Account.objects.get(name='DIESEL',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
                   if driverpay.other:
                      if Account.objects.filter(name='MISCELLANEOUS', accounts_id_id=income.id_acn):
                          AccountDescrip.objects.create(date=payment.pay_date,
                                                      value=driverpay.other,
                                                      accounts=Account.objects.get(name='MISCELLANEOUS',
                                                                                   accounts_id_id=income.id_acn),
                                                      document=payment.id_sal,
                                                      users_id=request.user.id,
                                                      waytopay=payment.waytopay,
                                                      type='Payments'
                                                      )
            accion_user(payment, CHANGE, request.user)
            messages.success(request, "Payment update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:payments'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            for e in form2.errors:
                messages.error(request, "ERROR: " + e)
            return self.get_context_data()


class PaymentDriverDelete(DeleteView):
    model = Payment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:payments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        payment = self.model.objects.get(id_sal=pk)
        payDriver = DriversHasPayment.objects.get(payments=payment)
        driver = DriversLogt.objects.get(id_dr=payDriver.driver_id)
        donw_payment = 0
        if driver.dow_payment:
            donw_payment = driver.dow_payment
        total_dow = payDriver.down_payment - donw_payment
        driver.dow_payment = total_dow
        escrow = 0
        if driver.escrow:
            escrow = driver.escrow
        total_esc = payDriver.escrow - escrow
        driver.escrow = total_esc
        driver.save()
        payDriver.delete()
        PaymentHasLoad.objects.filter(payments=payment).delete()
        AccountDescrip.objects.filter(document=int(payment.id_sal), type='Payments').delete()
        accion_user(payment, DELETION, request.user)
        payment.delete()
        messages.success(request, "Payment delete with an extension")
        return HttpResponseRedirect(self.success_url)



class PaymentDispatchCreate(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'accounting/payments/dispatchpayForm.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk', 0)
        dispatch = DispatchLogt.objects.get(id_dsp=id)
        loads = Load.objects.filter(dispatch=dispatch)
        load_dispatch = []
        start = datetime.strptime(str(kwargs.get('start')), '%Y-%m-%d')
        end = datetime.strptime(str(kwargs.get('end')), '%Y-%m-%d')
        for l in loads:
            pickup_date = datetime.strptime(str(l.pickup_date), '%Y-%m-%d')
            deliver_date = datetime.strptime(str(l.deliver_date), '%Y-%m-%d')
            if pickup_date > start and deliver_date < end:
                load_dispatch.append(l)
        form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end')})
        account = []
        exp = Account.objects.get(primary=True, name='Expenses')
        exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
        for e in exp_acconts:
            account.append(e)
        for a in exp_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
                for ac in exp_accont:
                    account.append(ac)
        context = {'form': form,
                   'title': 'Create new Dispatch Payment',
                   'loads': load_dispatch,
                   'dispatch': dispatch,
                   'accounts': account,
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        pay = Payment.objects.filter(business_id=form.data['business']).order_by('-serial')
        loads = Load.objects.all()
        dispatch = DispatchLogt.objects.get(id_dsp=kwargs['pk'])
        loadPay = []
        serial = 1
        serials = []
        for s in pay:
            serials.append(s.serial)
        if form.is_valid():
            if serials:
                serial = int(serials[0]) + 1
            payment = form.save(commit=False)
            payment.serial = serial
            payment.users_id = user.id
            payment.accounts_id = request.POST['accounts']
            payment.gross = request.POST['subtotal']
            payment.save()
            for l in loads:
                load = request.POST.get('id_'+str(l.id_lod), None)
                if load:
                    loadPay.append(l)
            for load in loadPay:
                PaymentHasLoad.objects.create(loads=load, payments=payment)
            DispatchHasPayment.objects.create(payments=payment, dispatch=dispatch)
            if payment.paid:
               AccountDescrip.objects.create(date=payment.pay_date,
                                          value=payment.value,
                                          accounts=payment.accounts,
                                          document=payment.id_sal,
                                          users_id=user.id,
                                          waytopay=payment.waytopay,
                                          type='Payments'
                                          )
            accion_user(payment, ADDITION, request.user)
            messages.success(request, "Payment save with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:payments'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get(request)

class PaymentDispatchEdit(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'accounting/payments/dispatchpayForm.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentDispatchEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        payment = self.model.objects.get(id_sal=pk)
        account = Account.objects.get(id_acn=payment.accounts_id)
        payDispatch = DispatchHasPayment.objects.get(payments=payment)
        payLoad = PaymentHasLoad.objects.filter(payments=payment)
        loads = []
        for l in payLoad:
            load = Load.objects.get(id_lod=l.loads_id)
            loads.append(load)
        dispatch = DispatchLogt.objects.get(id_dsp=payDispatch.dispatch_id)
        accounts = []
        exp = Account.objects.get(primary=True, name='Expenses')
        exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
        for e in exp_acconts:
            accounts.append(e)
        for a in exp_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
                for ac in exp_accont:
                    accounts.append(ac)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['title'] = 'Edit Dispatch Payment'
        context['loads'] = loads
        context['dispatch'] = dispatch
        context['accounts'] = accounts
        context['account'] = payment.accounts
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sal = kwargs['pk']
        payment = self.model.objects.get(id_sal=id_sal)
        payDispatch = DispatchHasPayment.objects.get(payments=payment)
        dispatch = DispatchLogt.objects.get(id_dsp=payDispatch.dispatch_id)
        form = self.form_class(request.POST, instance=payment)
        acountDescp = AccountDescrip.objects.filter(accounts=payment.accounts, document=int(payment.id_sal))
        if form.is_valid():
            payment = form.save(commit=False)
            payment.gross = request.POST['subtotal']
            payment.save()
            if payment.paid:
               if acountDescp:
                   acountDescp.delete()
               AccountDescrip.objects.create(date=payment.pay_date,
                                             value=payment.value,
                                             accounts=payment.accounts,
                                             document=payment.id_sal,
                                             users_id=request.user.id,
                                             waytopay=payment.waytopay,
                                             type='Payments'
                                             )
            accion_user(payment, CHANGE, request.user)
            messages.success(request, "Payment update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:payments'))
        else:
            for e in form.errors:
                messages.error(request, "ERROR: " + e)
            return self.get_context_data()

class PaymentDispatchDelete(DeleteView):
    model = Payment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:payments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        payment = self.model.objects.get(id_sal=pk)
        DispatchHasPayment.objects.filter(payments=payment).delete()
        PaymentHasLoad.objects.filter(payments=payment).delete()
        AccountDescrip.objects.filter(document=int(payment.id_sal), type='Payments').delete()
        accion_user(payment, DELETION, request.user)
        payment.delete()
        messages.success(request, "Payment delete with an extension")
        return HttpResponseRedirect(self.success_url)



class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'accounting/customer/noteForm.html'

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        customer  = Customer.objects.get(id_cut=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.users = request.user
            note.customers = customer
            note.save()
            accion_user(note, CHANGE, request.user)
            messages.success(request, 'Add your note to customer')
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Note'})

class NoteEdit(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'accounting/customer/noteForm.html'


    def get_context_data(self, **kwargs):
        context = super(NoteEdit, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class
        context['id'] = id
        context['title'] = 'Note Edit'
        return context

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        note = self.model.objects.get(id=id)
        form = self.form_class(request.POST, instance=note)
        if form.is_valid():
             note = form.save()
             accion_user(note, CHANGE, request.user)
             messages.success(request, 'Update your note to customer')
             return HttpResponseRedirect('/accounting/customers/view/' + str(note.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Note'})

class NoteDelete(DeleteView):
    model = Note
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        note = self.model.objects.get(id=id)
        accion_user(note, DELETION, request.user)
        note.delete()
        messages.success(request, "Receipt delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(note.customers_id))