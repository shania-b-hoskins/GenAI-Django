# Generated by Django 5.1.2 on 2024-10-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='investmentprofile',
            name='initial_investment_amount',
        ),
        migrations.RemoveField(
            model_name='investmentprofile',
            name='investment_goals',
        ),
        migrations.RemoveField(
            model_name='investmentprofile',
            name='preferred_sectors',
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='biggest_concern',
            field=models.CharField(blank=True, choices=[('losing_money', 'Losing money'), ('not_understanding', 'Not understanding how it works'), ('volatility', 'Market volatility'), ('other', 'Other')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='biggest_concern_other',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='experience_level',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('some_knowledge', 'A little (some knowledge but no experience)'), ('some_experience', 'Some experience')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='initial_investment',
            field=models.CharField(blank=True, choices=[('less_than_500', 'Less than $500'), ('between_500_1500', '$500 to $1,500'), ('between_1500_5000', '$1,500 to $5,000'), ('more_than_5000', 'More than $5,000')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='investment_goal',
            field=models.CharField(blank=True, choices=[('retirement', 'Saving for retirement'), ('wealth_building', 'Building wealth'), ('specific_goal', 'Saving for a specific goal'), ('other', 'Other')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='investment_goal_other',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='investment_type',
            field=models.CharField(blank=True, choices=[('individual_stocks', 'Individual stocks'), ('mutual_funds_etfs', 'Mutual funds or ETFs'), ('real_estate', 'Real estate'), ('other', 'Other')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='investment_type_other',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='monitoring_preference',
            field=models.CharField(blank=True, choices=[('enjoy', 'I enjoy it'), ('occasionally', 'I can do it occasionally'), ('rarely', 'I’d prefer not to monitor them often')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='ongoing_investment_budget',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='investmentprofile',
            name='risk_tolerance',
            field=models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=20, null=True),
        ),
        migrations.RemoveField(
            model_name='investmentprofile',
            name='sector',
        ),
        migrations.AlterField(
            model_name='investmentprofile',
            name='term_investment',
            field=models.CharField(blank=True, choices=[('short', 'Short-term (less than 1 year)'), ('medium', 'Medium-term (1-5 years)'), ('long', 'Long-term (more than 5 years)')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='investmentprofile',
            name='sector',
            field=models.ManyToManyField(blank=True, to='chatbot.sector'),
        ),
    ]
