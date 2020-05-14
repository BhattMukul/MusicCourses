# Generated by Django 2.2.12 on 2020-05-06 09:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_instructor_bank_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='last_requested',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 6, 9, 53, 47, 380112, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MoneyTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('requested', models.DateTimeField(auto_now=True)),
                ('tranfered', models.BooleanField(default=False)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='instructor', to='account.Instructor')),
            ],
        ),
    ]
