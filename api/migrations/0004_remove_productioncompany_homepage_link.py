# Generated by Django 2.0.3 on 2018-11-09 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181109_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productioncompany',
            name='homepage_link',
        ),
    ]
