from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
import string

# models
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    profile_image = models.ImageField(upload_to="profile", blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    is_google = models.BooleanField(default=False)
    is_facebook = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class OtpToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.otp_code:
            # Generate a random 6-digit OTP code
            self.otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Set otp_expires_at if not provided
        if not self.otp_expires_at:
            self.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP Token for {self.user.email}"


class PersonalDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="personal_details"
    )
    name = models.CharField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True)
    contact_number = PhoneNumberField(blank=True)
    email_id = models.EmailField(blank=True, null=True)
    country_of_residence = models.CharField(blank=True, null=True)
    nationality = models.CharField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    smoker = models.BooleanField(default=False, null=True)
    medical_history = models.CharField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate age from date of birth
        if self.date_of_birth:
            today = date.today()
            self.age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
        super().save(*args, **kwargs)


def create_personal_details(sender, instance, created, **kwargs):
    if created:
        PersonalDetails.objects.create(user=instance)


def save_personal_details(sender, instance, **kwargs):
    instance.personal_details.save()


post_save.connect(create_personal_details, sender=CustomUser)
post_save.connect(save_personal_details, sender=CustomUser)


class IncomeDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="income_details"
    )
    interest = models.CharField(blank=True, null=True)
    income_from_property = models.CharField(blank=True, null=True)
    bank_returns = models.CharField(blank=True, null=True)
    salary = models.CharField(blank=True, null=True)
    total_income = models.CharField(blank=True, null=True)
    bonus = models.CharField(blank=True, null=True)


def create_income_details(sender, instance, created, **kwargs):
    if created:
        IncomeDetails.objects.create(user=instance)


def save_income_details(sender, instance, **kwargs):
    instance.income_details.save()


post_save.connect(create_income_details, sender=CustomUser)
post_save.connect(save_income_details, sender=CustomUser)


class ExpenseDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="expense_details"
    )
    utility_bill = models.CharField(blank=True, null=True)
    rent = models.CharField(blank=True, null=True)
    loan = models.CharField(blank=True, null=True)
    shopping_expense = models.CharField(blank=True, null=True)
    leisure_expense = models.CharField(blank=True, null=True)
    total_expenses = models.CharField(blank=True, null=True)
    medical_expenses = models.CharField(blank=True, null=True)


def create_expense_details(sender, instance, created, **kwargs):
    if created:
        ExpenseDetails.objects.create(user=instance)


def save_expense_details(sender, instance, **kwargs):
    instance.expense_details.save()


post_save.connect(create_expense_details, sender=CustomUser)
post_save.connect(save_expense_details, sender=CustomUser)


class AssetDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="asset_details"
    )
    cash_in_hand = models.CharField(blank=True, null=True)
    property_value = models.CharField(blank=True, null=True)
    shares = models.CharField(blank=True, null=True)
    business_asset = models.CharField(blank=True, null=True)
    others = models.CharField(blank=True, null=True)
    total_assets = models.CharField(blank=True, null=True)


def create_asset_details(sender, instance, created, **kwargs):
    if created:
        AssetDetails.objects.create(user=instance)


def save_asset_details(sender, instance, **kwargs):
    instance.asset_details.save()


post_save.connect(create_asset_details, sender=CustomUser)
post_save.connect(save_asset_details, sender=CustomUser)


class LiabilityDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="liability_details"
    )
    bank_loans = models.CharField(blank=True, null=True)
    credit_card_outstanding = models.CharField(blank=True, null=True)
    mortages = models.CharField(blank=True, null=True)
    auto_loans = models.CharField(blank=True, null=True)
    hand_loans = models.CharField(blank=True, null=True)
    total_liabilities = models.CharField(blank=True, null=True)


def create_liability_details(sender, instance, created, **kwargs):
    if created:
        LiabilityDetails.objects.create(user=instance)


def save_liability_details(sender, instance, **kwargs):
    instance.liability_details.save()


post_save.connect(create_liability_details, sender=CustomUser)
post_save.connect(save_liability_details, sender=CustomUser)


class Goals(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="goals"
    )
    children_education = models.CharField(blank=True, null=True)
    credit_card_outstanding = models.CharField(blank=True, null=True)
    capital_required_for_univerisy = models.CharField(blank=True, null=True)
    years_left_for_university = models.CharField(blank=True, null=True)
    where_would_you_like_to_retire = models.CharField(blank=True, null=True)
    income_required_after_retirement = models.CharField(blank=True, null=True)
    annual_income_for_family_incase_of_death = models.CharField(blank=True, null=True)
    annual_income_for_family_incase_of_critical_illness = models.CharField(
        blank=True, null=True
    )
    annual_income_for_family_incase_of_disability = models.CharField(
        blank=True, null=True
    )


def create_goals(sender, instance, created, **kwargs):
    if created:
        Goals.objects.create(user=instance)


def save_goals(sender, instance, **kwargs):
    instance.goals.save()


post_save.connect(create_goals, sender=CustomUser)
post_save.connect(save_goals, sender=CustomUser)


class ExistingProvisionsDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="existing_provisions"
    )
    children_education = models.CharField(blank=True, null=True)
    life_insurance = models.CharField(blank=True, null=True)
    disability = models.CharField(blank=True, null=True)
    retirement = models.CharField(blank=True, null=True)
    critial_illness = models.CharField(blank=True, null=True)


def create_existing_provisions(sender, instance, created, **kwargs):
    if created:
        ExistingProvisionsDetails.objects.create(user=instance)


def save_existing_provisions(sender, instance, **kwargs):
    instance.existing_provisions.save()


post_save.connect(create_existing_provisions, sender=CustomUser)
post_save.connect(save_existing_provisions, sender=CustomUser)


class FinancialPlanningShortfall(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="financial_planning_shortfall",
    )
    children_education = models.CharField(blank=True, null=True)
    life_insurance = models.CharField(blank=True, null=True)
    disability = models.CharField(blank=True, null=True)
    retirement = models.CharField(blank=True, null=True)
    critial_illness = models.CharField(blank=True, null=True)


def create_financial_planning_shortfall(sender, instance, created, **kwargs):
    if created:
        FinancialPlanningShortfall.objects.create(user=instance)


def save_financial_planning_shortfall(sender, instance, **kwargs):
    instance.financial_planning_shortfall.save()


post_save.connect(create_financial_planning_shortfall, sender=CustomUser)
post_save.connect(save_financial_planning_shortfall, sender=CustomUser)


class ExistingPolicies(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="existing_policies",
    )
    policy_no = models.CharField(blank=True, null=True)
    annual_premium = models.CharField(blank=True, null=True)
    date_of_maturity = models.CharField(blank=True, null=True)
    date_of_commencement = models.CharField(blank=True, null=True)
    term = models.CharField(blank=True, null=True)
    benefits = models.CharField(blank=True, null=True)
    life_insurance_policy_no = models.CharField(blank=True, null=True)
    life_insurance_annual_premium = models.CharField(blank=True, null=True)
    life_insurance_date_of_maturity = models.CharField(blank=True, null=True)
    life_insurance_date_of_commencement = models.CharField(blank=True, null=True)
    life_insurance_term = models.CharField(blank=True, null=True)
    life_insurance_benefits = models.CharField(blank=True, null=True)
    retirement_policy_no = models.CharField(blank=True, null=True)
    retirement_annual_premium = models.CharField(blank=True, null=True)
    retirement_date_of_maturity = models.CharField(blank=True, null=True)
    retirement_date_of_commencement = models.CharField(blank=True, null=True)
    retirement_term = models.CharField(blank=True, null=True)
    retirement_benefits = models.CharField(blank=True, null=True)


def create_existing_policies(sender, instance, created, **kwargs):
    if created:
        ExistingPolicies.objects.create(user=instance)


def save_existing_policies(sender, instance, **kwargs):
    instance.existing_policies.save()


post_save.connect(create_existing_policies, sender=CustomUser)
post_save.connect(save_existing_policies, sender=CustomUser)
