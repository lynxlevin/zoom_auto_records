# Generated by Django 4.0.2 on 2022-02-21 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_zoom_access_token_customuser_zoom_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='zoom_expires_in',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zoom_refresh_token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
