from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import MenuItemForm, OrderForm
from .models import MenuItem
from django.shortcuts import render, redirect
from .models import MenuItem
from .forms import MenuItemForm, MenuItemModelForm, OrderForm
from django.shortcuts import render, redirect
from .forms import ContactFormForm
def landing(request):
    return render(request,'landing.html')



def dailyoffer(request):
    return render(request, 'dailyoffer.html')



def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            try:
                response = requests.post('http://127.0.0.1:5000/api/contact', json=data)  # replace with actual API URL
                if response.status_code == 200:
                    return redirect('success')
                else:
                    form.add_error(None, 'Failed to send data to the API.')
            except requests.exceptions.RequestException as e:
                form.add_error(None, f'Error connecting to the API: {e}')
    else:
        form = ContactFormForm()
    return render(request, 'contactus.html', {'form': form})


def train(request):
    return render(request, 'train.html')



# Example view for displaying menu items
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MenuItem
import json
from django.http import JsonResponse
import requests

def menu_view(request):
    menu_items = MenuItem.objects.all()
    
    # Get cart from session
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    context = {
        'menu_items': menu_items,
        'cart_count': cart_count,
    }
    return render(request, 'menu/menu.html', context)

def add_to_cart(request):
    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        try:
            item = MenuItem.objects.get(id=item_id)
            
            # Get or initialize cart in session
            cart = request.session.get('cart', {})
            cart[str(item.id)] = cart.get(str(item.id), 0) + 1
            request.session['cart'] = cart
            
            # Calculate total count
            cart_count = sum(cart.values())
            
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'message': f'{item.name} added to cart'
            })
        except MenuItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
def success_view(request):
    return render(request, 'success.html')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total += item_total
            
            cart_items.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
                'image': item.image.url,
                'quantity': quantity,
                'total': float(item_total)
            })
        except MenuItem.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'menu/cart_modal.html', context)

def update_cart(request):
    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        cart = request.session.get('cart', {})
        
        if action == 'increment':
            cart[item_id] = cart.get(item_id, 0) + 1
        elif action == 'decrement':
            if cart.get(item_id, 0) > 1:
                cart[item_id] -= 1
            else:
                cart.pop(item_id, None)
        elif action == 'remove':
            cart.pop(item_id, None)
        
        request.session['cart'] = cart
        
        # Recalculate cart
        cart_count = sum(cart.values())
        return JsonResponse({'success': True, 'cart_count': cart_count})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})