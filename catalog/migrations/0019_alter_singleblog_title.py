# Generated by Django 4.0.2 on 2022-08-28 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_singleblog_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleblog',
            name='title',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
    ]
