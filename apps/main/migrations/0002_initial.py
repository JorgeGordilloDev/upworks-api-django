# Generated by Django 4.0.4 on 2022-06-22 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='applications',
            name='id_alumn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.alumn', verbose_name='Alumno'),
        ),
        migrations.AddField(
            model_name='applications',
            name='id_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.job', verbose_name='Empleo'),
        ),
        migrations.AddField(
            model_name='alumn',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
