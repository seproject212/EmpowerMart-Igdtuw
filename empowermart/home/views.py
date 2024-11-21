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
                
                # Check if the entered password matches the stored hashed password
                if check_password(password, user_obj.password):
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

def add_product(request):
    if request.method == 'POST':
        # Handle form submission and create new product
        new_product = Product(
            Product_name=request.POST['Product_name'],
            Price_per_unit=request.POST['Price_per_unit'],
            Product_Description=request.POST['Product_Description'],
            Product_Image=request.FILES['Product_Image']
        )
        new_product.save()  # Save the new product to the database
        
        # Redirect to the product list page
        return redirect('product_list')


    # If GET request, render the form to add a product
    return render(request, 'add_product.html')