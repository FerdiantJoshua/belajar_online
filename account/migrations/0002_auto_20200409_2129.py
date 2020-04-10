# Generated by Django 3.0.4 on 2020-04-09 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='address',
            field=models.CharField(max_length=96),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='experiences',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='experiences_proofs',
            field=models.ImageField(upload_to='account/proof/%Y%m%d'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='ktp',
            field=models.ImageField(upload_to='account/ktp/%Y%m%d'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='occupation',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='Phone number must start with 0. Up to 13 digits allowed.', regex='0[\\d]{9,12}')]),
        ),
    ]