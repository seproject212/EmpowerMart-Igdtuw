from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('', views.home, name='home'),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('product', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product'),  # Ensure this matches your pattern
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:  # Only in development mode
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
