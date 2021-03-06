# Generated by Django 3.0.4 on 2020-04-17 15:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0002_auto_20200415_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='max_students',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='Maximum Students'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='student_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Total Student'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_booked', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Time Booked')),
                ('is_active', models.BooleanField(default=0, verbose_name='Is Active')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.Lesson', verbose_name='Lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserAppraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Rating')),
                ('feedback', models.CharField(blank=True, max_length=256, verbose_name='Feedback')),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('source_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_appraisal', to=settings.AUTH_USER_MODEL)),
                ('target_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.Lesson')),
            ],
            options={
                'unique_together': {('target_lesson', 'source_user')},
            },
        ),
    ]
