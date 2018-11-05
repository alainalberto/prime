from apps.tools.models import *
from apps.services.models import CustomerHasAlert
from django.contrib.auth.models import User, Group
from datetime import datetime, date, time, timedelta


def base(request):
    date_now = datetime.now().date()
    notif = []
    alert = []
    urgent = []
    alerts = []

    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    user_group = request.user.groups.all()
    cutAlrt = CustomerHasAlert.objects.all()
    for al in cutAlrt:
      if not al.alert.deactivated:
        for g in user_group:
          if al.alert.group.filter(name = g.name ).exists():
            if al.alert.show_date <= date_now and al.alert.end_date >= date_now:
               alerts.append(al)
    for n in alertNot:
      if not n.deactivated:
        for g in user_group:
          if n.group.filter(name = g.name ).exists():
            if n.show_date <= date_now and n.end_date >= date_now:
               notif.append(n)
    for a in alertAlt:
      if not a.deactivated:
        for g in user_group:
            if a.group.filter(name=g.name).exists():
               if a.show_date <= date_now and a.end_date >= date_now:
                  alert.append(a)
    for u in alertUrg:
      if not u.deactivated:
        for g in user_group:
            if u.group.filter(name=g.name).exists():
               if u.show_date <= date_now and u.end_date >= date_now:
                  urgent.append(u)
    all = len(notif) + len(alert) + len(urgent)
    c = Chat.objects.all()
    contexto = {'notif': len(notif), 'alrt': len(alert), 'urgent': len(urgent), 'all': all, 'chat': c}
    return (contexto)