# Generated by Django 4.2.5 on 2023-09-27 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0004_college'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
