# Generated by Django 3.2.5 on 2023-07-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallReportMaster',
            fields=[
                ('sno', models.AutoField(db_column='Sno', primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=20)),
                ('ref_type', models.TextField()),
                ('unique_id', models.TextField()),
                ('name', models.TextField()),
                ('design', models.TextField()),
                ('contact', models.TextField()),
                ('camp', models.TextField()),
                ('camp_details', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.TextField()),
                ('latitude', models.TextField()),
                ('longitude', models.TextField()),
                ('area', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('pincode', models.CharField(max_length=50)),
                ('district', models.TextField()),
                ('station', models.TextField()),
                ('branch', models.TextField()),
                ('source', models.TextField()),
                ('attendance', models.TextField()),
                ('reason', models.TextField()),
                ('type', models.TextField(db_column='Type')),
                ('ldate', models.DateField()),
                ('category', models.CharField(max_length=1)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'call_report_master',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('month', models.CharField(max_length=50)),
                ('pf_status', models.CharField(max_length=50)),
                ('gross', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_days', models.IntegerField()),
                ('arrears', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shift_allowance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'Employee',
            },
        ),
    ]