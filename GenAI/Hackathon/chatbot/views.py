from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ExperiencedInvestorForm, FirstTimeInvestorForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import InvestmentProfile, Sector
import yfinance as yf
import os
import logging
import markdown
from langchain_google_genai import ChatGoogleGenerativeAI
import re

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("Google API Key not found in environment variables.")
    raise ValueError("Google API Key not found in environment variables.")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    api_key=GOOGLE_API_KEY,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    handle_parsing_errors=True,
    temperature=0.6,
)

SECTOR_TICKER_MAP = {
    'Technology': ['AAPL', 'MSFT', 'GOOGL'],
    'Finance': ['JPM', 'BAC', 'C'],
    'Healthcare': ['JNJ', 'PFE', 'MRK'],
    'Energy': ['XOM', 'CVX', 'BP'],
    'Real Estate': ['AMT', 'PLD', 'CCI'],
}

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pass)
            if user is not None:
                login(request, user)
                messages.success(request, f"Account created for {username}!")
                return redirect('choose_investor_type')  
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Unsuccessful registration. Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'chatbot/signup.html', {'form': form})

def choose_investor_type_view(request):
    if request.method == 'POST':
        investor_type = request.POST.get('investor_type')
        if investor_type == 'First-Time':
            return redirect('first_time_investor')
        elif investor_type == 'Experienced':
            return redirect('experienced_investor')
        else:
            messages.error(request, "Invalid selection. Please choose again.")
    return render(request, 'chatbot/choose_investor_type.html')

@login_required
def experienced_investor_view(request):
    if request.method == 'POST':
        form = ExperiencedInvestorForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            # Check for required fields
            missing_fields = [
                field for field in ['amount_to_invest', 'income_percentage', 'profit_percentage', 
                                    'term_investment', 'penny_stocks', 'government_policies', 
                                    'momentum']
                if not cleaned_data[field]
            ]
            if missing_fields:
                messages.error(request, f"Please fill out the following fields: {', '.join(missing_fields)}.")
                return redirect('experienced_investor')

            investment_profile = InvestmentProfile.objects.create(
                user=request.user,
                investor_type='Experienced',
                amount_to_invest=cleaned_data['amount_to_invest'],
                income_percentage=cleaned_data['income_percentage'],
                profit_percentage=cleaned_data['profit_percentage'],
                term_investment=cleaned_data['term_investment'],
                penny_stocks=cleaned_data['penny_stocks'],
                government_policies=cleaned_data['government_policies'],
                momentum=cleaned_data['momentum'],
                investment_goal='',
                investment_goal_other='',
                experience_level='',
                initial_investment='',
                risk_tolerance='',
                investment_type='',
                investment_type_other='',
                monitoring_preference='',
                biggest_concern=''
            )
            investment_profile.sector.set(cleaned_data['sector'])
            investment_profile.save()
            messages.success(request, "Investment profile saved successfully.")
            return redirect('home')
    else:
        form = ExperiencedInvestorForm()
    return render(request, 'chatbot/experienced_investor.html', {'form': form})

@login_required
def first_time_investor_view(request):
    if request.method == 'POST':
        form = FirstTimeInvestorForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            # Check for required fields
            missing_fields = [
                field for field in ['investment_goal', 'experience_level', 'term_investment', 
                                    'initial_investment', 'risk_tolerance', 'investment_type', 
                                    'monitoring_preference', 'biggest_concern']
                if not cleaned_data[field]
            ]
            if missing_fields:
                messages.error(request, f"Please fill out the following fields: {', '.join(missing_fields)}.")
                return redirect('first_time_investor')
             # Handle 'Other' for investment_goal
            investment_goal = cleaned_data['investment_goal']
            investment_goal_other = cleaned_data['investment_goal_other'] if investment_goal == 'other' else ''

            # Handle 'Other' for investment_type
            investment_type = cleaned_data['investment_type']
            investment_type_other = cleaned_data['investment_type_other'] if investment_type == 'other' else ''

            # Handle 'Other' for biggest_concern
            biggest_concern = cleaned_data['biggest_concern']
            


            investment_profile = InvestmentProfile.objects.create(
                user=request.user,
                investor_type='First-Time',
                term_investment=cleaned_data['term_investment'],
                investment_goal=cleaned_data['investment_goal'],
                investment_goal_other=cleaned_data['investment_goal_other'],
                experience_level=cleaned_data['experience_level'],
                initial_investment=cleaned_data['initial_investment'],
                risk_tolerance=cleaned_data['risk_tolerance'],
                investment_type=cleaned_data['investment_type'],
                investment_type_other=cleaned_data['investment_type_other'],
                monitoring_preference=cleaned_data['monitoring_preference'],
                biggest_concern=cleaned_data['biggest_concern'],
            )
            investment_profile.save()
            messages.success(request, "Investment profile saved successfully.")
            return redirect('home')
    else:
        form = FirstTimeInvestorForm()
    return render(request, 'chatbot/first_time_investor.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


def start(request):
    return render(request,'chatbot/frontpage.html')

@login_required
def home_view(request):
    return render(request, 'chatbot/home.html')

@login_required
def chatbot_view(request):
    chatbot_answer = None
    investment_analysis = None

    try:
        investment_profile = InvestmentProfile.objects.get(user=request.user)
    except InvestmentProfile.DoesNotExist:
        messages.error(request, "Please fill out your investment profile first.")
        return redirect('choose_investor_type')

    if investment_profile.investor_type == 'Experienced':
        required_fields = [
            'sector',
            'amount_to_invest',
            'income_percentage',
            'profit_percentage',
            'term_investment',
            'penny_stocks',
            'government_policies',
            'momentum'
        ]
        prompt_template = (
            f"You are a well experienced stockbroker at an investment firm and brokerage house."
            f"Provide a detailed investment analysis for the sectors {', '.join([sector.name for sector in investment_profile.sector.all()])}. "
            f"Consider the amount to invest: ${investment_profile.amount_to_invest}, "
            f"income percentage: {investment_profile.income_percentage}%, "
            f"profit percentage: {investment_profile.profit_percentage}%, "
            f"term of investment: {investment_profile.term_investment}. "
            f"Address investing in Penny stocks: {investment_profile.penny_stocks}. "
            f"Consider government policies: {investment_profile.government_policies}. "
            f"Consider investing based on momentum: {investment_profile.momentum}."
        )
    elif investment_profile.investor_type == 'First-Time':
        required_fields = [
            'investment_goal',
            'experience_level',
            'term_investment',
            'initial_investment',
            'risk_tolerance',
            'investment_type',
            'monitoring_preference',
            'biggest_concern'
        ]
        investment_goal = investment_profile.get_investment_goal_display()
        if investment_profile.investment_goal == 'other' and investment_profile.investment_goal_other:
            investment_goal += f" ({investment_profile.investment_goal_other})"

        investment_type = investment_profile.get_investment_type_display()
        if investment_profile.investment_type == 'other' and investment_profile.investment_type_other:
            investment_type += f" ({investment_profile.investment_type_other})"

        biggest_concern = investment_profile.get_biggest_concern_display()
        

        prompt_template = (
            f"You are a well-experienced stockbroker at an investment firm and brokerage house. "
            f"Provide investment guidance for a first-time investor with the following details: "
            f"Investment goal: {investment_goal}, "
            f"Experience level: {investment_profile.get_experience_level_display()}, "
            f"Investment timeframe: {investment_profile.get_term_investment_display()}, "
            f"Initial investment: {investment_profile.get_initial_investment_display()}, "
            f"Risk tolerance: {investment_profile.get_risk_tolerance_display()}, "
            f"Preferred investment type: {investment_type}, "
            f"Monitoring preference: {investment_profile.get_monitoring_preference_display()}, "
            f"Biggest concern: {biggest_concern}."
        )
    else:
        messages.error(request, "Invalid investor type.")
        return redirect('choose_investor_type')

    missing_fields = [field.replace('_', ' ').capitalize() for field in required_fields if not getattr(investment_profile, field)]
    if missing_fields:
        messages.error(request, f"Please fill out the following fields: {', '.join(missing_fields)}.")
        return redirect('choose_investor_type')

    try:
        investment_response = llm.invoke(prompt_template)
        investment_analysis_markdown = investment_response.content  
        investment_analysis = markdown.markdown(investment_analysis_markdown)
    except Exception as e:
        logger.error(f"Error generating investment analysis: {e}")
        investment_analysis = "<p>Sorry, I couldn't generate the investment analysis at this time.</p>"

    if request.method == 'POST':
        user_question = request.POST.get('user_question')

        if user_question:
            current_keywords = re.findall(r'\b(now|current|2024)\b', user_question, re.IGNORECASE)
            if current_keywords:
                sectors = [sector.name for sector in investment_profile.sector.all()]
                stock_info = {}
                for sector in sectors:
                    tickers = SECTOR_TICKER_MAP.get(sector, [])
                    for ticker in tickers:
                        stock = yf.Ticker(ticker)
                        hist = stock.history(period="1d")
                        if not hist.empty:
                            stock_info[ticker] = hist['Close'].iloc[-1]  

                
                stock_info_str = ', '.join([f"{ticker}: ${price:.2f}" for ticker, price in stock_info.items()])
                prompt_template += f" Based on current market conditions, here are the latest closing prices for the relevant stocks: {stock_info_str}."

                try:
                    chatbot_response = llm.invoke(prompt_template)  
                    chatbot_answer = markdown.markdown(chatbot_answer_markdown)
                except Exception as e:
                    logger.error(f"Error invoking chatbot: {e}")
                    chatbot_answer = "<p>Sorry, I couldn't process your request.</p>"
            try:
                chatbot_response = llm.invoke(user_question)
                chatbot_answer_markdown = chatbot_response.content  
                chatbot_answer = markdown.markdown(chatbot_answer_markdown)
            except Exception as e:
                logger.error(f"Error invoking chatbot: {e}")
                chatbot_answer = "<p>Sorry, I couldn't process your request.</p>"
        else:
            messages.error(request, "Please enter a question.")

    context = {
        'response': investment_analysis,
        'chatbot_answer': chatbot_answer,
    }

    return render(request, 'chatbot/investment_result.html', context)