from django.db import models
from django.utils.six import with_metaclass
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.conf import settings
import os

# Create your models here.

# Model Table menus
class Menu(models.Model):
    id_men = models.AutoField(primary_key=True)
    menus_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    deactivated = models.BooleanField(default=False)
    url = models.CharField(max_length=45, blank=True, null=True)
    icon = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table business
class Busines(models.Model):
    id_bus = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    logo = models.ImageField(upload_to='img/', blank=True, null=True)
    date_created = models.DateField()
    deactivated = models.BooleanField(default=False)
    date_deactivated = models.DateField(blank=True, null=True)
    messager = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

@receiver(pre_delete, sender=Busines)
def _file_delete(sender, instance, using, **kwargs):
        file_path = settings.BASE_DIR + '/static/media/' + str(instance.logo)

        if os.path.isfile(file_path):
            os.remove(file_path)

# Model Tables relation profiler-alerts
class Alert(models.Model):
    id_alt = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    create_date = models.DateField(auto_now_add=True)
    show_date = models.DateField()
    end_date = models.DateField()
    deactivated = models.BooleanField(default=False)
    group = models.ManyToManyField(Group)

    def __str__(self):
        return '{}'.format(self.description)

# Model Table folders
class Folder(models.Model):
    id_fld = models.AutoField(primary_key=True)
    folders_id = models.ForeignKey('self',  blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table files
class File(models.Model):
    id_fil = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    folders = models.ForeignKey(Folder, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    url = models.FileField(upload_to="Forms/", blank=True, null=True)
    date_save = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

@receiver(pre_delete, sender=File)
def _file_delete(sender, instance, using, **kwargs):
    file_path = settings.BASE_DIR + '/static/media/'+str(instance.url)

    if os.path.isfile(file_path):
        os.remove(file_path)

class Calendar(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    allDay = models.BooleanField(default=True)
    start = models.DateField(blank=True, null=True)
    startTimer = models.TimeField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    endTimer = models.TimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)

class Chat(models.Model):
    id_cht = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.message)

class Directory(models.Model):
    id_dir = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)





