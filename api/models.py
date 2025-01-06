from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    



class Order(models.Model):
    class Choices(models.IntegerChoices):
        PENDING = 'Pending'
        SHIPPED =  'Shipped'
        DELIVERED = 'Delivered'

    order_id = models.UUIDField(primary_key=True,delattr=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Choices.choices, default=Choices.PENDING)
    product =models.ManyToManyField(Product, blank=True, through='OrderItem',related_name='orders')
    def __str__(self):
        return f"Order #{self.id} by f{self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()