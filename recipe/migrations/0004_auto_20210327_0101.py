# Generated by Django 3.1 on 2021-03-27 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0003_auto_20210326_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='chef',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Chef Name'),
        ),
    ]
