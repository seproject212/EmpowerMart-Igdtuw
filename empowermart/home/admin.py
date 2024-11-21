from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from home.models import user
from .models import Product

# Custom form to handle password hashing
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = user
        fields = '__all__'

    # Overriding save method to hash the password
    def save(self, commit=True):
        user_instance = super().save(commit=False)
        if self.cleaned_data['password']:
            # Hash the password before saving it
            user_instance.password = make_password(self.cleaned_data['password'])
        if commit:
            user_instance.save()
        return user_instance

# Custom admin class to use the custom form
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # Use the custom form
    list_display = ('business_name', 'password')  # Display business_name and password fields

# Register the user model with the custom admin class
admin.site.register(user, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'Price_per_unit', 'Product_Description', 'Product_Image')

