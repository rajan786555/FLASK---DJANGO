 # core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
import csv

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Admin panel views
@user_passes_test(is_admin)
def admin_panel(request):
    """Main admin dashboard view"""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def manage_users(request):
    """View to manage all users"""
    search_query = request.GET.get('search', '')
    
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        ).order_by('-date_joined')
    else:
        users = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/manage_users.html', {'page_obj': page_obj, 'search_query': search_query})

@user_passes_test(is_admin)
def user_detail(request, user_id):
    """View details of a specific user"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_detail.html', {'user': user})

@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Edit a user's information"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update user data
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        
        # Only update password if provided
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)
        
        try:
            user.save()
            messages.success(request, f'User {user.username} updated successfully')
            return redirect('user_detail', user_id=user.id)
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return render(request, 'admin/edit_user.html', {'user': user})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Delete a user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        try:
            username = user.username
            user.delete()
            messages.success(request, f'User {username} deleted successfully')
            return redirect('manage_users')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
            return redirect('user_detail', user_id=user.id)
    
    return render(request, 'admin/confirm_delete.html', {'user': user})

@user_passes_test(is_admin)
def create_user(request):
    """Create a new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_active = is_active
            user.is_staff = is_staff
            user.save()
            
            messages.success(request, f'User {username} created successfully')
            return redirect('user_detail', user_id=user.id)
        except IntegrityError:
            messages.error(request, 'Username or email already exists')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'admin/create_user.html')

@user_passes_test(is_admin)
def export_users(request):
    """Export users data as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Email', 'First Name', 'Last Name', 'Active', 'Staff', 'Date Joined'])
    
    users = User.objects.all().order_by('-date_joined')
    for user in users:
        writer.writerow([
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.is_active,
            user.is_staff,
            user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    """Toggle user active status via AJAX"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({
                'success': True,
                'active': user.is_active,
                'message': f'User {user.username} {"activated" if user.is_active else "deactivated"} successfully'
            })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@user_passes_test(is_admin)
def system_logs(request):
    """Mocked system logs view for the admin panel"""
    # In a real application, you would retrieve actual logs
    mock_logs = [
        {'timestamp': '2025-04-15 09:30:22', 'level': 'INFO', 'message': 'System startup complete'},
        {'timestamp': '2025-04-15 09:31:05', 'level': 'INFO', 'message': 'User admin logged in'},
        {'timestamp': '2025-04-15 09:42:18', 'level': 'WARNING', 'message': 'Failed login attempt: username "test"'},
        {'timestamp': '2025-04-15 10:15:33', 'level': 'ERROR', 'message': 'Database connection timeout'},
        {'timestamp': '2025-04-15 10:16:02', 'level': 'INFO', 'message': 'Database connection restored'},
        {'timestamp': '2025-04-15 10:30:45', 'level': 'INFO', 'message': 'New user registered: johndoe'},
    ]
    
    return render(request, 'admin/system_logs.html', {'logs': mock_logs})

@user_passes_test(is_admin)
def site_settings(request):
    """Mock site settings management"""
    if request.method == 'POST':
        # In a real app, you would save these settings to a database
        messages.success(request, 'Settings updated successfully')
        return redirect('site_settings')
    
    # Mock settings
    settings = {
        'site_name': 'Your Application',
        'enable_registrations': True,
        'maintenance_mode': False,
        'email_notifications': True
    }
    
    return render(request, 'admin/site_settings.html', {'settings': settings})