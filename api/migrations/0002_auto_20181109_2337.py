# Generated by Django 2.0.3 on 2018-11-09 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='production_company',
        ),
        migrations.AddField(
            model_name='movies',
            name='production_company',
            field=models.ManyToManyField(to='api.ProductionCompany'),
        ),
    ]
