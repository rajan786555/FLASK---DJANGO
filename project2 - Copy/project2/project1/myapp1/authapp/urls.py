from django.contrib import admin
from django.urls import path
from . import views
from .views import flask_app_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('tracking/', views.tracking, name='tracking'),
    path('wallet/', views.wallet, name='wallet'),
    path('profit/', views.profit_dashboard, name='profit'),
    path('flask-api/', views.flask_app_view, name='flask_api')
]

