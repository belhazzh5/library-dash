# Generated by Django 4.0.2 on 2022-08-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_remove_course_category_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='course',
            field=models.ManyToManyField(to='system.Course'),
        ),
    ]
