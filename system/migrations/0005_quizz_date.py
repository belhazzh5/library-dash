# Generated by Django 4.0.6 on 2022-07-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_course_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizz',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]