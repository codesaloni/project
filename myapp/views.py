from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser,Product,CartItem

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        email=request.POST.get('email')
        
        if not username or not password or not user_type:
            messages.error(request, 'All fields are required.')
            return redirect('register')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        user = CustomUser.objects.create_user(username=username, password=password, user_type=user_type,email=email)
        auth_login(request, user)
        return redirect('login')
        
      
    
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            
        
            if user.user_type == 'lister':
                return redirect('product')  
            else:
                return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')

           
        
    
    return render(request, 'login.html')

def home(request):
    pro=Product.objects.all()
    pro={'pro':pro}
    
    return render(request,"home.html",pro)

def product(request):
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        image = request.FILES.get('image')
        pro=Product(name=name,price=price,image=image)
        pro.save()

        return redirect('product') 
    
    return render(request,"product.html")

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

#     if not created:
#         cart_item.quantity += 1
#     cart_item.save()

def add_to_cart(request, product_id):
    # Ensure that this view only handles POST requests
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('view_cart')  # Redirect to the cart page after adding the product

    # If the request method is not POST, you could either return a 405 error
    # or handle it in some other way. Here, let's just return a simple HttpResponse.
    return HttpResponse("Method not allowed", status=405)

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('view_cart')

    return redirect('view_cart')


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


    
   
