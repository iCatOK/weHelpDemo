# Generated by Django 3.0.8 on 2020-07-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
