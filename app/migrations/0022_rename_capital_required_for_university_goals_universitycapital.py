# Generated by Django 5.0.3 on 2024-03-18 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_incomedetails_interest_incomedetails_interest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goals',
            old_name='capital_required_for_university',
            new_name='universityCapital',
        ),
    ]
