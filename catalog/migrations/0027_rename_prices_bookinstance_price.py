# Generated by Django 4.0.2 on 2022-09-02 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_bookinstance_prices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinstance',
            old_name='prices',
            new_name='price',
        ),
    ]