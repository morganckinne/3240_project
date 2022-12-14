# Generated by Django 3.2.15 on 2022-10-31 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0011_auto_20221023_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='associated_dept',
        ),
        migrations.AddField(
            model_name='post',
            name='associated_dept',
            field=models.CharField(choices=[('BME', 'Biomedical Engineering'), ('CHE', 'Chemical Engineering'), ('CS', 'Computer Science'), ('ECE', 'Electrical and Computer Engineering'), ('STS', 'Engineering and Society'), ('MSE', 'Material Sciences Engineering'), ('MAE', 'Mechanical and Aerospace Engineering'), ('SYS', 'Systems Engineering'), ('CE', 'Civil Engineering')], default='CS', max_length=6),
        ),
    ]
