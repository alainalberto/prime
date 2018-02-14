from django.contrib.admin.models import LogEntry,ADDITION, CHANGE, DELETION
from django.contrib.auth.views import logout_then_login
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from System import settings
from django.contrib import auth

def accion_user(object, action_flag, user):
    """Log changes to Admin log."""
    if action_flag:
        if action_flag == ADDITION:
            change_message = {"added": force_text(object)}
        elif action_flag == CHANGE:
            change_message = {"change": force_text(object)}
        elif action_flag == DELETION:
            change_message = {"delete": force_text(object)}
        try:
            LogEntry.objects.log_action(
                user_id = user.pk,
                content_type_id = ContentType.objects.get_for_model(object).pk,
                object_id = object.pk,
                object_repr = force_text(object),
                change_message = change_message,
                action_flag = action_flag,
                )
        except:
            print("Failed to log action.")



class AutoLogout:
    def process_request(self, request):
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            if ('last_login' in request.session):
                last = (current_datetime - request.session['last_login']).seconds
                if last > settings.SESSION_IDLE_TIMEOUT:
                    logout_then_login
            else:
                request.session['last_login'] = current_datetime
        return None