from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),

   path('dailyoffer/', views.dailyoffer, name='dailyoffer'),
   path('menu/', views.menu, name='menu'),
   path('about/', views.about, name='about'),
   path('contact/', views.contact_view, name='contact'),
    path('success/', views.success_view, name='success'),
   path('train/', views.train, name='train'),
]
