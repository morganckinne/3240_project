# Generated by Django 3.2.15 on 2022-11-05 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0015_auto_20221105_0400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='book_isbn',
            new_name='book_ISBN',
        ),
    ]
