# Generated by Django 2.2.15 on 2020-08-24 14:27
from django.contrib.postgres.operations import TrigramExtension, BtreeGinExtension
import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20200823_1553'),
    ]

    operations = [
        TrigramExtension(),
        BtreeGinExtension(),
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddIndex(
            model_name='article',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='api_article_title_81ceae_gin'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=django.contrib.postgres.indexes.GinIndex(fields=['name'], name='api_questio_name_638061_gin'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=django.contrib.postgres.indexes.GinIndex(fields=['email'], name='api_user_email_adeff9_gin'),
        ),
    ]
