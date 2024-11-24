from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from home.models import user, Product


# Custom UserAdmin form
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = user
        fields = '__all__'

    def save(self, commit=True):
        user_instance = super().save(commit=False)  # Call the parent save method
        if self.cleaned_data.get('password') and not user_instance.password.startswith('pbkdf2_'):
            user_instance.password = make_password(self.cleaned_data['password'])
        if commit:
            user_instance.save()
            self.save_m2m()  # Save many-to-many relationships
        return user_instance

# Custom UserAdmin class
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # Use the custom form
    list_display = ('business_name', 'is_active', 'is_staff', 'is_superuser')  # Display these fields
    search_fields = ('business_name',)  # Allow searching by business_name

    # Customize admin form layout
    fieldsets = (
        (None, {'fields': ('business_name', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

# Register the user model with the custom UserAdmin class
admin.site.register(user, UserAdmin)

# Product model admin class
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'Price_per_unit', 'Product_Description', 'Product_Image')
# this is admin.py