# Generated by Django 2.2.12 on 2020-05-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200506_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='last_requested',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
