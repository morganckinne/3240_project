# Generated by Django 3.2.15 on 2022-11-12 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testapp', '0016_rename_book_isbn_post_book_isbn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='John Wick', max_length=100)),
                ('year', models.CharField(choices=[('First', '1st'), ('Third', '3rd'), ('Fourth', '4th'), ('Other', 'Other')], default='First', max_length=6)),
                ('major', models.CharField(default='CS', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
