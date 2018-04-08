from django.db import models

from django.contrib.auth.models import User

from apps.tools.models import Folder, File, Alert

from apps.accounting.models import Customer, Invoice

from datetime import datetime

# Create your models here.

class CountState(models.Manager):
    def is_state(self,state, customer):
        return self.filter(state=state, customers = customer ).count()

class Permit(models.Model):
    id_com = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    is_new = models.BooleanField(default=True)
    legal_status = models.CharField(max_length=10, blank=True, null=True)
    gusiness_type = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    attorney = models.CharField(max_length=100, blank=True, null=True)
    otheattorney = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    othephone = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    ein = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    unit = models.IntegerField(blank=True, null=True)
    usdot = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    usdot_pin = models.CharField(max_length=20, blank=True, null=True)
    txdmv = models.CharField(max_length=20, blank=True, null=True)
    txdmv_user = models.CharField(max_length=20, blank=True, null=True)
    txdmv_passd = models.CharField(max_length=45, blank=True, null=True)
    txdmv_date = models.DateField(blank=True, null=True)
    txdmv_date_exp = models.DateField(blank=True, null=True)
    mc = models.CharField(max_length=20, blank=True, null=True)
    mc_pin = models.CharField(max_length=20, blank=True, null=True)
    boc3 = models.BooleanField(default=False)
    boc3_date = models.DateField(blank=True, null=True)
    ucr = models.BooleanField(default=False)
    ucr_date_exp = models.DateField(blank=True, null=True)
    account_number = models.CharField(max_length=45, blank=True, null=True)
    account_user = models.CharField(max_length=45, blank=True, null=True)
    account_password = models.CharField(max_length=45, blank=True, null=True)
    inter = models.BooleanField(default=False)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.name)


class Equipment(models.Model):
    id_tru = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=45, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    plate_date_exp = models.DateField(blank=True, null=True)
    title_date_reg = models.DateField(blank=True, null=True)
    title_date_exp_reg = models.DateField(blank=True, null=True)
    title_date_insp = models.DateField(blank=True, null=True)
    title_date_exp_insp = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.number)



class Contract(models.Model):
    id_con = models.AutoField(primary_key=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    files = models.ForeignKey(File, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    objects= CountState()

    def __str__(self):
        return '{} {}'.format(self.type, self.serial)

class Audit(models.Model):
    id_aud = models.AutoField(primary_key=True)
    folders = models.ForeignKey(Folder, on_delete=models.CASCADE)  # Field name made lowercase.
    contracts = models.ForeignKey(Contract, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    auditor_name = models.CharField(max_length=100, blank=True, null=True)
    action_plan = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    results = models.CharField(max_length=255, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.customers)

class Driver(models.Model):
    id_drv = models.AutoField(primary_key=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)  # Field name made lowercase.
    users = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    license_numb = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    lic_date_exp = models.DateField(blank=True, null=True)
    medicard_date_exp = models.DateField(blank=True, null=True)
    drugtest_date = models.DateField(blank=True, null=True)
    drugtest_date_exp = models.DateField(blank=True, null=True)
    mbr_date = models.DateField(blank=True, null=True)
    mbr_date_exp = models.DateField(blank=True, null=True)
    begining_date = models.DateField(blank=True, null=True)
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)

    objects = CountState()

    def __str__(self):
        return '{}'.format(self.name)

class Insurance(models.Model):
    id_ins = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    down_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    policy_efective_date = models.DateField(blank=True, null=True)
    policy_date_exp = models.DateField(blank=True, null=True)
    policy_cargo_exp = models.DateField(blank=True, null=True)
    policy_physical_exp = models.DateField(blank=True, null=True)
    liability = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    policy_liability = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cargo_policy = models.CharField(max_length=100, blank=True, null=True)
    physical_damage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    physical_damg_policy = models.CharField(max_length=100, blank=True, null=True)
    sale_type = models.CharField(max_length=20, blank=True, null=True)
    sale_date_fee = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comision = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    paid_out= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    monthlypay = models.IntegerField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=250, blank=True, null=True)
    other_description = models.CharField(max_length=45, blank=True, null=True)
    other = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_policy = models.CharField(max_length=100, blank=True, null=True)
    policy_other_exp = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.customers)


class Ifta(models.Model):
    id_ift = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    period = models.CharField(max_length=45, blank=True, null=True)
    nex_period = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    payment_due = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.type)

class DispatchLoad(models.Model):
    id_inv = models.AutoField(primary_key=True)
    biller = models.CharField(max_length=45, blank=True, null=True)
    biller_address = models.CharField(max_length=100, blank=True, null=True)
    biller_email = models.EmailField( blank=True, null=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    serial = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    waytopay = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comission_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    wire_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ach_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    prefix = models.CharField(max_length=4, default='invl')
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.serial)


class Application(models.Model):
    id_apl = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    fullname = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    no_social = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255)
    license_numb = models.CharField(max_length=45, blank=True, null=True)
    usdot = models.CharField(max_length=25, blank=True, null=True)
    mc = models.CharField(max_length=25, blank=True, null=True)
    txdmv = models.CharField(max_length=25, blank=True, null=True)
    ein = models.CharField(max_length=25, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    date_view = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    update = models.DateField(blank=True, null=True)
    objects = CountState()

    def __str__(self):
        return '{}'.format(self.fullname)


class CustomerHasAlert(models.Model):
    id_cal = models.AutoField(primary_key=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
