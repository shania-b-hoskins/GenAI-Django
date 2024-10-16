from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('home/', views.home_view, name='home'),                          
    path('signup/', views.signup_view, name='signup'),              
    path('login/', views.login_view, name='login'),                  
    path('logout/', views.logout_view, name='logout'),               
    path('choose_investor_type/', views.choose_investor_type_view, name='choose_investor_type'),  
    path('experienced_investor/', views.experienced_investor_view, name='experienced_investor'),    
    path('first_time_investor/', views.first_time_investor_view, name='first_time_investor'),        
    path('chatbot/', views.chatbot_view, name='chatbot'),                
]
