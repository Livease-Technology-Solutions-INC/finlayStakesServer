# Generated by Django 5.0.3 on 2024-03-16 10:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='email_id',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(max_length=6, verbose_name='2c7af2'),
        ),
        migrations.CreateModel(
            name='AssetDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_in_hand', models.CharField(blank=True, null=True)),
                ('property_value', models.CharField(blank=True, null=True)),
                ('shares', models.CharField(blank=True, null=True)),
                ('business_asset', models.CharField(blank=True, null=True)),
                ('others', models.CharField(blank=True, null=True)),
                ('total_assets', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='asset_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExistingPolicies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_no', models.CharField(blank=True, null=True)),
                ('annual_premium', models.CharField(blank=True, null=True)),
                ('date_of_maturity', models.CharField(blank=True, null=True)),
                ('date_of_commencement', models.CharField(blank=True, null=True)),
                ('term', models.CharField(blank=True, null=True)),
                ('benefits', models.CharField(blank=True, null=True)),
                ('life_insurance_policy_no', models.CharField(blank=True, null=True)),
                ('life_insurance_annual_premium', models.CharField(blank=True, null=True)),
                ('life_insurance_date_of_maturity', models.CharField(blank=True, null=True)),
                ('life_insurance_date_of_commencement', models.CharField(blank=True, null=True)),
                ('life_insurance_term', models.CharField(blank=True, null=True)),
                ('life_insurance_benefits', models.CharField(blank=True, null=True)),
                ('retirement_policy_no', models.CharField(blank=True, null=True)),
                ('retirement_annual_premium', models.CharField(blank=True, null=True)),
                ('retirement_date_of_maturity', models.CharField(blank=True, null=True)),
                ('retirement_date_of_commencement', models.CharField(blank=True, null=True)),
                ('retirement_term', models.CharField(blank=True, null=True)),
                ('retirement_benefits', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='existing_policies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExistingProvisionsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children_education', models.CharField(blank=True, null=True)),
                ('life_insurance', models.CharField(blank=True, null=True)),
                ('disability', models.CharField(blank=True, null=True)),
                ('retirement', models.CharField(blank=True, null=True)),
                ('critial_illness', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='existing_provisions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utility_bill', models.CharField(blank=True, null=True)),
                ('rent', models.CharField(blank=True, null=True)),
                ('loan', models.CharField(blank=True, null=True)),
                ('shopping_expense', models.CharField(blank=True, null=True)),
                ('leisure_expense', models.CharField(blank=True, null=True)),
                ('total_expenses', models.CharField(blank=True, null=True)),
                ('medical_expenses', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expense_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialPlanningShortfall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children_education', models.CharField(blank=True, null=True)),
                ('life_insurance', models.CharField(blank=True, null=True)),
                ('disability', models.CharField(blank=True, null=True)),
                ('retirement', models.CharField(blank=True, null=True)),
                ('critial_illness', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='financial_planning_shortfall', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children_education', models.CharField(blank=True, null=True)),
                ('credit_card_outstanding', models.CharField(blank=True, null=True)),
                ('capital_required_for_univerisy', models.CharField(blank=True, null=True)),
                ('years_left_for_university', models.CharField(blank=True, null=True)),
                ('where_would_you_like_to_retire', models.CharField(blank=True, null=True)),
                ('income_required_after_retirement', models.CharField(blank=True, null=True)),
                ('annual_income_for_family_incase_of_death', models.CharField(blank=True, null=True)),
                ('annual_income_for_family_incase_of_critical_illness', models.CharField(blank=True, null=True)),
                ('annual_income_for_family_incase_of_disability', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(blank=True, null=True)),
                ('income_from_property', models.CharField(blank=True, null=True)),
                ('bank_returns', models.CharField(blank=True, null=True)),
                ('salary', models.CharField(blank=True, null=True)),
                ('total_income', models.CharField(blank=True, null=True)),
                ('bonus', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='income_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LiabilityDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_loans', models.CharField(blank=True, null=True)),
                ('credit_card_outstanding', models.CharField(blank=True, null=True)),
                ('mortages', models.CharField(blank=True, null=True)),
                ('auto_loans', models.CharField(blank=True, null=True)),
                ('hand_loans', models.CharField(blank=True, null=True)),
                ('total_liabilities', models.CharField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='liability_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
