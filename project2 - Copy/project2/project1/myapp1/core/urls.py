from django.urls import path
from . import views

# Admin panel URL patterns
urlpatterns = [
    # Main admin dashboard
    path('admin/', views.admin_panel, name='admin_panel'),
    
    # User management
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/create/', views.create_user, name='create_user'),
    path('admin/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('admin/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin/users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/export/', views.export_users, name='export_users'),
    
    # System logs
    path('admin/logs/', views.system_logs, name='system_logs'),
    
    # Site settings
    path('admin/settings/', views.site_settings, name='site_settings'),
]