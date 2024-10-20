# Generated by Django 4.2.15 on 2024-10-17 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MarathonServer', '0007_rename_group_racer_age_gender_group_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('racer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='MarathonServer.racer')),
                ('gun_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('personal_record', models.DurationField()),
                ('marathon_record', models.DurationField()),
            ],
        ),
    ]
