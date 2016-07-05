# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ('-date_added',),
                'verbose_name': 'blacklisted e-mail address',
                'verbose_name_plural': 'blacklisted e-mail addresses',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.PositiveSmallIntegerField(choices=[(0, b'success'), (1, b'not sent (blacklisted)'), (2, b'failure')])),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('log_message', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_address', models.CharField(max_length=200)),
                ('from_address', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=255)),
                ('encoded_message', models.TextField()),
                ('html_message', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('attachment', models.ManyToManyField(to='django_mailer_plus.Attachment')),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
        migrations.CreateModel(
            name='QueuedMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveSmallIntegerField(default=3, choices=[(1, b'high'), (3, b'normal'), (5, b'low')])),
                ('deferred', models.DateTimeField(null=True, blank=True)),
                ('retries', models.PositiveIntegerField(default=0)),
                ('date_queued', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.OneToOneField(editable=False, to='django_mailer_plus.Message')),
            ],
            options={
                'ordering': ('priority', 'date_queued'),
            },
        ),
        migrations.AddField(
            model_name='log',
            name='message',
            field=models.ForeignKey(editable=False, to='django_mailer_plus.Message'),
        ),
    ]
