# Generated by Django 3.0.4 on 2020-04-14 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True, verbose_name='Name')),
                ('description', models.CharField(max_length=96, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], default='MON', max_length=3, null=True, verbose_name='Day of Week')),
                ('time', models.TimeField(null=True, verbose_name='Time')),
                ('fee', models.IntegerField(blank=True, default=0, verbose_name='Fee')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.Course', verbose_name='Course')),
                ('student', models.ManyToManyField(blank=True, db_table='learning_attend_lesson', related_name='student_lessons', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_lessons', to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
            ],
            options={
                'unique_together': {('teacher', 'course', 'day_of_week', 'time')},
            },
        ),
    ]
