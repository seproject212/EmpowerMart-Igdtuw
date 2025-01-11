"""
URL configuration for empowermart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('about', views.about, name="about"),
    path('internship', views.internship, name="internship"),
    path('startup', views.startup, name="startup"),
    # path('product', views.products, name="product"),
    path('product/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # Ensure this matches your pattern
    path('login/', views.login_view, name='login'), 
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard_view, name="dashboard_view"),
    path('add-product/', views.add_product, name='add_product'),
    path('logout/', views.logout_view, name='logout'),
    # path('product-list/', views.product_list, name='product_list'),
    path('edit-product/<int:product_id>/', views.update_product, name='update_product'), 
     path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('dashboard/reset_password/', views.reset_password, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
