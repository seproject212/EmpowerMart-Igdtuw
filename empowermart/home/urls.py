from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    # path('login/', views.login, name="login"),
    # path('dashboard/', views.dashboard, name="dashboard"),
] 
if settings.DEBUG:  # Only in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
