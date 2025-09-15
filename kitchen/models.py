from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.username}, {self.years_of_experience} ({self.first_name} {self.last_name})"


class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(Cook, related_name="dishes")
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")

    def __str__(self) -> str:
        return f"{self.name}, price: {self.price}"
