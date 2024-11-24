from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, business_name, password=None, **extra_fields):
        if not business_name:
            raise ValueError('The Business name must be set')
        user = self.model(business_name=business_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, business_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(business_name, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin):
    business_name = models.CharField(max_length=255, unique=True, default="default_username")
    # username = models.CharField(max_length=150, unique=True, default="default_username")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # This grants access to the admin interface
    is_superuser = models.BooleanField(default=False)  # For superuser access

    objects = UserManager()

    USERNAME_FIELD = 'business_name'  # Use business_name to log in
    REQUIRED_FIELDS = []  # No additional fields required

    def __str__(self):
        return self.business_name

    def get_full_name(self):
        return self.business_name

    def get_short_name(self):
        return self.business_name


    
# class Product(models.Model):
#     Product_Id = models.AutoField(primary_key=True)
#     Product_name = models.CharField(max_length = 200)
#     Product_Description = models.TextField()
#     Product_Image = models.ImageField(upload_to='product/', null=True, blank=True)
#     Price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #         return self.Product_name
class Product(models.Model):
    Product_Id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=200)
    Price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Product_Description = models.TextField()
    Product_Image = models.ImageField(upload_to='products/')
    business_name = models.ForeignKey('user', on_delete=models.CASCADE)  # Foreign key to the user model

    def __str__(self):
        return self.Product_name