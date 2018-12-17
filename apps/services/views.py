from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import Group, GroupManager
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponse
from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from apps.services.components.ServicesForm import *
from apps.tools.components.AlertForm import AlertForm
from apps.services.models import *
from apps.accounting.models import Customer
from apps.logistic.models import CustomerHasLoad, Load, DispatchLoadHasLoad
from apps.tools.models import Folder, Busines, File, Alert
from datetime import datetime, date, time, timedelta
from Prime.util import accion_user
import os


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

def PermitView(request, pk, popup):
    permit = Permit.objects.get(id_com=pk)
    return render(request, 'services/permit/permitView.html', {'permit': permit, 'is_popup':popup, 'title':'Permit', 'deactivate':True})


def SelectView(request, pk):

    if request.method == 'POST':
       if request.POST.get('permit', False):
          return HttpResponseRedirect('/services/permit/create/'+ pk)
       elif request.POST.get('equipment', False):
          return HttpResponseRedirect('/services/equipment/create/' + pk)
       elif request.POST.get('insurance', False):
          return HttpResponseRedirect('/services/insurance/create/' + pk)
       elif request.POST.get('driver', False):
          return HttpResponseRedirect('/services/driver/create/' + pk)
       elif request.POST.get('ifta', False):
          return HttpResponseRedirect('/services/ifta/create/' + pk)
       elif request.POST.get('audit', False):
          return HttpResponseRedirect('/services/audit/create/' + pk)
       elif request.POST.get('contract', False):
          return HttpResponseRedirect('/services/contract/create/' + pk)
       elif request.POST.get('dispatch', False):
          return HttpResponseRedirect('/services/dispatch/select/' + pk)
       else:
           return HttpResponseRedirect('/accounting/customers/view/' + pk)


class PermitCreate(CreateView):
      model = Permit
      template_name = 'services/permit/permitForm.html'
      form_class = PermitForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('pk'):
            id = kwargs['pk']
          else:
            id = None
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'id': id, 'form': form, 'customers':customer, 'title': 'Create Permit'})

      def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          if form.is_valid():
              permit_exist = Permit.objects.filter(name=request.POST['name'], ein=request.POST['ein'])
              if permit_exist:
                  messages.error(request, 'The Company already exists')
                  form = self.form_class(initial=self.initial)
                  return self.get(request)
              else:
                  permit = form.save(commit=False)
                  if kwargs.__contains__('pk'):
                    customer = Customer.objects.get(id_cut=kwargs['pk'])
                  else:
                    customer = Customer.objects.get(id_cut=request.POST['customers'])
                  permit.customers = customer
                  permit.users_id = request.user.id
                  permit.update = datetime.now().strftime("%Y-%m-%d")
                  if permit.deactivate:
                      permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      permit.deactivate_date = None
                  permit.save()
                  customer.company_name = permit.name+' '+permit.legal_status
                  customer.ein = permit.ein
                  customer.save()
                  if request.POST.get('txdmv_alert', False) and len(request.POST['txdmv_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = permit.txdmv_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the TXDMV Permit of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('ucr_alert', False) and len(request.POST['ucr_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = permit.ucr_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the UCR Permit of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  accion_user(permit, ADDITION, request.user)
                  messages.success(request, 'The Permit was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(permit.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return self.get(request)


class PermitEdit(UpdateView):
    model = Permit
    template_name = 'services/permit/permitForm.html'
    form_class = PermitForm

    def get_context_data(self, **kwargs):
        context = super(PermitEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        permit = self.model.objects.get(id_com=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=permit)
        context['id'] = pk
        context['title'] = 'Edit Permit'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        permit = self.model.objects.get(id_com=pk)
        form = self.form_class(request.POST, instance=permit)
        if form.is_valid():
                permit = form.save(commit=False)
                permit.update = datetime.now().strftime("%Y-%m-%d")
                permit.users_id = request.user.id
                if permit.deactivate:
                    permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    permit.deactivate_date = None
                permit.save()
                customer = Customer.objects.get(id_cut=permit.customers_id)
                customer.company_name = permit.name + ' ' + permit.legal_status
                customer.ein = permit.ein
                customer.save()
                alerCust = CustomerHasAlert.objects.filter(customers=customer)
                if request.POST.get('txdmv_alert', False) and len(request.POST['txdmv_date_exp']) != 0:
                   dateExp = permit.txdmv_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the TXDMV Permit of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                      for a in alert:
                          if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                              CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the TXDMV Permit of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the TXDMV Permit of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('ucr_alert', False) and len(request.POST['ucr_date_exp']) != 0:
                   dateExp = permit.ucr_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the UCR Permit of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                       for a in alert:
                           if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                               CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the UCR Permit of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(description="Expires the UCR Permit of the customer " + str(customer), category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                accion_user(permit, CHANGE, request.user)
                messages.success(request, 'The Permit was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(permit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form,  'is_popup': popup, 'title': 'Edit Permit'})

class PermitDelete(DeleteView):
    model = Permit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        permit = self.model.objects.get(id_com=id)
        customer = permit.customers
        alerCust = CustomerHasAlert.objects.filter(customers=customer)
        alert_txdmv = Alert.objects.filter(description = "Expires the TXDMV Permit of the customer " + str(permit.customers),
                                     end_date=permit.txdmv_date_exp)
        alert_ucr = Alert.objects.filter(description = "Expires the UCR Permit of the customer" + str(permit.customers),
                                           end_date=permit.ucr_date_exp)
        accion_user(permit, DELETION, request.user)
        if alert_txdmv:
            for a in alert_txdmv:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        if alert_ucr:
            for a in alert_ucr:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        permit.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

class FormView(ListView):
    model = File
    template_name = 'services/form/fileViews.html'

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        if Folder.objects.filter(name='Forms'):
            folder_father = Folder.objects.get(name='Forms')
            forms = pagination(self.request, File.objects.filter(folders=folder_father).order_by('name'))
            context['forms'] = forms
            return context

class FormCreate(CreateView):
    model = File
    form_class = FileForm
    template_name = 'services/form/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Form'})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            folder_exist = Folder.objects.filter(name='Forms')
            if not folder_exist:
                folder = Folder.objects.create(name='Forms', description='All Forms')
            else:
                folder = Folder.objects.get(name='Forms')
            file = form.save(commit=False)
            file.users_id = user.id
            file.folders_id = folder.id_fld
            file.description = file.name
            file.save()
            messages.success(request, "Form saved with an extension")
            accion_user(file, ADDITION, request.user)

            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Form'})


class FormEdit(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'services/form/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def get_context_data(self, **kwargs):
        context = super(FormEdit, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', 0)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        if 'form' not in context:
            context['form'] = self.form_class
        context['id'] = id
        context['is_popup'] = popup
        context['title'] = 'Edit Form'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        form = self.form_class(request.POST, request.FILES, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit File'})

class FormDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        file = self.model.objects.get(id_fil=id)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete")
        return HttpResponseRedirect(self.success_url)

class FolderView(ListView):
    model = File
    template_name = 'services/folder/folderViews.html'

    def get_context_data(self, **kwargs):
        context = super(FolderView, self).get_context_data(**kwargs)
        folders = pagination(self.request, Folder.objects.all().order_by('name'))
        file = pagination(self.request,File.objects.all().order_by('name'))
        context['folders'] = folders
        context['files'] = file
        return context


class FolderCreate(CreateView):
    model = File
    form_class = inlineformset_factory(
        Folder,
        File,
        form=FileForm,
        fields=['name',
                'category',
                'url',
                ],
        extra=10
    )
    template_name = 'services/folder/folderForm.html'


    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pk'):
            customer = None
        else:
            customer = pagination(request, Customer.objects.filter(deactivated=False).order_by('company_name'))
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form_files': form,  'customers': customer, 'title': 'Create new Folder'})

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs.__contains__('pk'):
            id = kwargs['pk']
            customer = Customer.objects.get(id_cut=id)
        else:
            customer = Customer.objects.get(id_cut=request.POST['customers'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            folder = Folder.objects.get(id_fld=customer.folders_id)
            file = form.save(commit=False)
            for f in file:
              f.users = user
              f.folders = folder
              f.save()
            messages.success(request, "Form saved with an extension")
            accion_user(file, ADDITION, request.user)
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form_files': form, 'customers':customer,'title': 'Create new Folder'})


class FolderEdit(UpdateView):
    model = File
    template_name = 'services/folder/folderForm.html'
    form_class = FileForm

    def get_context_data(self, **kwargs):
        context = super(FolderEdit, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', 0)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        if 'form_file' not in context:
            context['form_file'] = self.form_class
        context['id'] = id
        context['is_popup'] = popup
        context['title'] = 'Edit File'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        customer = Customer.objects.get(folders=file.folders)
        form = self.form_class(request.POST, request.FILES, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form_file': form, 'title': 'Edit File'})

class FolderDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        file = self.model.objects.get(id_fil=id)
        customer = Customer.objects.get(folders=file.folders)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))


def EquipmentView(request, pk, popup):
    equipment = Equipment.objects.get(id_tru=pk)
    return render(request, 'services/equipment/equipmentView.html', {'equipment': equipment, 'is_popup':popup, 'title':'Equipment', 'deactivate':True})


class EquipmentCreate(CreateView):
    model = Equipment
    template_name = 'services/equipment/equipmentForm.html'
    form_class = EquipmentForm

    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pk'):
            id = kwargs['pk']
        else:
            id = None
        customer = Customer.objects.filter(deactivated=False).order_by('company_name')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form, 'customers': customer, 'id': id, 'title': 'Create Equipment'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            equipment_exist = Equipment.objects.filter(type=form.data['type'], serial=form.data['serial'])
            if equipment_exist:
                messages.error(request, 'The Equipment already exists')
                return self.get(request)
            else:
                equipment = form.save(commit=False)
                if kwargs.__contains__('pk'):
                    customer = Customer.objects.get(id_cut=kwargs['pk'])
                else:
                    customer = Customer.objects.get(id_cut=request.POST['customers'])
                equipment.customers = customer
                equipment.users = request.user
                equipment.update = datetime.now().strftime("%Y-%m-%d")
                if equipment.deactivate:
                    equipment.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    equipment.deactivate_date = None
                equipment.save()
                if request.POST.get('plate_alert', False) and len(request.POST['plate_date_exp']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.plate_date_exp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Plate Equipment Number "+str(equipment.serial) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=customer, alert=alert)
                if request.POST.get('reg_alert', False) and len(request.POST['title_date_exp_reg']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.title_date_exp_reg
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Title Register Equipment Number "+str(equipment.serial) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=customer, alert=alert)
                if request.POST.get('insp_alert', False) and len(request.POST['title_date_exp_insp']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.title_date_exp_insp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Inspection Equipment Number "+str(equipment.serial) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=customer, alert=alert)
                accion_user(equipment, ADDITION, request.user)
                messages.success(request, 'The Permit was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(equipment.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get(request)


class EquipmentEdit(UpdateView):
    model = Equipment
    template_name = 'services/equipment/equipmentForm.html'
    form_class = EquipmentForm

    def get_context_data(self, **kwargs):
        context = super(EquipmentEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        equipment = self.model.objects.get(id_tru=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=equipment)
        context['id'] = pk
        context['title'] = 'Edit Equipment'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        equipment = self.model.objects.get(id_tru=pk)
        form = self.form_class(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.update = datetime.now().strftime("%Y-%m-%d")
            equipment.users_id = request.user.id
            if equipment.deactivate:
                equipment.deactivate_date = datetime.now().strftime("%Y-%m-%d")
            else:
                equipment.deactivate_date = None
            equipment.save()
            customer = equipment.customers
            alerCust = CustomerHasAlert.objects.filter(customers=customer)
            if request.POST.get('plate_alert', False)  and len(request.POST['plate_date_exp']) != 0:
                dateExp = equipment.plate_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Plate Equipment Number " + str(equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                    for a in alert:
                        if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                           CustomerHasAlert.objects.create(customers=customer, alert=a)
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Plate Equipment Number " + str(equipment.serial) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=customer, alert=alert)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Plate Equipment Number " + str(equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    for a in alert:
                        if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                            CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                        a.delete()
            if request.POST.get('reg_alert', False) and len(request.POST['title_date_exp_reg']) != 0:
                dateExp = equipment.title_date_exp_reg
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Title Register Equipment Number " + str(equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                    for a in alert:
                        if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                           CustomerHasAlert.objects.create(customers=customer, alert=a)
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Title Register Equipment Number " + str(
                            equipment.serial) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=equipment.customers, alert=alert)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Title Register Equipment Number " + str(
                        equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    for a in alert:
                        if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                            CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                        a.delete()
            if request.POST.get('insp_alert', False) and len(request.POST['title_date_exp_insp']) != 0:
                dateExp = equipment.title_date_exp_insp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Inspection Equipment Number " + str(equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                    for a in alert:
                        if not CustomerHasAlert.objects.filter(customers=equipment.customers, alert=a):
                           CustomerHasAlert.objects.create(customers=equipment.customers, alert=a)
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Inspection Equipment Number " + str(
                            equipment.serial) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=equipment.customers, alert=alert)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Inspection Equipment Number " + str(
                        equipment.serial) + " of the customer " + str(equipment.customers))
                if alert:
                    for a in alert:
                        if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                            CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                        a.delete()
            accion_user(equipment, CHANGE, request.user)
            messages.success(request, 'The Equipment was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(equipment.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get_context_data()

class EquipmentDelete(DeleteView):
    model = Permit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        equipment = self.model.objects.get(id_com=id)
        customer = equipment.customers
        alert_plate = Alert.objects.filter(
            category="Urgents",
            description="Expires of the Plate Equipment Number " + str(
                equipment.serial) + " of the customer " + str(equipment.customer))

        alert_reg = Alert.objects.filter(category="Urgents",
                                     description="Expires of the Title Register Equipment Number " + str(
                                         equipment.serial) + " of the customer " + str(equipment.customer))

        alert_insp = Alert.objects.filter(
            category="Urgents",
            description="Expires of the Inspection Equipment Number " + str(
                equipment.serial) + " of the customer " + str(equipment.customer))
        accion_user(equipment, DELETION, request.user)
        if alert_plate:
            for a in alert_plate:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        if alert_reg:
            for a in alert_reg:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        if alert_insp:
            for a in alert_insp:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        equipment.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect(HttpResponseRedirect('/accounting/customers/view/' + str(equipment.customers_id)))

def InsuranceView(request, pk, popup):
    insurance = Insurance.objects.get(id_ins=pk)
    return render(request, 'services/insurance/insuranceView.html', {'insurance': insurance, 'is_popup':popup, 'title':'Insurance', 'deactivate':True})


class InsuranceCreate(CreateView):
      model = Insurance
      template_name = 'services/insurance/insuranceForm.html'
      form_class = InsuranceForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('pk'):
            id = kwargs['pk']
          else:
              id = None
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'id': id, 'title': 'Create Insurance'})

      def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          if form.is_valid():
                  insurance = form.save(commit=False)
                  if kwargs.__contains__('pk'):
                    customer = Customer.objects.get(id_cut=kwargs['pk'])
                  else:
                    customer = Customer.objects.get(id_cut=request.POST['customers'])
                  insurance.customers = customer
                  insurance.users = request.user
                  insurance.update = datetime.now().strftime("%Y-%m-%d")
                  insurance.save()
                  if request.POST.get('liability_alert', False) and len(request.POST['policy_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.policy_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Insurance Liability Policy  of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('cargo_alert', False) and len(request.POST['policy_cargo_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.policy_cargo_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Insurance Cargo Policy  of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('physical_alert', False) and len(request.POST['policy_physical_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.policy_physical_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Insurance Physical Damage Policy  of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('other_alert', False) and len(request.POST['policy_other_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.policy_other_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Insurance "+str(insurance.other_description)+" Policy  of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('monthly_alert', False) and len(request.POST['monthlypay']) != 0:
                      group_admin = Group.objects.get(name='System Administrator')
                      group_manag = Group.objects.get(name='System Manager')
                      group_offic = Group.objects.get(name='Office Specialist')
                      monthpay = int(insurance.months)
                      day = insurance.monthlypay
                      today = datetime.now()
                      cont = 0
                      while cont < monthpay:

                          if today.month + cont > 12:
                              month = (today.month + cont) - 12
                          else:
                              month = today.month + cont
                          if month < today.month:
                              year = today.year + 1
                          else:
                              year = today.year
                          dateExp = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")
                          dateShow = dateExp - timedelta(days=15)
                          alert = Alert.objects.create(
                              category="Urgents",
                              description="The next " + str(
                                  insurance.monthlypay) + " is the monthly insurance payment day of the customer" + str(
                                  customer),
                              create_date=today.strftime("%Y-%m-%d"),
                              show_date=dateShow.strftime("%Y-%m-%d"),
                              end_date=dateExp.strftime("%Y-%m-%d"),
                              users=request.user)
                          alert.group.add(group_admin, group_manag, group_offic)
                          CustomerHasAlert.objects.create(customers=customer, alert=alert)
                          cont += 1
                  accion_user(insurance, ADDITION, request.user)
                  messages.success(request, 'The Insurance was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(insurance.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return self.get(request)


class InsuranceEdit(UpdateView):
    model = Insurance
    template_name = 'services/insurance/insuranceForm.html'
    form_class = InsuranceForm

    def get_context_data(self, **kwargs):
        context = super(InsuranceEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        insurance = self.model.objects.get(id_ins=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=insurance)
        context['id'] = pk
        context['title'] = 'Edit Insurance'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        insurance = self.model.objects.get(id_ins=pk)
        form = self.form_class(request.POST, instance=insurance)
        if form.is_valid():
                insurance = form.save(commit=False)
                insurance.update = datetime.now().strftime("%Y-%m-%d")
                insurance.users = request.user
                insurance.save()
                customer = Customer.objects.get(id_cut=insurance.customers_id)
                alerCust = CustomerHasAlert.objects.filter(customers=customer)
                if request.POST.get('liability_alert', False) and len(request.POST['policy_date_exp']) != 0:
                   dateExp = insurance.policy_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Insurance Liability Policy  of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                      for a in alert:
                          if not a in alerCust:
                              CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Insurance Liability Policy  of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the Insurance Liability Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if not a in alerCust:
                                a.delete()
                if request.POST.get('cargo_alert', False) and len(request.POST['policy_cargo_exp']) != 0:
                   dateExp = insurance.policy_cargo_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Insurance Cargo Policy  of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                      for a in alert:
                          if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                              CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Insurance Cargo Policy  of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the Insurance Cargo Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('physical_alert', False) and len(request.POST['policy_physical_exp']) != 0:
                    dateExp = insurance.policy_physical_exp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="Expires the Insurance Physical Damage Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                        for a in alert:
                            if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.create(customers=customer, alert=a)
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Expires the Insurance Physical Damage Policy  of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the Insurance Physical Damage Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('other_alert', False) and len(request.POST['policy_other_exp']) != 0:
                    dateExp = insurance.policy_other_exp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="Expires the Insurance "+str(insurance.other_description)+" Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                        for a in alert:
                            if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.create(customers=customer, alert=a)
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Expires the Insurance "+str(insurance.other_description)+" Policy  of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)

                else:
                    alert = Alert.objects.filter(
                        description="Expires the Insurance "+str(insurance.other_description)+" Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('monthly_alert', False) and len(request.POST['monthlypay']) != 0:
                   alert = Alert.objects.filter(description = "The next "+str(insurance.monthlypay)+" is the monthly insurance payment day of the customer" + str(customer), category="Urgents")
                   if alert:
                       monthpay = int(insurance.months)
                       day = insurance.monthlypay
                       today = datetime.now()
                       cont = 0
                       while cont < monthpay:

                           if today.month + cont > 12:
                               month = (today.month + cont) - 12
                           else:
                               month = today.month + cont
                           if month < today.month:
                               year = today.year + 1
                           else:
                               year = today.year
                           dateExp = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")
                           dateShow = dateExp - timedelta(days=15)

                           alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                           cont += 1
                       for a in alert:
                          if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                              CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       monthpay = int(insurance.months)
                       day = insurance.monthlypay
                       today = datetime.now()
                       cont = 0
                       while cont < monthpay:

                           if today.month + cont > 12:
                               month = (today.month + cont) - 12
                           else:
                               month = today.month + cont
                           if month < today.month:
                               year = today.year + 1
                           else:
                               year = today.year
                           dateExp = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")
                           dateShow = dateExp - timedelta(days=15)
                           alert = Alert.objects.create(
                               category="Urgents",
                               description="The next " + str(
                                   insurance.monthlypay) + " is the monthly insurance payment day of the customer" + str(
                                   customer),
                               create_date=today.strftime("%Y-%m-%d"),
                               show_date=dateShow.strftime("%Y-%m-%d"),
                               end_date=dateExp.strftime("%Y-%m-%d"),
                               users=request.user)
                           alert.group.add(group_admin, group_manag, group_offic)
                           CustomerHasAlert.objects.create(customers=customer, alert=alert)
                           cont += 1
                else:
                    alert = Alert.objects.filter(
                        description="The next "+str(insurance.monthlypay)+" is the monthly insurance payment day of the customer" + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                accion_user(insurance, CHANGE, request.user)
                messages.success(request, 'The Insurance was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(insurance.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get(request)

class InsuranceDelete(DeleteView):
    model = Insurance
    template_name = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        insurance = self.model.objects.get(id_ins=id)
        dateExp = insurance.monthlypay
        customer = insurance.customers
        alert_liability = Alert.objects.filter(description = "Expires the Insurance Liability Policy  of the customer " + str(insurance.customers),
                                     end_date=insurance.policy_date_exp)
        alert_cargo = Alert.objects.filter(
            description="Expires the Insurance Cargo Policy  of the customer " + str(insurance.customers),
            end_date=insurance.policy_cargo_exp)
        alert_physical = Alert.objects.filter(
            description="Expires the Insurance Physical Damage Policy  of the customer " + str(insurance.customers),
            end_date=insurance.policy_physical_exp)
        alert_other = Alert.objects.filter(
            description="Expires the Insurance "+str(insurance.other_description)+" Policy  of the customer " + str(insurance.customers),
            end_date=insurance.policy_other_exp)
        alert_monthly = Alert.objects.filter(
            description="The next "+str(insurance.monthlypay)+" is the monthly insurance payment day of the customer" + str(insurance.customers),
            end_date=insurance.monthlypay)
        accion_user(insurance, DELETION, request.user)
        if alert_liability:
          for a in alert_liability:
              if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                  CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
              a.delete()
        if alert_cargo:
          for a in alert_cargo:
              if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                  CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
              a.delete()
        if alert_physical:
          for a in alert_physical:
              if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                  CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
              a.delete()
        if alert_other:
          for a in alert_other:
              if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                  CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
              a.delete()
        if alert_monthly:
            for a in alert_monthly:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        insurance.delete()
        messages.success(request, "Insurance delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(insurance.customers_id))

def DriverView(request, pk, popup):
    driver = Driver.objects.get(id_drv=pk)
    return render(request, 'services/driver/driverView.html', {'driver': driver, 'is_popup':popup, 'title':'Driver', 'deactivate':True})

class DriverCreate(CreateView):
      model = Driver
      template_name = 'services/driver/driverForm.html'
      form_class = DriverForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('pk'):
            id = kwargs['pk']
          else:
              id = None
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'id': id, 'title': 'Create Driver'})

      def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          if form.is_valid():
              driver_exist = Driver.objects.filter(name=request.POST['name'], license_numb=request.POST['license_numb'])
              if driver_exist:
                  messages.error(request, 'The driver already exists')
                  return self.get(request)
              else:
                  driver = form.save(commit=False)
                  if kwargs.__contains__('pk'):
                    customer = Customer.objects.get(id_cut=kwargs['pk'])
                  else:
                    customer = Customer.objects.get(id_cut=request.POST['customers'])
                  driver.customers = customer
                  driver.users = request.user
                  driver.update = datetime.now().strftime("%Y-%m-%d")
                  if driver.deactivate:
                      driver.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      driver.deactivate_date = None
                  driver.save()
                  if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = driver.lic_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the License Driver of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = driver.medicard_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Medicard Driver of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                      group_admin = Group.objects.get(name='System Administrator')
                      group_manag = Group.objects.get(name='System Manager')
                      group_offic = Group.objects.get(name='Office Specialist')
                      dateExp = driver.drugtest_date_exp
                      dateShow = dateExp - timedelta(days=30)
                      alert = Alert.objects.create(
                          category="Urgents",
                          description="Expires the Drugtest Driver of the customer " + str(customer),
                          create_date=datetime.now().strftime("%Y-%m-%d"),
                          show_date=dateShow.strftime("%Y-%m-%d"),
                          end_date=dateExp.strftime("%Y-%m-%d"),
                          users=request.user)
                      alert.group.add(group_admin, group_manag, group_offic)
                      CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                      group_admin = Group.objects.get(name='System Administrator')
                      group_manag = Group.objects.get(name='System Manager')
                      group_offic = Group.objects.get(name='Office Specialist')
                      dateExp = driver.mbr_date_exp
                      dateShow = dateExp - timedelta(days=30)
                      alert = Alert.objects.create(
                          category="Urgents",
                          description="Expires the Mbr Driver of the customer " + str(customer),
                          create_date=datetime.now().strftime("%Y-%m-%d"),
                          show_date=dateShow.strftime("%Y-%m-%d"),
                          end_date=dateExp.strftime("%Y-%m-%d"),
                          users=request.user)
                      alert.group.add(group_admin, group_manag, group_offic)
                      CustomerHasAlert.objects.create(customers=customer, alert=alert)
                  accion_user(driver, ADDITION, request.user)
                  messages.success(request, 'The Driver was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(driver.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return self.get(request)


class DriverEdit(UpdateView):
    model = Driver
    template_name = 'services/driver/driverForm.html'
    form_class = DriverForm

    def get_context_data(self, **kwargs):
        context = super(DriverEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        driver = self.model.objects.get(id_drv=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=driver)
        context['id'] = pk
        context['title'] = 'Edit Driver'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        driver = self.model.objects.get(id_drv=pk)
        form = self.form_class(request.POST, instance=driver)
        if form.is_valid():
                driver = form.save(commit=False)
                driver.update = datetime.now().strftime("%Y-%m-%d")
                driver.users = request.user
                driver.save()
                customer = Customer.objects.get(id_cut=driver.customers_id)
                alerCust = CustomerHasAlert.objects.filter(customers=customer)
                if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                   dateExp = driver.lic_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the License Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                      for a in alert:
                          if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                              CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='SystemManager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the License Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the License Driver of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                   dateExp = driver.medicard_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Medicard Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                       for a in alert:
                           if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                               CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Medicard Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(description="Expires the Medicard Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                   dateExp = driver.drugtest_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Drugtest Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                       for a in alert:
                           if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                               CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Drugtest Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(description="Expires the Drugtest Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                   dateExp = driver.mbr_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Mbr Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                       for a in alert:
                           if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                               CustomerHasAlert.objects.create(customers=customer, alert=a)
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Mbr Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                       CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(description="Expires the Mbr Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                accion_user(driver, CHANGE, request.user)
                messages.success(request, 'The Driver was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(driver.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get_context_data()

class DriverDelete(DeleteView):
    model = Driver
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        driver = self.model.objects.get(id_drv=id)
        customer = driver.customers
        alert_lic = Alert.objects.filter(description="Expires the License Driver of the customer " + str(driver.customers),
                                           end_date=driver.lic_date_exp)
        alert_medicard = Alert.objects.filter(description="Expires the Medicard Driver of the customer" + str(driver.customers),
                                           end_date=driver.medicard_date_exp)
        alert_drugtest = Alert.objects.filter(description="Expires the Drugtest Driver of the customer " + str(driver.customers),
                                           end_date=driver.drugtest_date_exp)
        alert_mbr = Alert.objects.filter(description="Expires the Mbr Driver of the customer" + str(driver.customers),
                                           end_date=driver.mbr_date_exp)
        accion_user(driver, DELETION, request.user)
        if alert_lic:
            for a in alert_lic:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        if alert_medicard:
            for a in alert_medicard:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        if alert_drugtest:
            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
            for a in alert_drugtest:
                a.delete()
        if alert_mbr:
            for a in alert_mbr:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        customer = driver.customers
        driver.delete()
        messages.success(request, "Driver delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def IftaView(request, pk, popup):
        ifta = Ifta.objects.get(id_ift=pk)
        return render(request, 'services/ifta/iftaView.html',
                      {'ifta': ifta, 'is_popup': popup, 'title': 'Ifta', 'deactivate': True})

class IftaCreate(CreateView):
        model = Ifta
        template_name = 'services/ifta/iftaForm.html'
        form_class = IftaForm

        def get(self, request, *args, **kwargs):
            if kwargs.__contains__('pk'):
                id = kwargs['pk']
            else:
                id = None
            customer = Customer.objects.filter(deactivated=False).order_by('company_name')
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name,
                          {'form': form, 'customers': customer, 'id': id, 'title': 'Create Ifta'})

        def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                    ifta = form.save(commit=False)
                    if kwargs.__contains__('pk'):
                        customer = Customer.objects.get(id_cut=kwargs['pk'])
                    else:
                        customer = Customer.objects.get(id_cut=request.POST['customers'])
                    ifta.customers = customer
                    ifta.users = request.user
                    ifta.update = datetime.now().strftime("%Y-%m-%d")
                    ifta.save()
                    if request.POST.get('nex_period_alert', False) and len(request.POST['nex_period']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = ifta.nex_period
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Next period of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                    if request.POST.get('payment_alert', False) and len(request.POST['payment_due']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = ifta.payment_due
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="IFTA Payment Due of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                    accion_user(ifta, ADDITION, request.user)
                    messages.success(request, 'The Ifta was saved successfully')
                    return HttpResponseRedirect('/accounting/customers/view/' + str(ifta.customers_id))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                return self.get(request)

class IftaEdit(UpdateView):
        model = Ifta
        template_name = 'services/ifta/iftaForm.html'
        form_class = IftaForm

        def get_context_data(self, **kwargs):
            context = super(IftaEdit, self).get_context_data(**kwargs)
            if self.kwargs.__contains__('popup'):
                popup = self.kwargs.get('popup')
            else:
                popup = 0
            pk = self.kwargs.get('pk', 0)
            ifta = self.model.objects.get(id_ift=pk)
            if 'form' not in context:
                context['form'] = self.form_class(instance=ifta)
            context['id'] = pk
            context['is_popup'] = popup
            context['title'] = 'Edit Ifta'
            return context

        def post(self, request, *args, **kwargs):
            self.object = self.get_object
            pk = kwargs['pk']
            ifta = self.model.objects.get(id_ift=pk)
            form = self.form_class(request.POST, instance=ifta)
            if form.is_valid():
                ifta = form.save(commit=False)
                ifta.update = datetime.now().strftime("%Y-%m-%d")
                ifta.users = request.user
                ifta.save()
                customer = Customer.objects.get(id_cut=ifta.customers_id)
                if request.POST.get('nex_period_alert', False) and len(request.POST['nex_period']) != 0:
                    dateExp = ifta.nex_period
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="Next period of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                        for a in alert:
                            if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.create(customers=customer, alert=a)
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Next period of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="Next period of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                if request.POST.get('payment', False) and len(request.POST['payment_due']) != 0:
                    dateExp = ifta.payment_due
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="IFTA Payment Due of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                        for a in alert:
                            if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.create(customers=customer, alert=a)
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="IFTA Payment Due of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                        CustomerHasAlert.objects.create(customers=customer, alert=alert)
                else:
                    alert = Alert.objects.filter(
                        description="IFTA Payment Due of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        for a in alert:
                            if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                                CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                            a.delete()
                accion_user(ifta, CHANGE, request.user)
                messages.success(request, 'The Ifta was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(ifta.customers_id))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                return self.get_context_data()

class IftaDelete(DeleteView):
        model = Ifta
        template_name = 'confirm_delete.html'
        success_url = reverse_lazy('accounting:customer')

        def delete(self, request, *args, **kwargs):
            self.object = self.get_object
            id = kwargs['pk']
            ifta = self.model.objects.get(id_ift=id)
            customer = ifta.customers
            nex_period_alert = Alert.objects.filter(
                description="Next period of the customer " + str(ifta.customers),
                end_date=ifta.nex_period)
            payment_alert = Alert.objects.filter(
                description="IFTA Payment Due of the customer " + str(ifta.customers),
                end_date=ifta.payment_due)
            accion_user(ifta, DELETION, request.user)
            if nex_period_alert:
                for a in nex_period_alert:
                    if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                        CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                    a.delete()
            if payment_alert:
                for a in payment_alert:
                    if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                        CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                    a.delete()
            ifta.delete()
            messages.success(request, "Ifta delete with an extension")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def AuditView(request, pk, popup):
    audit = Audit.objects.get(id_aud=pk)
    return render(request, 'services/audit/auditView.html',
                  {'audit': audit, 'is_popup': popup, 'title': 'Audit', 'deactivate': True})


class AuditCreate(CreateView):
    model = Audit
    template_name = 'services/audit/auditForm.html'
    form_class = AuditForm

    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pk'):
            id = kwargs['pk']
        else:
            id = None
        customer = Customer.objects.filter(deactivated=False).order_by('company_name')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form, 'customers': customer, 'id': id, 'title': 'Create Audit'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            if kwargs.__contains__('pk'):
                customer = Customer.objects.get(id_cut=kwargs['pk'])
            else:
                customer = Customer.objects.get(id_cut=request.POST['customers'])
            audit.customers = customer
            audit.users = request.user
            audit.update = datetime.now().strftime("%Y-%m-%d")
            audit.save()
            accion_user(audit, ADDITION, request.user)
            messages.success(request, 'The Audit was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(audit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get(request)


class AuditEdit(UpdateView):
    model = Audit
    template_name = 'services/audit/auditForm.html'
    form_class = AuditForm

    def get_context_data(self, **kwargs):
        context = super(AuditEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        audit = self.model.objects.get(id_aud=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=audit)
        context['id'] = pk
        context['title'] = 'Edit Audit'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        audit = self.model.objects.get(id_aud=pk)
        form = self.form_class(request.POST, instance=audit)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.update = datetime.now().strftime("%Y-%m-%d")
            audit.users = request.user
            audit.save()
            accion_user(audit, CHANGE, request.user)
            messages.success(request, 'The Audit was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(audit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form, 'title': 'Edit Audit'})


class AuditDelete(DeleteView):
    model = Audit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        audit = self.model.objects.get(id_aud=id)
        accion_user(audit, DELETION, request.user)
        customer = audit.customers
        audit.delete()
        messages.success(request, "Audit delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def ContractView(request, pk, popup):
    contract = Contract.objects.get(id_con=pk)
    return render(request, 'services/contract/contractView.html',
                  {'contract': contract, 'is_popup': popup, 'title': 'Contract', 'deactivate': True})

class ContractCreate(CreateView):
    model = Contract
    template_name = 'services/contract/contractForm.html'
    form_class = ContractForm
    form_file_class = FileForm

    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pk'):
            id = kwargs['pk']
        else:
            id = None
        customer = Customer.objects.filter(deactivated=False).order_by('company_name')
        form = self.form_class()
        form_file = self.form_file_class()
        return render(request, self.template_name,
                      {'form': form, 'customers': customer, 'id': id, 'title': 'Create Contract', 'form2':form_file})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_file = self.form_file_class(request.POST, request.FILES)
        if form.is_valid() and form_file.is_valid():
            contract = form.save(commit=False)
            file = form_file.save(commit=False)
            if kwargs.__contains__('pk'):
                customer = Customer.objects.get(id_cut=kwargs['pk'])
            else:
                customer = Customer.objects.get(id_cut=request.POST['customers'])
            file.folders = customer.folders
            file.users = request.user
            file.save()
            contract.customers = customer
            contract.users = request.user
            contract.files = file
            contract.update = datetime.now().strftime("%Y-%m-%d")
            contract.save()
            if request.POST.get('end_alert', False) and len(request.POST['end_date']) != 0:
                group_admin = Group.objects.get(name='System Administrator')
                group_manag = Group.objects.get(name='System Manager')
                group_offic = Group.objects.get(name='Office Specialist')
                dateExp = contract.end_date
                dateShow = dateExp - timedelta(days=30)

                alert = Alert.objects.create(
                    category="Urgents",
                    description="The client's " + str(contract.type) + " contract ("+contract.serial+") " + str(customer) + " expires ",
                    create_date=datetime.now().strftime("%Y-%m-%d"),
                    show_date=dateShow.strftime("%Y-%m-%d"),
                    end_date=dateExp.strftime("%Y-%m-%d"),
                    users=request.user)
                alert.group.add(group_admin, group_manag, group_offic)
                CustomerHasAlert.objects.create(customers=customer, alert=alert)
            accion_user(contract, ADDITION, request.user)
            messages.success(request, 'The Contract was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(contract.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get(request)


class ContractEdit(UpdateView):
    model = Contract
    template_name = 'services/contract/contractForm.html'
    form_class = ContractForm
    form_file_class = FileForm

    def get_context_data(self, **kwargs):
        context = super(ContractEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        contract = self.model.objects.get(id_con=pk)
        file = File.objects.get(id_fil=contract.files_id)
        if 'form' not in context:
            context['form'] = self.form_class(instance=contract)
        if 'form2' not in context:
            context['form2'] = self.form_file_class(instance=file)
        context['id'] = pk
        context['title'] = 'Edit Contract'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        contract = self.model.objects.get(id_con=pk)
        file = File.objects.get(id_fil=contract.files_id)
        form = self.form_class(request.POST, instance=contract)
        form_file = self.form_file_class(request.POST, request.FILES, instance=file)
        if form.is_valid() and form_file.is_valid():
            contract = form.save(commit=False)
            file = form_file.save(commit=False)
            if kwargs.__contains__('pk'):
                customer = Customer.objects.get(id_cut=kwargs['pk'])
            else:
                customer = Customer.objects.get(id_cut=request.POST['customers'])
            file.folders = customer.folders
            file.save()
            contract.customers = customer
            contract.users = request.user
            contract.files = file
            contract.update = datetime.now().strftime("%Y-%m-%d")
            contract.save()
            if request.POST.get('end_alert', False) and len(request.POST['end_date']) != 0:
                dateExp = contract.end_date
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="The client's "+str(contract.type)+" contract ("+contract.serial+") "+str(customer)+" expires ")
                if alert:
                    alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                    for a in alert:
                        if not CustomerHasAlert.objects.filter(customers=customer, alert=a):
                            CustomerHasAlert.objects.create(customers=customer, alert=a)
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="The client's " + str(contract.type) + " contract ("+contract.serial+") " + str(customer) + " expires ",
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                    CustomerHasAlert.objects.create(customers=customer, alert=alert)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="The client's " + str(contract.type) + " contract ("+contract.serial+") " + str(customer) + " expires ")
                if alert:
                    for a in alert:
                        if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                            CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                        a.delete()
            accion_user(contract, CHANGE, request.user)
            messages.success(request, 'The Audit was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(contract.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return self.get_context_data()


class ContractDelete(DeleteView):
    model = Contract
    template_name = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        contract = self.model.objects.get(id_con=id)
        customer = contract.customers
        alert = Alert.objects.filter(
            category="Urgents",
            description="The client's " + str(contract.type) + " contract (" + contract.serial + ") " + str(
                customer) + " expires ")
        if alert:
            for a in alert:
                if CustomerHasAlert.objects.filter(customers=customer, alert=a):
                    CustomerHasAlert.objects.filter(customers=customer, alert=a).delete()
                a.delete()
        accion_user(contract, DELETION, request.user)
        contract.delete()
        messages.success(request, "Audit delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))


def Email(request, pk):

    customer = Customer.objects.get(id_cut=pk)
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
             att = form.cleaned_data['file']
             mail = EmailMessage(form.cleaned_data['topic'],form.cleaned_data['message'],to=[form.cleaned_data['email']])
             mail.attach_file(att)
             mail.send()
             accion_user(customer, CHANGE, request.user)
             messages.success(request, "Mail sent with success")
             return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, 'home/Email/sendEmail.html', {'form': form, 'customer': customer})
    else:
        sms = 'HELLO DEAR '+customer.fullname
        form = EmailForm(initial={'topic': str(customer.business.name)+' Information!', 'email': customer.email, 'message': sms})
    return render(request, 'home/Email/sendEmail.html', {'form': form, 'customer': customer})

def EmailSend(request, pk, fl):

    if not fl == 0:
       file = File.objects.get(id_fil=fl)
    else:
       file = None

    customer = Customer.objects.get(id_cut=pk)
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
             if file:
                att = 'static/media/'+str(file.url)
             else:
                att = form.cleaned_data['file']
             mail = EmailMessage(form.cleaned_data['topic'],form.cleaned_data['message'],to=[form.cleaned_data['email']])
             mail.attach_file(att)
             mail.send()
             accion_user(customer, CHANGE, request.user)
             messages.success(request, "Mail sent with success")
             return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, 'home/Email/sendEmail.html', {'form': form, 'customer': customer, 'file': file})
    else:
        sms = 'HELLO DEAR '+customer.fullname+', THIS EMAIL HAS BEEN GENERATED FROM THE AUTOMATED FIRST CALL INTERMODAL SYSTEM WITH INFORMATION THAT MAY BE OF INTEREST TO YOU, PLEASE DO NOT FORWARD THIS EMAIL, THANKS FIRST CALL INTERMODAL TEAM'
        form = EmailForm(initial={'topic': str(customer.business.name)+' Information!', 'email': customer.email, 'message': sms, 'file':file})
    return render(request, 'home/Email/sendEmail.html', {'form': form, 'customer': customer, 'file': file})


def CompanyLoadSelect(request):

     customerLoad = []
     for c in CustomerHasLoad.objects.all():
         customerLoad.append(c.customers)
     customers = Customer.objects.all()

     context = {
        'customersLoad': customerLoad,
        'customers': customers,
        'title': 'Selected Customer'
     }
     if request.method == 'POST':
          id = request.POST.get('customers', None)
          start = request.POST.get('start', None)
          end = request.POST.get('end', None)
          return HttpResponseRedirect('/services/dispatch/invoice/create/'+id+'&'+start+'&'+end)

     return render(request, 'services/companiesDispatch/selectLoadsForm.html', context)


def CompanyLoadSelectCoust(request, pk):

    context = {
        'id':pk,
        'title': 'Selected Customer'
    }
    if request.method == 'POST':
        start = request.POST.get('start', None)
        end = request.POST.get('end', None)
        return HttpResponseRedirect('/services/dispatch/invoice/create/' + pk + '&' + start + '&' + end)

    return render(request, 'services/companiesDispatch/selectLoadsForm.html', context)


class InvoicesLogViews(ListView):
    model = Invoice
    template_name = 'accounting/invoices/invoiceslogViews.html'

    def get_context_data(self, **kwargs):
        context = super(InvoicesLogViews, self).get_context_data(**kwargs)
        invoice = self.model.objects.filter(type='load').order_by('-start_date')
        context['title'] = 'List Invoices'
        context['object_list'] = invoice
        return context



def InvoiceLogView(request, pk):
            invoice = DispatchLoad.objects.get(id_inv=pk)
            InvLod = DispatchLoadHasLoad.objects.filter(invoices=invoice.id)
            loads = []
            for d in InvLod:
               loads.append(Load.objects.get(id_lod=d.loads_id))
            context = {'invoice': invoice,
                       'description': loads,
                       'id': pk,
                       'title': 'Invoice',
                       }
            return render(request, 'services/companiesDispatch/invoiceslogView.html', context)

class InvoicesLogCreate(CreateView):
        model = DispatchLoad
        form_class = CompanesDispatchForm
        template_name = 'services/companiesDispatch/invoiceslogForm.html'

        def get(self, request, *args, **kwargs):
            load_customer = []
            customer = Customer.objects.get(id_cut=self.kwargs.get('pk', 0))
            loads = CustomerHasLoad.objects.filter(customers=customer)
            start = datetime.strptime(str(kwargs.get('start')), '%Y-%m-%d')
            end = datetime.strptime(str(kwargs.get('end')), '%Y-%m-%d')
            for l in loads:
                load = Load.objects.get(id_lod=l.loads_id)
                pickup_date = datetime.strptime(str(load.pickup_date), '%Y-%m-%d')
                deliver_date = datetime.strptime(str(load.deliver_date), '%Y-%m-%d')
                if pickup_date >= start and deliver_date <= end:
                     load_customer.append(load)
            form = self.form_class(initial={'start_date': kwargs.get('start'), 'end_date': kwargs.get('end')})
            context= {'form': form,
                      'title':'Create new Invoice',
                      'loads':load_customer,
                      'customer':customer
                      }
            return render(request, self.template_name, context)

        def post(self, request, *args, **kwargs):

            form = self.form_class(request.POST)
            customer = Customer.objects.get(id_cut=self.kwargs.get('pk', 0))
            user = request.user
            invs = DispatchLoad.objects.filter(customers=customer).order_by('-serial')
            loads = Load.objects.filter(other_company=True)
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
                invoice.type = 'service'
                invoice.users = user
                invoice.customers = customer
                invoice.save()
                accion_user(invoice, ADDITION, request.user)
                for lodinv in loadInv:
                    DispatchLoadHasLoad.objects.create(
                      invoices=invoice,
                      loads=lodinv
                    )
                    if request.POST.get('paid_'+str(lodinv.id_lod), False):
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='True')
                    else:
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='False')
                messages.success(request, "Invoice saved with an extension")

                return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
            else:
                for er in form.errors:
                    messages.error(request, er)
                return self.get(request)


class InvoicesLogEdit(UpdateView):
        model = DispatchLoad
        form_class = CompanesDispatchForm
        template_name = 'services/companiesDispatch/invoiceslogForm.html'

        def get_context_data(self, **kwargs):
            context = super(InvoicesLogEdit, self).get_context_data(**kwargs)
            pk = self.kwargs.get('pk', 0)
            adjust = self.kwargs.get('bill')

            invoice = self.model.objects.get(id_inv=pk)
            customer = invoice.customers
            description = []
            loadInv = DispatchLoadHasLoad.objects.filter(invoices=invoice)
            for l in loadInv:
                load = Load.objects.get(id_lod=l.loads_id)
                description.append(load)
            context['title'] = 'Create new Invoice'
            context['customers'] = customer
            context['loads'] = description
            context['adjust'] = adjust
            return context

        def post(self, request, *args, **kwargs):
            self.object = self.get_object
            id_inv = kwargs['pk']
            invoice = self.model.objects.get(id_inv=id_inv)
            customer = invoice.customers
            form = self.form_class(request.POST, instance=invoice)
            loads = Load.objects.all()
            loadInv = []
            for l in loads:
                load = request.POST.get('id_' + str(l.id_lod), None)
                if load:
                    loadInv.append(l)
            if form.is_valid():
                invoice = form.save()
                InvHasLod = DispatchLoadHasLoad.objects.filter(invoices=invoice)
                for i in InvHasLod:
                    load = Load.objects.get(id_lod=i.loads_id)
                    if loadInv.__contains__(load):
                        i.delete()
                for lodinv in loadInv:
                    if not DispatchLoadHasLoad.objects.filter(invoices=invoice, loads=lodinv):
                       DispatchLoadHasLoad.objects.create(
                        invoices=invoice,
                        loads=lodinv
                        )
                    if request.POST.get('paid_' + str(lodinv.id_lod), False):
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='True')
                    else:
                        Load.objects.filter(id_lod=lodinv.id_lod).update(paid='False')
                messages.success(request, "Invoice update with an extension")
                return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + str(er))
                return self.get_context_data()

class InvoicesLogDelete(DeleteView):
        model = Invoice
        template_name = 'confirm_delete.html'

        def delete(self, request, *args, **kwargs):
            self.object = self.get_object
            id_inv = kwargs['pk']
            invoice = self.model.objects.get(id_inv=id_inv)
            customer = Customer.objects.get(id_cut=invoice.customers.id_cut)
            DispatchLoadHasLoad.objects.filter(invoices=invoice).delete()
            accion_user(invoice, DELETION, request.user)
            invoice.delete()
            messages.success(request, "Invoice delete with an extension")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))


class CustomerAplicView(ListView):
    model = CustomerAplic
    template_name = 'services/customerAplic/adminAplication.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerAplicView, self).get_context_data(**kwargs)
        proccustomer = ProcessAplic.objects.all().order_by('update')
        customer = CustomerAplic.objects.all().order_by('-dateaplic')
        newcustomer = []
        for p in proccustomer:
            for c in customer:
               if not c.id == p.customeraplic_id:
                  newcustomer.append(c)

        context['customers_proc'] = proccustomer
        context['customers_new'] = newcustomer
        return context

def CustomerAplicCreate(request):

    form_customer = CustomerAplicForm()
    form_payment = PaymentInfoForm()
    form_newcompany = NewCompanyForm()
    form_ifta = IftaAplicForm()
    form_dispatch = DispatchAplicForm()
    form_audit = AuditAplicForm()
    form_apportioned = ApportionedAplicForm()
    Form_file = inlineformset_factory(
        Folder,
        File,
        form=FileForm,
        fields=['name',
                'category',
                'url',
                ],
        extra=10
    )
    Form_driver = inlineformset_factory(
        CustomerAplic,
        DriverAplic,
        form=DriverAplicForm,
        fields=['name',
                'license_numb',
                'experience',
                'dob',
                'lic_date_exp'],
        extra=5
    )
    Form_vehicle = inlineformset_factory(
        CustomerAplic,
        VehicleAplic,
        form=VehicleAplicForm,
        fields=['type',
                'year',
                'marke',
                'vin',
                'owned',
                'leased'],
        extra=5
    )

    if request.method == 'POST':
        user = request.user
        form_customer = CustomerAplicForm(request.POST)
        form_payment = PaymentInfoForm(request.POST)
        form_newcompany = NewCompanyForm(request.POST)
        form_ifta = IftaAplicForm(request.POST)
        form_dispatch = DispatchAplicForm(request.POST)
        form_audit = AuditAplicForm(request.POST)
        form_apportioned = ApportionedAplicForm(request.POST)
        form_file = FileForm(request.POST, request.FILES)
        form_driver = Form_driver(request.POST)
        form_vehicle = Form_vehicle(request.POST)
        if form_customer.is_valid() and form_payment.is_valid():
            folder = Folder.objects.create(name=form_customer.data['fullname'] + "_Customer",
                                           description=form_customer.data['fullname'] + "_Customer",
                                           )
            customer = form_customer.save(commit=False)
            customer.folders = folder
            customer.save()
            payment = form_payment.save(commit=False)
            payment.customeraplic = customer
            payment.save()
            if request.POST.get('new_company', False):
                comp = ServicesAplic.objects.filter(service='new_company')
                if comp:
                    comp = ServicesAplic.objects.get(service='new_company')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='new_company', description= 'New Company')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('ifta', False):
                comp = ServicesAplic.objects.filter(service='ifta')
                if comp:
                    comp = ServicesAplic.objects.get(service='ifta')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='ifta', description='IFTA')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('dispatch', False):
                comp = ServicesAplic.objects.filter(service='dispatch')
                if comp:
                    comp = ServicesAplic.objects.get(service='dispatch')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='dispatch', description= 'Dispatch')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('audit', False):
                comp = ServicesAplic.objects.filter(service='audit')
                if comp:
                    comp = ServicesAplic.objects.get(service='audit')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='audit', description= 'Audit')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('training', False):
                comp = ServicesAplic.objects.filter(service='training')
                if comp:
                    comp = ServicesAplic.objects.get(service='training')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='training', description= 'Training')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('apportions', False):
                comp = ServicesAplic.objects.filter(service='apportions')
                if comp:
                    comp = ServicesAplic.objects.get(service='apportions')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='apportions', description= 'Apportioned')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('title', False):
                comp = ServicesAplic.objects.filter(service='title')
                if comp:
                    comp = ServicesAplic.objects.get(service='title')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='title', description= 'Title')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('insurance', False):
                comp = ServicesAplic.objects.filter(service='insurance')
                if comp:
                    comp = ServicesAplic.objects.get(service='insurance')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='insurance', description= 'Insurance')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if request.POST.get('permit', False):
                comp = ServicesAplic.objects.filter(service='permit')
                if comp:
                    comp = ServicesAplic.objects.get(service='permit')
                    ServicesCustomer.objects.create(servicesaplic=comp, customeraplic=customer)
                else:
                    serv = ServicesAplic.objects.create(service='permit', description= 'Permit')
                    ServicesCustomer.objects.create(servicesaplic=serv, customeraplic=customer)
            if form_newcompany.is_valid():
                newcompany = form_newcompany.save(commit=False)
                newcompany.customeraplic = customer
                newcompany.save()
            if form_ifta.is_valid():
                ifta = form_ifta.save(commit=False)
                ifta.customeraplic = customer
                ifta.save()
            if form_ifta.is_valid():
                ifta = form_ifta.save(commit=False)
                ifta.customeraplic = customer
                ifta.save()
            if form_dispatch.is_valid():
                dispatch = form_dispatch.save(commit=False)
                dispatch.customeraplic = customer
                dispatch.save()
            if form_audit.is_valid():
                audit = form_audit.save(commit=False)
                audit.customeraplic = customer
                audit.save()
            if form_apportioned.is_valid():
                apportioned = form_ifta.save(commit=False)
                apportioned.customeraplic = customer
                apportioned.save()
            if form_driver.is_valid():
                driver = form_driver.save(commit=False)
                for d in driver:
                    d.customeraplic = customer
                    d.save()
            if form_vehicle.is_valid():
                vehicle = form_vehicle.save(commit=False)
                for v in vehicle:
                    v.customeraplic = customer
                    v.save()
            #if form_file.is_valid():
                #files = form_file.save(commit=False)
               # for f in files:
                   # f.users = user
                   # f.folders = folder
                    #f.save()

            messages.success(request, "Form saved with an extension")
            return render(request, 'services/customerAplic/aplicsucces.html')
    return render(request, 'services/customerAplic/customeraplic.html',{
        'form_customer':form_customer,
        'form_payment': form_payment,
        'form_newcompany': form_newcompany,
        'form_ifta': form_ifta,
        'form_dispatch': form_dispatch,
        'form_audit': form_audit,
        'form_apportioned': form_apportioned,
        'form_driver': Form_driver,
        'form_vehicle': Form_vehicle,
        'form_file' : Form_file
    })

def CustomerProce(request, pk, popup):

    newcustomer = CustomerAplic.objects.get(id=pk)
    payment = PaymentInfo.objects.get(customeraplic=newcustomer)
    customer = ProcessAplic.objects.get(customeraplic=newcustomer).customers
    company = None
    ifta = None
    driver = None
    vehicle = None
    audit = None
    apportioned = None
    dispatch = None
    services = ServicesCustomer.objects.filter(customeraplic=newcustomer)
    files = File.objects.filter(folders=newcustomer.folders).order_by('category')

    if NewCompany.objects.filter(customeraplic=newcustomer):
        company = NewCompany.objects.get(customeraplic=newcustomer)

    if IftaAplic.objects.filter(customeraplic=newcustomer):
        ifta = IftaAplic.objects.get(customeraplic=newcustomer)

    if DriverAplic.objects.filter(customeraplic=newcustomer):
        driver= DriverAplic.objects.filter(customeraplic=newcustomer)

    if VehicleAplic.objects.filter(customeraplic=newcustomer):
        vehicle = VehicleAplic.objects.filter(customeraplic=newcustomer)

    if AuditAplic.objects.filter(customeraplic=newcustomer):
        audit = AuditAplic.objects.get(customeraplic=newcustomer)

    if ApportionedAplic.objects.filter(customeraplic=newcustomer):
        apportioned = ApportionedAplic.objects.get(customeraplic=newcustomer)

    if DispatchAplic.objects.filter(customeraplic=newcustomer):
        dispatch = DispatchAplic.objects.get(customeraplic=newcustomer)

    return render(request, 'services/customerAplic/procecingAplic.html', {
        'customer': newcustomer,
        'payment': payment,
        'company': company,
        'ifta': ifta,
        'driver': driver,
        'vehicle': vehicle,
        'audit': audit,
        'apportioned': apportioned,
        'dispatch': dispatch,
        'files': files,
        'services': services,
        'customers': customer,
        'is_popup': popup,
        'title': 'Process Request'})



def CustomerAplicProce(request, pk):

    newcustomer = CustomerAplic.objects.get(id=pk)
    payment = PaymentInfo.objects.get(customeraplic=newcustomer)
    company = None
    ifta = None
    driver = None
    vehicle = None
    audit = None
    apportioned = None
    dispatch = None
    busines = Busines.objects.all()
    services = ServicesCustomer.objects.filter(customeraplic=newcustomer)
    files = File.objects.filter(folders=newcustomer.folders).order_by('category')

    if NewCompany.objects.filter(customeraplic=newcustomer):
        company = NewCompany.objects.get(customeraplic=newcustomer)

    if IftaAplic.objects.filter(customeraplic=newcustomer):
        ifta = IftaAplic.objects.get(customeraplic=newcustomer)

    if DriverAplic.objects.filter(customeraplic=newcustomer):
        driver= DriverAplic.objects.filter(customeraplic=newcustomer)

    if VehicleAplic.objects.filter(customeraplic=newcustomer):
        vehicle = VehicleAplic.objects.filter(customeraplic=newcustomer)

    if AuditAplic.objects.filter(customeraplic=newcustomer):
        audit = AuditAplic.objects.get(customeraplic=newcustomer)

    if ApportionedAplic.objects.filter(customeraplic=newcustomer):
        apportioned = ApportionedAplic.objects.get(customeraplic=newcustomer)

    if DispatchAplic.objects.filter(customeraplic=newcustomer):
        dispatch = DispatchAplic.objects.get(customeraplic=newcustomer)

    if request.method == 'POST':
        customer_exist = Customer.objects.filter(email=newcustomer.email, fullname=newcustomer.fullname)
        if customer_exist:
            messages.error(request, 'The customer already exists')
            return render(request, 'services/customerAplic/procecingAplic.html', {
                'customer': newcustomer,
                'payment': payment,
                'company': company,
                'ifta': ifta,
                'driver': driver,
                'vehicle': vehicle,
                'audit': audit,
                'apportioned': apportioned,
                'dispatch': dispatch,
                'files': files,
                'services': services,
                'busines': busines,
                'title': 'Process Request'})
        else:
            customer = Customer.objects.create(
                users = request.user,
                folders =  newcustomer.folders,
                fullname = newcustomer.fullname,
                email = newcustomer.email,
                company_name = newcustomer.company_name,
                address = newcustomer.address,
                phone = newcustomer.phone,
                usdot = newcustomer.usdot,
                mc = newcustomer.mc,
                txdmv = newcustomer.txdmv,
             )
            customer.business = request.POST.getlist('business')
            customer.save()
            if NewCompany.objects.filter(customeraplic=newcustomer):
               company = NewCompany.objects.get(customeraplic=newcustomer)
               Permit.objects.create(
                  users = request.user,
                  customers = customer
               )

            if IftaAplic.objects.filter(customeraplic=newcustomer):
                 ifta = IftaAplic.objects.get(customeraplic=newcustomer)
                 Ifta.objects.create(
                    users=request.user,
                    customers=customer
                  )
            if DriverAplic.objects.filter(customeraplic=newcustomer):
                 driver = DriverAplic.objects.filter(customeraplic=newcustomer)
                 for d in driver:
                    Driver.objects.create(
                        users=request.user,
                        customers=customer,
                        name = d.name,
                        license_numb = d.license_numb,
                        dob = d.dob,
                    )

            if VehicleAplic.objects.filter(customeraplic=newcustomer):
                vehicle = VehicleAplic.objects.filter(customeraplic=newcustomer)
                for v in vehicle:
                    Equipment.objects.create(
                       users=request.user,
                       customers=customer,
                       type = v.type,
                       year = v.year,
                       model = v.marke,
                       serial = v.vin
                    )
            if VehicleAplic.objects.filter(customeraplic=newcustomer) or DriverAplic.objects.filter(customeraplic=newcustomer):
                Insurance.objects.create(
                    users=request.user,
                    customers=customer,
                )

            if AuditAplic.objects.filter(customeraplic=newcustomer):
                audit = AuditAplic.objects.get(customeraplic=newcustomer)
                Audit.objects.create(
                    users=request.user,
                    customers=customer,
                    folders = newcustomer.folders,
                    contracts = Contract.objects.create(users=request.user, customers=customer),
                    auditor_name = audit.auditormane,
                    date = audit.date,
                 )

            if ApportionedAplic.objects.filter(customeraplic=newcustomer):
               apportioned = ApportionedAplic.objects.get(customeraplic=newcustomer)

            if DispatchAplic.objects.filter(customeraplic=newcustomer):
                dispatch = DispatchAplic.objects.get(customeraplic=newcustomer)

            ProcessAplic.objects.create(
                customeraplic = newcustomer,
                customers = customer,
                users = request.user,
                state = 'Process'
            )

            accion_user(customer,ADDITION, request.user)
            messages.success(request, 'The Customer was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
    return render(request, 'services/customerAplic/procecingAplic.html', {
        'customer': newcustomer,
        'payment' : payment,
        'company' : company,
        'ifta' : ifta,
        'driver' : driver,
        'vehicle' : vehicle,
        'audit' : audit,
        'apportioned' : apportioned,
        'dispatch' : dispatch,
        'files': files,
        'services' : services,
        'busines' : busines,
        'title': 'Process Request'})

class CustomerAplicDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        file = self.model.objects.get(id_fil=id)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete")
        return HttpResponseRedirect(self.success_url)
