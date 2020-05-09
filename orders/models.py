from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PizzaName(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

class Size(models.Model):
    size = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.size}"

class Topping(models.Model):
    topping = models.CharField(max_length=64)
    user = models.ManyToManyField(User, blank=True, related_name="topping_orders")

    def __str__(self):
        return f"{self.topping}"

class Addition(models.Model):
    addition = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="addn_orders")

    def __str__(self):
        return f"{self.addition}: ${self.price}"

class PizzaType(models.Model):
    p_type = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.p_type}"
        
class Pizza(models.Model):
    name = models.ForeignKey(PizzaName, on_delete=models.CASCADE, related_name="type")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="pizsize")
    p_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="tops")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="pizza_orders")

    def __str__(self):
        return f"{self.size} {self.name} pizza with {self.p_type}: ${self.price}"

class Sub(models.Model):
    sub_type = models.CharField(max_length=64)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="subsize")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="sub_orders")
    addn = models.ManyToManyField(Addition, blank=True, related_name="subs")

    def __str__(self):
        return f"{self.size}, {self.sub_type} sub: ${self.price}"

class Pasta(models.Model):
    pasta_type = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="pasta_orders")

    def __str__(self):
        return f"{self.pasta_type} pasta: ${self.price}"

class Salad(models.Model):
    salad_type = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="salad_orders")

    def __str__(self):
        return f"{self.salad_type}: ${self.price}"

class DinnerPlatter(models.Model):
    plat_type = models.CharField(max_length=16)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="platsize")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ManyToManyField(User, blank=True, related_name="plat_orders")

    def __str__(self):
        return f"{self.size}, {self.plat_type} dinner platter: ${self.price}"

class CartItem(models.Model):
    item = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    item_type = models.CharField(max_length=32)
    item_id = models.IntegerField(0)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.item}"