from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from base.models import Category, ScrapItem, Order
from django.db.models import Q

def home(request):
    categories = Category.objects.all()[:6]
    recent_items = ScrapItem.objects.filter(is_available=True).order_by('-created')[:8]
    context = {
        'categories': categories,
        'recent_items': recent_items,
        'page_title': 'Home'
    }
    return render(request, 'base/home.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'base/login.html', {'page_title': 'Login'})

def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Collect all validation errors
        errors = []
        
        # Username validations
        if not username:
            errors.append('Username is required')
            
        elif len(username) > 150:
            errors.append('Username must be 150 characters or fewer')
            
        elif ' ' in username:
            errors.append('Username cannot contain spaces')
            
        # Check if username contains only allowed characters
        elif not all(c.isalnum() or c in "@.+-_" for c in username):
            errors.append('Username may only contain letters, numbers, and @/./+/-/_')
            
        # Check if username already exists
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists')
            
        # Password validations
        if not password1:
            errors.append('Password is required')
            
        elif len(password1) < 8:
            errors.append('Password must contain at least 8 characters')
            
        elif password1.isdigit():
            errors.append('Password cannot be entirely numeric')
            
        if password1 != password2:
            errors.append('Passwords do not match')
        
        # If there are any errors, show them all at once
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'base/register.html', {'page_title': 'Register'})
        
        # Create the user if no errors
        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'base/register.html', {'page_title': 'Register'})
    
    return render(request, 'base/register.html', {'page_title': 'Register'})

def logout_page(request):
    logout(request)
    return redirect('home')

def marketplace(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    
    scraps = ScrapItem.objects.filter(is_available=True)
    
    if query:
        scraps = scraps.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    if category_id:
        scraps = scraps.filter(category__id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'scraps': scraps,
        'categories': categories,
        'query': query,
        'category_id': category_id,
        'page_title': 'Marketplace'
    }
    return render(request, 'base/marketplace.html', context)

def scrap_detail(request, pk):
    scrap = get_object_or_404(ScrapItem, id=pk)
    related_items = ScrapItem.objects.filter(category=scrap.category).exclude(id=pk)[:4]
    
    context = {
        'scrap': scrap,
        'related_items': related_items,
        'page_title': scrap.title
    }
    return render(request, 'base/scrap_detail.html', context)

@login_required
def add_scrap(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        location = request.POST.get('location')
        condition = request.POST.get('condition')
        image = request.FILES.get('image')
        
        category = Category.objects.get(id=category_id)
        
        scrap = ScrapItem.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            quantity=quantity,
            location=location,
            condition=condition,
            image=image,
        )
        
        messages.success(request, 'Your scrap item has been listed!')
        return redirect('scrap_detail', pk=scrap.id)
    
    return render(request, 'base/add_scrap.html', {'categories': categories, 'page_title': 'Add Scrap Item'})

@login_required
def edit_scrap(request, pk):
    scrap = get_object_or_404(ScrapItem, id=pk, seller=request.user)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        scrap.title = request.POST.get('title')
        scrap.description = request.POST.get('description')
        scrap.price = request.POST.get('price')
        category_id = request.POST.get('category')
        scrap.category = Category.objects.get(id=category_id)
        scrap.quantity = request.POST.get('quantity')
        scrap.location = request.POST.get('location')
        scrap.condition = request.POST.get('condition')
        
        if 'image' in request.FILES:
            scrap.image = request.FILES.get('image')
        
        scrap.save()
        messages.success(request, 'Your scrap item has been updated!')
        return redirect('scrap_detail', pk=scrap.id)
    
    context = {
        'scrap': scrap,
        'categories': categories,
        'page_title': 'Edit Scrap Item'
    }
    return render(request, 'base/edit_scrap.html', context)

@login_required
def delete_scrap(request, pk):
    scrap = get_object_or_404(ScrapItem, id=pk, seller=request.user)
    
    if request.method == 'POST':
        scrap.delete()
        messages.success(request, 'Your scrap item has been deleted!')
        return redirect('profile')
    
    return render(request, 'base/delete_scrap.html', {'scrap': scrap, 'page_title': 'Delete Scrap Item'})

@login_required
def profile(request):
    my_scraps = ScrapItem.objects.filter(seller=request.user)
    my_purchases = Order.objects.filter(buyer=request.user)
    my_sales = Order.objects.filter(seller=request.user)
    
    context = {
        'my_scraps': my_scraps,
        'my_purchases': my_purchases,
        'my_sales': my_sales,
        'page_title': 'Profile'
    }
    return render(request, 'base/profile.html', context)

@login_required
def place_order(request, pk):
    scrap = get_object_or_404(ScrapItem, id=pk, is_available=True)
    
    if request.user == scrap.seller:
        messages.error(request, 'You cannot buy your own item')
        return redirect('scrap_detail', pk=scrap.id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > scrap.quantity:
            messages.error(request, f'Only {scrap.quantity} units available')
            return redirect('scrap_detail', pk=scrap.id)
        
        total_price = quantity * scrap.price
        
        order = Order.objects.create(
            buyer=request.user,
            seller=scrap.seller,
            scrap_item=scrap,
            quantity=quantity,
            total_price=total_price,
        )
        
        # Update quantity or mark as unavailable
        scrap.quantity -= quantity
        if scrap.quantity <= 0:
            scrap.is_available = False
        scrap.save()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('my_orders')
    
    return render(request, 'base/place_order.html', {'scrap': scrap, 'page_title': 'Place Order'})

@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created')
    
    return render(request, 'base/my_orders.html', {'orders': orders, 'page_title': 'My Orders'})
