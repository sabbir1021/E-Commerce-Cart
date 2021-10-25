from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField()

    def __str__(self):
        return str(self.user)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        return sum(i.get_total for i in items)
    
    @property
    def get_item_total(self):
        items = self.orderitem_set.all()
        total = 0
        for i in items:
            quantity = i.quantity
            total = total + quantity
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity