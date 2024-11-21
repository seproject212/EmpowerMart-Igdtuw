from django.db import models

# Create your models here.
class user(models.Model):
    business_name = models.CharField(max_length=122)
    password = models.CharField(max_length=128)  # Store hashed passwords
    instagram = models.URLField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=10)
    def __str__(self):
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
    Product_name = models.CharField(max_length = 200)
    Product_Description = models.TextField()
    Product_Image = models.ImageField(upload_to='product/', null=True, blank=True)
    Price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    business_name = models.ForeignKey(user, on_delete=models.CASCADE, related_name="product") 

    def _str_(self):
        return self.Product_name

