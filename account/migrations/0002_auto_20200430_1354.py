# Generated by Django 2.2.12 on 2020-04-30 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='credits_15',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='total_credits',
            field=models.IntegerField(default=0),
        ),
    ]
