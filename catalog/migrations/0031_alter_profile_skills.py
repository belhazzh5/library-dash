# Generated by Django 4.0.2 on 2022-09-02 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_alter_profile_adresse_alter_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='catalog.Skill'),
        ),
    ]
