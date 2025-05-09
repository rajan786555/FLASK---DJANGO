from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import json
import csv
from datetime import datetime
from django.views.decorators.http import require_GET
import random
from datetime import datetime, timedelta
import requests
from django.http import JsonResponse

def flask_app_view(request):
    return JsonResponse({"status": "success", "message": "Flask app endpoint working!"})

def home_view(request):

    return render(request, 'dashboard.html')


import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if not all([username, email, password, cpassword]):
            messages.error(request, 'All fields are required')
            return render(request, 'register.html')
            
        if password != cpassword:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')


        api_url = 'http://127.0.0.1:5000/api/signup'  
        payload = {
            'username': username,
            'email': email,
            'password': password,
            'cpassword': cpassword
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 201:
                messages.success(request, 'Registration successful! You can now login.')
                return redirect('login')
            else:
                res_data = response.json()
                error_msg = res_data.get('error') or res_data.get('message') or 'Registration failed'
                messages.error(request, error_msg)

        except requests.exceptions.RequestException as e:
            messages.error(request, f'API connection error: {str(e)}')

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both fields are required')
            return render(request, 'login.html')

        api_url = 'http://127.0.0.1:5000/api/login'
        payload = {'email': email, 'password': password}

        try:
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                username = email.split('@')[0]
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.set_unusable_password()  
                    user.email = email
                    user.save()

                login(request, user) 
                return redirect('dashboard')

            else:
                res_data = response.json()
                messages.error(request, res_data.get('message', 'Login failed'))

        except requests.exceptions.RequestException as e:
            messages.error(request, f'API connection error: {str(e)}')

    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def tracking(request):
    return render( request,'tracking.html')


@login_required
def wallet(request):
    return render( request,'wallet.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@require_GET
def profit_dashboard(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    current_year = [random.randint(5000, 20000) for _ in range(12)]
    
    previous_year = [random.randint(4000, 18000) for _ in range(12)]
    
    quarters = [
        {'name': 'Q1', 'profit': sum(current_year[0:3]), 'growth': random.randint(5, 25)},
        {'name': 'Q2', 'profit': sum(current_year[3:6]), 'growth': random.randint(5, 25)},
        {'name': 'Q3', 'profit': sum(current_year[6:9]), 'growth': random.randint(5, 25)},
        {'name': 'Q4', 'profit': sum(current_year[9:12]), 'growth': random.randint(5, 25)},
    ]
    
    # Recent transactions
    transactions = []
    for i in range(10):
        transactions.append({
            'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'amount': random.randint(100, 5000),
            'type': random.choice(['Sale', 'Service', 'Subscription']),
            'status': random.choice(['Completed', 'Pending', 'Refunded'])
        })
    
    context = {
        'months': months,
        'current_year': current_year,
        'previous_year': previous_year,
        'quarters': quarters,
        'transactions': transactions,
        'total_profit': sum(current_year),
        'growth_rate': random.randint(5, 30),
        'top_product': 'Premium Subscription',
        'top_product_value': max(current_year),
    }
    
    return render(request, 'profit.html', context)