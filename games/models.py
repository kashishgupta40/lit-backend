from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(unique=True)
#     score = models.IntegerField(default=0)
#     # Other user-related fields

#     def __str__(self):
#         return self.username

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image_url = models.URLField()
#     # Other product-related fields

#     def __str__(self):
#         return self.name

# class GameSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product1')
#     product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product2')
#     chosen_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chosen_product', null=True)
#     correct_answer = models.BooleanField(default=False)
#     # Other session-related fields

#     def __str__(self):
#         return f"Session for {self.user.username}"

class Category(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_url=models.URLField()
    
    def __str__(self):
        return self.name
    

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item1 = models.ForeignKey(Item, related_name='item1', on_delete=models.CASCADE)
    item2 = models.ForeignKey(Item, related_name='item2', on_delete=models.CASCADE)
    chosen_item = models.ForeignKey(Item, related_name='chosen_item', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)