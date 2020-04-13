# Generated by Django 3.0.4 on 2020-04-12 11:03

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userappraisal_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender')),
                ('date_of_birth', models.DateField(null=True, verbose_name='Date of Birth')),
                ('address', models.CharField(max_length=96, verbose_name='Address')),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='Phone number must start with 0. Up to 13 digits allowed.', regex='0[\\d]{9,12}')], verbose_name='Phone Number')),
                ('ktp', models.ImageField(help_text='Only accepts images', upload_to='account/document/ktp/%Y%m%d', verbose_name='Identification ID (KTP/SIM/Student Card)')),
                ('occupation', models.CharField(max_length=32, verbose_name='Occupation')),
                ('experiences', models.CharField(max_length=32, verbose_name='Experiences')),
                ('cv', models.ImageField(help_text='Only accepts pdfs', upload_to='account/document/cv/%Y%m%d', validators=[account.models.validate_file_extension], verbose_name='CV')),
            ],
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserAppraisal',
        ),
        migrations.DeleteModel(
            name='UserDetails',
        ),
    ]
