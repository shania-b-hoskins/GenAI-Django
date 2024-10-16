from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Sector

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ExperiencedInvestorForm(forms.Form):
    SECTOR_CHOICES = Sector.objects.all()

    TERM_INVESTMENT_CHOICES = [
        ('Short-term (less than 1 year)', 'Short-term (less than 1 year)'),
        ('Medium-term (1-5 years)', 'Medium-term (1-5 years)'),
        ('Long-term (more than 5 years)', 'Long-term (more than 5 years)'),
    ]

    PENNY_STOCKS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    GOVERNMENT_POLICIES_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    MOMENTUM_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    sector = forms.ModelMultipleChoiceField(
        label='Which sectors?',
        queryset=Sector.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    amount_to_invest = forms.DecimalField(
        label='Monthly Investment ($)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    income_percentage = forms.DecimalField(
        label='Annual Investment of Income (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    profit_percentage = forms.DecimalField(
        label='Expected profit (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    term_investment = forms.ChoiceField(
        label='Term of investment',
        choices=TERM_INVESTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    penny_stocks = forms.ChoiceField(
        label='Do you wish to invest in penny stocks?',
        choices=PENNY_STOCKS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    government_policies = forms.ChoiceField(
        label='Do you follow government policies?',
        choices=GOVERNMENT_POLICIES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    momentum = forms.ChoiceField(
        label='Do you follow momentum?',
        choices=MOMENTUM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class FirstTimeInvestorForm(forms.Form):
    investment_goal_choices = [
        ('retirement', 'Saving for retirement'),
        ('wealth_building', 'Building wealth'),
        ('specific_goal', 'Saving for a specific goal (e.g., a home, education)'),
        ('other', 'Other (please specify)'),
    ]
    investment_goal = forms.ChoiceField(
        label="What is your main reason you wish to invest in the stock market?",
        choices=investment_goal_choices,
    )
    investment_goal_other = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your other goal'}),
    )
    experience_level_choices = [
        ('none', 'None'),
        ('some_knowledge', 'A little (some knowledge but no experience)'),
        ('some_experience', 'Some experience (I\'ve invested a little)'),
    ]
    experience_level = forms.ChoiceField(
        label="How much experience do you have with investing?",
        choices=experience_level_choices,
    )
    term_investment_choices = [
        ("short", "Short-term (less than 1 year)"),
        ("medium", "Medium-term (1-5 years)"),
        ("long", "Long-term (more than 5 years)"),
    ]
    term_investment = forms.ChoiceField(
        label="What is your investment timeframe?",
        choices=term_investment_choices,
    )
    initial_investment_choices = [
        ('less_than_500', 'Less than $500'),
        ('between_500_1500', '$500 to $1,500'),
        ('between_1500_5000', '$1,500 to $5,000'),
        ('more_than_5000', 'More than $5,000'),
    ]
    initial_investment = forms.ChoiceField(
        label="How much money are you planning to invest initially?",
        choices=initial_investment_choices,
    )
    risk_tolerance_choices = [
        ('low', 'Low (I prefer safer investments)'),
        ('medium', 'Medium (I’m okay with some risk)'),
        ('high', 'High (I’m willing to take risks for potential higher returns)'),
    ]
    risk_tolerance = forms.ChoiceField(
        label="What is your risk tolerance?",
        choices=risk_tolerance_choices,
    )
    investment_type_choices = [
        ('individual_stocks', 'Individual stocks'),
        ('mutual_funds_etfs', 'Mutual funds or ETFs'),
        ('real_estate', 'Real estate'),
        ('other', 'Other (please specify)'),
    ]
    investment_type = forms.ChoiceField(
        label="Which sector interests you the most?",
        choices=investment_type_choices,
    )
    investment_type_other = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your other investment type'}),
    )
    
    monitoring_preference_choices = [
        ('enjoy', 'I enjoy it'),
        ('occasionally', 'I can do it occasionally'),
        ('rarely', 'I’d prefer not to monitor them often'),
    ]
    monitoring_preference = forms.ChoiceField(
        label="How do you feel about monitoring your investments regularly?",
        choices=monitoring_preference_choices,
        required=True
    )
    concern_choices = [
        ('losing_money', 'Losing money'),
        ('not_understanding', 'Not understanding how it works'),
        ('volatility', 'Market volatility'),
        ('no', 'No Concerns')
    ]
    biggest_concern = forms.ChoiceField(
        label="What is your biggest concern about investing in the stock market?",
        choices=concern_choices,
        required=True
    )
    
