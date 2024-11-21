from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from home.models import user
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Product
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def internship(request):
    return render(request, 'internship.html')

def startup(request):
    return render(request, 'startup.html')

def products(request):
    return render(request, 'product.html')

def login(request):
    if request.method == "POST":
        business_name = request.POST.get('business_name')
        password = request.POST.get('password')

        if business_name and password:
            try:
                # Retrieve the user based on the business_name
                user_obj = user.objects.get(business_name=business_name)
                
                # Use the custom check_password method to verify the password
                if user_obj.check_password(password):
                    # Successful login
                    return HttpResponse(f"Welcome, {user_obj.business_name}!")
                else:
                    return HttpResponse("Invalid username or password.", status=401)
            
            except user.DoesNotExist:
                return HttpResponse("User does not exist.", status=404)
        else:
            return HttpResponse("Missing business name or password.", status=400)
    
    return render(request, "login.html")

from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == "POST":
        business_name = request.POST.get('business_name')
        password = request.POST.get('password')
        if business_name and password:
            # Hash the password before saving it
            new_user = user(business_name=business_name, password=make_password(password))
            new_user.save()
            return HttpResponse("User registered successfully!")
        else:
            return HttpResponse("Missing business name or password.", status=400)
    return render(request, "register.html")

def dashboard(request):
    products = Product.objects.filter(business_name=request.user.business_name)
    return render(request, 'dashboard.html', {'products': products})

def dashboard_view(request):
    return render(request, "dashboard.html", {"user": request.user})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


# View to display the details of a single product
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from home.models import Product

def add_product(request):
    if request.method == 'POST':
        # Retrieve form data
        product_name = request.POST.get('Product_name')
        price_per_unit = request.POST.get('Price_per_unit')
        product_description = request.POST.get('Product_Description')
        product_image = request.FILES.get('Product_Image')  # Use .get to avoid errors if the file isn't uploaded

        # Ensure required fields are provided
        if not product_name or not product_description:
            return render(request, 'add_product.html', {
                'error': 'Product name and description are required.'
            })

        # Validate price_per_unit
        try:
            price = Decimal(price_per_unit) if price_per_unit else None
        except InvalidOperation:
            return render(request, 'add_product.html', {'error': 'Invalid price value.'})

        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not logged in

        # Get the currently logged-in user
        current_user = request.user

        # Create and save the new product
        new_product = Product(
            Product_name=product_name,
            Price_per_unit=price,
            Product_Description=product_description,
            Product_Image=product_image,
            business_name=current_user  # This should now work correctly
        )
        new_product.save()

        # Redirect to the product list page or a success page
        return redirect('product_list')

    # If GET request, render the form to add a product
    return render(request, 'add_product.html')
