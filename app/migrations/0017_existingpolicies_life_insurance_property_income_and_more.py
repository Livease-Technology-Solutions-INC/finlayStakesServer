# Generated by Django 5.0.3 on 2024-03-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_capital_required_for_univerisy_goals_capital_required_for_university_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='existingpolicies',
            name='life_insurance_property_income',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='existingpolicies',
            name='property_income',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='existingpolicies',
            name='retirement_property_income',
            field=models.CharField(blank=True, null=True),
        ),
    ]
