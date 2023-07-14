from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    month = models.CharField(max_length=50)
    pf_status = models.CharField(max_length=50)
    gross = models.DecimalField(max_digits=10, decimal_places=2)
    net_days = models.IntegerField()
    arrears = models.DecimalField(max_digits=10, decimal_places=2)
    shift_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'Employee'

class CallReportMaster(models.Model):
    sno = models.AutoField(db_column='Sno', primary_key=True)  # Field name made lowercase.
    emp_id = models.CharField(max_length=20)
    ref_type = models.TextField()
    unique_id = models.TextField()
    name = models.TextField()
    design = models.TextField()
    contact = models.TextField()
    camp = models.TextField()
    camp_details = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    area = models.TextField()
    city = models.TextField()
    state = models.TextField()
    pincode = models.CharField(max_length=50)
    district = models.TextField()
    station = models.TextField()
    branch = models.TextField()
    source = models.TextField()
    attendance = models.TextField()
    reason = models.TextField()
    type = models.TextField(db_column='Type')  # Field name made lowercase.
    ldate = models.DateField()
    category = models.CharField(max_length=1)
    status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        
        db_table = 'call_report_master'        