# Generated by Django 3.1 on 2021-03-27 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20210327_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation_mode',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]