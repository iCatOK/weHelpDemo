# Generated by Django 3.0.8 on 2020-08-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200810_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
    ]
