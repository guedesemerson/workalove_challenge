from django.db import models
from user.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ingredient Name")
    amount = models.CharField(max_length=50, verbose_name="amount/portion")

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Chef Name")
    recipe_name = models.CharField(max_length=100, verbose_name='Name of Recipe')
    ingredient = models.ManyToManyField(Ingredient)
    preparation_mode = models.TextField()

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.recipe_name