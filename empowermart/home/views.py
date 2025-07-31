from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from home.models import user
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Product
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

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

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_view')

            # return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

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

@login_required
def dashboard_view(request):
    # Get the current user
    user = request.user
    
    # Generate uidb64 and token for the user
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    
    # Get the user's products (existing logic)
    products = Product.objects.filter(business_name=user)
    
    # Pass the generated uidb64 and token to the template context
    return render(request, 'dashboard.html', {'products': products, 'uidb64': uidb64, 'token': token})
# def dashboard_view(request):
#     return render(request, "dashboard.html", {"user": request.user})

# @login_required
def product_list(request):
    # Filter products based on the logged-in user
    # products = Product.objects.filter(business_name=request.user)
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


# View to display the details of a single product

# @login_required
def product_detail(request, id):
    product = get_object_or_404(Product, Product_Id=id)  # Fetch the product by its ID
    user = product.business_name
    return render(request, 'product_detail.html', {'product': product, 'user': user})
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from home.models import Product

import logging
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from .models import Product

logger = logging.getLogger(__name__)

from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from .models import Product

@login_required
def add_product(request):
    if request.method == 'POST':
        # Retrieve form data
        product_name = request.POST.get('Product_name')
        price_per_unit = request.POST.get('Price_per_unit')
        product_description = request.POST.get('Product_Description')
        product_image = request.FILES.get('Product_Image')

        # Validate required fields
        if not product_name or not product_description:
            return render(request, 'add_product.html', {
                'error': 'Product name and description are required.',
                'form_data': request.POST  # Preserve form data for re-rendering
            })

        # Validate price_per_unit
        try:
            price = Decimal(price_per_unit) if price_per_unit else None
        except InvalidOperation:
            return render(request, 'add_product.html', {
                'error': 'Invalid price value.',
                'form_data': request.POST
            })

        # Create and save the new product
        try:
            new_product = Product(
                Product_name=product_name,
                Price_per_unit=price,
                Product_Description=product_description,
                Product_Image=product_image,
                business_name=request.user  # Assign the logged-in user
            )
            new_product.save()
        except Exception as e:
            return render(request, 'add_product.html', {
                'error': f"Error saving product: {str(e)}",
                'form_data': request.POST
            })

        # Redirect to the dashboard on success
        return redirect('/dashboard')  

    # For GET requests, render the form
    return render(request, 'add_product.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_product(request, product_id):
    # Fetch the product using the product_id
    product = get_object_or_404(Product, Product_Id=product_id)

    if request.method == "POST":
        # Get data from the form
        product_name = request.POST.get('product_name', '').strip()
        price = request.POST.get('price', '').strip()
        product_description = request.POST.get('product_description', '').strip()
        product_image = request.FILES.get('product_image')  # Optional field

        # Validate inputs (basic validation)
        if not product_name or not price or not product_description:
            messages.error(request, "All fields except image are required!")
        else:
            # Update the product fields
            product.Product_name = product_name
            product.Price_per_unit = price
            product.Product_Description = product_description
            
            if product_image:
                product.Product_Image = product_image  # Update image only if a new one is uploaded

            product.save()  # Save changes to the database

            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard_view')  # Redirect to a product list or detail page

    # Render the edit product form with current product details
    return render(request, 'edit_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    # Match the primary key name in the model
    product = get_object_or_404(Product, Product_Id=product_id)
    
    if product.business_name == request.user:  # Ensure the logged-in user owns the product
        product.delete()
        messages.success(request, "Product deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this product.")
    
    return redirect('dashboard_view')


from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "The passwords do not match. Please try again.")
            return render(request, 'dashboard/reset_password.html')

        # Update the password
        user = request.user
        user.set_password(new_password)
        user.save()

        # Log out the user after updating the password
        logout(request)

        # Flush the session to make sure the user is completely logged out
        request.session.flush()

        # Show a success message
        messages.success(request, "Your password has been updated successfully. Please log in again.")

        # Redirect to the login page after logging out
        return redirect('login')  # Make sure the 'login' URL pattern exists

    return render(request, 'dashboard/reset_password.html')
