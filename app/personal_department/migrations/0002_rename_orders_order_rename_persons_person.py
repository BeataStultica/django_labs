# Generated by Django 4.0 on 2021-12-26 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal_department', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='Persons',
            new_name='Person',
        ),
    ]
