# Generated by Django 5.0.3 on 2024-03-15 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_otptoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(max_length=6, verbose_name='9c0df1'),
        ),
    ]
