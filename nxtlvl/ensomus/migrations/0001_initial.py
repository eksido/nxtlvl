# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('my_effort', models.TextField(null=True, verbose_name='my contribution', blank=True)),
                ('my_needs', models.TextField(null=True, verbose_name='my need for support', blank=True)),
                ('approved_at', models.DateTimeField(null=True, verbose_name='approved at', blank=True)),
                ('follow_up_at', models.DateField(null=True, verbose_name='follow up at', blank=True)),
                ('sort_order', models.IntegerField(verbose_name='sort order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('type', models.CharField(max_length=1, null=True)),
                ('difficulty', models.IntegerField(null=True)),
                ('created_by', models.ForeignKey(related_name='action_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
            },
        ),
        migrations.CreateModel(
            name='ActionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('follow_up_at', models.DateField(default=None, null=True, verbose_name='follow up at', blank=True)),
                ('action', models.ForeignKey(related_name='comments', verbose_name='action', blank=True, to='ensomus.Action', null=True)),
                ('created_by', models.ForeignKey(related_name='action_comment_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'action comment',
                'verbose_name_plural': 'action comments',
            },
        ),
        migrations.CreateModel(
            name='ActionStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_da', models.CharField(max_length=30, verbose_name='name_da')),
                ('name_en', models.CharField(max_length=30, verbose_name='name_en')),
            ],
            options={
                'verbose_name': 'action status',
                'verbose_name_plural': 'action statuses',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_by', models.ForeignKey(related_name='company_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='company_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=4000, verbose_name='title')),
                ('description', tinymce.models.HTMLField(null=True, verbose_name='description')),
                ('sort_order', models.IntegerField(verbose_name='sort order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'competence',
                'verbose_name_plural': 'competences',
            },
        ),
        migrations.CreateModel(
            name='CompetenceField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=4000, verbose_name='title')),
                ('description', tinymce.models.HTMLField(null=True, verbose_name='description')),
                ('is_system', models.BooleanField(default=False, verbose_name='is system')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('language_code', models.CharField(default=b'en-us', max_length=15, verbose_name='language', choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('is_manager', models.BooleanField(default=False, verbose_name='for manager')),
                ('sort_order', models.IntegerField(verbose_name='sort order')),
                ('company', models.ForeignKey(default=None, blank=True, to='ensomus.Company', null=True, verbose_name='company')),
                ('created_by', models.ForeignKey(related_name='competence_field_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'competence field',
                'verbose_name_plural': 'competence fields',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en-us', max_length=15, verbose_name='language', choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('competence_fields', models.ManyToManyField(related_name='development_plan_competence_fields', verbose_name='competence fields', to='ensomus.CompetenceField')),
                ('created_by', models.ForeignKey(related_name='development_plan_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'development plan',
                'verbose_name_plural': 'development plans',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlanPageStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagelink', models.CharField(max_length=255, verbose_name='page link')),
                ('status', models.CharField(default=b'UR', max_length=2, choices=[(b'UR', 'Unread'), (b'RE', 'Read')])),
            ],
            options={
                'verbose_name': 'Development plan page status',
                'verbose_name_plural': 'Development plan page statuses',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlanToUserRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('finished_at', models.DateTimeField(default=None, null=True, verbose_name='finished at', blank=True)),
                ('is_private', models.BooleanField(default=True, verbose_name='is private')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('created_by', models.ForeignKey(related_name='development_plan_user_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'development plan to user relation',
                'verbose_name_plural': 'development plan to user relations',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlanType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(verbose_name='company', blank=True, to='ensomus.Company', null=True)),
            ],
            options={
                'verbose_name': 'development plan type',
                'verbose_name_plural': 'development plan types',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_manager', models.BooleanField(default=False, verbose_name='is manager')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('language_code', models.CharField(default=b'en-us', max_length=15, verbose_name='language', choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('plaintext_password', models.CharField(max_length=200, blank=True)),
                ('access_code', models.CharField(max_length=200, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(verbose_name='company', to='ensomus.Company')),
                ('created_by', models.ForeignKey(related_name='employee_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('development_plan_type', models.ForeignKey(verbose_name='development plan type', blank=True, to='ensomus.DevelopmentPlanType', null=True)),
                ('manager', models.ForeignKey(verbose_name='manager', blank=True, to='ensomus.Employee', null=True)),
                ('newest_development_plan', models.ForeignKey(verbose_name='newest_development_plan', blank=True, to='ensomus.DevelopmentPlan', null=True)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('created_by', models.ForeignKey(related_name='employee_role_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('employee', models.ForeignKey(verbose_name='employee', to='ensomus.Employee')),
            ],
            options={
                'verbose_name': 'employee role',
                'verbose_name_plural': 'employee roles',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=255)),
                ('mime_type', models.CharField(max_length=100)),
                ('file_size', models.BigIntegerField()),
                ('file_path', models.FileField(upload_to=b'temp')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(related_name='files', to='ensomus.Company')),
                ('created_by', models.ForeignKey(related_name='file_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Fil',
                'verbose_name_plural': 'Filer',
            },
        ),
        migrations.CreateModel(
            name='FileBytes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', models.TextField(db_column=b'data', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', tinymce.models.HTMLField(max_length=4000, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('sort_order', models.IntegerField(verbose_name='sort order')),
                ('allow_response', models.BooleanField(default=True, verbose_name='allow response')),
                ('competence', models.ForeignKey(verbose_name='competence', to='ensomus.Competence')),
                ('created_by', models.ForeignKey(related_name='question_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='question_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, verbose_name='text')),
                ('client_timestamp', models.BigIntegerField(null=True, verbose_name='client timestamp')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_by', models.ForeignKey(related_name='question_response_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('development_plan_to_user_relation', models.ForeignKey(related_name='question_response_development_plan_to_user_relation', verbose_name='development plan to user relation', to='ensomus.DevelopmentPlanToUserRelation')),
                ('question', models.ForeignKey(verbose_name='question', to='ensomus.Question')),
                ('updated_by', models.ForeignKey(related_name='question_response_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'response',
                'verbose_name_plural': 'responses',
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('send_date', models.DateTimeField()),
                ('sent', models.DateTimeField(null=True)),
                ('error', models.CharField(max_length=500, null=True)),
                ('created_by', models.ForeignKey(related_name='reminder_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reminder',
                'verbose_name_plural': 'Reminders',
            },
        ),
        migrations.CreateModel(
            name='ReminderTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_en', models.CharField(max_length=255, null=True)),
                ('subject_da', models.CharField(max_length=255, null=True)),
                ('body_en', models.TextField(null=True)),
                ('body_da', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Reminder Template',
                'verbose_name_plural': 'Reminders Template',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_by', models.ForeignKey(related_name='role_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='role_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.AddField(
            model_name='reminder',
            name='template',
            field=models.ForeignKey(related_name='reminder_template', to='ensomus.ReminderTemplate'),
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.ForeignKey(default=None, blank=True, to='ensomus.FileBytes', null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='role',
            field=models.ForeignKey(related_name='files', default=None, blank=True, to='ensomus.Role', null=True),
        ),
        migrations.AddField(
            model_name='employeerole',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='ensomus.Role'),
        ),
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(to='ensomus.Role', through='ensomus.EmployeeRole'),
        ),
        migrations.AddField(
            model_name='employee',
            name='updated_by',
            field=models.ForeignKey(related_name='employee_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(related_name='employee_user', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='developmentplanpagestatus',
            name='development_plan_relation',
            field=models.ForeignKey(verbose_name='development plan relation', to='ensomus.DevelopmentPlanToUserRelation'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='employee_response_relation',
            field=models.ForeignKey(related_name='development_plan_employee', verbose_name='employee response relation', to='ensomus.DevelopmentPlanToUserRelation'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='manager_response_relation',
            field=models.ForeignKey(related_name='development_plan_manager', verbose_name='manager response relation', to='ensomus.DevelopmentPlanToUserRelation'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='type',
            field=models.ForeignKey(verbose_name='type', blank=True, to='ensomus.DevelopmentPlanType', null=True),
        ),
        migrations.AddField(
            model_name='competencefield',
            name='development_plan_type',
            field=models.ForeignKey(verbose_name='development plan type', to='ensomus.DevelopmentPlanType'),
        ),
        migrations.AddField(
            model_name='competencefield',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='parent', blank=True, to='ensomus.CompetenceField', null=True),
        ),
        migrations.AddField(
            model_name='competencefield',
            name='updated_by',
            field=models.ForeignKey(related_name='competence_field_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='competence',
            name='competence_field',
            field=models.ForeignKey(related_name='competence_competence_field', verbose_name='competence field', to='ensomus.CompetenceField'),
        ),
        migrations.AddField(
            model_name='competence',
            name='created_by',
            field=models.ForeignKey(related_name='competence_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='competence',
            name='updated_by',
            field=models.ForeignKey(related_name='competence_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='actioncomment',
            name='status',
            field=models.ForeignKey(verbose_name='status', blank=True, to='ensomus.ActionStatus', null=True),
        ),
        migrations.AddField(
            model_name='actioncomment',
            name='updated_by',
            field=models.ForeignKey(related_name='action_comment_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='employee',
            field=models.ForeignKey(verbose_name='employee', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='action',
            name='status',
            field=models.ForeignKey(default=5, blank=True, to='ensomus.ActionStatus', null=True, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='action',
            name='updated_by',
            field=models.ForeignKey(related_name='action_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
