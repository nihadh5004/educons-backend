# Generated by Django 4.2.5 on 2023-09-27 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0006_remove_college_country_delete_coursetype_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Country',
        ),
    ]