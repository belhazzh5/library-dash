# Generated by Django 4.0.2 on 2022-08-28 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_blog_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/blogs/%d-%m-%y/'),
        ),
    ]
