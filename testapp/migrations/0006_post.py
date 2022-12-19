# Generated by Django 3.2.15 on 2022-10-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=200)),
                ('post_text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('sell_status', models.BooleanField(default=False)),
            ],
        ),
    ]
