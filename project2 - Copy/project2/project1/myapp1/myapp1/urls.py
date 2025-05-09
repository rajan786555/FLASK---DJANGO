
from django.contrib import admin
from django.urls import path , include
from authapp import views as auth_views
from course1 import views as course1
from core import views as core
admin.site.site_header = "Mini Blog Header" 
admin.site.site_title = "Mini Blog Title" 
admin.site.index_title= "Dashboard" 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth2/', include('course1.urls') ),
    path('', include('authapp.urls') ),
    path('super', include('core.urls') ),
]
