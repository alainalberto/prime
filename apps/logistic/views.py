import datetime
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from apps.logistic.components.LogisticForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from Prime.util import accion_user
from apps.logistic.models import *
from apps.accounting.models import Invoice, AccountDescrip
from apps.accounting.components.AccountingForm import InvoicesForm
from apps.tools.models import Folder, Busines, File, Alert
from apps.services.models import Application, Customer, Driver
from datetime import datetime, date, time, timedelta

# Create your views here.

#Invoices

def InvoicesLoadSelect(request):
    context = {
        'title': 'Selected Period'
    }
    if request.method == 'POST':
        start = request.POST.get('start', None)
        end = request.POST.get('end', None)
        return HttpResponseRedirect('/logistic/invoices/load/create/'+ start + '&' + end)

    return render(request, 'logistic/invoiceslog/selectLoadsForm.html', context)

class InvoicesLogView(ListView):
    model = Invoice
    template_name = 'logistic/invoiceslog/invoiceslogViews.html'

    def get_context_data(self, **kwargs):
        context = super(InvoicesLogView, self).get_context_data(**kwargs)
        invoice = self.model.objects.filter(type='load').order_by('-start_date')
        context['title'] = 'List Invoices'
        context['object_list'] = invoice
        return context



def InvoiceLogView(request, pk):
            invoice = Invoice.objects.get(id_inv=pk)
            InvLod = InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv)
            loads = []
            for d in InvLod:
               loads.append(Load.objects.get(id_lod=d.loads_id))
            context = {'invoice': invoice,
                       'description': loads,
                       'id': pk,
                       'title': 'Invoice',
                       }
            return render(request, 'logistic/invoiceslog/invoiceslogView.html', context)

class InvoicesLogCreate(CreateView):
        model = Invoice
        form_class = InvoicesForm
        template_name = 'logistic/invoiceslog/invoiceslogForm.html'

        def get(self, request, *args, **kwargs):
            load_customer = []
            loads = Load.objects.filter(paid=False)
            start = datetime.strptime(str(kwargs.get('start')), '%Y-%m-%d').date()
            end = datetime.strptime(str(kwargs.get('end')), '%Y-%m-%d').date()
            for l in loads:
                pickup_date = l.pickup_date
                deliver_date = l.deliver_date
                if pickup_date >= start and deliver_date <= end:
                     load_customer.append(l)
            form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end')})
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
            context= {'form': form,
                      'accounts':accounts,
                      'title':'Create new Invoice',
                      'loads':load_customer,
                      'customers':customer
                      }
            return render(request, self.template_name, context)

        def post(self, request, *args, **kwargs):

            form = self.form_class(request.POST)
            user = request.user
            invs = Invoice.objects.filter(business_id=form.data['business']).order_by('-serial')
            loads = Load.objects.all()
            account = Account.objects.get(id_acn=request.POST['id_accounts'])
            serial = 1
            serials = []
            loadInv = []
            for s in invs:
                serials.append(s.serial)
            for l in loads:
                load = request.POST.get('id_'+str(l.id_lod), None)
                if load:
                    loadInv.append(l)
            if form.is_valid() and loadInv:
                if serials:
                    serial = int(serials[0]) + 1
                invoice = form.save(commit=False)
                invoice.serial = serial
                invoice.type = 'load'
                invoice.users_id = user.id
                invoice.save()
                accion_user(invoice, ADDITION, request.user)
                for lodinv in loadInv:
                    InvoicesHasLoad.objects.create(
                      invoices=invoice,
                      loads=lodinv
                    )
                    if request.POST.get('paid_'+str(lodinv.id_lod), False):
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='True')
                    else:
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='False')
                if invoice.paid:
                   AccountDescrip.objects.create(date=invoice.start_date,
                                                                        value=invoice.total,
                                                                        accounts=account,
                                                                        document=invoice.id_inv,
                                                                        users_id=user.id,
                                                                        waytopay=invoice.waytopay,
                                                                        type='Invoices')

                messages.success(request, "Invoice saved with an extension")

                return HttpResponseRedirect(reverse_lazy('accounting:invoices_log'))
            else:
                for er in form.errors:
                    messages.error(request, er)
                return self.get(request)


class InvoicesLogEdit(UpdateView):
        model = Invoice
        form_class = InvoicesForm
        template_name = 'logistic/invoiceslog/invoiceslogForm.html'

        def get_context_data(self, **kwargs):
            context = super(InvoicesLogEdit, self).get_context_data(**kwargs)
            pk = self.kwargs.get('pk', 0)
            adjust = self.kwargs.get('bill')
            invoice = self.model.objects.get(id_inv=pk)
            loads = Load.objects.filter(paid='False').order_by('-pickup_date')
            customer = Customer.objects.filter(deactivated=False)
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
            description = []
            loadInv = InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv)
            for l in loadInv:
                load = Load.objects.get(id_lod=l.loads_id)
                description.append(load)
            context['accounts'] = accounts
            context['title'] = 'Edit Invoice'
            context['loads'] = loads
            context['customers'] = customer
            context['invoice'] = invoice
            context['description'] = description
            context['adjust'] = adjust
            return context

        def post(self, request, *args, **kwargs):
            self.object = self.get_object
            id_inv = kwargs['pk']
            invoice = self.model.objects.get(id_inv=id_inv)
            account = Account.objects.get(id_acn=request.POST['id_accounts'])
            form = self.form_class(request.POST, instance=invoice)
            loads = Load.objects.all()
            loadInv = []
            for l in loads:
                load = request.POST.get('id_' + str(l.id_lod), None)
                if load:
                    loadInv.append(l)
            if form.is_valid():
                invoice = form.save()
                InvHasLod = InvoicesHasLoad.objects.filter(invoices=invoice)
                for i in InvHasLod:
                    load = Load.objects.get(id_lod=i.loads_id)
                    if loadInv.__contains__(load):
                        i.delete()
                for lodinv in loadInv:
                    if not InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv, loads_id=lodinv.id_lod):
                       InvoicesHasLoad.objects.create(
                        invoices=invoice,
                        loads=lodinv
                        )
                    if request.POST.get('paid_' + str(lodinv.id_lod), False):
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='True')
                    else:
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='False')
                if invoice.paid:
                    accounts = AccountDescrip.objects.filter(document=int(invoice.id_inv), accounts=account, type='Invoices')
                    if accounts:
                        accounts.delete()
                    AccountDescrip.objects.create(date=invoice.start_date,
                                                  value=invoice.total,
                                                  accounts=account,
                                                  document=invoice.id_inv,
                                                  users_id=request.user.id,
                                                  waytopay=invoice.waytopay,
                                                  type='Invoices')

                messages.success(request, "Invoice update with an extension")
                return HttpResponseRedirect(reverse_lazy('accounting:invoices_log'))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                return self.get_context_data()

class InvoicesLogDelete(DeleteView):
        model = Invoice
        template_name = 'confirm_delete.html'
        success_url = reverse_lazy('accounting:invoices_log')

        def delete(self, request, *args, **kwargs):
            self.object = self.get_object
            id_inv = kwargs['pk']
            invoice = self.model.objects.get(id_inv=id_inv)
            accounts = AccountDescrip.objects.filter(type='Invoices', document=int(invoice.id_inv))
            if accounts:
                accounts.delete()
            InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv).delete()
            accion_user(invoice, DELETION, request.user)
            invoice.delete()
            messages.success(request, "Invoice delete with an extension")
            return HttpResponseRedirect(self.success_url)



# Load
class LoadsView(ListView):
    model = Load
    template_name = 'logistic/load/loadViews.html'

    def get_context_data(self, **kwargs):
        context = super(LoadsView, self).get_context_data(**kwargs)
        loads = Load.objects.filter(other_company='False')
        loads_other = CustomerHasLoad.objects.all()
        context['loads'] = loads
        context['loads_other'] = loads_other
        return context

class LoadsCreate(CreateView):
     model = Load
     form_class = LoadsForm
     template_name = 'logistic/load/loadForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class()
         customer = []
         customers = Customer.objects.filter(deactivated=False).order_by('company_name')
         driver = Driver.objects.filter(deactivate=False).order_by('customers')
         for c in customers:
             for d in driver:
                 if d.customers == c:
                     customer.append(c)
         driver = Driver.objects.filter(deactivate=False).order_by('customers')
         return render(request, self.template_name, {'form': form, 'customers':customer, 'drivers':driver, 'title': 'Create new Load'})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
             load_exist = Load.objects.filter(broker=form.data['broker'], number=form.data['number'])
             if load_exist:
                 messages.error(request, 'The load already exists')
                 form = self.form_class()
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})
             else:
                load = form.save(commit=False)
                load.users = request.user
                load.save()
                if load.other_company:
                    if request.POST.get('customer', None):
                        customer = Customer.objects.get(id_cut=request.POST['customer'])
                        driver = Driver.objects.get(id_drv=request.POST['drivers'])
                        CustomerHasLoad.objects.create(
                            customers=customer,
                            driver = driver,
                            loads = load
                        )
                accion_user(load, ADDITION, request.user)
                messages.success(request, 'Load save with an extension')
                return HttpResponseRedirect(reverse_lazy('logistic:loads'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)

class LoadsEdit(UpdateView):
    model = Load
    form_class = LoadsForm
    template_name = 'logistic/load/loadForm.html'
    success_url = reverse_lazy('logistic:loads')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_lod = kwargs['pk']
        load = self.model.objects.get(id_lod=id_lod)
        form = self.form_class(request.POST, instance=load)
        if form.is_valid():
            load =form.save()
            accion_user(load, CHANGE, request.user)
            messages.success(request, "Load update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Load'})

class LoadsDelete(DeleteView):
    model = Load
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:loads')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_lod = kwargs['pk']
        load = self.model.objects.get(id_lod=id_lod)
        accion_user(load, DELETION, request.user)
        load.delete()
        messages.success(request, "Load delete with an extension")
        return HttpResponseRedirect(self.success_url)


#Drivers

class DriversView(ListView):
    model = DriversLogt
    template_name = 'logistic/drivers/driversViews.html'

class DriversCreate(CreateView):
     model = DriversLogt
     form_class = DriversForm
     template_name = 'logistic/drivers/driversForm.html'

     def get_context_data(self, **kwargs):
         context = super(DriversCreate, self).get_context_data(**kwargs)
         if 'form' not in context:
             context['form'] = self.form_class(self.request.GET)
         context['title'] = 'Create new Driver'
         return context

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
             driver_exist = DriversLogt.objects.filter(license_numb=form.data['license_numb'], name=form.data['name'])
             if driver_exist:
                 messages.error(request, 'The driver already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})
             else:
                 user_exist = User.objects.filter(username=request.POST['email'])
                 if user_exist:
                     user = User.objects.get(username=request.POST['email'])
                 else:
                    user = User.objects.create_user(username=request.POST['email'],email=request.POST['email'], password=request.POST['license_numb'], is_staff=False, is_active=True)
                 driver = form.save(commit=False)
                 driver.users_id = user.id
                 driver.save()
                 if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                     group_admin = Group.objects.get(name='System Administrator')
                     group_manag = Group.objects.get(name='System Manager')
                     group_offic = Group.objects.get(name='Logistic Specialist')
                     dateExp = driver.lic_date_exp
                     dateShow = dateExp - timedelta(days=30)
                     alert = Alert.objects.create(
                         category="Urgents",
                         description="Expires the License Driver of " + str(driver),
                         create_date=datetime.now().strftime("%Y-%m-%d"),
                         show_date=dateShow.strftime("%Y-%m-%d"),
                         end_date=dateExp.strftime("%Y-%m-%d"),
                         users=request.user)
                     alert.group.add(group_admin, group_manag, group_offic)
                 if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                     group_admin = Group.objects.get(name='System Administrator')
                     group_manag = Group.objects.get(name='System Manager')
                     group_offic = Group.objects.get(name='Logistic Specialist')
                     dateExp = driver.medicard_date_exp
                     dateShow = dateExp - timedelta(days=30)
                     alert = Alert.objects.create(
                         category="Urgents",
                         description="Expires the Medicard Driver of " + str(driver),
                         create_date=datetime.now().strftime("%Y-%m-%d"),
                         show_date=dateShow.strftime("%Y-%m-%d"),
                         end_date=dateExp.strftime("%Y-%m-%d"),
                         users=request.user)
                     alert.group.add(group_admin, group_manag, group_offic)
                 if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                     group_admin = Group.objects.get(name='System Administrator')
                     group_manag = Group.objects.get(name='System Manager')
                     group_offic = Group.objects.get(name='Logistic Specialist')
                     dateExp = driver.drugtest_date_exp
                     dateShow = dateExp - timedelta(days=30)
                     alert = Alert.objects.create(
                         category="Urgents",
                         description="Expires the Drugtest Driver of " + str(driver),
                         create_date=datetime.now().strftime("%Y-%m-%d"),
                         show_date=dateShow.strftime("%Y-%m-%d"),
                         end_date=dateExp.strftime("%Y-%m-%d"),
                         users=request.user)
                     alert.group.add(group_admin, group_manag, group_offic)
                 if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                     group_admin = Group.objects.get(name='System Administrator')
                     group_manag = Group.objects.get(name='System Manager')
                     group_offic = Group.objects.get(name='Logistic Specialist')
                     dateExp = driver.mbr_date_exp
                     dateShow = dateExp - timedelta(days=30)
                     alert = Alert.objects.create(
                         category="Urgents",
                         description="Expires the MVR Driver of " + str(driver),
                         create_date=datetime.now().strftime("%Y-%m-%d"),
                         show_date=dateShow.strftime("%Y-%m-%d"),
                         end_date=dateExp.strftime("%Y-%m-%d"),
                         users=request.user)
                     alert.group.add(group_admin, group_manag, group_offic)
                 accion_user(driver, ADDITION, request.user)
                 messages.success(request, 'Driver save with an extension')
             return HttpResponseRedirect(reverse_lazy('logistic:drivers'))
         else:
            for er in form.errors:
               messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})

class DriversEdit(UpdateView):
    model = DriversLogt
    form_class = DriversForm
    template_name = 'logistic/drivers/driversForm.html'
    success_url = reverse_lazy('logistic:drivers')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dr = kwargs['pk']
        driver = self.model.objects.get(id_dr=id_dr)
        form = self.form_class(request.POST, instance=driver)
        if form.is_valid():
            driver =form.save()
            if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                dateExp = driver.lic_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(description="Expires the License Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Logistic Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires the License Driver of " + str(driver),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(
                    description="Expires the License Driver of " + str(driver),
                    category="Urgents")
                if alert:
                    for a in alert:
                        a.delete()
            if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                dateExp = driver.medicard_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(description="Expires the Medicard Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Logistic Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires the Medicard Driver of the customer " + str(driver),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(description="Expires the Medicard Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    for a in alert:
                        a.delete()
            if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                dateExp = driver.drugtest_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(description="Expires the Drugtest Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Logistic Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires the Drugtest Driver of " + str(driver),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(description="Expires the Drugtest Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    for a in alert:
                        a.delete()
            if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                dateExp = driver.mbr_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(description="Expires the Mbr Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Logistic Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires the Mbr Driver of " + str(driver),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(description="Expires the Mbr Driver of " + str(driver),
                                             category="Urgents")
                if alert:
                    for a in alert:
                        a.delete()
            accion_user(driver, CHANGE, request.user)
            messages.success(request, "Driver update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Drivers'})


class DriversDelete(DeleteView):
    model = DriversLogt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:drivers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dr = kwargs['pk']
        driver = self.model.objects.get(id_dr=id_dr)
        alert_lic = Alert.objects.filter(
            description="Expires the License Driver of " + str(driver),
            end_date=driver.lic_date_exp)
        alert_medicard = Alert.objects.filter(
            description="Expires the Medicard Driver of " + str(driver),
            end_date=driver.medicard_date_exp)
        alert_drugtest = Alert.objects.filter(
            description="Expires the Drugtest Driver of " + str(driver),
            end_date=driver.drugtest_date_exp)
        alert_mbr = Alert.objects.filter(description="Expires the Mbr Driver of " + str(driver),
                                         end_date=driver.mbr_date_exp)
        accion_user(driver, DELETION, request.user)
        if alert_lic:
            for a in alert_lic:
                a.delete()
            alert_lic.delete()
        if alert_medicard:
            for a in alert_medicard:
                a.delete()
        if alert_drugtest:
            for a in alert_drugtest:
                a.delete()
        if alert_mbr:
            for a in alert_mbr:
                a.delete()
        accion_user(driver, DELETION, request.user)
        driver.delete()
        messages.success(request, "Driver delete with an extension")
        return HttpResponseRedirect(self.success_url)


#Distpacher

class DispatchView(ListView):
    model = DispatchLogt
    template_name = 'logistic/dispatch/dispatchViews.html'

class DispatchCreate(CreateView):
     model = DispatchLogt
     form_class = DispatchForm
     template_name = 'logistic/dispatch/dispatchForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class()
         return render(request, self.template_name, {'form': form, 'title': 'Create new Dispatch'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             disp_exist = DispatchLogt.objects.filter(name=form.data['name'])
             if disp_exist:
                 messages.error(request, 'The dispatch already exists')
                 form = self.form_class()
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Dispatch'})
             else:
                 disp = form.save(commit=False)
                 disp.users = user
                 disp.save()
                 accion_user(disp, ADDITION, request.user)
                 messages.success(request, "Dispatch save with an extension")
             return HttpResponseRedirect(reverse_lazy('logistic:dispatch'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Edit Dispatch'})

class DispatchEdit(UpdateView):
    model = DispatchLogt
    form_class = DispatchForm
    template_name = 'logistic/dispatch/dispatchForm.html'
    success_url = reverse_lazy('logistic:dispatch')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dsp = kwargs['pk']
        disp = self.model.objects.get(id_dsp=id_dsp)
        form = self.form_class(request.POST, instance=disp)
        if form.is_valid():
            disp =form.save()
            accion_user(disp, CHANGE, request.user)
            messages.success(request, "Dispatch update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)


class DispatchDelete(DeleteView):
    model = DispatchLogt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:dispatch')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dsp = kwargs['pk']
        disp = self.model.objects.get(id_dsp=id_dsp)
        accion_user(disp, DELETION, request.user)
        disp.delete()
        messages.success(request, "Dispatch delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Diesel

class DieselView(ListView):
    model = Diesel
    template_name = 'logistic/diesel/dieselViews.html'

class DieselCreate(CreateView):
     model = Diesel
     form_class = DieselForm
     template_name = 'logistic/diesel/dieselForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class()
         return render(request, self.template_name, {'form': form, 'title': 'Create new Diesel Report'})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
            diesel = form.save(commit=False)
            diesel.users = request.user
            diesel.save()
            accion_user(diesel, ADDITION, request.user)
            messages.success(request, 'Diesel Report save with an extension')
            return HttpResponseRedirect(reverse_lazy('logistic:diesel'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)


class DieselEdit(UpdateView):
    model = Diesel
    form_class = DieselForm
    template_name = 'logistic/diesel/dieselForm.html'
    success_url = reverse_lazy('logistic:diesel')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        diesel = self.model.objects.get(id_dse=id)
        form = self.form_class(request.POST, instance=diesel)
        if form.is_valid():
            diesel =form.save()
            accion_user(diesel, CHANGE, request.user)
            messages.success(request, "Diesel Report update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Diesel Report'})

class DieselDelete(DeleteView):
    model = Diesel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:diesel')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        diesel = self.model.objects.get(id_dse=id)
        accion_user(diesel, DELETION, request.user)
        diesel.delete()
        messages.success(request, "Diesel Report delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Application

class ApplicationViews(ListView):
    model = Application
    template_name = 'logistic/application/aplicationViews.html'

class ApplicationCreate(CreateView):
     model = Application
     form_class = ApplicationForm
     template_name = 'logistic/application/aplicationForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class()
         return render(request, self.template_name, {'form': form, 'company': 'J&L 24/7 LLC'})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
            apply = form.save(commit=False)
            apply.users = request.user
            apply.date = datetime.now().strftime("%Y-%m-%d")
            apply.update = datetime.now().strftime("%Y-%m-%d")
            apply.state = 'Request'
            apply.save()
            accion_user(apply, ADDITION, request.user)
            if request.POST.get('leng', False):
               messages.success(request, 'Applicaction send with an extension!!!')
            else:
                messages.success(request, 'Aplicacion enviada con exito!!!')
            return HttpResponseRedirect(reverse_lazy('home'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return self.get(request)

class ApplicationEdit(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'logistic/application/aplicationForm.html'
    success_url = reverse_lazy('application:apply_views')

    def get_context_data(self, **kwargs):
        context = super(ApplicationEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['id'] = self.kwargs.get('pk', 0)
        context['title'] = 'Edit Application'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        apply = self.model.objects.get(id_apl=id)
        form = self.form_class(request.POST, instance=apply)
        if form.is_valid():
            apply =form.save(commit=False)
            if apply.state == 'Request':
                apply.state = 'Viewed'
            apply.update = datetime.now().strftime("%Y-%m-%d")
            apply.save()

            accion_user(apply, CHANGE, request.user)
            messages.success(request, "Applicacion update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Diesel Report'})

class ApplicationDelete(DeleteView):
    model = Application
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('application:apply_views')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        apply = self.model.objects.get(id_apl=id)
        accion_user(apply, DELETION, request.user)
        apply.delete()
        messages.success(request, "Application delete with an extension")
        return HttpResponseRedirect(self.success_url)
