from django.core.mail.backends import console
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from Prime.util import accion_user
from apps.accounting.models import AccountDescrip, Account
from apps.tools.models import *
from apps.tools.components import CalendarForm, AlertForm
from apps.tools.components.AlertForm import AlertForm
from apps.services.models import *
from apps.tools.components.DirectoryForm import DirectoryForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from datetime import datetime, date, time, timedelta
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

# Create your views here.
def pagination(request, objects):
    paginator = Paginator(objects, 5)  # Show 25 contacts per page

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

def Chats(request):
    return render(request, "home/complement/chat.html")

class DirectoryTelephone(ListView):
    model = Directory
    template_name = 'directorytelephone/directoryViews.html'


class DirectoryTelephoneCreate(CreateView):
    model = Directory
    form_class = DirectoryForm
    template_name = 'directorytelephone/directoryForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Directory'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user
        if form.is_valid():
            alert = form.save(commit=False)
            alert.users = user
            alert.save()
            accion_user(alert, ADDITION, request.user)
            messages.success(request, "Contact save")

        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create New Contact'})
        return HttpResponseRedirect(reverse_lazy('panel:directory'))

class DirectoryTelephoneEdit(UpdateView):
    model = Directory
    form_class = DirectoryForm
    template_name = 'directorytelephone/directoryForm.html'
    success_url = reverse_lazy('panel:directory')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dir = kwargs['pk']
        directory = self.model.objects.get(id_dir=id_dir)
        form = self.form_class(request.POST, instance=directory)
        if form.is_valid():
            directory =form.save()
            accion_user(directory, CHANGE, request.user)
            messages.success(request, "Contact update")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Contact'})

class DirectoryTelephoneDelete(DeleteView):
    model = Directory
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:directory')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dir = kwargs['pk']
        directory = self.model.objects.get(id_dir=id_dir)
        accion_user(directory, DELETION, request.user)
        directory.delete()
        messages.success(request, "Contact delete")
        return HttpResponseRedirect(self.success_url)

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(users=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.users.username})
    else:
        return HttpResponse('Request must be POST.')

def Message(request):
    c = Chat.objects.all()
    return render(request, 'home/complement/messages.html', {'chat': c})

def panel_view(request):
    incomes = []
    expenses = []
    cash_i_total = {'total': 0}
    credit_i_total = {'total': 0}
    check_i__total = {'total': 0}
    cash_e_total = {'total': 0}
    credit_e_total = {'total': 0}
    check_e__total = {'total': 0}
    income_total = {'total': 0}
    expenses_total = {'total': 0}

    alert=[]
    inc = Account.objects.filter(primary=False, accounts_id = 1)
    exp = Account.objects.filter(primary=False, accounts_id=2)
    for i in inc:
        cash_i = {'total': 0}
        credit_i = {'total': 0}
        check_i = {'total': 0}
        if AccountDescrip.objects.filter(accounts_id = i.id_acn , waytopay='Cash'):
            cash_i = AccountDescrip.objects.get_waytopay('Cash', i.id_acn)
        if AccountDescrip.objects.filter(accounts_id = i.id_acn , waytopay='Check'):
            check_i = AccountDescrip.objects.get_waytopay('Check', i.id_acn)
        if AccountDescrip.objects.filter(accounts_id = i.id_acn , waytopay='Credit Card'):
            credit_i = AccountDescrip.objects.get_waytopay('Credit Card', i.id_acn)
        total_i = (cash_i['total']) + (check_i['total']) + (credit_i['total'])
        incomes.append({'account':i, 'cash': cash_i, 'check': check_i, 'credit': credit_i, 'total': total_i})
        cash_i_total['total'] += cash_i['total']
        credit_i_total['total'] += credit_i['total']
        check_i__total['total'] += check_i['total']
        income_total['total'] = (cash_i_total['total']) + (credit_i_total['total']) + (check_i__total['total'])
    for e in exp:
        credit_e = {'total': 0}
        cash_e = {'total': 0}
        check_e = {'total': 0}
        if AccountDescrip.objects.filter(accounts_id = e.id_acn , waytopay='Cash'):
            cash_e = AccountDescrip.objects.get_waytopay('Cash', e.id_acn)
        if AccountDescrip.objects.filter(accounts_id = e.id_acn , waytopay='Check'):
            check_e = AccountDescrip.objects.get_waytopay('Check', e.id_acn)
        if AccountDescrip.objects.filter(accounts_id = e.id_acn , waytopay='Credit Card'):
            credit_e = AccountDescrip.objects.get_waytopay('Credit Card', e.id_acn)
        total_e = (cash_e['total']) + (check_e['total']) + (credit_e['total'])
        expenses.append({'account':e, 'cash': cash_e, 'check': check_e, 'credit': credit_e, 'total': total_e})
        cash_e_total['total'] += cash_e['total']
        credit_e_total['total'] += credit_e['total']
        check_e__total['total'] += check_e['total']
        expenses_total['total'] = (cash_e_total['total']) + (credit_e_total['total']) + (check_e__total['total'])
    date_now = datetime.now().date()
    user_group = request.user.groups.all()
    alertUrg = Alert.objects.filter(category='Urgents').order_by('end_date')
    for u in alertUrg:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
               if u.show_date <= date_now and u.end_date >= date_now:
                  alert.append(u)
    permit = Permit.objects.all()
    insurance = Insurance.objects.all()
    equipment = Equipment.objects.all()
    ifta = Ifta.objects.all()
    contract = Contract.objects.all()
    audit = Audit.objects.all()
    # driver = Driver.objects.all()
    contexto = {'incomes': incomes,
                'expenses': expenses,
                'cash_i_total': cash_i_total,
                'credit_i_total': credit_i_total,
                'check_i_total': check_i__total,
                'cash_e_total': cash_e_total,
                'credit_e_total': credit_e_total,
                'check_e_total': check_e__total,
                'expenses_total':expenses_total,
                'income_total': income_total,
                'permits': permit,
                'insurances': insurance,
                'equipments': equipment,
                'contracts': contract,
                'iftas': ifta,
                #'drives': driver,
                'audits': audit,
                'alert': pagination(request, alert),
                'date_now': date_now}
    return render(request, 'home/complement/panel.html', contexto)

class PostCalendar(CreateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.users_id = user.id
            calendar.save()
            accion_user(calendar, ADDITION, request.user)
            messages.success(request, 'Event saved with an extension')
            return HttpResponseRedirect(reverse_lazy('panel:calendar'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Event'})

class UpdateCalendar(UpdateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'
    success_url = reverse_lazy('panel:calendar')

    def get_context_data(self, **kwargs):
        context = super(UpdateCalendar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        event = self.model.objects.get(id=pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['event'] = event
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cal = kwargs['pk']
        calendar = self.model.objects.get(id=id_cal)
        form = self.form_class(request.POST, instance=calendar)
        if form.is_valid():
            calendar =form.save()
            accion_user(calendar, CHANGE, request.user)
            messages.success(request, "Event update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit new Event'})

class DeleteCalendar(DeleteView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:calendar')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        calendar = self.model.objects.get(id=id)
        accion_user(calendar, DELETION, request.user)
        calendar.delete()
        messages.success(request, "Enent delete with an extension")
        return HttpResponseRedirect(self.success_url)

class Calendar_Panel(TemplateView):
    template_name = 'home/calendar/calendar_panel.html'


def GetCalendar(requiret):
    calendar = Calendar.objects.filter(users=requiret.user.id)
    event_json = []
    for event in calendar:
        events_user = {}
        events_user['start'] = str(event.start) + "T" + str(event.startTimer)
        events_user['end'] = str(event.end) + "T" + str(event.endTimer)
        events_user['title'] = event.title
        events_user['color'] = event.color
        events_user['url'] = "/panel/calendar/edit/"+str(event.id)
        event_json.append(events_user)
    context = event_json
    return JsonResponse(context, safe=False)

#Alert

def AlertsView(request, pk):
    alert = Alert.objects.get(id_alt=pk)
    contexto = {'form': alert, 'title':'Alert', 'style': 'primary', 'deactivate':True, 'is_popup':True}
    return render(request, 'alert/alertForm.html', contexto)


def NotificationView(request):
    alert = []
    date_now = datetime.now().date()
    user_group = request.user.groups.all()
    notifications = Alert.objects.filter(category='Notification')
    for u in notifications:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
                    alert.append(u)

    contexto = {'alerts': alert, 'today':date_now , 'title':'List Notification', 'style':'success'}
    return render(request, 'alert/alertViews.html', contexto)

def AlertView(request):
    alert = []
    date_now = datetime.now().date()
    user_group = request.user.groups.all()
    alerts = Alert.objects.filter(category='Alerts')
    for u in alerts:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
                    alert.append(u)
    contexto = {'alerts': alert, 'today':date_now ,'title':'List Alert', 'style':'warning'}
    return render(request, 'alert/alertViews.html', contexto)

def UrgentView(request):
    alert = []
    date_now = datetime.now().date()
    user_group = request.user.groups.all()
    urgents = Alert.objects.filter(category='Urgents')
    for u in urgents:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
                    alert.append(u)
    contexto = {'alerts': alert, 'today':date_now ,'title':'List Urgent', 'style':'danger'}
    return render(request, 'alert/alertViews.html', contexto)

def AllalertView(request):
    alert = []
    date_now = datetime.now().date()
    user_group = request.user.groups.all()
    allalert = Alert.objects.all().order_by('-category')
    for u in allalert:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
                    alert.append(u)
    contexto = {'alerts': alert, 'today':date_now , 'title':'List All Alerts', 'style':'primary'}
    return render(request, 'alert/alertViews.html', contexto)

class AlertsCreate(CreateView):
     model = Alert
     form_class = AlertForm
     template_name = 'alert/alertForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Alert'})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         user = request.user
         if form.is_valid():
             alert = form.save(commit=False)
             alert.users = user
             alert.save()
             accion_user(alert, ADDITION, request.user)
             messages.success(request, "Alert save with an extension")

             #send_mail('Prime Alert',
             #   'Usted tiene una alerta:',
             #   'administrator@fcintermodal.com',
             #    ['ranselr@gmail.com'],
             #    fail_silently=False)
             # Your Account SID from twilio.com/console
             # account_sid = "ACc2b4aa7154629a3f9b2767e7ddf9981d"
             # Your Auth Token from twilio.com/console
             # auth_token = "b6318ebc29ac5cbdc257bb9acac2d89c"

             #client = Client(account_sid, auth_token)

             # message = client.messages.create(
             #  to="+18322071590",
             # from_="+18329002832",
             #  body="Hello my wife!")

         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Create new Alert'})
         return HttpResponseRedirect(reverse_lazy('panel:panel'))


class AlertstEdit(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'alert/alertForm.html'
    success_url = reverse_lazy('panel:allalert')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_alt = kwargs['pk']
        alert = self.model.objects.get(id_alt=id_alt)
        form = self.form_class(request.POST, instance=alert)
        if form.is_valid():
            alert =form.save()
            accion_user(alert, CHANGE, request.user)
            messages.success(request, "Alert update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Alert'})

class AlertsDelete(DeleteView):
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:allalert')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_alt = kwargs['pk']
        alert = self.model.objects.get(id_alt=id_alt)
        accion_user(alert, DELETION, request.user)
        alert.delete()
        messages.success(request, "Enent delete with an extension")
        return HttpResponseRedirect(self.success_url)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Login/change_password.html', {
        'form': form
    })
