from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    score = models.IntegerField(default=0)
    # Other user-related fields

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    # Other product-related fields

    def __str__(self):
        return self.name

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product1')
    product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product2')
    chosen_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chosen_product', null=True)
    correct_answer = models.BooleanField(default=False)
    # Other session-related fields

    def __str__(self):
        return f"Session for {self.user.username}"
