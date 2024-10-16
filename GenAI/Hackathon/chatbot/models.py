from django.db import models
from django.contrib.auth.models import User

class Sector(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class InvestmentProfile(models.Model):
    INVESTOR_TYPE_CHOICES = [
        ('First-Time', 'First-Time Investor'),
        ('Experienced', 'Experienced Investor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investment_profile')
    investor_type = models.CharField(max_length=20, choices=INVESTOR_TYPE_CHOICES)

    sector = models.ManyToManyField(Sector, blank=True)
    amount_to_invest = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    income_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    term_investment = models.CharField(max_length=20, choices=[
        ("short", "Short-term (less than 1 year)"),
        ("medium", "Medium-term (1-5 years)"),
        ("long", "Long-term (more than 5 years)"),
    ], blank=True, null=True)
    penny_stocks = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    government_policies = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    momentum = models.CharField(max_length=6, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], blank=True, null=True)

    investment_goal = models.CharField(max_length=50, choices=[
        ('retirement', 'Saving for retirement'),
        ('wealth_building', 'Building wealth'),
        ('specific_goal', 'Saving for a specific goal'),
        ('other', 'Other'),
    ], blank=True, null=True)
    investment_goal_other = models.CharField(max_length=255, blank=True)

    experience_level = models.CharField(max_length=50, choices=[
        ('none', 'None'),
        ('some_knowledge', 'A little (some knowledge but no experience)'),
        ('some_experience', 'Some experience'),
    ], blank=True, null=True)

    initial_investment = models.CharField(max_length=50, choices=[
        ('less_than_500', 'Less than $500'),
        ('between_500_1500', '$500 to $1,500'),
        ('between_1500_5000', '$1,500 to $5,000'),
        ('more_than_5000', 'More than $5,000'),
    ], blank=True, null=True)

    risk_tolerance = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], blank=True, null=True)

    investment_type = models.CharField(max_length=50, choices=[
        ('individual_stocks', 'Individual stocks'),
        ('mutual_funds_etfs', 'Mutual funds or ETFs'),
        ('real_estate', 'Real estate'),
        ('other', 'Other'),
    ], blank=True, null=True)
    investment_type_other = models.CharField(max_length=255, blank=True)



    monitoring_preference = models.CharField(max_length=50, choices=[
        ('enjoy', 'I enjoy it'),
        ('occasionally', 'I can do it occasionally'),
        ('rarely', 'I’d prefer not to monitor them often'),
    ], blank=True, null=True)

    biggest_concern = models.CharField(max_length=50, choices=[
        ('losing_money', 'Losing money'),
        ('not_understanding', 'Not understanding how it works'),
        ('volatility', 'Market volatility'),
        ('no', 'No Concerns.'),
    ], blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Investment Profile"
