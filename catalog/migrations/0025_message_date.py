# Generated by Django 4.0.2 on 2022-08-30 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]