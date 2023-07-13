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