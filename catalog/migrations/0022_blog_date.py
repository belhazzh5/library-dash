# Generated by Django 4.0.2 on 2022-08-28 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]