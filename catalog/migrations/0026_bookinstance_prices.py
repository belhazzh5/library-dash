# Generated by Django 4.0.2 on 2022-09-02 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_message_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='prices',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
