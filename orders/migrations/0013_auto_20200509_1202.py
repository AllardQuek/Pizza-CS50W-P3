# Generated by Django 3.0.6 on 2020-05-09 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_additions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Additions',
            new_name='Addition',
        ),
    ]