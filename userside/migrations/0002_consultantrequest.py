# Generated by Django 4.2.5 on 2023-10-07 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0020_course_added_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userside', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intake_year', models.CharField(max_length=100)),
                ('intake_month', models.CharField(max_length=100)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultant_requests', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
