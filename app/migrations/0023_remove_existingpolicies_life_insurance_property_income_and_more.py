# Generated by Django 5.0.3 on 2024-03-18 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_rename_capital_required_for_university_goals_universitycapital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='existingpolicies',
            name='life_insurance_property_income',
        ),
        migrations.RemoveField(
            model_name='existingpolicies',
            name='property_income',
        ),
        migrations.RemoveField(
            model_name='existingpolicies',
            name='retirement_property_income',
        ),
    ]
